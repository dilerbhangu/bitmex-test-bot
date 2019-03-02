
class Trader():
    def __init__(self, client,sc, strategy, ohlcv_candles, money_to_trade=100, leverage=5):
        self.client = client
        self.sc = sc
        self.strategy = strategy
        self.money_to_trade = money_to_trade
        self.leverage = leverage
        self.ohlcv_candles = ohlcv_candles

    def execute_trade(self):
        predict, self.ohlcv_candles = self.strategy.predict()
        print('Predication: {}'.format(predict))

        try:
            if predict == -1:
                response = self.client.Order.Order_new(
                    symbol="XBTUSD", side="Sell", orderQty=self.money_to_trade * self.leverage).result()
                return response
            elif predict == 1:
                response = self.client.Order.Order_new(
                    symbol="XBTUSD", side="Buy", orderQty=self.money_to_trade * self.leverage).result()
                return response
            else:
                response = None
                return response

        except Exception as e:
            print('something goes wrong')

        return

    def set_stop_limit(self, exec_price, response):
        if response[0]['side'] == 'Buy':
            stop_order_response = self.client.Order.Order_new(
                symbol="XBTUSD", side="Sell", orderQty=self.money_to_trade * self.leverage, stopPx=exec_price-7, price=exec_price-10).result()
        elif response[0]['side'] == 'Sell':
            stop_order_response = self.client.Order.Order_new(
                symbol="XBTUSD", side="Buy", orderQty=self.money_to_trade * self.leverage, stopPx=exec_price+7, price=exec_price+10).result()

        return stop_order_response

    def set_take_profit(self, exec_price, response):
        if response[0]['side'] == 'Buy':
            take_profit_order_response = self.client.Order.Order_new(
                symbol="XBTUSD", side="Sell", orderQty=self.money_to_trade * self.leverage, stopPx=exec_price+15, price=exec_price+20, ordType='LimitIfTouched').result()
        elif response[0]['side'] == 'Sell':
            take_profit_order_response = self.client.Order.Order_new(
                symbol="XBTUSD", side="Buy", orderQty=self.money_to_trade * self.leverage, stopPx=exec_price-15, price=exec_price-20, ordType='LimitIfTouched').result()

        return take_profit_order_response

    def send_notifcation(self,sc,response):
        msg = ''
        if response = 1:
            msg = 'Buy Signal From Bitmex'
            return slack_msg(sc,msg)
        elif response = -1:
            msg = 'Sell Signal From Bitmex'
            return slack_msg(sc,msg)
        elif response = None:
            msg = 'Order Filled Signal From Bitmex'
            return slack_msg(sc,msg)


    def slack_msg(self,sc,msg):
        try:
            sc.api_call(
              "chat.postMessage",
              channel="bitmexbot",
              text=msg+":smile:",
               icon_emoji=':robot_face:')
               return True
        except:
            print('Exception in Slack API')
            return False
