import requests ## pip install requests
from bs4 import BeautifulSoup
import logging
from time import gmtime, strftime


class AppModel:
    url_content = {}
    response_string = []

    def _init_(self):
        self.url_content = AppModel.url_content
        self.response_string = AppModel.response_string

    def read(self):

        with open('configuration.txt', 'r') as file:
            for line in file:
                line = line.strip()
                temp_list = line.split(',')
                url = temp_list[0]
                content = temp_list[1:]
                content = list(filter(None, content))
                self.url_content.__setitem__(url,content)
            return self.url_content

    def get_response(self, url_content):
        urls = url_content.keys()
        urls = list(filter(None, urls))
        #print(urls)
        logging.basicConfig(filename='app.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
        for url in urls:
                #print(url)
                logging.info('New Request')
                logging.info('Url Requested(Checked) = %s', url)
                r = requests.get(url)
                time_in_seconds = r.elapsed.total_seconds()
                status = r.status_code
                time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                if status == requests.codes.ok:
                    status_url = 'Up and Running'
                    self.generate_html(url, status_url, time)
                    logging.info('Status = %s',status_url)
                    logging.info('Time taken for Request to complete in seconds (Response Time) = %s', time_in_seconds)
                    html_content = r.content
                    soup = BeautifulSoup(html_content, "html.parser")
                    pretty_soup = soup.prettify()
                    #print(pretty_soup)
                    content = url_content.get(url)
                    for item in content:
                        if pretty_soup.__contains__(item):
                            print("Contains Given Content(String) - ", item)
                            logging.info('Contains Given Content(String) - %s', item)
                        else:
                            print("Does not Matched Given Content(String) - ", item)
                            logging.info('Does not Matched Given Content(String) - %s', item)
                else:
                     status_url = 'Url not Found/Website is Down'
                     self.generate_html(url, status_url, time)
                     logging.info('Url not found(Website is Down)')
                logging.info('Finished')

    def generate_html(self, url, status_url, last_checked_time):
        with open("AppView.html") as inf:
            txt = inf.read()
            soup = BeautifulSoup(txt, "html.parser")
            #print(soup.prettify())
        new_tr = soup.new_tag('tr')
        new_td_url = soup.new_tag('td')
        new_td_url.append(soup.new_string(url))
        new_td_status_url = soup.new_tag('td')
        new_td_status_url.append(soup.new_string(status_url))
        new_td_last_checked_time = soup.new_tag('td')
        new_td_last_checked_time.append(soup.new_string(last_checked_time))
        # insert it into the document
        new_tr.append(new_td_url)
        new_tr.append(new_td_status_url)
        new_tr.append(new_td_last_checked_time)

        old_tr = soup.findChildren('tr')
        for tr in old_tr:
            old_td = tr.findChildren('td')
            url_string = old_td[0].getText()
            if url_string != '':
                if url_string == url:
                    soup.table.tr.replaceWith(new_tr)
                else:
                    soup.table.append(new_tr)

            else:
                soup.table.tr.replaceWith(new_tr)


        # save the file again
        with open("AppView.html", "w") as outf:
            outf.write(str(soup))


