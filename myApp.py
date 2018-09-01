from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
import sqlite3

from controller import CoinmarketcapController

myApp=Flask(__name__)

#app.config['sqlite3_CURSORCLASS']='DictCursor'
#database_path = app.root_path+"\..\database\cinema_booking.db"


@myApp.route('/')
def index():

    return render_template('home.html')





############################################## coin market Api's#####################################################################################
@myApp.route('/getCoinDetails/<string:url>', methods =['GET','POST'])
def getCoinDetails(url):
    print(url)
    if(url == "coinmarketcap.com"):
        CoinmarketcapController.get_coin_details()
        return render_template('home.html')
    else:
        print("not matched url")
        return render_template('home.html')


@myApp.route('/getCoinDetailsFromCrypto')
def getCoinDetailsFromCrypto():
    CoinmarketcapController.get_coin_details_from_crypto()
    return render_template('home.html')

@myApp.route('/updateCoinSourceTable')
def updateCoinSourceTable():
    CoinmarketcapController.updateCoinSourceTable()
    return render_template('home.html')

@myApp.route('/getHistoryData/<string:url>', methods =['GET','POST'])# to get history data for all coins
def getHistoryData(url):
    print(url)
    if url == 'coinmarketcap.com':
        CoinmarketcapController.get_history_data()
        return render_template('home.html')
    else:
        print('not matched url')
        return render_template('home.html')

@myApp.route('/getMinuteData/<string:url>', methods =['GET','POST'])# to get history data for all coins
def getMinuteData(url):
    print(url)
    if url == 'coinmarketcap.com':
        CoinmarketcapController.get_minute_data()
        return render_template('home.html')
    else:
        print('not matched url')
        return render_template('home.html')


if __name__=='__main__':
    #app.secret_key='secret123'
    myApp.run(debug=True)
