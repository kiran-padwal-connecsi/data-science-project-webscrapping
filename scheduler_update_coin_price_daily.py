import schedule #pip install schedule
import time

from controller.CoinmarketcapController import CoinmarketcapController




def getHistoryDataByCoin(url):
    print(url)
    if url == 'coinmarketcap.com':
        conObj = CoinmarketcapController()
        conObj.get_history_data_by_coin()
    else:
        print('not matched url')

def getDailyData(url):
    print(url)
    if url == 'coinmarketcap.com':
        conObj = CoinmarketcapController()
        conObj.get_daily_data()


getDailyData(url='coinmarketcap.com')
# def periodic_task():
#     my_controller = MyController()
#     my_controller.monitor()

############change parameter for required periodic tasks###################
#default is 1 minute it can be changed as per requirement
#schedule.every(1).minutes.do(getCoinDetails,'coinmarketcap.com')
#schedule.every().day.at("10:30").do(getCoinDetails,'coinmarketcap.com')
# schedule.every().day.at("15:00").do(getDailyData,'coinmarketcap.com')
#schedule.every(5).minutes.do(getMinuteData,'coinmarketcap.com')
#schedule.every(1).minutes.do(getDailyData,'coinmarketcap.com')

#schedule.every().hour.do(periodic_task)
#schedule.every().day.at("10:30").do(getCoinDetails,'coinmarketcap.com')
#schedule.every(5).to(10).minutes.do(periodic_task)
#schedule.every().monday.do(periodic_task)
#schedule.every().wednesday.at("13:15").do(periodic_task)
#schedule.cancel_job(periodic_task())
###########################################################################
# while True:
#
#     schedule.run_pending()
#     time.sleep(1)


