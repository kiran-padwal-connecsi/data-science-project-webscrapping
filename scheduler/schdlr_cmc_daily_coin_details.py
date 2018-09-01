import schedule #pip install schedule
import time


import sys
sys.path.append('/cryto_trading/CryptoMasterMindsApi/controller')
from controller.CoinmarketcapController import CoinmarketcapController

def getCoinDetails(url):
    print(url)
    if(url == "coinmarketcap.com"):
        conObj = CoinmarketcapController()
        conObj.get_coin_details()
    else:
        print("not matched url")

getCoinDetails('coinmarketcap.com')
