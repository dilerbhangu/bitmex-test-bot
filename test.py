# import bitmex
# from keys import ID,SECRET
# import time
# client = bitmex.bitmex(test=False,api_key=ID,api_secret=SECRET)
# x=client.Trade.Trade_getBucketed(binSize='5m',reverse=True,symbol='XBTUSD',count=1).result()[0]
# # print(x[0]['close'])
#
# counter = 1
# responnse=client.Order.Order_new(
#     symbol="XBTUSD", side="Buy", orderQty=1 * 1).result()
#
# print(responnse)
# # while True:
#     print(responnse)
#     print('Order Status is :{}'.format(responnse[0]['ordStatus']))
#     time.sleep(5)
#     print('print after sleep {}'.format(counter))
#     counter = counter + 1

import requests
import json

URL = 'http://www.way2sms.com/api/v1/sendCampaign'

# get request
def sendPostRequest(reqUrl, apiKey, secretKey, useType, phoneNo, textMessage):
  req_params = {
  'apikey':apiKey,
  'secret':secretKey,
  'usetype':useType,
  'phone': phoneNo,
  'message':textMessage,
  }
  return requests.post(reqUrl, req_params)

# get response
response = sendPostRequest(URL, '7CMBFVNTMWO7R2WRQPYMYIKD2JV562YG', '527YQE4QEJ84OEJ0', 'prod', '7988487456', 'HII' )
"""
  Note:-
    you must provide apikey, secretkey, usetype, mobile, senderid and message values
    and then requst to api
"""
# print response if you want
print(response.text)
