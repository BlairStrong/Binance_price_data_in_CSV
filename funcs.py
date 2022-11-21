import requests
import json
from datetime import datetime, timedelta
import csv
from time import sleep
import os.path


#url = "https://api.binance.com/api/v3/klines?symbol="+symbol+"&interval="+interval+"&startTime="+startTime+"&endTime="+endTime+"&limit=1000"
#Start time of: 1501545600000 = 2017-08-01 01:00:00
#Binance API call: https://api.binance.com/
#looking for kline: api/v3/klines
#kline data:
"""symbol	    STRING	    YES	
interval	    ENUM	    YES	
startTime	    LONG	    NO	
endTime	L       ONG	        NO	
limit	        INT     	NO"""



def get_price_history(symbol, interval):

    #The endtime must be identified to stop the script
    date_time_Last_2_hours = datetime.now() - timedelta(hours=2)
    endTime = datetime.fromtimestamp(int("1501545600000") / 1000)

    #define the start_time

    #check if a file already exists, if it does, collect data from last readding. if not, collect data from 2017 start time.
    fe = os.path.exists(f"{symbol}_prices_{interval}.csv")
    if fe:
        with open(f"{symbol}_prices_{interval}.csv", "r", newline='') as f1:
            last_line = f1.readlines()[-1]
            startTime = last_line[:13]
            print(startTime)

    #below is the standard start time for collecting data. 1501545600000 comes out to be: 2017-08-01 01:00:00
    else:
        startTime = "1501545600000"

    print('startTime:',startTime)

    while endTime < date_time_Last_2_hours:
        url = "https://api.binance.com/api/v3/klines?symbol="+symbol+"&interval="+interval+"&startTime="+startTime+"&limit=1000"

        #run requests to get the url data from binance
        r = requests.get(url)
        prices_json = r.json()

        #save the json
        with open(f"{symbol}_prices_{interval}.json", "a") as fp:
            json.dump('r.json', fp)


        #If there is data in the file, find the last entry to avoid duplicating entries.
        if fe:
            #open the csv to save data to
            data_csv = open(f"{symbol}_prices_{interval}.csv", "a", newline='')
            csv_writer = csv.writer(data_csv)

            #open the json to save data to
            data_json = open(f"{symbol}_prices_{interval}.json", "a", newline='')

            #writing price data with timestap after
            for item in prices_json:
                if int(item[0]) > int(startTime):
                    print(symbol, item)
                    csv_writer.writerow(item)


        #if new file, create write file and use start date of 2017
        else:
            data_csv = open(f"{symbol}_prices_{interval}.csv", "a", newline='')
            csv_writer = csv.writer(data_csv)
            csv_writer.writerow(["Kline open time", "Open", "High", "Low", "Close", "Volume", "Kline Close time", "Quote asset volume", "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume", "unused field, Ignore"])

            for item in prices_json:
                csv_writer.writerow(item)

        data_csv.close()
        list_len = len(prices_json)-1
        print(symbol, prices_json[list_len])
        startTime = str(prices_json[len(prices_json)-1][0])
        endTime = datetime.fromtimestamp(prices_json[len(prices_json)-1][0]/1000)
        sleep(0.3)

