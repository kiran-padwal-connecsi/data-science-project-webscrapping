import urllib.request, json
from datetime import datetime, timedelta
import math
import os
import pandas
import xlrd

from model.MyModel import MyModel
import time
import requests
import re

class CryptoCompareController:
    def __init__(self):
        self.all_exchanges_and_trading_pairs_url = "https://min-api.cryptocompare.com/data/all/exchanges"
        self.all_coin_list_url = "https://min-api.cryptocompare.com/data/all/coinlist"
        self.daily_data_url = "https://min-api.cryptocompare.com/data/histoday?"
        self.hourly_data_url = "https://min-api.cryptocompare.com/data/histohour?"
        self.allData = 'allData=true'
        self.limit='limit=1500'
        self.e = 'e='
        self.fsym = 'fsym='
        self.tsym = 'tsym='
        self.url_rate_limit = "https://min-api.cryptocompare.com/stats/rate/limit"
        self.application_name = "extraParams=phamminhhiep280690@gmail.com"


    def get_all_exchanges_and_trading_pairs(self):
        json_data = self.get_Json_data(url=self.all_exchanges_and_trading_pairs_url)
        print(json_data)
        return json_data

    def get_all_coin_list(self):
        json_data = self.get_Json_data(url=self.all_coin_list_url)
        print(json_data['Data'])
        return json_data



    def get_Json_data(self, url):
        with urllib.request.urlopen(url) as url:
            json_data = json.loads(url.read().decode())
        return json_data

    def get_Json_data_Request_Lib(self, url):
        r = requests.get(url=url)
        json_data = r.json()
        return json_data

    ############################### Insert and update calls##############################
    def get_all_coins_list(self):
        json_data = self.get_Json_data(url=self.all_coin_list_url)
        coins_list = json_data['Data']
        # print(coins_list)
        # print(len(coins_list))
        # exit()
        data = []
        for name,value in coins_list.items():
            print(name)
            coin_data = []
            coin_data.append(value['Id'])
            coin_data.append(value['Url'])
            if 'ImageUrl' in value:
                coin_data.append(value['ImageUrl'])
            else: coin_data.append(None)
            coin_data.append(value['Name'])
            coin_data.append(value['Symbol'])
            coin_data.append(value['CoinName'])
            coin_data.append(value['FullName'])
            coin_data.append(value['Algorithm'])
            coin_data.append(value['ProofType'])
            coin_data.append(value['FullyPremined'])
            coin_data.append(value['TotalCoinSupply'])
            coin_data.append(value['PreMinedValue'])
            coin_data.append(value['TotalCoinsFreeFloat'])
            coin_data.append(value['SortOrder'])
            coin_data.append(value['Sponsored'])
            coin_data.append(value['IsTrading'])

            coin_data = tuple(coin_data)
            # print(coin_data)
            data.append(coin_data)
        myModelObj = MyModel()
        myModelObj.insertUpdate_cryptoCompare_all_coin_list(data=data)


    def update_exchange_pairs(self):
        json_data = self.get_Json_data(url=self.all_exchanges_and_trading_pairs_url)
        # print(json_data)
        # exit()
        # print(type(json_data))
        # print(len(json_data))
        # exit()
        # myModelObj2 = MyModel()
        # coin_list = myModelObj2.get_cryptoCompare_coin_list()
        # crypto_symbol = []
        # for item in coin_list:
        #     print(item[4])
            # crypto_symbol.append(item[4])

        # exit()
        myModelObj1 = MyModel()
        exchange_pairs = myModelObj1.get_exchange_pair_data(is_fiat_pair=False)
        # print(exchange_pairs)
        # exit()
        list_of_exchange_pair_tuple = []
        for pair in exchange_pairs:
            tuple_pair = (pair[1],pair[2],pair[3],pair[4])
        #     string_pair = str(pair[1])+str(pair[2])+str(pair[3])+str(pair[4])
            list_of_exchange_pair_tuple.append(tuple_pair)


        myModelObj = MyModel()
        fiat_symbols = myModelObj.get_fiat_symbols()
        # print(fiat_symbols)
        fiat_currency = []
        for item in fiat_symbols:
            # print(item[0])
            fiat_currency.append(item[0])
        # exit()
        # fiat_symbol = ['JPY', 'USD', 'EUR', 'USDT', 'AIC', 'PLN',
        #               'GBP', 'CAD', 'ZAR', 'RUB', 'BRL', 'AUD', 'CNY', 'KRW']
        data = []

        for exchange_name,trading_pairs in json_data.items():

            for symbol,currencies in trading_pairs.items():

                for currency in currencies:

                    if currency  in fiat_currency:
                        is_fiat_pair = 1
                    else:
                        is_fiat_pair = 0
                    tuple_data = (exchange_name,symbol,currency,is_fiat_pair)
                    if tuple_data not in list_of_exchange_pair_tuple:
                        data.append(tuple_data)
                # print("-----------------")
        print(data)
        print(len(data))
        # exit()
        myModelObj = MyModel()
        myModelObj.insertUpdate_cryptoCompare_exchange_pairs(data=data)


    def get_fiat_daily_data(self):
        myModelObj = MyModel()
        exchange_pair_data = myModelObj.get_exchange_pair_data(is_fiat_pair="True")

        print(len(exchange_pair_data))
        # print(exchange_pair_data)
        # exit()
        counter = 1
        for item in exchange_pair_data:
            symbol = item[2]
            currency = item[3]
            exchange_name = item[1]
            exchange_pair_id = item[0]
            #url = self.daily_data_url+self.fsym+symbol+'&'+self.tsym+currency+'&limit=1&'+self.e+exchange_name+'&'+self.application_name
            url = self.daily_data_url+self.fsym+symbol+'&'+ self.tsym+currency+'&allData=true&'+self.e+exchange_name+'&'+self.application_name
            #url = self.daily_data_url+self.fsym+symbol+'&'+self.tsym+currency+'&limit=1&'+self.e+exchange_name+'&'+self.application_name
            # url = self.daily_data_url+self.fsym+symbol+'&'+ self.tsym+currency+'&allData=true&'+self.e+exchange_name+'&'+self.application_name
            #url = self.daily_data_url+self.fsym+symbol+'&'+ self.tsym+currency+'&allData=true&'+self.e+exchange_name+'&'+self.application_name
            # print(url)
            # url = self.daily_data_url + self.fsym + "QTUM" + '&' + self.tsym + "USD" + '&allData=true&' + self.e + "LiveCoin" + '&' + self.application_name
            # print("exchange pair id = ",exchange_pair_id)
            print(url)
            # exit()
            rate_limit = self.get_Json_data(url=self.url_rate_limit)
            calls_left_per_minute_histo = rate_limit['Minute']['CallsLeft']['Histo']
            calls_left_per_hour_histo = rate_limit['Hour']['CallsLeft']['Histo']
            # print("Calls left per minute histo = ", calls_left_per_minute_histo)
            # print("Calls left per hour histo = ", calls_left_per_hour_histo)
            # while calls_left_per_minute_histo < 20:
            # if calls_left_per_hour_histo < 20:
            #     print("Calls left per minute < 20 ", calls_left_per_minute_histo)
            #     print("Calls left per Hour < 20 ", calls_left_per_hour_histo)
            #
            while calls_left_per_hour_histo < 20:
                # print("i m sleeping 5 secs again...")
                time.sleep(5)
                # rate_limit1 = self.get_Json_data(url=self.url_rate_limit)
                calls_left_per_hour_histo = self.get_Json_data(url=self.url_rate_limit)['Hour']['CallsLeft']['Histo']
                # print("calls per hour limit = ",calls_left_per_hour_histo)
               # calls_left_per_hour_histo = calls_left_per_hour_histo1

            # if calls_left_per_minute_histo < 20:
            #     print("Calls left per minute < 20 ",calls_left_per_minute_histo)
            #     print("i m sleeping 60 secs ")
            while calls_left_per_minute_histo <20 :
                # print("i m sleeping 5 secs again...")
                time.sleep(5)
                #rate_limit2 = self.get_Json_data(url=self.url_rate_limit)
                calls_left_per_minute_histo = self.get_Json_data(url=self.url_rate_limit)['Minute']['CallsLeft']['Histo']
                # print("calls left per minute = ",calls_left_per_minute_histo)
                #calls_left_per_minute_histo = calls_left_per_minute_histo1

            json_data = self.get_Json_data_Request_Lib(url=url)
            time.sleep(1)

            daily_data = json_data['Data']

            # print(len(daily_data))
            myData = []
            for row in daily_data:
                updated_date=row['time']
                last_updated_utc = datetime.utcfromtimestamp(updated_date).strftime('%Y-%m-%d %H:%M:%S')
                # print(type(last_updated_utc))
                lastUpdatedTime = datetime.strptime(last_updated_utc, "%Y-%m-%d %H:%M:%S")

                open=row['open']
                high=row['high']
                low=row['low']
                close = row['close']
                volume_from = row['volumefrom']
                volume_to = row['volumeto']
                tuple_data = (exchange_pair_id,lastUpdatedTime,open,high,low,close,volume_from,volume_to)
                # print(tuple_data)

                myData.append(tuple_data)


            if myData:
                # print(myData)
                print("id is not empty",exchange_pair_id)
                # exit()
                final_data = []
                # print("length my all data = ", len(myData))
                try:
                    del myData[-1]

                    for element in myData:
                        if element[7]!=0:
                            # print(element[7])
                            final_data.append(element)
                except:
                    pass

                # print(exchange_pair_id)
                # # print(final_data)
                # print("length my final data = ",len(final_data))
                # exit()
                if final_data:
                    try:
                        myModelObj1 = MyModel()
                        myModelObj1.insertUpdate_cryptoCompare_fiat_daily_data(data=final_data)
                    except:pass
                else: print("empty final data")
            else: print(symbol,currency,exchange_pair_id)
            # exit()

    # redundant method 
    def get_fiat_last_day_data(self):
        myModelObj = MyModel()
        exchange_pair_data = myModelObj.get_exchange_pair_data(is_fiat_pair="True")

        print(len(exchange_pair_data))
        # exit()
        counter = 1
        for item in exchange_pair_data:
            symbol = item[2]
            currency = item[3]
            exchange_name = item[1]
            exchange_pair_id = item[0]
            url = self.daily_data_url+self.fsym+symbol+'&'+self.tsym+currency+'&'+'limit=1'+'&'+self.e+exchange_name+'&'+self.application_name
            # url="https://min-api.cryptocompare.com/data/histoday?fsym=DJASANYANVIX&tsym=JPY&limit=1&e=Zaif"
            print(url)
            # exit()
            print("exchange pair id = ",exchange_pair_id)

            rate_limit = self.get_Json_data(url=self.url_rate_limit)
            calls_left_per_minute_histo = rate_limit['Minute']['CallsLeft']['Histo']
            calls_left_per_hour_histo = rate_limit['Hour']['CallsLeft']['Histo']
            print("Calls left per minute histo = ", calls_left_per_minute_histo)
            print("Calls left per hour histo = ", calls_left_per_hour_histo)
            # while calls_left_per_minute_histo < 20:
            #     if calls_left_per_hour_histo < 20:
            #         print("Calls left per minute < 20 ", calls_left_per_minute_histo)
            #         print("Calls left per Hour < 20 ", calls_left_per_hour_histo)
            #         print("i have to sleep 10 Minutes")
            #         time.sleep(600)
            #     else:
            #         print("Calls left per minute < 20 ",calls_left_per_minute_histo)
            #         print("i m sleeping 2 Minutes ")
            #         time.sleep(120)
            while counter > 296:
                print("counter = ",counter)
                print(" i m sleeping 60 secs")
                time.sleep(60)
                counter = 0
            json_data = self.get_Json_data_Request_Lib(url=url)
            counter+=1
            # print(counter)
            # exit()
            daily_data = json_data['Data']
            print("daily data = ",daily_data)
            last_day_data = []
            if daily_data:
                last_day_data.append(daily_data[-1])
            # print(type(last_day_data))
            print(last_day_data)
            # exit()
            # print(len(daily_data))
            myData = []
            for row in last_day_data:
                # print(exchange_pair_id)
                # print(exchange_name)
                # print(symbol)
                # print(currency)
                # print(row)
                updated_date=row['time']
                last_updated_utc = datetime.utcfromtimestamp(updated_date).strftime('%Y-%m-%d %H:%M:%S')
                # print(type(last_updated_utc))
                lastUpdatedTime = datetime.strptime(last_updated_utc, "%Y-%m-%d %H:%M:%S")
                # print(lastUpdatedTime)
                lastUpdatedTime = lastUpdatedTime - timedelta(seconds=1)
                # print(lastUpdatedTime)
                # exit()
                open=row['open']
                high=row['high']
                low=row['low']
                close = row['close']
                volume_from = row['volumefrom']
                volume_to = row['volumeto']
                tuple_data = (exchange_pair_id,lastUpdatedTime,open,high,low,close,volume_from,volume_to)
                # print(tuple_data)
                if open !=0 and high != 0 and low != 0 and close !=0:
                    myData.append(tuple_data)
                # print(myData)
                # print(len(myData))
                # exit()

            if  myData:
                    print(myData)
                    print("length my data = ",len(myData))
                    # exit()
                    myModelObj1 = MyModel()
                    myModelObj1.insertUpdate_cryptoCompare_fiat_daily_data(data=myData)
            else: print('my data is empty')



    def get_fiat_24hour_data(self):
        myModelObj = MyModel()
        fiat_exchange_pair_data = myModelObj.get_exchange_pair_data(is_fiat_pair="True")
        counter = 1

        for item in fiat_exchange_pair_data:
            symbol = item[2]
            currency = item[3]
            exchange_name = item[1]
            exchange_pair_id = item[0]
            # url = self.hourly_data_url + self.fsym + symbol + '&' + self.tsym + currency + '&' +'limit=39'+'&'+ self.e + exchange_name+'&toTs=1527580800'
            url = self.hourly_data_url + self.fsym + symbol + '&' + self.tsym + currency + '&' + 'limit=24' + '&' + self.e + exchange_name
            print(url)
            # exit()
            print("counter = ",counter)
            print("exchange pair id = ",exchange_pair_id)
            while counter > 290:
                print("counter = ", counter)
                # exit()
                time.sleep(60)
                print("i m sleeping 30 secs")
                counter = 1

            json_data = self.get_Json_data(url=url)
            counter +=1
            hourly_data = json_data['Data']
            print(len(hourly_data))
            myData = []
            for row in hourly_data:
                # print(exchange_pair_id)
                # print(exchange_name)
                # print(symbol)
                # print(currency)
                # print(row)
                updated_date = row['time']
                last_updated_utc = datetime.utcfromtimestamp(updated_date).strftime('%Y-%m-%d %H:%M:%S')
                # print(type(last_updated_utc))
                lastUpdatedTime = datetime.strptime(last_updated_utc, "%Y-%m-%d %H:%M:%S")
                # print(lastUpdatedTime)
                # lastUpdatedTime = lastUpdatedTime - timedelta(seconds=1)
                # print(lastUpdatedTime)
                # exit()
                open = row['open']
                high = row['high']
                low = row['low']
                close = row['close']
                volume_from = row['volumefrom']
                volume_to = row['volumeto']
                tuple_data = (exchange_pair_id, lastUpdatedTime, open, high, low, close, volume_from, volume_to)
                # print(tuple_data)
                if volume_from !=0:
                    myData.append(tuple_data)
                # print(myData)
                # exit()

            if myData:
                # print(myData)
                try:
                    del myData[-1]
                except:
                    pass
                myModelObj1 = MyModel()
                myModelObj1.insertUpdate_cryptoCompare_fiat_hourly_data(data=myData)
                # exit()
            else:
                print('my data is empty')

    def get_fiat_24hour_data_by_days(self):
        myModelObj = MyModel()
        fiat_exchange_pair_data = myModelObj.get_exchange_pair_data(is_fiat_pair="True")
        counter = 1

        for item in fiat_exchange_pair_data:
            symbol = item[2]
            currency = item[3]
            exchange_name = item[1]
            exchange_pair_id = item[0]
            # url = self.hourly_data_url + self.fsym + symbol + '&' + self.tsym + currency + '&' +'limit=39'+'&'+ self.e + exchange_name+'&toTs=1527580800'
            url = self.hourly_data_url + self.fsym + symbol + '&' + self.tsym + currency + '&' + 'limit=48&toTs=1527811200' + '&' + self.e + exchange_name
            print(url)
            # exit()
            print("counter = ",counter)
            print("exchange pair id = ",exchange_pair_id)
            while counter > 290:
                print("counter = ", counter)
                # exit()
                time.sleep(60)
                print("i m sleeping 30 secs")
                counter = 1

            json_data = self.get_Json_data(url=url)
            counter +=1
            hourly_data = json_data['Data']
            print(len(hourly_data))
            myData = []
            for row in hourly_data:
                # print(exchange_pair_id)
                # print(exchange_name)
                # print(symbol)
                # print(currency)
                # print(row)
                updated_date = row['time']
                last_updated_utc = datetime.utcfromtimestamp(updated_date).strftime('%Y-%m-%d %H:%M:%S')
                # print(type(last_updated_utc))
                lastUpdatedTime = datetime.strptime(last_updated_utc, "%Y-%m-%d %H:%M:%S")
                # print(lastUpdatedTime)
                # lastUpdatedTime = lastUpdatedTime - timedelta(seconds=1)
                # print(lastUpdatedTime)
                # exit()
                open = row['open']
                high = row['high']
                low = row['low']
                close = row['close']
                volume_from = row['volumefrom']
                volume_to = row['volumeto']
                tuple_data = (exchange_pair_id, lastUpdatedTime, open, high, low, close, volume_from, volume_to)
                # print(tuple_data)
                if volume_from !=0:
                    myData.append(tuple_data)
                # print(myData)
                # exit()

            if myData:
                # print(myData)
                try:
                    del myData[-1]
                except:
                    pass
                myModelObj1 = MyModel()
                myModelObj1.insertUpdate_cryptoCompare_fiat_hourly_data_test(data=myData)
                # exit()
            else:
                print('my data is empty')



    def get_fiat_historical_hour_data(self):

        # yesterDay = datetime.today() - timedelta(days=1)
        # print(yesterDay)
        # timeStamp = yesterDay.timestamp()
        # print(timeStamp)
        # m = re.search(r'(.)\w+', str(timeStamp))

        # print(to_timeStamp)
        # exit()
        # exchange_name= ['Coinbase']
        # exchange_name=['bitFlyerFX','OKCoin', 'Bitfinex', 'Bithumb', 'BTCChina', 'Coinbase', 'Kraken', 'Binance','Bitstamp','OKEX','bitFlyer','Coinone','HuobiPro','Coincheck','Poloniex','Korbit','Gemini','Quoine','BitTrex','TrustDEX' 'Zaif','HitBTC','LakeBTC','Upbit','Huobi']
        # exchange_pair_ids = []
        # for name in exchange_name:
        myModelObj = MyModel()
        exchange_pair_data = myModelObj.get_exchange_pair_data(is_fiat_pair="True")
        # pairs = [('BTC','USD'),('LTC','USD')]
        print(len(exchange_pair_data))
        # myModelObj3= MyModel()
        # results_priority = myModelObj3.get_priority_exchange_names(priority=1)
        # print(results_priority)
        # exit()
        # pri_exchange_names = []
        # for name in results_priority:
        #     pri_exchange_names.append(name[0])

        # priority_exchange_pair_data_list = []
        # for pair in exchange_pair_data:
        #     if pair[1] not in pri_exchange_names:
        #         print("i m inside")
        #         priority_exchange_pair_data_list.append(pair)
        # print(priority_exchange_pair_data_list)
        # print(len(priority_exchange_pair_data_list))
        # exit()
        # for pair in pairs:
        #     exchange_pair_data = myModelObj.get_exchange_pair_data_custom(is_fiat_pair="True",symbol=pair[0],currency=pair[1])
        #     print(len(exchange_pair_data))
        #     print(exchange_pair_data)
        #     exchange_pair_data_list.extend(exchange_pair_data)
        # print(exchange_pair_data_list)
        # print(len(exchange_pair_data_list))
        # exit()

            # for pair_id in results:
            #     exchange_pair_ids.append(pair_id)
        # print(len(data))
        # print(exchange_pair_ids)
        # print(len(exchange_pair_ids))
        # exit()


        for item in exchange_pair_data:
            # to_timeStamp = m.group(0)
            to_timeStamp = "1529305200"
            # print(to_timeStamp)
            symbol = item[2]
            currency = item[3]
            exchange_name = item[1]
            exchange_pair_id = item[0]
            loop_count= 0
            total_hourly_data=[]

            while loop_count<7:
                # print("to timestamp",to_timeStamp)
                url = self.hourly_data_url + self.fsym + symbol + '&' + self.tsym + currency + '&' + 'limit=2000' + '&' + self.e + exchange_name+'&toTs='+str(to_timeStamp)
                # url = "https://min-api.cryptocompare.com/data/histohour?fsym=BTC&tsym=USD&limit=2000&e=CoinBase"+"&toTs="+str(to_timeStamp)
                # url_list.append(url)
                # url = "https://min-api.cryptocompare.com/data/histohour?fsym=DJASANYANVIX&tsym=JPY&limit=2000&e=Zaif&toTs=1527430163"
                print(url)
                loop_count+=1

                rate_limit = self.get_Json_data(url=self.url_rate_limit)
                calls_left_per_minute_histo = rate_limit['Minute']['CallsLeft']['Histo']
                calls_left_per_hour_histo = rate_limit['Hour']['CallsLeft']['Histo']
                print("Calls left per minute histo = ", calls_left_per_minute_histo)
                print("Calls left per hour histo = ", calls_left_per_hour_histo)

                while calls_left_per_hour_histo < 20:
                    time.sleep(5)
                    calls_left_per_hour_histo = self.get_Json_data(url=self.url_rate_limit)['Hour']['CallsLeft']['Histo']
                while calls_left_per_minute_histo < 20:
                    time.sleep(5)
                    calls_left_per_minute_histo = self.get_Json_data(url=self.url_rate_limit)['Minute']['CallsLeft']['Histo']

                json_data = self.get_Json_data(url=url)
                time.sleep(1)

                hourly_data = json_data['Data']
                total_hourly_data.extend(hourly_data)
                # print(len(total_hourly_data))
                try:
                    time_from = json_data['TimeFrom']
                    to_timeStamp = time_from
                except:
                    pass
                # print("time from = ",time_from)

            # print(total_hourly_data)
            print("length before duplicate",len(total_hourly_data))
            new_total_hourly_data = self.remove_duplicates_from_listof_dict(list_dict=total_hourly_data)
            print("new length after removing duplicates",len(new_total_hourly_data))

            myData = []
            for row in new_total_hourly_data:
                updated_date = row['time']
                last_updated_utc = datetime.utcfromtimestamp(updated_date).strftime('%Y-%m-%d %H:%M:%S')
                lastUpdatedTime = datetime.strptime(last_updated_utc, "%Y-%m-%d %H:%M:%S")
                # lastUpdatedTime = lastUpdatedTime - timedelta(seconds=1)
                open = row['open']
                high = row['high']
                low = row['low']
                close = row['close']
                volume_from = row['volumefrom']
                # print("Volume from = ",volume_from)
                volume_to = row['volumeto']
                tuple_data = (exchange_pair_id, lastUpdatedTime, open, high, low, close, volume_from, volume_to)
                # print(tuple_data)
                if volume_from !=0:
                    print("Volume from = ",volume_from)
                    myData.append(tuple_data)

                # print(myData)
                # exit()

            if myData:
                # print(myData)
                print(len(myData))
                myModelObj1 = MyModel()
                myModelObj1.insertUpdate_cryptoCompare_fiat_hourly_data(data=myData)
                # exit()
            else:
                print('my data is empty')
                # exit()


    def update_cryptoCompare_fiat_list(self):
         path = os.path.dirname(os.path.abspath(__file__))
         print(path)
         # exit()
         df = pandas.read_excel(path+"/"'fiats.xlsx')
         # print the column names
         # print(df.columns)
         # exit()
         # get the values for a given column
         # symbols = df['index'].values
         # print(symbols)
         # exit()
         # get a data frame with selected columns
         FORMAT = ['index', 'Currency', 'fxUSD']

         df_selected = df[FORMAT]
         # print(df_selected)
         # print(type(df_selected))
         data = []
         # print(df_selected)
         df1 = df_selected.replace(pandas.np.nan, '', regex=True)
         # print(df1)
         # exit()
         for index, row in df1.iterrows():
             tuple_data = (row['index'], row['Currency'], row['fxUSD'])
             # print(tuple_data)
             data.append(tuple_data)
             # exit()
         print(data)
         # exit()
         myMdolelObj = MyModel()
         myMdolelObj.update_cryptoCompare_fiat_list(data=data)
         # exit()

    def remove_duplicates_from_listof_dict(self,list_dict):
        seen = set()
        new_l = []
        for d in list_dict:
            t = tuple(d.items())
            if t not in seen:
                seen.add(t)
                new_l.append(d)
        return new_l

    def get_agg_daily(self):
        myModelObj = MyModel()
        symbol = myModelObj.get_symbol_from_cryptoCompare_coin_list()
        # print(symbol)
        counter = 1
        for item in symbol:
            sym = item[0]
            currency = 'USD'
            url = self.daily_data_url + self.fsym + sym + '&' + self.tsym + currency + '&' + 'limit=1'
            rate_limit = self.get_Json_data(url=self.url_rate_limit)
            calls_left_per_minute_histo = rate_limit['Minute']['CallsLeft']['Histo']
            calls_left_per_hour_histo = rate_limit['Hour']['CallsLeft']['Histo']
            print("Calls left per minute histo = ", calls_left_per_minute_histo)
            print("Calls left per hour histo = ", calls_left_per_hour_histo)

            while counter > 296:
                print("counter = ", counter)
                print("Calls left per minute histo = ", calls_left_per_minute_histo)
                print("Calls left per hour histo = ", calls_left_per_hour_histo)
                print(" i m sleeping 60 secs")
                time.sleep(60)
                counter = 0
            json_data = self.get_Json_data_Request_Lib(url=url)
            counter += 1
            daily_data = json_data['Data']
            print(len(daily_data))
            myData = []
            for row in daily_data:
                updated_date = row['time']
                last_updated_utc = datetime.utcfromtimestamp(updated_date).strftime('%Y-%m-%d %H:%M:%S')
                # print(type(last_updated_utc))
                lastUpdatedTime = datetime.strptime(last_updated_utc, "%Y-%m-%d %H:%M:%S")
                open = row['open']
                high = row['high']
                low = row['low']
                close = row['close']
                volume_from = row['volumefrom']
                volume_to = row['volumeto']
                tuple_data = (sym, currency, lastUpdatedTime, open, high, low, close, volume_from, volume_to)
                # print(tuple_data)
                if volume_to != 0:
                    myData.append(tuple_data)

            if myData:
                # print(myData)
                try:
                    del myData[-1]
                except:
                    pass
                print(sym)
                # print(myData)
                # print("length my data = ", len(myData))
                # exit()
                myModelObj1 = MyModel()
                myModelObj1.insertUpdate_cryptoCompare_agg_daily_data(data=myData)
            else:
                print('my data is empty')

    def get_agg_daily_historical(self):
        myModelObj = MyModel()
        symbol = myModelObj.get_symbol_from_cryptoCompare_coin_list()
        # print(symbol)
        counter = 1
        for item in symbol:
            sym = item[0]
            currency = 'USD'
            url = self.daily_data_url + self.fsym + sym + '&' + self.tsym + currency + '&' + 'allData=true'
            rate_limit = self.get_Json_data(url=self.url_rate_limit)
            calls_left_per_minute_histo = rate_limit['Minute']['CallsLeft']['Histo']
            calls_left_per_hour_histo = rate_limit['Hour']['CallsLeft']['Histo']
            print("Calls left per minute histo = ", calls_left_per_minute_histo)
            print("Calls left per hour histo = ", calls_left_per_hour_histo)

            while counter > 296:
                print("counter = ", counter)
                print("Calls left per minute histo = ", calls_left_per_minute_histo)
                print("Calls left per hour histo = ", calls_left_per_hour_histo)
                print(" i m sleeping 60 secs")
                time.sleep(60)
                counter = 0
            json_data = self.get_Json_data_Request_Lib(url=url)
            counter += 1
            daily_data = json_data['Data']
            print(len(daily_data))
            myData = []
            for row in daily_data:
                updated_date = row['time']
                last_updated_utc = datetime.utcfromtimestamp(updated_date).strftime('%Y-%m-%d %H:%M:%S')
                # print(type(last_updated_utc))
                lastUpdatedTime = datetime.strptime(last_updated_utc, "%Y-%m-%d %H:%M:%S")
                open = row['open']
                high = row['high']
                low = row['low']
                close = row['close']
                volume_from = row['volumefrom']
                volume_to = row['volumeto']
                tuple_data = (
                sym, currency, lastUpdatedTime, open, high, low, close, volume_from, volume_to)
                # print(tuple_data)
                if volume_to != 0:
                    myData.append(tuple_data)

            if myData:
                # print(myData)
                try:
                    del myData[-1]
                except:
                    pass
                print(sym)
                # print(myData)
                # print("length my data = ", len(myData))
                # exit()
                myModelObj1 = MyModel()
                myModelObj1.insertUpdate_cryptoCompare_agg_daily_data(data=myData)
            else:
                print('my data is empty')

    def get_agg_historical_hour_data(self):
        myModelObj = MyModel()
        symbols = myModelObj.get_symbol_from_cryptoCompare_coin_list()
        # pairs = [('BTC','USD'),('LTC','USD')]
        print(len(symbols))

        for sym in symbols:
            # to_timeStamp = m.group(0)
            to_timeStamp = "1528369200"
            # print(to_timeStamp)
            symbol = sym[0]
            currency = 'USD'
            loop_count = 0
            total_hourly_data = []

            while loop_count < 7:
                # print("to timestamp",to_timeStamp)
                url = self.hourly_data_url + self.fsym + symbol + '&' + self.tsym + currency + '&' + 'limit=2000&toTs=' + str(to_timeStamp)
                print(url)
                loop_count += 1
                rate_limit = self.get_Json_data(url=self.url_rate_limit)
                calls_left_per_minute_histo = rate_limit['Minute']['CallsLeft']['Histo']
                calls_left_per_hour_histo = rate_limit['Hour']['CallsLeft']['Histo']
                print("Calls left per minute histo = ", calls_left_per_minute_histo)
                print("Calls left per hour histo = ", calls_left_per_hour_histo)
                # while calls_left_per_minute_histo < 20:
                if calls_left_per_hour_histo < 20:
                    print("Calls left per Hour < 20 ", calls_left_per_hour_histo)
                    print("i have to sleep 20 Minutes")
                    time.sleep(1200)
                if calls_left_per_minute_histo < 20:
                    print("Calls left per minute < 20 ", calls_left_per_minute_histo)
                    print("i m sleeping 60 secs ")
                    time.sleep(60)

                json_data = self.get_Json_data_Request_Lib(url=url)

                hourly_data = json_data['Data']
                total_hourly_data.extend(hourly_data)
                # print(len(total_hourly_data))
                try:
                    time_from = json_data['TimeFrom']
                    to_timeStamp = time_from
                except:
                    pass
                    # print("time from = ",time_from)

            # print(total_hourly_data)
            print("length before duplicate", len(total_hourly_data))
            new_total_hourly_data = self.remove_duplicates_from_listof_dict(list_dict=total_hourly_data)
            print("new length after removing duplicates", len(new_total_hourly_data))

            myData = []
            for row in new_total_hourly_data:
                updated_date = row['time']
                last_updated_utc = datetime.utcfromtimestamp(updated_date).strftime('%Y-%m-%d %H:%M:%S')
                lastUpdatedTime = datetime.strptime(last_updated_utc, "%Y-%m-%d %H:%M:%S")
                # lastUpdatedTime = lastUpdatedTime - timedelta(seconds=1)
                open = row['open']
                high = row['high']
                low = row['low']
                close = row['close']
                volume_from = row['volumefrom']
                # print("Volume from = ",volume_from)
                volume_to = row['volumeto']
                tuple_data = (symbol,currency, lastUpdatedTime, open, high, low, close, volume_from, volume_to)
                # print(tuple_data)
                if volume_from != 0:
                    print("Volume from = ", volume_from)
                    myData.append(tuple_data)

                    # print(myData)
                    # exit()

            if myData:
                # print(myData)
                print(len(myData))
                myModelObj1 = MyModel()
                myModelObj1.insertUpdate_cryptoCompare_fiat_hourly_data(data=myData)
                # exit()
            else:
                print('my data is empty')
                # exit()



                            #####################################################################################

