import schedule #pip install schedule
import time

import sys
sys.path.append('/cryto_trading/CryptoMasterMindsApi/controller')
from controller.CoinmarketcapController import CoinmarketcapController




def getHistoryData(url):
    print(url)
    if url == 'coinmarketcap.com':
        conObj = CoinmarketcapController()
        conObj.get_history_data()
    else:
        print('not matched url')

def getDailyData(url):
    print(url)
    if url == 'coinmarketcap.com':
        conObj = CoinmarketcapController()
        conObj.get_daily_data()

#getDailyData('coinmarketcap.com')
getHistoryData('coinmarketcap.com')
