import time


class Trader():
    def __init__(self, client, sc, strategy, ohlcv_candles, money_to_trade=100, leverage=5):
        self.client = client
        self.sc = sc
        self.strategy = strategy
        self.money_to_trade = money_to_trade
        self.leverage = leverage
        self.ohlcv_candles = ohlcv_candles

    def execute_trade(self):
        predict, self.ohlcv_candles = self.strategy.predict()
        print('Predication: {}'.format(predict))
        limit_price = self.ohlcv_candles['close'][-2]
        response = None
        try:
            if predict == -1:
                response = self.client.Order.Order_new(
                    symbol="XBTUSD", side="Sell", orderQty=self.money_to_trade * self.leverage, price=limit_price+1).result()
            elif predict == 1:
                response = self.client.Order.Order_new(
                    symbol="XBTUSD", side="Buy", orderQty=self.money_to_trade * self.leverage, price=limit_price-1).result()
            else:
                response = None

        except Exception as e:
            print('something goes wrong')
            print(e)
            time.sleep(2)

        return response

    def set_stop_limit(self, exec_price, response):
        if response[0]['side'] == 'Buy':
            stop_order_response = self.client.Order.Order_new(
                symbol="XBTUSD", side="Sell", orderQty=self.money_to_trade * self.leverage, stopPx=exec_price-10, price=exec_price-10, execInst="LastPrice,ReduceOnly").result()
        elif response[0]['side'] == 'Sell':
            stop_order_response = self.client.Order.Order_new(
                symbol="XBTUSD", side="Buy", orderQty=self.money_to_trade * self.leverage, stopPx=exec_price+10, price=exec_price+10, execInst="LastPrice,ReduceOnly").result()

        return stop_order_response

    def set_take_profit(self, exec_price, response):
        if response[0]['side'] == 'Buy':
            take_profit_order_response = self.client.Order.Order_new(
                symbol="XBTUSD", side="Sell", orderQty=self.money_to_trade * self.leverage, stopPx=exec_price+7, price=exec_price+10, ordType='LimitIfTouched', execInst="LastPrice,ReduceOnly").result()
        elif response[0]['side'] == 'Sell':
            take_profit_order_response = self.client.Order.Order_new(
                symbol="XBTUSD", side="Buy", orderQty=self.money_to_trade * self.leverage, stopPx=exec_price-7, price=exec_price-10, ordType='LimitIfTouched', execInst="LastPrice,ReduceOnly").result()

        return take_profit_order_response

    def send_notifcation(self, response, **kwargs):
        msg = ''
        if response is None:
            msg = kwargs.get('extra', None)
            self.slack_msg(msg)
            return True
        elif response == 'Active Order':
            msg = kwargs.get('extra', None)
            self.slack_msg(msg)
            return True
        elif response[0]['side'] == 'Buy':
            msg = 'Buy Signal From Bitmex'
            self.slack_msg(msg)
            return True
        elif response[0]['side'] == 'Sell':
            msg = 'Sell Signal From Bitmex'
            self.slack_msg(msg)
            return True

    def slack_msg(self, msg):
        try:
            self.sc.api_call(
                "chat.postMessage",
                channel="bitmexbot",
                text=msg+":smile:",
                username='My Robot',
                icon_emoji=':robot_face:')
            # return True
        except:
            print('Exception in Slack API')
            # return False
