import bitmex
import time
from keys import ID, SECRET
from strategy import Strategy
from trader import Trader
from config import TIMEFRAME, AMOUNT_MONEY_TO_TRADE, LEVERAGE, ohlcv_candles,time_to_wait_new_trade

response = None
stop_order_response=[]
take_profit_order_response=[]
ohlcv_candles=[]

client = bitmex.bitmex(test=False, api_key=ID, api_secret=SECRET)
strategy = Strategy(client, timeframe=TIMEFRAME)
trader = Trader(client, strategy,ohlcv_candles, money_to_trade=AMOUNT_MONEY_TO_TRADE, leverage=LEVERAGE, )

while True:
    if round(time.time()) % time_to_wait_new_trade[TIMEFRAME] == 0:
        trader.execute_trade()
        if response is not None:
            exec_price = response[0][price]
            stop_order_response=trader.set_stop_limit(exec_price)
            take_profit_order_response=trader.set_take_profit(exec_price)
            while True:
                if stop_order_response[0]['ordStatus']=='Filled' or take_profit_order_response[0]['ordStatus']=='Filled':
                    response = None
                    break
                time.sleep(1)
    time.sleep(1)
