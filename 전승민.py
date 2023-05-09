import requests
import json
import time
from datetime import datetime

url = "https://api.upbit.com/v1/orderbook?markets=KRW-BTC"
headers = {"accept": "application/json"}

f = open("response.csv", "w")
f.write("price|size|type|timestamp\n")

def getOrderBook():
    response = requests.get(url, headers=headers)
   # print (response.text)
    jsonObject = json.loads(response.text)

    for some_variable in jsonObject:
        jsonArray = some_variable.get("orderbook_units")
        for list in jsonArray:
            f.write(str(list.get("bid_price")) + "|" + str(list.get("bid_size")) + "|0|" + str(datetime.fromtimestamp(some_variable.get("timestamp")//1000))+ '\n')
        for list in jsonArray:
            f.write(str(list.get("ask_price")) + "|" + str(list.get("ask_size")) + "|1|" + str(datetime.fromtimestamp(some_variable.get("timestamp")//1000))+ '\n')
  
def main():
    st = updt = datetime.now()
    i = 0
    while True:
        now = datetime.now()
        exetime =  now - updt
        if (exetime.seconds >= 1):
            updt = datetime.now()
            i+=1
            #print("count="+str(i))
            getOrderBook()
        diff =  now - st
        if (diff.seconds/60 > 1440):
            f.close()
            break        

main()

 

    
    
