import bitmex
import time
from keys import ID, SECRET
from strategy import Strategy
from trader import Trader
from config import *

client = bitmex.bitmex(test=False, api_key=ID, api_secret=SECRET)
strategy = Strategy(client, timeframe=TIMEFRAME)
trader = Trader(client, strategy, money_to_trade=AMOUNT_MONEY_TO_TRADE, leverage=LEVERAGE)

# while True:
#     if round(time.time()) % time_to_wait_new_trade[TIMEFRAME] == 0:
#         trader.execute_trade()
#     time.sleep(1)
response = trader.execute_trade()
if response == None:
    print(response)
