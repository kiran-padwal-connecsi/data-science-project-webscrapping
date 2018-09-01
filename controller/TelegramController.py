import re

from datetime import date, datetime, timedelta
from telethon import TelegramClient
from telethon import utils
from telethon.tl.functions.messages import SearchRequest
from model.MyModel import MyModel
import math

class TelegramController:

    def __init__(self):
        api_id ="276187"
        api_hash = "817b6ae988baadd02b7f415c5d6ac682"
        self.client = TelegramClient('kiran', api_id, api_hash)
        self.client.start(phone='+48729675768')
        # self.zone_type=''

    def getMyself(self):
        print(self.client.get_me().stringify())

    def sendMessage(self,username):
        self.client.send_message(username, 'lets eat  PASTA!!! hiep pham')

    def getMessageFromChat(self,username):
        # Retrieving messages from a chat
        #from telethon import utils
        messages = self.client.get_messages(username,limit = 10000)
        # messages = self.client.get_message_history(username,limit = 1000)
        data = []
        print(len(messages))
        counter = 0
        for message in messages:
            message_id = self.client._get_message_id(message)
            # print(message.message).stringify())
            # print("_____________________")
            # print(message.date, message.message)
            myString = re.sub('[^\.\-A-Za-z0-9]+', ' ', str(message.message))
            myString = myString.replace('If','')
            myString = myString.replace('SIGNAL', '')
            signal_date = message.date
            # print(signal_date)
            # print(type(signal_date))
            # tempData = []
            # tempData.append(signal_date)
            # data.append(tempData)
            # print(data)
            # exit()
            todays_date = date.today()
            yesterday = datetime.now() - timedelta(days=1)
            # print("signal date =",signal_date.date())
            # print("yesterday date = ",yesterday.date())
            qTypes = ["Short Term", "SHORT TERM", "Mid Term","MID TERM","Long Term","LONG TERM"]
            target1_words = ["Target 1", "T 1"]
            target2_words = ["Target 2", "T 2"]
            target3_words = ["Target 3", "T 3"]
            target4_words = ["Target 4", "T 4"]
            stop_loss_words = ["Stop loss","Stop-loss","SL","Stop-Loss","Stop Loss","STOP LOSS"]
            zone_type_words = ["Buy Zone", "Sell Zone"]
            signals = []
            for item in qTypes:
                if item in myString:
                    # if yesterday.date() == signal_date.date():
                        print("_____________________")
                        counter=counter+1
                        print(counter)
                        print("yesterday's date = ", yesterday.date())
                        print("signal date = ", signal_date.date())
                        q_type = item
                        print("q_type = ", q_type)
                        symbol = self.getSymbol(myString=myString,search_string=item)
                        print("Symbol  = ",symbol)

                        zone_type=''
                        zone = ''
                        for item in zone_type_words:
                            if item in myString:
                                if item == "Buy Zone":
                                    print("zone type = ", item)
                                    zone_type = "BUY"
                                    zone = self.getZone(myString=myString,search_string=item)
                                if item == "Sell Zone":
                                    zone_type = "Sell"


                        target1 = ''
                        for item in target1_words:
                            if item in myString:
                                target1 = self.getTarget(myString=myString,search_string=item)
                                if target1.__contains__("k"):
                                    # print("yes")
                                    target1=target1.replace("k","")
                                    target1 = float(target1)
                                    target1 = target1 * 1000
                                    target1 = str(target1)
                                if target1.__contains__("K"):
                                    # print("yes")
                                    target1=target1.replace("K","")
                                    target1 = float(target1)
                                    target1 = target1 * 1000
                                    target1 = str(target1)
                                if target1.__contains__("sats"):
                                    target1=target1.replace("sats","")
                                print("target1 = ", target1)

                        target2 = ''
                        for item in target2_words:
                            if item in myString:
                                target2 = self.getTarget(myString=myString, search_string=item)
                                if target2.__contains__("k"):
                                    # print("yes")
                                    target2 = target2.replace("k", "")
                                    target2 = float(target2)
                                    target2 = target2 * 1000
                                    target2 = str(target2)
                                if target2.__contains__("K"):
                                    # print("yes")
                                    target2 = target2.replace("K", "")
                                    target2 = float(target2)
                                    target2 = target2 * 1000
                                    target2 = str(target2)
                                if target2.__contains__("sats"):
                                    target2=target2.replace("sats","")
                                print("target2 = ", target2)

                        target3 = ''
                        for item in target3_words:
                            if item in myString:
                                target3 = self.getTarget(myString=myString, search_string=item)
                                if target3.__contains__("k"):
                                    # print("yes")
                                    target3 = target3.replace("k", "")
                                    target3 = float(target3)
                                    target3 = target3 * 1000
                                    target3 = str(target3)
                                if target3.__contains__("K"):
                                    # print("yes")
                                    target3 = target3.replace("K", "")
                                    target3 = float(target3)
                                    target3 = target3 * 1000
                                    # print(type(stop_loss))
                                    target3 = str(target3)
                                if target3.__contains__("sats"):
                                    target3=target3.replace("sats","")
                                print("target3 = ", target3)

                        target4 = ''
                        for item in target4_words:
                            if item in myString:
                                target4 = self.getTarget(myString=myString, search_string=item)
                                if target4.__contains__("k"):
                                    # print("yes")
                                    target4 = target4.replace("k", "")
                                    target4 = float(target4)
                                    target4 = target4 * 1000
                                    # print(type(stop_loss))
                                    target4 = str(target4)
                                if target4.__contains__("K"):
                                    # print("yes")
                                    target4 = target4.replace("K", "")
                                    target4 = float(target4)
                                    target4 = target4 * 1000
                                    # print(type(stop_loss))
                                    target4 = str(target4)
                                if target4.__contains__("sats"):
                                    target4=target4.replace("sats","")
                                print("target4 = ", target4)

                        stop_loss = ''
                        for item in stop_loss_words:
                            if item in myString:
                                stop_loss = self.getStopLoss(myString=myString,search_string=item)
                                if stop_loss.__contains__("k"):
                                    # print("yes")
                                    stop_loss = stop_loss.replace("k",'')
                                    # print(type(stop_loss))
                                    stop_loss = float(stop_loss)
                                    stop_loss = stop_loss*1000
                                    # print(type(stop_loss))
                                    stop_loss = str(stop_loss)
                                    # print(type(stop_loss))

                                if stop_loss.__contains__("K"):
                                    # print("yes")
                                    stop_loss = stop_loss.replace("K", '')
                                    stop_loss = float(stop_loss)
                                    stop_loss = stop_loss * 1000
                                    # print(type(stop_loss))
                                    stop_loss = str(stop_loss)
                                if stop_loss.__contains__("sats"):
                                    stop_loss=stop_loss.replace("sats","")
                                print("stop loss = ", stop_loss)





                        currency = self.getCurrency()

                        myModelObj = MyModel()
                        coin_id = myModelObj.get_coin_id_by_symbol(symbol=symbol)
                        # coin_id = 1
                        # print("coin_id = ",coin_id[0])

                        print(myString)

                        if coin_id:
                            signals.append(coin_id)# coin id
                        else:signals.append(0)
                        source_id = 2
                        signals.append(source_id)#source id
                        if symbol:
                            signals.append(symbol)#symbol
                        else:signals.append("")

                        if target1:
                            if target1 == "MOON" or target1 =="moon":
                                signals.append(99999)
                            else:
                                sats = float(target1)
                                target1BTC = self.convertSatsToBTC(satoshi=sats)
                                signals.append(target1BTC)# target 1
                        else:signals.append(target1)

                        if target2:
                            if target2 == "MOON" or target2 =="moon":
                                signals.append(99999)
                            else:
                                sats = float(target2)
                                target2BTC = self.convertSatsToBTC(satoshi=sats)
                                signals.append(target2BTC)# target 2
                        else:signals.append(target2)

                        if target3:
                            if target3 == "MOON" or target3 =="moon":
                                signals.append(99999)
                            else:
                                sats = float(target3)
                                target3BTC = self.convertSatsToBTC(satoshi=sats)
                                signals.append(target3BTC)#target 3
                        else:signals.append(target3)

                        if stop_loss:
                            if stop_loss == "MOON" or stop_loss =="moon":
                                signals.append(99999)
                            else:
                                sats = float(stop_loss)
                                stop_lossBTC = self.convertSatsToBTC(satoshi=sats)
                                signals.append(stop_lossBTC)# stop loss
                        else:signals.append(stop_loss)

                        signals.append(signal_date)# signal date
                        signals.append(message_id)# signal id
                        if target4:
                            if target4 == "MOON" or target4 =="moon":
                                signals.append(99999)
                            else:
                                sats = float(target4)
                                target4BTC = self.convertSatsToBTC(satoshi=sats)
                                signals.append(target4BTC) # target 4
                        else:signals.append(target4)

                        signals.append(currency)# currency

                        signals.append(q_type)# q_type
                        if zone_type:
                            # print("im in if")
                            signals.append(zone_type)#zone type
                        else:
                            # print("i m in else")
                            signals.append('')
                        if zone:
                            signals.append(zone)
                        else:signals.append(zone)

                        data.append(signals)
                        break
        print(data)
        myModelObj = MyModel()
        myModelObj.insert_telegram_Signal_details(data=data)



            # print(utils.get_display_name(message.sender), message.message)
        # print(message)
    def convertSatsToBTC(self,satoshi):
        if int(satoshi) != 0:
            BTC = satoshi/10000000
            return BTC
        else:
            return satoshi
    def getCurrency(self):
        currency = "BTC"
        return currency
    def getSymbol(self,myString,search_string):
        p = re.compile(r''+ search_string + '\s*(\w*)', re.IGNORECASE)
        # print(p)
        match = p.search(myString)
        if match:
            next_string = match.group(1)
            # print(next_string)
            symbol=''
            if next_string:
                symbol = next_string.split(None, 1)[0]
                return symbol
            else: return symbol




    def getTarget(self,myString,search_string):
        p = re.compile(r''+ search_string + '\s*(\w*\.*\w*)', re.IGNORECASE)
        # print(p)
        match = p.search(myString)
        if match:
            next_string = match.group(1)
            # print("next  string =",next_string)
            target =''
            if next_string:
                target = next_string.split(None, 1)[0]
                return target
            else: return target

    def getStopLoss(self, myString, search_string):
        p = re.compile(r'' + search_string + '\s*(\w*\.*\w*)', re.IGNORECASE)
        # print(p)
        match = p.search(myString)
        if match:
            next_string = match.group(1)
            print("next  string =", next_string)
            stop_loss = ''
            if next_string:
                stop_loss = next_string.split(None, 1)[0]
                return stop_loss
            else:
                return stop_loss

    def getZone(self, myString, search_string):
        p = re.compile(r'' + search_string + '\s*(\w*)', re.IGNORECASE)
        # print(p)
        match = p.search(myString)
        if match:
            next_string = match.group(1)
            print("next  string =", next_string)
            zone = ''
            if next_string:
                zone = next_string.split(None, 1)[0]
                return zone
            else:
                return zone



# myTelegramController = TelegramController()
#myTelegramController.getMyself()
# myTelegramController.sendMessage(username='xtapy')
# myTelegramController.getMessageFromChat(username='PALMBEACHSIGNALS')