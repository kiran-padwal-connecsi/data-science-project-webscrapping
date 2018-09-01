import datetime
import re
import requests
from bs4 import BeautifulSoup
# from controller.pytextbelt import Textbelt


class NewCoinListingController:

    def __init__(self,url):
        self.url = url

    def get_data(self):

        data = []
        r = requests.get(url=self.url)
        html_content = r.content
        soup = BeautifulSoup(html_content, "html.parser")
        ul = soup.find('ul', {'class': 'article-list'})
        if ul:
            li = ul.find_all('li')
            if li:
                for element in li:
                    text = element.text.strip()
                    data.append(text)
            else:
                print("i m in else")
                data.append("")
        return data


    def send_sms(self):
        # print(data)
        # for number in numbers:
        #     print(number)
        Recipient = Textbelt.Recipient("729675768", "intl")
        reponse = Recipient.send("Hello World!")
        # reponse = Recipient.send("Its me, The Bot.")
        print(reponse)


conObj = NewCoinListingController(url="https://support.binance.com/hc/en-us/sections/115000106672-New-Listings")
data = conObj.get_data()
print(data)
conObj.send_sms()