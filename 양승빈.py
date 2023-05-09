import time
import requests
import pandas as pd
import datetime 
import os

fn = './2023-05-08-bithumb-btc-orderbook.csv'
last_update_time = 0
while True:
    timestamp = int(time.time())
    if timestamp <= 1683471599: continue
    if timestamp >= 1683590400:  break
    if timestamp-last_update_time < 1: continue

    book = {}
    response = requests.get ('https://api.bithumb.com/public/orderbook/BTC_KRW/?count=5')
    book = response.json()

    data = book['data']

    bids = (pd.DataFrame(data['bids'])).apply(pd.to_numeric,errors='ignore')
    bids.sort_values('price', ascending=False, inplace=True)
    bids = bids.reset_index(); del bids['index']
    bids['type'] = 0
    
    asks = (pd.DataFrame(data['asks'])).apply(pd.to_numeric,errors='ignore')
    asks.sort_values('price', ascending=True, inplace=True)
    asks['type'] = 1 

    df = bids._append(asks)
        
    last_update_time = int(time.time())
    timestamp = datetime.datetime.fromtimestamp(last_update_time)
    req_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')

    df['quantity'] = df['quantity'].round(decimals=4)
    df['timestamp'] = req_timestamp
    
    print (df)
    print ("\n")
    should_write_header = os.path.exists(fn)

    if should_write_header == False:
       df.to_csv(fn, index=False, header=True, mode = 'a', sep = '|')
    else:
       df.to_csv(fn, index=False, header=False, mode = 'a', sep = '|')


