import requests
from bs4 import BeautifulSoup
import logging
from time import gmtime, strftime
from datetime import datetime
import pandas as pd
from tabulate import tabulate
import pymysql,pymysql.cursors


class CoinmarketcapModel :
    URL = ""
    # Connect to the database
    #connection = pymysql.connect(host='localhost',
     #                            user='root',
      #                           password='',
       #                          db='cryptomasterminds',
        #                         charset='utf8mb4',
         #                        cursorclass=pymysql.cursors.DictCursor)

    def __init__(self,url):
        self.URL = url
        logging.basicConfig(filename='app.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.INFO)

    def get_coin_data(self):
        data = []
        r = requests.get(self.URL)
        html_content = r.content
        soup = BeautifulSoup(html_content, "html.parser")
        table = soup.find('table')
        if table :
            table_body = table.find('tbody')
            if table_body :
                rows = table_body.find_all('tr')
                #print("i m here in table body")
                print(len(rows))
                if len(rows) > 1 :
                    for row in rows:
                        cols = row.find_all('td')
                        id = row.get('id')
                        #print(id)
                        cols = [ele.text.strip() for ele in cols]
                        cols.append(id)
                        data.append([ele for ele in cols if ele])# Get rid of empty values
                    #print(data)
                    return data
                return data
            return data
        return data


    def get_data(self):
        data = []
        logging.info('New Request')
        logging.info('Url Requested(Checked) = %s', self.URL)
        r = requests.get(self.URL)
        time_in_seconds = r.elapsed.total_seconds()
        status = r.status_code
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        logging.info('Time taken for Request to complete in seconds (Response Time) = %s', time_in_seconds)
        html_content = r.content
        soup = BeautifulSoup(html_content, "html.parser")
        #table = soup.find_all('table')[0]
        #df = pd.read_html(str(table))
        #print(tabulate(df[0], headers='keys', tablefmt='psql'))
        name = soup.find('h2',{'class':'pull-left bottom-margin-2x'})
        ul = soup.find('ul',{'class':'list-unstyled'})
        url=''
        if ul:
            a = ul.find_all('a')
            if a:
                for item in a:
                    # print(item.get('href'))
                    try:
                        url = a[0].get('href')
                        print(url)
                    except:pass
        table = soup.find('table')
        if table :
            table_body = table.find('tbody')
            if table_body :
                rows = table_body.find_all('tr')
                #print("i m here in table body")
                print(len(rows))
                if len(rows) > 1 :
                    for row in rows:
                        cols = row.find_all('td')
                        id = row.get('id')
                        #print(id)
                        cols = [ele.text.strip() for ele in cols]
                        cols.append(id)
                        if name:
                            try:
                                cols.append(name.text)
                            except:pass
                        if url:
                            try:
                                cols.append(url)
                            except:

                                pass
                        data.append([ele for ele in cols if ele])# Get rid of empty values
                    #print(data)
                    logging.info('Finished')
                    return data
                return data
            return data
        return data


    def get_daily_data(self):
        data = []
        r = requests.get(self.URL)
        html_content = r.content
        soup = BeautifulSoup(html_content, "html.parser")

        table = soup.find('table')
        if table :
            table_body = table.find('tbody')
            if table_body :
                rows = table_body.find_all('tr')
                print(len(rows))
                if len(rows) > 1 :
                    for row in rows:
                        cols = row.find_all('td')
                        # id = row.get('id')
                        #print(id)
                        cols = [ele.text.strip() for ele in cols]
                        # cols.append(id)
                        data.append([ele for ele in cols if ele])# Get rid of empty values
                    #print(data)
                    return data
                return data
            return data
        return data



    def get_coin_details_for_update(self):
        data = []
        r = requests.get(self.URL)
        html_content = r.content
        soup = BeautifulSoup(html_content, "html.parser")
        name = soup.find('h2',{'class':'pull-left bottom-margin-2x'})
        if name:
            data.append(name.text)
        else:data.append("")


        ul = soup.find('ul',{'class':'list-unstyled'})
        if ul:
            a = ul.find_all('a')
            if a:
                for item in a:
                    # print(item.get('href'))
                    url = a[0].get('href')
                print(url)
                if url:
                    data.append(url)
                else:data.append("")
        return data



    def get_minute_data(self):

        #data = []
        logging.info('New Request')
        logging.info('Url Requested(Checked) = %s', self.URL)
        r = requests.get(self.URL)
        time_in_seconds = r.elapsed.total_seconds()
        status = r.status_code
        time = strftime("%Y-%m-%d %H:%M:%S")
        #print(r.elapsed)
        print(time)
        logging.info('Time taken for Request to complete in seconds (Response Time) = %s', time_in_seconds)
        json_data = r.json()
        #print(json_data)
        return json_data







