import talib
import pandas as pd

class Strategy():
    def __init__(self,client ,timeframe='5m'):
        self.client = client
        self.timeframe = timeframe

    def predict(self):
        df = self.client.Trade.Trade_getBucketed(binSize=self.timeframe,reverse=True,symbol='XBTUSD',count=100).result()[0]
        ohlcv_candles = pd.DataFrame(df)
        ohlcv_candles.set_index(['timestamp'],inplace=True)
        ohlcv_candles.sort_values(by=['timestamp'],ascending=True,inplace=True)

        macd,signal,hist=talib.MACD(ohlcv_candles['close'],fastperiod=12,slowperiod=26,signalperiod=9)
        # print('close: {} '.format(ohlcv_candles['close']))

        #sell
        # print(hist)
        print('hist -2 {}'.format(hist[-2]))
        print('hist -1 {}'.format(hist[-1]))
        if hist[-2]>0 and hist[-1]<0:
            return -1
        elif hist[-2]<0 and hist[-1]>0:
            return 1.
        else:
            return 0.
