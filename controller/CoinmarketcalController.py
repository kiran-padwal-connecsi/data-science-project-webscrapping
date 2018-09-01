import urllib.request, json
from pandas.io.json import json_normalize
import pandas as pd
from datetime import datetime
import numpy as np
#import matplotlib.pyplot as plt
import re
from model.MyModel import MyModel

class CoinmarketcalController:

    def __init__(self):
        self.client_id = '614_33285ony1la8000k80wko00c8kw0c4c4sckoc0o4ck8w8owcow'
        self.client_secret = '2vf9dmzc4x4wokcw0wssgs0ccsws8w0w4wg8swcc008co8o0k0'
        self.accesstoken = self.generate_accesstoken(client_id=self.client_id,client_secret=self.client_secret)
        self.categories_url = 'https://api.coinmarketcal.com/v1/categories?access_token=' + self.accesstoken
        self.coins_url = 'https://api.coinmarketcal.com/v1/coins?access_token=' + self.accesstoken
        self.events_url = 'https://api.coinmarketcal.com/v1/events?access_token=' + self.accesstoken+'&max=150'
        self.events_history_url = 'https://api.coinmarketcal.com/v1/events?access_token=' + self.accesstoken + '&max=150&dateRangeStart=01/01/2010'


    def generate_accesstoken(self,client_id,client_secret):
        # 1---------- generate access token
        url_accesstoken = 'https://api.coinmarketcal.com/oauth/v2/token?grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret
        with urllib.request.urlopen(url_accesstoken) as url:
            access_token = json.loads(url.read().decode())['access_token']
            print(access_token)
        return access_token

    def get_all_categories_json(self):
        categories_json = self.get_Json_data(url=self.categories_url)
        # print(categories_json)
        return categories_json

    def get_all_coins_json(self):
        coins_json = self.get_Json_data(url=self.coins_url)
        return coins_json

    def get_all_events_json(self,page):
        final_url = self.events_url+page
        events_json = self.get_Json_data(url=final_url)
        return events_json

    def get_all_events_history(self,page):
        final_url = self.events_history_url + page
        events_json = self.get_Json_data(url=final_url)
        return events_json

    def get_events_by_coin_name(self,coin_name):
        url = self.events_url+"&coins="+coin_name
        events_json = self.get_Json_data(url=url)
        return events_json

    def update_categories(self):
        json_data = self.get_all_categories_json()
        # exit()
        data = []
        for i in json_data:
            cat_id = int(i['id'])
            cat_name = i['name']
            tuple_data = (cat_id, cat_name)
            data.append(tuple_data)
        print(data)
        # exit()
        myModelObj = MyModel()
        myModelObj.insertUpdate_coinmarketcal_categories(data=data)

    def update_coins(self):
        json_data = self.get_all_coins_json()
        # exit()
        myModelObj1 = MyModel()
        coin_details = myModelObj1.get_coin_details()
        data = []
        # del json_data[0]
        for i in json_data:
            ID = i['id']
            name = i['name']
            symbol = i['symbol']
            coin_id = 0
            for item in coin_details:
                # print(item[3])
                if item[3] == ID:
                    # print("i m in if")
                    coin_id = item[0]

            tuple_data = (coin_id, ID, name, symbol)
            data.append(tuple_data)
        print(data)
        # exit()
        myModelObj = MyModel()
        myModelObj.insertUpdate_coinmarketcal_coins(data=data)


    def update_events(self):
        # json_data = self.get_events_by_coin_name(coin_name='bitcoin')
        pages_remaining = True
        counter=1
        json_data=[]
        # for i in range(counter,10):
        while pages_remaining:
            page = '&page='+str(counter)
            # print(page)
            try:
                # json_data_temp = self.get_all_events_json(page=page)
                json_data_temp = self.get_all_events_history(page=page)
                json_data.extend(json_data_temp)
                # print(json_data)
                print(len(json_data))
            except:pages_remaining=False

            counter=counter+1
        # print(json_data)
        # exit()
        data = []
        for i in json_data:
            event_id = i['id']
            title = i['title']
            coins = i['coins']
            date_event = i['date_event']
            created_date = i['created_date']
            description = i['description']
            proof = i['proof']
            source = i['source']
            is_hot = i['is_hot']
            vote_count = i['vote_count']
            positive_vote_count = i['positive_vote_count']
            percentage = i['percentage']
            categories = i['categories']
            tip_symbol = i['tip_symbol']
            tip_adress = i['tip_adress']
            can_occur_before = i['can_occur_before']
            ##############################################
            event_coin_ids = []
            for coin in coins:
                myModelObj = MyModel()
                coin_id = myModelObj.get_coin_id_by_coin_name(coin_name=coin['id'])
                tuple_event_coin_ids=(event_id,coin_id,coin['id'])
                event_coin_ids.append(tuple_event_coin_ids)
            myModelObj2 = MyModel()
            myModelObj2.insertUpdate_event_coin_ids(data=event_coin_ids)
            # exit()
            event_cat_ids = []
            for category in categories:
                cat_id = category['id']
                tuple_event_cat_ids = (event_id,cat_id)
                event_cat_ids.append(tuple_event_cat_ids)
            myModelObj3 = MyModel()
            myModelObj3.insertUpdate_event_cat_ids(data = event_cat_ids)


            ##############################################

            tuple_data = (event_id, title, date_event, created_date,description,proof,source,is_hot,vote_count,positive_vote_count,percentage,tip_symbol,tip_adress,can_occur_before)
            data.append(tuple_data)

        print("my data = ",len(data))
        # exit()
        myModelObj = MyModel()
        myModelObj.insertUpdate_coinmarketcal_events(data=data)



    def get_Json_data(self,url):
        with urllib.request.urlopen(url) as url:
            json_data = json.loads(url.read().decode())
        return json_data

    def del_all_events(self):
        myModelObj = MyModel()
        myModelObj.del_all_events()