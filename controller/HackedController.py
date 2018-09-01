import re

from datetime import date, datetime, timedelta, time
import oauth2client
#import PyOpenSSL
import gspread as gspread
import os

import timestring

from model.MyModel import MyModel
import math
from oauth2client.service_account import ServiceAccountCredentials

class HackedController:

    def __init__(self,url):
        self.url = url
        self.key = '14H_zNKCjJeN_OQD1OXM0ig12Gtum11MPx5oj5O7cOqY'

    def getDataFromSpreadSheet(self):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        dirname = os.path.dirname(__file__)
        # print(dirname)
        # jsonFile_path = os.path.abspath("hacked-com-341cc7ab5979.json")
        # print(jsonFile_path)
        # exit()
        credentials = ServiceAccountCredentials.from_json_keyfile_name(dirname+'/hacked-com-341cc7ab5979.json', scope)
        # exit()
        print(credentials)
        # exit()
        gc = gspread.authorize(credentials)
        wks = gc.open("Hacked.com").sheet1
        # sht1 = gc.open_by_key(self.key)
        # sht1 = gc.open_by_url(url='https://docs.google.com/spreadsheets/d/14H_zNKCjJeN_OQD1OXM0ig12Gtum11MPx5oj5O7cOqY/edit#gid=0')
        rows = wks.get_all_values()
        # print(rows[1:])
        data = rows[1:]
        # print(data)
        myModelObj = MyModel()
        for item in data:
            print(item)
            symbol = item[2]
            print(symbol)
            coin_id = myModelObj.get_coin_id_by_symbol(symbol=symbol)
            item[0]= coin_id
            item[1]= 3
            # signal_date = item[7]
            # print(item[7])
            mydate = item[7].replace("."," ")
            # print(mydate)
            item[7] = datetime.strptime(mydate, "%d %m %Y")
            # print(item[7])
            # exit()

        myModelObj = MyModel()
        myModelObj.insert_hackedCom_Signal_details(data=data)





# myCon = HackedController(url='hacked.com')
# myCon.getDataFromSpreadSheet()