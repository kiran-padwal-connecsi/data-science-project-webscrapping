import re

from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from model.coinmarketcapModel import CoinmarketcapModel
from model.MyModel import MyModel
from datetime import datetime, date, time


#coinmarketcapController = Flask(__name__)
class CoinmarketcapController:
    #coinmarketcapController.config['sqlite3_CURSORCLASS']='DictCursor'
    #database_path = coinmarketcapController.root_path+"\..\database\coinmarketcap.db"
    ############################################## Crypto Master Minds Api's START #####################################################################################
    ############################################# Crypto Master Minds Api's  END ##################


    ################################## Model Api calls to Coin Market Capital###################################
    ###get coin details#####
    def get_coin_details(self):
        URL = "https://coinmarketcap.com/all/views/all/"
        obj = CoinmarketcapModel(URL)
        rawData = obj.get_coin_data()
        # print(rawData)
        # exit()
        #myData = [item[1] for item in data]
        cleanData = []
        for item in rawData:
            #myList = str(item[1]).split("\n")
            tempList = []
            symbol = item[2]
            coin_name = item[10]
            coin_name=coin_name.split("id-")[1]
            tempList.append(symbol)
            tempList.append(coin_name)
            cleanData.append(tempList)
        print(cleanData)
        # exit()
        myModelObj = MyModel()
        myModelObj.insert_coin_details(data=cleanData)
        #obj.insert_coin_details(cleanData)

    #### get the historical daily data #######
    def get_history_data(self):
        end = datetime.today().date()
        end = str(end).replace("-","")
        # print(type(end))
        # print("end = ",end)
        # exit()
        myModelObj = MyModel()
        coin_data = myModelObj.get_coin_price_daily_records_by_range(start=0,end=100)
        # print(coin_data)
        source_id = 1
        # coin_data = [[1417,'safecoin',4]]
        #print(coin_data[0][1])
        # print(coin_data)
        print(len(coin_data))
        # exit()
        for item_coin in coin_data:
            coin_id = item_coin[0]
            no_of_rows_crypto_database= item_coin[2]
            print(type(no_of_rows_crypto_database))
            URL = "https://coinmarketcap.com/currencies/"+item_coin[1]+"/historical-data/?start=20130428&end="+end
            print(URL)
            # exit()
            # URL = "https://coinmarketcap.com/currencies/slimcoin/historical-data/?start=20130428&end=20180430"
            #URL = "https://coinmarketcap.com/currencies/farstcoin/historical-data/?start=20130428&end=20180311"
            coinmarketcapObj = CoinmarketcapModel(URL)
            rawData = coinmarketcapObj.get_daily_data()
            # print(rawData)
            # exit()
            no_of_records_coinmarketcap = len(rawData)
            print("Number of records in coinmarketcap = ",no_of_records_coinmarketcap)
            print("Number of records in crypto database = ", no_of_rows_crypto_database)
            # exit()
            if no_of_records_coinmarketcap > no_of_rows_crypto_database:
                print(no_of_records_coinmarketcap)
                print(coin_id)
                # exit()
                myModelObj1 = MyModel()
                myModelObj1.del_records_coin_price_daily(coin_id=coin_id)
                # exit()
                cleanData = []
                ### cleaing data
                for item in rawData:
                    # print(item)
                    # print(item[0])
                    idate = item[0]
                    myDate = datetime.strptime(idate, '%b %d, %Y').date()
                    # print(date.date())

                    # print(date)
                    # open = float(item[1])
                    if item[1] == "-":
                        open = 0
                    else:
                        open = float(item[1].replace(',', ''))
                    # high = float(item[2])
                    if item[2] == "-":
                        high = 0
                    else:
                        high = float(item[2].replace(',', ''))
                    # low = float(item[3])
                    if item[3] == "-":
                        low = 0
                    else:
                        low = float(item[3].replace(',', ''))
                    # close = float(item[4])
                    if item[4] == "-":
                        close = 0
                    else:
                        close = float(item[4].replace(',', ''))
                    if item[5] == "-":
                        volume = 0
                    else:
                        volume = float(item[5].replace(',', ''))
                    if item[6] == "-":
                        marketCap = 0
                    else:
                        marketCap = float(item[6].replace(',', ''))
                    # coin_id = coin_name[0]
                    #######
                    # del item[7]
                    # del item[7]
                    item.append(coin_id)
                    item.append(source_id)
                    item[0] = myDate
                    item[1] = open
                    item[2] = high
                    item[3] = low
                    item[4] = close
                    item[5] = volume
                    item[6] = marketCap

                    # print(" item  = ",item)
                    cleanData.append(item)
                    # print("clean data = ", cleanData)
                    # exit()
                # print(cleanData)
                myModelObj2 = MyModel()
                myModelObj2.insert_coin_price_daily(data=cleanData)
            else:
                # print(no_of_rows_crypto_database)
                print("History Records are Up To Date")
            # exit()

    #### get the historical daily data #######
    def get_all_historical_data(self):
        end = datetime.today().date()
        end = str(end).replace("-","")
        myModelObj = MyModel()
        coin_data = myModelObj.get_coin_details()
        # print(coin_data)
        source_id = 1
        for item_coin in coin_data:
            coin_id = item_coin[0]
            URL = "https://coinmarketcap.com/currencies/"+item_coin[3]+"/historical-data/?start=20130428&end="+end
            print(URL)
            # exit()
            coinmarketcapObj = CoinmarketcapModel(URL)
            rawData = coinmarketcapObj.get_daily_data()
            no_of_records_coinmarketcap = len(rawData)

            if no_of_records_coinmarketcap > 0:
                # exit()
                myModelObj1 = MyModel()
                myModelObj1.del_records_coin_price_daily(coin_id=coin_id)
                # exit()
                cleanData = []
                ### cleaing data
                for item in rawData:
                    idate = item[0]
                    myDate = datetime.strptime(idate, '%b %d, %Y').date()
                    if item[1] == "-":
                        open = 0
                    else:
                        open = float(item[1].replace(',', ''))
                    # high = float(item[2])
                    if item[2] == "-":
                        high = 0
                    else:
                        high = float(item[2].replace(',', ''))
                    # low = float(item[3])
                    if item[3] == "-":
                        low = 0
                    else:
                        low = float(item[3].replace(',', ''))
                    # close = float(item[4])
                    if item[4] == "-":
                        close = 0
                    else:
                        close = float(item[4].replace(',', ''))
                    if item[5] == "-":
                        volume = 0
                    else:
                        volume = float(item[5].replace(',', ''))
                    if item[6] == "-":
                        marketCap = 0
                    else:
                        marketCap = float(item[6].replace(',', ''))
                    # coin_id = coin_name[0]
                    #######
                    # del item[7]
                    # del item[7]
                    item.append(coin_id)
                    item.append(source_id)
                    item[0] = myDate
                    item[1] = open
                    item[2] = high
                    item[3] = low
                    item[4] = close
                    item[5] = volume
                    item[6] = marketCap

                    # print(" item  = ",item)
                    cleanData.append(item)
                    # print("clean data = ", cleanData)
                    # exit()
                # print(cleanData)
                myModelObj2 = MyModel()
                myModelObj2.insert_coin_price_daily(data=cleanData)

            else:

                # print(no_of_rows_crypto_database)
                print("History Records are Up To Date")


    def get_daily_data(self):
        myModelObj = MyModel()
        coin_data = myModelObj.get_coin_details()
        # print(coin_data)
        # exit()
        # coin_data = [(728260,'EFX', 0, 'effect-ai', None, None, None)]
        source_id = 1
        # print(coin_data[0][1])
        for coin_name in coin_data:
            # print(coin_name[1])
            coin_id = coin_name[0]
            URL = "https://coinmarketcap.com/currencies/" + coin_name[3] + "/historical-data/"
            # URL = "https://coinmarketcap.com/currencies/bitcoin/historical-data/"
            # URL = "https://coinmarketcap.com/currencies/quantum-resistant-ledger/historical-data/"
            coinmarketcapObj = CoinmarketcapModel(URL)
            rawData = coinmarketcapObj.get_data()
            # print("raw data = ",rawData)
            # exit()
            updateData = []
            if rawData:
                try:
                    name = rawData[0][7]
                    print(name)
                    name = name.replace('Historical data for ','')
                    print("name = ",name)
                    url = rawData[0][8]
                    print(url)
                    url = re.sub(r'http[s]?://', '', url)
                    url = re.sub(r'www[a-z0-9]?\.', '', url)
                    url = re.sub(r'/.*', '', url)
                    print("url  = ",url)
                    norm_name = name
                    print(norm_name)
                    norm_name = re.sub(r'[\.\-_]*', '', norm_name)
                    norm_name = re.sub(r'\s*', '', norm_name)
                    norm_name = re.sub(r'\(.*\)', '', norm_name)
                    norm_name = norm_name.lower().strip()
                    print("norm name = ",norm_name)
                    updateData.append(name)
                    updateData.append(norm_name)
                    updateData.append(url)
                    updateData.append(coin_id)
                    print(updateData)
                except:pass
            firstRecord = []
            if rawData:
                try:
                    firstRecord.append(rawData[0])
                except:pass
            else:
                firstRecord = []
            cleanData = []
            ### cleaing data
            for item in firstRecord:
                idate = item[0]
                myDate = datetime.strptime(idate, '%b %d, %Y').date()
                if item[1] == "-":
                    open = 0
                else:
                    open = float(item[1].replace(',', ''))
                # high = float(item[2])
                if item[2] == "-":
                    high = 0
                else:
                    high = float(item[2].replace(',', ''))
                # low = float(item[3])
                if item[3] == "-":
                    low = 0
                else:
                    low = float(item[3].replace(',', ''))
                # close = float(item[4])
                if item[4] == "-":
                    close = 0
                else:
                    close = float(item[4].replace(',', ''))
                if item[5] == "-":
                    volume = 0
                else:
                    volume = float(item[5].replace(',', ''))
                if item[6] == "-":
                    marketCap = 0
                else:
                    marketCap = float(item[6].replace(',', ''))

                #######
                try:
                    del item[7]
                    del item[7]
                except:
                    pass

                item.append(coin_id)
                item.append(source_id)
                item[0] = myDate
                item[1] = open
                item[2] = high
                item[3] = low
                item[4] = close
                item[5] = volume
                item[6] = marketCap

                # print(item)
                cleanData.append(item)

            print(cleanData)
            # exit()
            myModelObj = MyModel()
            myModelObj.insert_coin_price_daily(data=cleanData)
            #
            myModelObj1 = MyModel()
            myModelObj1.updateCoinDetails(data = updateData)




    def get_minute_data(self):
        mymodelObj = MyModel()
        coin_data = mymodelObj.get_coin_details()
        #print(coin_data)
        url = "https://api.coinmarketcap.com/v1/ticker/?limit=0"
        coinmarketcapObj = CoinmarketcapModel(url=url)
        jsonData = coinmarketcapObj.get_minute_data()
        # print(jsonData)
        # exit()
        data = []
        for i in jsonData:
            #print(i['id'])
            coin_name = i['id']
            rank = int(i['rank'])

            if i['price_usd'] == None:
                close_usd = 0
            else:
                close_usd = float(i['price_usd'])

            if i['price_btc'] == None:
                close_btc = 0
            else:
                close_btc = float(i['price_btc'])

            if i['24h_volume_usd'] == None:
                volume_usd = 0
            else:
                volume_usd = float(i['24h_volume_usd'])

            if i['market_cap_usd'] == None:
                market_cap_usd = 0
            else:
                market_cap_usd = float(i['market_cap_usd'])

            if i['available_supply'] == None:
                available_supply = 0
            else:
                available_supply = float(i['available_supply'])


            if i['total_supply'] == None:
                total_supply = 0
            else:
                total_supply = float(i['total_supply'])

            if i['max_supply'] == None:
                max_supply = 0
            else:
                max_supply = float(i['max_supply'])

            if i['last_updated'] == None:
                lastUpdatedTime = 0
                # print("i m in if ")
            else:
                last_updated = int(i['last_updated'])
                # print("i m in else ")
                print(last_updated)
                # exit()
                last_updated_utc = datetime.utcfromtimestamp(last_updated).strftime('%Y-%m-%d %H:%M:%S')
                # last_updated_utc = datetime.utcfromtimestamp(last_updated)
                print(type(last_updated_utc))
                # exit()
                lastUpdatedTime = datetime.strptime(last_updated_utc, "%Y-%m-%d %H:%M:%S")
                # lastUpdatedTime = datetime.strptime(last_updated_utc, "%Y-%m-%d")
                print(lastUpdatedTime)
                print(type(lastUpdatedTime))
                # exit()
                # print(type(last_updated_utc))
                # exit()
                # print(type(last_updated_utc))
                #
                # tempData = []
                # tempData.append(last_updated_utc)
                # data.append(tempData)
                # print(data)
            # exit()

            for item in coin_data:
                # print(item[3])
                if item[3] == coin_name:
                    #print(j[0])
                    tempData = []
                    tempData.append(item[0])
                    # tempData.append(rank)
                    # tempData.append(close_usd)
                    # tempData.append(close_btc)
                    # tempData.append(volume_usd)
                    # tempData.append(market_cap_usd)
                    tempData.append(available_supply)
                    tempData.append(total_supply)
                    tempData.append(max_supply)
                    tempData.append(lastUpdatedTime)
                    print(tempData)
                    # exit()
                    data.append(tempData)

        # print(data)
        # exit()
        mymodelObj2 = MyModel()
        mymodelObj2.insert_coin_price_minute(data=data)

    def get_daily_data_records(self,no_records):
        myModelObj = MyModel()
        coin_data = myModelObj.get_coin_details()
        # print(coin_data)
        source_id = 1
        print(no_records)
        # print(coin_data[0][1])
        for coin_name in coin_data:
            # print(coin_name[1])
            URL = "https://coinmarketcap.com/currencies/" + coin_name[1] + "/historical-data/"
            #URL = "https://coinmarketcap.com/currencies/mithril/historical-data/"
            #URL = "https://coinmarketcap.com/currencies/fsfdsf/historical-data/"
            coinmarketcapObj = CoinmarketcapModel(URL)
            rawData = coinmarketcapObj.get_data()
            # print(rawData)
            records = []
            if rawData:
                # print(rawData[0])
                j = no_records
                if len(rawData) <= j :
                    i = 0
                    while i < len(rawData) :
                        records.append(rawData[i])
                        i = i+1
                else:
                    i = 0
                    while i < j :
                        records.append(rawData[i])
                        i = i+1
            else:
                records = []

            print(records)
            #exit()
            cleanData = []
            ### cleaing data
            for item in records:
                # print(item)
                # print(item[0])
                idate = item[0]
                myDate = datetime.strptime(idate, '%b %d, %Y').date()
                # print(date.date())

                # print(date)
                # open = float(item[1])
                if item[1] == "-":
                    open = 0
                else:
                    open = float(item[1].replace(',', ''))
                # high = float(item[2])
                if item[2] == "-":
                    high = 0
                else:
                    high = float(item[2].replace(',', ''))
                # low = float(item[3])
                if item[3] == "-":
                    low = 0
                else:
                    low = float(item[3].replace(',', ''))
                # close = float(item[4])
                if item[4] == "-":
                    close = 0
                else:
                    close = float(item[4].replace(',', ''))
                if item[5] == "-":
                    volume = 0
                else:
                    volume = float(item[5].replace(',', ''))
                if item[6] == "-":
                    marketCap = 0
                else:
                    marketCap = float(item[6].replace(',', ''))
                coin_id = coin_name[0]
                #######
                item.append(coin_id)
                item.append(source_id)
                item[0] = myDate
                item[1] = open
                item[2] = high
                item[3] = low
                item[4] = close
                item[5] = volume
                item[6] = marketCap

                # print(item)
                cleanData.append(item)

            print(cleanData)
            #exit()
            myModelObj = MyModel()
            myModelObj.insert_coin_price_daily(data=cleanData)

    def updateCoinDetails(self):
        myModelObj = MyModel()
        coin_data = myModelObj.get_coin_details()
        # print(coin_data)
        # coin_data = ["bitcoin","ethrium"]
        # source_id = 1
        # print(coin_data[0][1])
        for coin_name in coin_data:
            # print(coin_name[1])
            URL = "https://coinmarketcap.com/currencies/" + coin_name[1] + "/historical-data/"
            # URL = "https://coinmarketcap.com/currencies/bitcoin/historical-data/"
            # URL = "https://coinmarketcap.com/currencies/quantum-resistant-ledger/historical-data/"
            coinmarketcapObj = CoinmarketcapModel(URL)
            rawData = coinmarketcapObj.get_coin_details_for_update()
            # print("raw data = ", rawData)
            updateData = []
            if rawData:
                try:
                    name = rawData[0]
                # print(name)
                    name = name.replace('Historical data for ', '')
                # print(name)
                except:
                    name = ""
                try:

                    url = rawData[1]
                    # print(url)
                    url = re.sub(r'http[s]?://', '', url)
                    url = re.sub(r'www[a-z0-9]?\.', '', url)
                    url = re.sub(r'/.*', '', url)
                    # print(url)
                except: url = ""
                if name:
                    norm_name = name
                    # print(norm_name)
                    norm_name = re.sub(r'[\.\-_]*', '', norm_name)
                    norm_name = re.sub(r'\s*', '', norm_name)
                    norm_name = re.sub(r'\(.*\)', '', norm_name)
                    norm_name = norm_name.lower().strip()
                else:
                    norm_name = ""
                # print(norm_name)

                updateData.append(name)
                updateData.append(norm_name)
                updateData.append(url)
                updateData.append(coin_name[1])
                print(updateData)

            myModelObj = MyModel()
            myModelObj.updateCoinDetails(data=updateData)


                    ################################## Model Api calls to Coin Market Capital###################################
    # if __name__=='__main__':
    #     app.secret_key='secret123'
        # coinmarketcapController.run(debug=True)
