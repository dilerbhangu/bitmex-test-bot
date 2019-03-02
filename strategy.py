import talib
import pandas as pd


class Strategy():
    def __init__(self, client, timeframe='1m'):
        self.client = client
        self.timeframe = timeframe

    def predict(self):
        df = self.client.Trade.Trade_getBucketed(
            binSize=self.timeframe, reverse=True, symbol='XBTUSD', count=10, partial=True).result()[0]
        ohlcv_candles = pd.DataFrame(df)
        ohlcv_candles.set_index(['timestamp'], inplace=True)
        ohlcv_candles.sort_values(by=['timestamp'], ascending=True, inplace=True)

        # macd,signal,hist=talib.MACD(ohlcv_candles['close'],fastperiod=12,slowperiod=26,signalperiod=9)
        # print('close: {} '.format(ohlcv_candles['close']))

        # sell
        # print(hist)
        print('voulume previous {}'.format(ohlcv_candles['volume'][-3]))
        print('volume current {}'.format(ohlcv_candles['volume'][-2]))

        cond1 = ohlcv_candles['volume'][-2] > ohlcv_candles['volume'][-3]
        cond2 = ohlcv_candles['close'][-3] > ohlcv_candles['close'][-2]
        cond3 = ohlcv_candles['close'][-3] < ohlcv_candles['close'][-2]
        print('cond1 {}'.format(cond1))
        print('cond2 {}'.format(cond2))
        print('cond3 {}'.format(cond3))

        if cond1 and cond3:
            print('condition 1')
            return -1, ohlcv_candles
        elif cond1 and cond2:
            print('condition 2')
            return 1, ohlcv_candles
        else:
            print('condition 3')
            return 0, ohlcv_candles
