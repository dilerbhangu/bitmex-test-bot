from slackclient import SlackClient
import bitmex
from keys import ID, SECRET
import time
import pandas as pd
client = bitmex.bitmex(test=False, api_key=ID, api_secret=SECRET)
x = client.Order.Order_cancelAll()
print(x)


# print(order_status[1]['orderID'])
# print(order_status[2]['orderID'])

# # x=client.Trade.Trade_getBucketed(binSize='5m',reverse=True,symbol='XBTUSD',count=10,partial=True).result()[0]
# # print(x[0]['close'])
# df = client.Trade.Trade_getBucketed(binSize='1m', reverse=True,
#                                     symbol='XBTUSD', count=10, partial=True).result()[0]
# ohlcv_candles = pd.DataFrame(df)
# ohlcv_candles.set_index(['timestamp'], inplace=True)
# ohlcv_candles.sort_values(by=['timestamp'], ascending=True, inplace=True)
# while True:
#     df = client.Trade.Trade_getBucketed(
#         binSize='1m', reverse=True, symbol='XBTUSD', count=10, partial=True).result()[0]
#     ohlcv_candles = pd.DataFrame(df)
#     ohlcv_candles.set_index(['timestamp'], inplace=True)
#     ohlcv_candles.sort_values(by=['timestamp'], ascending=True, inplace=True)
#     print('{}'.format(ohlcv_candles['volume'][-1]))
#     # print('volume previos candle: {}'.format(ohlcv_candles['volume'][-2]))
#     # print('volume second previous candle: {}'.format(ohlcv_candles['volume'][-3]))
#     time.sleep(1)
