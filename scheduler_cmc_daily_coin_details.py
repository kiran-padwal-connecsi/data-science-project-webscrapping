import schedule #pip install schedule
import time

from controller.CoinmarketcapController import CoinmarketcapController


def getCoinDetails(url):
    print(url)
    if(url == "coinmarketcap.com"):
        conObj = CoinmarketcapController()
        conObj.get_coin_details()

    else:
        print("not matched url")
getCoinDetails('coinmarketcap.com')

#getDailyData_records(url='coinmarketcap.com')
############change parameter for required periodic tasks###################
#default is 1 minute it can be changed as per requirement
#schedule.every(1).minutes.do(getCoinDetails,'coinmarketcap.com')
#schedule.every().day.at("02:00").do(getCoinDetails,'coinmarketcap.com')
#schedule.every().day.at("11:00").do(getDailyData,'coinmarketcap.com')
#schedule.every(5).minutes.do(getCoinDetails,'coinmarketcap.com')
#schedule.every(1).minutes.do(getDailyData,'coinmarketcap.com')

#schedule.every().hour.do(getCoinDetails,'coinmarketcap.com')

#schedule.every().day.at("10:30").do(getCoinDetails,'coinmarketcap.com')
#schedule.every(5).to(10).minutes.do(periodic_task)
#schedule.every().monday.do(periodic_task)
#schedule.every().wednesday.at("13:15").do(periodic_task)
#schedule.cancel_job(periodic_task())

###########################################################################
# while True:

#     schedule.run_pending()
#     time.sleep(1)


