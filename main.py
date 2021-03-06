
import bitmex
import time
from keys import ID, SECRET, SLACK_TOKEN
from strategy import Strategy
from trader import Trader
from config import TIMEFRAME, AMOUNT_MONEY_TO_TRADE, LEVERAGE, ohlcv_candles, time_to_wait_new_trade
from slackclient import SlackClient

response = None
stop_order_response = []
take_profit_order_response = []
ohlcv_candles = []
order_counter = 0
msg = ''
flag = False

sc = SlackClient(SLACK_TOKEN)

client = bitmex.bitmex(test=False, api_key=ID, api_secret=SECRET)
strategy = Strategy(client, timeframe=TIMEFRAME)
trader = Trader(client, sc, strategy, ohlcv_candles,
                money_to_trade=AMOUNT_MONEY_TO_TRADE, leverage=LEVERAGE)

while True:
    if round(time.time()) % time_to_wait_new_trade[TIMEFRAME] == 0:
        time.sleep(1)
        response = trader.execute_trade()
        if response is not None:
            if trader.send_notifcation(response) is True:
                print('Notification send successfully')
            else:
                print('Notification Failed')
            exec_price = response[0]['price']
            order_counter = order_counter + 1.
            print('Order Number : {}'.format(order_counter))
            time.sleep(2)
            while True:
                order_status = client.Order.Order_getOrders(
                    symbol='XBTUSD', count=2, reverse=True).result()
                if order_status[0][0]['ordStatus'] == 'Filled' and flag == False:
                    stop_order_response = trader.set_stop_limit(exec_price, response)
                    take_profit_order_response = trader.set_take_profit(exec_price, response)
                    order_status = client.Order.Order_getOrders(
                        symbol='XBTUSD', count=3, reverse=True).result()
                    flag = True
                    time.sleep(2)

                    msg = 'Active Order Filled at Price: '+str(order_status[0][2]['price'])
                    response = 'Active Order'
                    trader.send_notifcation(response, extra=msg)

                if flag == True:
                    if order_status[0][0]['ordStatus'] == 'Filled' or order_status[0][1]['ordStatus'] == 'Filled':
                        response = None
                        if order_status[0][0]['ordStatus'] == 'Filled':
                            msg = 'Order Filled With Profit and excute price: ' + \
                                str(order_status[0][0]['price'])
                        else:
                            msg = 'Order Filled With Loss and excute price: ' + \
                                str(order_status[0][1]['price'])
                        if trader.send_notifcation(response, extra=msg) is True:
                            print('Notification send successfully')
                        else:
                            print('Notification Failed')
                        client.Order.Order_cancelAll().result()
                        print('order filled and cancel all other orders')
                        flag = False
                        break
                time.sleep(2)
    time.sleep(1)
