import bitmex
from keys import ID,SECRET
import time
client = bitmex.bitmex(test=False,api_key=ID,api_secret=SECRET)
x=client.Trade.Trade_getBucketed(binSize='5m',reverse=True,symbol='XBTUSD',count=1).result()[0]
# print(x[0]['close'])

counter = 1
responnse=client.Order.Order_new(
    symbol="XBTUSD", side="Buy", orderQty=1 * 1).result()

print(responnse)
# while True:
#     print(responnse)
#     print('Order Status is :{}'.format(responnse[0]['ordStatus']))
#     time.sleep(5)
#     print('print after sleep {}'.format(counter))
#     counter = counter + 1
