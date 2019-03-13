from slackclient import SlackClient
import bitmex
from keys import ID, SECRET
import time
import pandas as pd
client = bitmex.bitmex(test=False, api_key=ID, api_secret=SECRET)
x = client.Order.Order_new(
    symbol="XBTUSD", side="Sell", orderQty=1, stopPx=3840, price=3840, execInst="LastPrice,ReduceOnly").result()
print(x)
