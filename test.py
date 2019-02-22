import bitmex
from keys import ID,SECRET
import time
client = bitmex.bitmex(test=False,api_key=ID,api_secret=SECRET)
while True:
    x=client.Trade.Trade_getBucketed(binSize='1m',reverse=True,symbol='XBTUSD',count=1).result()[0]
    print(x[0]['close'])
    time.sleep(1)
