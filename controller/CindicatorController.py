import re
import email
import os
from bs4 import BeautifulSoup


from model.MyModel import MyModel


from datetime import datetime, timedelta
import imaplib
import timestring

class CindicatorController :

    def readEmail(self):

        myEmail = 'kiran.padwal.cmm@gmail.com'
        mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        username = 'kiran.padwal.cmm@gmail.com'
        password = 'cryptomasterminds'
        mail.login(username, password)
        # print(mail.list())
        # exit()

        mail.select('inbox')

        # result, data = mail.search(None, "ALL")
        result, data = mail.uid('search', None, "ALL")  # search and return uids instead
        uids = data[0]  # data is a list.
        # print(uids)
        uid_list = uids.split()  # ids is a space separated string
        print(uid_list)
        latest_email_uid = uid_list[-1]  # get the latest
        # print(latest_email_uid)

        for uid in uid_list:
            result, data = mail.uid('fetch', uid, '(RFC822)')
            raw_email = data[0][1]
            # print(raw_email)
            email_message = email.message_from_bytes(raw_email)
            # email_from = email_message['from']
            email1 = email.utils.parseaddr(email_message['From'])
            email_from = email1[1]
            # print(email_from)
            # exit()
            email_date= email_message['date']
            # print(email_date)

            # today = datetime.today().date()
            # print(today)
            yesterday = datetime.today().date()-timedelta(1)
            print(yesterday)
            # exit()
            email_date = re.sub("[+-].*$", "", email_date)
            email_date = datetime.strptime(email_date, '%a, %d %b %Y %H:%M:%S ').date()

            if email_from == myEmail and email_date == yesterday:
                print("email is correct", email_from)
                print("email date = ",email_date)
                # raw_email
                msg = email.message_from_bytes(raw_email)
                for part in msg.walk():
                    # each part is a either non-multipart, or another multipart message
                    # that contains further parts... Message is organized like a tree
                    if part.get_content_type() == 'text/plain':
                        # print("i m in if")
                        myString=part.get_payload(None,True)# prints the raw text
                        # print(string)
                        # string = string.splitlines()
                        # print(string)


                myString = str(myString)

                print(type(myString))
                # myString = myString.replace('\n', ' ').replace('\r', '')
                # myString = myString.replace('\r\n',"")
                print("my string = ",myString)
                # exit()
                question = myString.split("Question")
                print(type(question))
                # for item in question:
                #     print(item)
                # exit()
                print(len(question))
                # print(type(question))

                # print(question[0])
                # exit()
                question.remove(question[0])
                print(len(question))
                print(question)
                # exit()
                mydata = []
                for item in question:
                    print("item = ",item)
                    # exit()

                    stripedString = item.replace('\\n', ' ').replace('\\r','')
                    # stripedString = stripedString.replace('\r', '')
                    # print("stripped string  = ",stripedString)
                    # stripedString = re.sub("[]", " ", stripedString)
                    # print(stripedString)
                    # exit()
                    q_type = self.getTypeofQuestion(myString=stripedString)
                    print("Question Type = ", q_type)
                    if q_type == "Support_Resistance":
                        settled_price = self.getSettledPrice(search_string="settled at", myString=stripedString)
                        print("settled price = ", settled_price)
                        signal_date = self.getSignalDate(search_string="UTC", myString=stripedString)
                        print("signal date = ", signal_date)
                        currency = self.getCurrency(myString=stripedString, search_string="/")
                        print("currency = ", currency)
                        symbol = self.getSymbol(myString=stripedString, search_string="/")
                        print("symbol =", symbol)
                        start_date = self.getStartEndDate(myString=stripedString, search_string="from",
                                                          seprator="until")
                        print("start date = ", start_date)
                        end_date = self.getStartEndDate(myString=stripedString, search_string="until", seprator="?")
                        print("end date = ", end_date)
                        r_level = self.getResistanceLevel(myString=stripedString, search_string="Resistance level:")
                        print("resistance level = ", r_level)
                        s_level = self.getSupportLevel(myString=stripedString, search_string="Support level:")
                        print("support level = ", s_level)
                        srList = []
                        srList.append(q_type)
                        srList.append(signal_date)
                        srList.append(start_date)
                        srList.append(end_date)
                        srList.append(symbol)
                        srList.append(currency)
                        srList.append(settled_price)
                        srList.append(s_level)
                        srList.append(r_level)
                        srList.append(" ")  # target = null
                        srList.append(" ")  # probability = null
                        srList.append(" ")  # notes = null
                        srList.append(uid)
                        srList.append(email_from)
                        srList.append(email_date)
                        mydata.append(srList)

                    if q_type == "Market Share":
                        final_q_type = ""
                        upper = ""
                        lower = ""
                        if "above" in stripedString:
                            final_q_type = "Above Market Share"
                            target = self.getTarget(myString=stripedString, search_string="above")
                            upper = target
                            print("Target =", target)
                        else:
                            final_q_type = "Below Market Share"
                            target = self.getTarget(myString=stripedString, search_string="below")
                            lower = target
                            print("Target =", target)
                        print("Final Question Type = ", final_q_type)

                        signal_date = self.getSignalDate(search_string="UTC", myString=stripedString)
                        print("signal date = ", signal_date)
                        words_for_end_date = ["before", "by"]
                        for item in words_for_end_date:
                            if item in stripedString:
                                end_date = self.getEndDateMarketShare(myString=stripedString, search_string=item,
                                                                      seprator="?")

                        print("End date = ", end_date)
                        words_for_settled_price = ["settled at", "reached"]
                        for item in words_for_settled_price:
                            if item in stripedString:
                                settled_price = self.getSettledPrice(search_string=item, myString=stripedString)

                        print("settled price = ", settled_price)
                        symbol = "BTC"
                        print("Symbol = ", symbol)
                        indicator = self.getIndicator(myString=stripedString, search_string="Indicator:")
                        print("Indicator = ", indicator)

                        mkshareList = []
                        mkshareList.append(final_q_type)
                        mkshareList.append(signal_date)  # signal date
                        mkshareList.append(" ")  # start date
                        mkshareList.append(end_date)  # end date
                        mkshareList.append(symbol)  # symbol
                        mkshareList.append(" ")  # currency
                        mkshareList.append(settled_price)  # settled price
                        mkshareList.append(lower)  # lower
                        mkshareList.append(upper)  # upper
                        mkshareList.append(" ")  # target
                        mkshareList.append(indicator)  # probability
                        mkshareList.append(" ")  # notes
                        mkshareList.append(uid)
                        mkshareList.append(email_from)
                        mkshareList.append(email_date)
                        mydata.append(mkshareList)

                    if q_type == "above ATH":
                        settled_price = self.getSettledPrice(myString=stripedString, search_string="settled at")
                        print("settled price = ", settled_price)
                        signal_date = self.getSignalDate(myString=stripedString, search_string="UTC")
                        print("signal date =", signal_date)
                        end_date = self.getEndDateMarketShare(myString=stripedString, search_string="before",
                                                              seprator="?")
                        print(end_date)
                        currency = self.getCurrency(myString=stripedString, search_string="/")
                        print("currency = ", currency)
                        symbol = self.getSymbol(myString=stripedString, search_string="/")
                        print("symbol =", symbol)
                        target = self.getTarget(myString=stripedString, search_string="all-time high of")
                        print("Target =", target)
                        indicator = self.getIndicator(myString=stripedString, search_string="Indicator:")
                        print("Indicator = ", indicator)

                        athList = []
                        athList.append(q_type)
                        athList.append(signal_date)  # signal date
                        athList.append(signal_date)  # start date
                        athList.append(end_date)  # end date
                        athList.append(symbol)  # symbol
                        athList.append(currency)  # currency
                        athList.append(settled_price)  # settled price
                        athList.append(" ")  # lower
                        athList.append(target)  # upper
                        athList.append(" ")  # target
                        athList.append(indicator)  # probability
                        athList.append(" ")  # notes
                        athList.append(uid)
                        athList.append(email_from)
                        athList.append(email_date)
                        mydata.append(athList)

                    if q_type == "Ico Rank":
                        end_date = self.getEndDateMarketShare(myString=stripedString, search_string="by", seprator="?")
                        print("End Date = ", end_date)
                        ranking = self.getIcoRanking(myString=stripedString, search_string="ICO Ranking:")
                        print("ranking = ", ranking)
                        icoList = []
                        icoList.append(q_type)
                        icoList.append(" ")  # signal date
                        icoList.append(" ")  # start date
                        icoList.append(end_date)  # end date
                        icoList.append(" ")  # symbol
                        icoList.append(" ")  # currency
                        icoList.append(" ")  # settled price
                        icoList.append(" ")  # lower
                        icoList.append(" ")  # upper
                        icoList.append(" ")  # target = null
                        icoList.append(" ")  # probability = null
                        icoList.append(ranking)  # notes
                        icoList.append(uid)
                        icoList.append(email_from)
                        icoList.append(email_date)
                        mydata.append(icoList)

                    if q_type == "Above price and before time":
                        settled_price = self.getSettledPrice(myString=stripedString, search_string="settled at")
                        print("settled price = ", settled_price)
                        signal_date = self.getSignalDate(myString=stripedString, search_string="UTC")
                        print("signal date =", signal_date)
                        currency = self.getCurrency(myString=stripedString, search_string="/")
                        print("currency = ", currency)
                        symbol = self.getSymbol(myString=stripedString, search_string="/")
                        print("symbol =", symbol)
                        indicator = self.getIndicator(myString=stripedString, search_string="Indicator:")
                        print("Indicator = ", indicator)
                        end_date = self.getEndDateMarketShare(myString=stripedString, search_string="before",
                                                              seprator="?")
                        print("end date = ", end_date)
                        target = self.getTarget(myString=stripedString, search_string="above")
                        print("Target =", target)

                        apbt = []
                        apbt.append(q_type)
                        apbt.append(signal_date)  # signal date
                        apbt.append(signal_date)  # start date
                        apbt.append(end_date)  # end date
                        apbt.append(symbol)  # symbol
                        apbt.append(currency)  # currency
                        apbt.append(settled_price)  # settled price
                        apbt.append(" ")  # lower
                        apbt.append(target)  # upper
                        apbt.append(" ")  # target
                        apbt.append(indicator)  # probability
                        apbt.append(" ")  # notes
                        apbt.append(uid)
                        apbt.append(email_from)
                        apbt.append(email_date)
                        mydata.append(apbt)

                    if q_type == "Below price and before time":
                        settled_price = self.getSettledPrice(myString=stripedString, search_string="settled at")
                        print("settled price = ", settled_price)
                        signal_date = self.getSignalDate(myString=stripedString, search_string="UTC")
                        print("signal date =", signal_date)
                        currency = self.getCurrency(myString=stripedString, search_string="/")
                        print("currency = ", currency)
                        symbol = self.getSymbol(myString=stripedString, search_string="/")
                        print("symbol =", symbol)
                        indicator = self.getIndicator(myString=stripedString, search_string="Indicator:")
                        print("Indicator = ", indicator)
                        end_date = self.getEndDateMarketShare(myString=stripedString, search_string="before",
                                                              seprator="?")
                        print("end date = ", end_date)
                        target = self.getTarget(myString=stripedString, search_string="below")
                        print("Target =", target)

                        bpbt = []
                        bpbt.append(q_type)
                        bpbt.append(signal_date)  # signal date
                        bpbt.append(signal_date)  # start date
                        bpbt.append(end_date)  # end date
                        bpbt.append(symbol)  # symbol
                        bpbt.append(currency)  # currency
                        bpbt.append(settled_price)  # settled price
                        bpbt.append(target)  # lower
                        bpbt.append(" ")  # upper
                        bpbt.append(" ")  # target
                        bpbt.append(indicator)  # probability
                        bpbt.append(" ")  # notes
                        bpbt.append(uid)
                        bpbt.append(email_from)
                        bpbt.append(email_date)
                        mydata.append(bpbt)

                    if q_type == "Above price and before price":
                        settled_price = self.getSettledPrice(myString=stripedString, search_string="settled at")
                        print("settled price = ", settled_price)
                        signal_date = self.getSignalDate(myString=stripedString, search_string="UTC")
                        print("signal date =", signal_date)
                        currency = self.getCurrency(myString=stripedString, search_string="/")
                        print("currency = ", currency)
                        symbol = self.getSymbol(myString=stripedString, search_string="/")
                        print("symbol =", symbol)
                        indicator = self.getIndicator(myString=stripedString, search_string="Indicator:")
                        print("Indicator = ", indicator)
                        # end_date = self.getEndDateMarketShare(myString=stripedString, search_string="before", seprator="?")
                        # print("end date = ",end_date)
                        upper = self.getTarget(myString=stripedString, search_string="above")
                        print("upper =", upper)
                        lower = self.getTarget(myString=stripedString, search_string="below")
                        print("lower =", lower)

                        apbp = []
                        apbp.append(q_type)
                        apbp.append(signal_date)  # signal date
                        apbp.append(signal_date)  # start date
                        apbp.append(" ")  # end date
                        apbp.append(symbol)  # symbol
                        apbp.append(currency)  # currency
                        apbp.append(settled_price)  # settled price
                        apbp.append(lower)  # lower
                        apbp.append(upper)  # upper
                        apbp.append(" ")  # target
                        apbp.append(indicator)  # probability
                        apbp.append(" ")  # notes
                        apbp.append(uid)
                        apbp.append(email_from)
                        apbp.append(email_date)
                        mydata.append(apbp)

                    if q_type == "Below price and before price":
                        settled_price = self.getSettledPrice(myString=stripedString, search_string="settled at")
                        print("settled price = ", settled_price)
                        signal_date = self.getSignalDate(myString=stripedString, search_string="UTC")
                        print("signal date =", signal_date)
                        currency = self.getCurrency(myString=stripedString, search_string="/")
                        print("currency = ", currency)
                        symbol = self.getSymbol(myString=stripedString, search_string="/")
                        print("symbol =", symbol)
                        indicator = self.getIndicator(myString=stripedString, search_string="Indicator:")
                        print("Indicator = ", indicator)
                        # end_date = self.getEndDateMarketShare(myString=stripedString, search_string="before", seprator="?")
                        # print("end date = ",end_date)
                        lower = self.getTarget(myString=stripedString, search_string="below")
                        print("lower =", lower)
                        upper = self.getTarget(myString=stripedString, search_string="above")
                        print("upper =", upper)

                        bpbp = []
                        bpbp.append(q_type)
                        bpbp.append(signal_date)  # signal date
                        bpbp.append(signal_date)  # start date
                        bpbp.append(" ")  # end date
                        bpbp.append(symbol)  # symbol
                        bpbp.append(currency)  # currency
                        bpbp.append(settled_price)  # settled price
                        bpbp.append(lower)  # lower
                        bpbp.append(upper)  # upper
                        bpbp.append(" ")  # target
                        bpbp.append(indicator)  # probability
                        bpbp.append(" ")  # notes
                        bpbp.append(uid)
                        bpbp.append(email_from)
                        bpbp.append(email_date)
                        mydata.append(bpbp)


                # print(uid)
                # mail.close()
                # mail.logout()
                # print(os.path.dirname(os.path.abspath(__file__)))
                # print("data = ",data)

                if mydata:
                    print(mydata)
                    # exit()
                    myModelObj = MyModel()
                    myModelObj.insert_cindicator_Question_details(data=mydata)

            else:
                print("Email From is not correct")

        mail.close()
        mail.logout()
                # exit()
            # else: print("not correct email from", email_from)
            # exit()


        #print(data)

    def get_first_text_block(self, email_message_instance):
        maintype = email_message_instance.get_content_maintype()
        if maintype == 'multipart':
            for part in email_message_instance.get_payload():
                if part.get_content_maintype() == 'text':
                    return part.get_payload()
        elif maintype == 'text':
            return email_message_instance.get_payload()


    def getTarget(self,myString,search_string):
        p = re.compile(r''+ search_string + '\s*\D*(\d*\.*\,*\d*)', re.IGNORECASE)
        # print(p)
        match = p.search(myString)
        if match:
            next_string = match.group(1)
            # print(next_string)
            target = ''
            if next_string:
                target = next_string.split(None, 1)[0]
                return target
            else:
                return  target


    def getIcoRanking(self,myString,search_string):
        p = re.compile(r''+ search_string + '\s*(.*)',re.DOTALL)
        # print(p)
        match = p.search(myString)
        if match:
            next_string = match.group(1)
            #print("next string =",next_string)
            ranking =','.join(re.findall('(\d+\.\s+\S*\D*)', next_string))
            # print(ranking)
            # ranking = next_string.replace('.', ',').replace('\r', '')
            # print("ranking = ",ranking)
            # strippedRanking = ranking.rstrip(", ,\n")
            # print("stripped string = ",strippedRanking)
            ranking = ranking.rstrip(" ")
            # ranking = next_string.replace("\n",",")
            # print(ranking)
            # exit()
            return ranking


    def getIndicator(self,myString,search_string):
        p = re.compile(r''+ search_string + '\s*(\S*)', re.IGNORECASE)
        # print(p)
        match = p.search(myString)
        if match:
            next_string = match.group(1)
            # print(next_string)
            indicator=''
            if next_string:
                indicator = next_string.split(None, 1)[0]
                return indicator
            else:
                return indicator


    def getResistanceLevel(self,myString,search_string):
        p = re.compile(r''+ search_string + '\s*(\S*)', re.IGNORECASE)
        # print(p)
        match = p.search(myString)
        if match:
            next_string = match.group(1)
            # print(next_string)
            r_level = ''
            if next_string:
                r_level = next_string.split(None, 1)[0]
                return r_level
            else:
                return r_level

    def getSupportLevel(self,myString,search_string):
        p = re.compile(r''+ search_string + '\s*(\S*)', re.IGNORECASE)
        # print(p)
        match = p.search(myString)
        if match:
            next_string = match.group(1)
            # print(next_string)
            s_level = ''
            if next_string:
                s_level = next_string.split(None, 1)[0]
                return s_level
            else:
                return s_level


    def getCurrency(self,myString,search_string):
        p = re.compile(r''+ search_string + '(\w*)', re.IGNORECASE)
        # print(p)
        match = p.search(myString)
        if match:
            next_string = match.group(1)
            # print(next_string)
            currency=''
            if next_string:
                currency = next_string.split(None, 1)[0]
                return currency
            else: return currency

    def getSymbol(self,myString,search_string):
        p = re.compile(r''+'(\w*)'+ search_string + '(\S*)', re.IGNORECASE)
        # print(p)
        match = p.search(myString)
        if match:
            next_string = match.group(1)
            # print(next_string)
            symbol = ''
            if next_string:
                symbol = next_string.split(None, 1)[0]
                return symbol
            else:return symbol

    def getSettledPrice(self,myString,search_string):
         p = re.compile(r''+ search_string +'\s*\D*(\d*\.*\,*\d*)', re.IGNORECASE)
         #print(p)
         match = p.search(myString)
         #print(m)
         if match:
                #print("i m inside match")
                next_string = match.group(1)
                #print(next_string)
                settledPrice=next_string.split(None, 1)[0]
                return settledPrice

    def getSignalDate(self,myString,search_string):
         p = re.compile(r''+'(\S+)\s*(\S+)\s*'+search_string +'\s(.*\d)', re.IGNORECASE)
         #print(p)
         match = p.search(myString)
         #print(m)
         if match:

                next_string = match.group(0)
                # print(next_string)

                signalString=next_string.split(".")[0]
                # print(signalString)
                signalTime = signalString.split(None, 1)[0]
                # print(signalTime)
                am_pm = signalString.split(None,2)[1]
                rest_string = signalString.split(None,2)[2]
                # print(rest_string)

                # print(am_pm)
                final_string = rest_string + " " +"at"+" "+ signalTime +" "+ am_pm
                # print(final_string)
                signalDate = timestring.Date(final_string).date
                return signalDate

    def getStartEndDate(self,myString,search_string,seprator):
         p = re.compile(r''+search_string +'\s(.*\d)', re.IGNORECASE)
         #print(p)
         match = p.search(myString)
         #print(m)
         if match:

                next_string = match.group(1)
                #print(next_string)

                dateString=next_string.split(seprator)[0]
                #print(dateString)

                time = dateString.split(None, 1)[0]
                # print(time)
                am_pm = dateString.split(None,2)[1]
                rest_string = dateString.split(None,2)[2]
                # print(rest_string)

                # print(am_pm)
                final_string = rest_string + " " +"at"+" "+ time +" "+ am_pm
                # print(final_string)
                myDate = timestring.Date(final_string).date
                return myDate

    def getEndDateMarketShare(self, myString, search_string, seprator):
        p = re.compile(r'' + search_string + '\s(.*\d)', re.IGNORECASE)
        # print(p)
        match = p.search(myString)
        # print(m)
        if match:
            next_string = match.group(1)
            # print(next_string)

            dateString = next_string.split(seprator)[0]
            # print(dateString)

            # time = dateString.split(None, 1)[0]
            # print(time)
            # am_pm = dateString.split(None, 2)[1]
            # rest_string = dateString.split(None, 2)[2]
            # print(rest_string)

            # print(am_pm)
            # final_string = rest_string + " " + "at" + " " + time + " " + am_pm
            # print(final_string)
            myDate = timestring.Date(dateString).date
            return myDate

    def getTypeofQuestion(self,myString):
        q_type = ""
        below = myString.find('below')
        above = myString.find('above')
        # print(below)
        # print(above)
        if "ICO Ranking:" in myString:
            q_type = "Ico Rank"
            return q_type
        if "Resistance level:" and "Support level:" in myString:
            q_type = "Support_Resistance"
            return q_type
        if "market share" in myString:
            q_type = "Market Share"
            return q_type
        if "all-time high" in myString:
            q_type = "above ATH"
            return q_type
        if above!=-1:
            if below !=-1:
                if above < below :
                    q_type = self.nextWord(myString=myString,result='Above')
                    return q_type
                else:
                    q_type = self.nextWord(myString=myString,result='Below')
                    return q_type
            else:
                q_type = self.nextWord(myString=myString,result='Above')
                return  q_type
        if below != -1:
            if above != -1:
                if above < below:
                    q_type = self.nextWord(myString=myString, result='Above')
                    return q_type
                else:
                    q_type = self.nextWord(myString=myString, result='Below')
                    return q_type
            else:
                q_type = self.nextWord(myString=myString, result='Below')
                return q_type



        else:return q_type


    def nextWord(self,myString,result):
        search_string = "before"
        p = re.compile(r'' + search_string + '\s(.*\d)', re.IGNORECASE)
        # print(p)
        match = p.search(myString)
        # print(m)
        if match:
            # print(m.group())
            next_string = match.group(1)
            next_word = next_string.split(None, 1)[0]

            # print("next word after before = ", next_word)
            try:
                month = timestring.Date(next_word).month
                # print(month)

                q_type = result+" price and before time"
                return q_type
            except Exception as e:
                print(e)
                q_type = result+" price and before price"
                return q_type

# cinObj = CindicatorController()
# cinObj.readEmail()

