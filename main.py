
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
            stop_order_response = trader.set_stop_limit(exec_price, response)
            order_counter += order_counter
            print('Order Number : {}'.format(order_counter))
            while True:
                order_status = client.Order.Order_getOrders(
                    symbol='XBTUSD', count=3, reverse=True).result()
                if order_status[0][1]['ordStatus'] == 'Filled' and flag == False:
                    take_profit_order_response = trader.set_take_profit(exec_price, response)
                    flag = True

                if flag = True:
                    if order_status[0][1]['ordStatus'] == 'Filled' or order_status[0][0]['ordStatus'] == 'Filled':
                        response = None
                        if trader.send_notifcation(response) is True:
                            print('Notification send successfully')
                        else:
                            print('Notification Failed')
                        client.Order.Order_cancelAll()
                        print('order filled and cancel all other orders')
                        break
                time.sleep(2)
    time.sleep(1)
