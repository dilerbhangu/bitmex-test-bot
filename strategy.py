import talib
import pandas as pd

class Strategy():
    def __init__(self,client ,timeframe='15m'):
        self.client = client
        self.timeframe = timeframe




    def predict(self):
        df = self.client.Trade.Trade_getBucketed(binSize=self.timeframe,reverse=True,symbol='XBTUSD',count=100).result()[0]
        ohlcv_candles = pd.DataFrame(df)
        ohlcv_candles.set_index(['timestamp'],inplace=True)
        ohlcv_candles.sort_values(by=['timestamp'],ascending=True,inplace=True)

        # macd,signal,hist=talib.MACD(ohlcv_candles['close'],fastperiod=12,slowperiod=26,signalperiod=9)
        # print('close: {} '.format(ohlcv_candles['close']))

        #sell
        # print(hist)
        print('voulume -2 {}'.format(ohlcv_candles['volume'][-2]))
        print('volume -1 {}'.format(ohlcv_candles['volume'][-1]))

        cond1 = ohlcv_candles['volume'][-1]> 4*ohlcv_candles['volume'][-2]
        cond2 = ohlcv_candles['close'][-2]>ohlcv_candles['close'][-1]
        cond3 = ohlcv_candles['close'][-2]<ohlcv_candles['close'][-1]
        if cond1 and cond3:
            return -1,ohlcv_candles
        elif cond1 and cond2:
            return 1,ohlcv_candles
        else:
            return 0,ohlcv_candles
