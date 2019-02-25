import bitmex
import time
from keys import ID, SECRET
from strategy import Strategy
from trader import Trader
from config import TIMEFRAME, AMOUNT_MONEY_TO_TRADE, LEVERAGE, ohlcv_candles

response = None
client = bitmex.bitmex(test=False, api_key=ID, api_secret=SECRET)
strategy = Strategy(client, timeframe=TIMEFRAME)
trader = Trader(client, strategy, money_to_trade=AMOUNT_MONEY_TO_TRADE, leverage=LEVERAGE, ohlcv_candles)

# while True:
   if response is None:
        if round(time.time()) % time_to_wait_new_trade[TIMEFRAME] == 0:
            trader.execute_trade()
    elif response[0]['side'] = 'Sell':
        trader.buy_trade()
    elif response[0]['side'] = 'Buy':
        trader.sell_trade()
    else:
        print('something goes wrong during response')
