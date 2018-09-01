import requests 
from bs4 import BeautifulSoup
import csv
import re

url = "https://icobench.com/icos"

r = requests.get(url)

soup = BeautifulSoup(r.content,"lxml")

pages=[]

#page 1
refs = soup.find_all ("a", {"class": "name"})
for ref in refs: pages+=["https://icobench.com/"+ref.get("href")]

#page 2- all 

total_pages=int(soup.find_all("div", {"class": "pages"})[0].find_all("a")[len(soup.find_all("div", {"class": "pages"})[0].find_all("a"))-2].get_text())

for i in range (2,total_pages):
   url = "https://icobench.com/icos?page=%d" %i
   r = requests.get(url)
   soup = BeautifulSoup(r.content,"lxml")
   refs = soup.find_all ("a", {"class": "name"})
   for ref in refs: pages+=["https://icobench.com/"+ref.get("href")]

with open ('icobench_data.csv','w') as outfile:
   csv_writer= csv.writer (outfile)
   csv_writer.writerow (["title","subtitle","categs","profile", "team", "vision", "product","Token","PreICO_Price","Price","Price_in_ICO","Platform","Accepting","Minimum_investment","Soft_cap","Hard_cap","Country","Whitelist_KYC","Restricted_areas","preICO_start","preICO_end","ICO_start","ICO_end","Raised","Status","Time"])

for page in pages:

   with open ('icobench_index_pages.csv','a') as outfile:
      csv_writer= csv.writer (outfile)
      csv_writer.writerow ([page])

   print(page)

   url = page

   r = requests.get(url)

   soup = BeautifulSoup(r.content,"lxml")

   #info

   title= ''
   subtitle= ''
   desc= ''
   categs= ''

   try:title=soup.find_all ("h1")[0].text
   except: pass
   try:subtitle=soup.find_all ("h2")[0].text
   except: pass
   try:desc=soup("p")[0].text
   except: pass

   for cat in soup.find_all("div", {"class": "categories"})[0].find_all("a"): 
      try:categs += cat.text+'|'
      except: pass

   print (title)
   print (subtitle)
   print (desc)
   print (categs)

   #ratings

   profile= ''
   team= ''
   vision= ''
   product= ''

   try: profile = re.findall("\d+\.\d+",soup.find_all("div", {"class": "distribution"})[0].find_all("div", {"class": "col_4"})[0].text )[0]
   except: pass
   try: team = re.findall("\d+\.\d+",soup.find_all("div", {"class": "distribution"})[0].find_all("div", {"class": "col_4"})[1].text )[0]
   except: pass
   try: vision = re.findall("\d+\.\d+",soup.find_all("div", {"class": "distribution"})[0].find_all("div", {"class": "col_4"})[2].text )[0]
   except: pass
   try: product = re.findall("\d+\.\d+",soup.find_all("div", {"class": "distribution"})[0].find_all("div", {"class": "col_4"})[3].text ) [0]
   except: pass

   print (profile, team, vision, product)

   #raised

   Raised=''
   try: Raised = soup.find_all("div", {"class": "raised"})[0].get_text()
   except: pass

   #time

   Time=''
   a=''
   b=''
   c=''


   try: a = soup.find_all("div", {"class": "financial_data"})[0].find_all("div",{"class":"row"})[0].find_all("div",{"class":"col_2 expand"})[0].find_all()[0].get_text()
   except: pass

   try: b = soup.find_all("div", {"class": "financial_data"})[0].find_all("div",{"class":"row"})[0].find_all("div",{"class":"col_2 expand"})[0].find_all()[1].get_text()
   except: pass

   try: c = soup.find_all("div", {"class": "financial_data"})[0].find_all("div",{"class":"row"})[0].find_all("div",{"class":"col_2 expand"})[0].find_all()[2].get_text()
   except: pass

   if a=='Time': Time=b+'  '+c


   #financials

   financials = soup.find_all("div", {"class": "financial_data"})[0].find_all("div",{"class":"data_row"})

   #for row in financials:
   #   row.find_all("div",{"class":"col_2"})[0].prettify()
   #   row.find_all("div",{"class":"col_2"})[1].prettify()


   Status=''

   Token=''
   PreICO_Price=''
   Price=''
   Price_in_ICO=''
   Platform=''
   Accepting=''
   Minimum_investment=''
   Soft_cap=''
   Hard_cap=''
   Country=''
   Whitelist_KYC=''
   Restricted_areas=''
   preICO_start =''
   preICO_end = ''
   ICO_start = ''
   ICO_end = ''

   for row in financials:
      try: a= row.find_all("div",{"class":"col_2"})[0].get_text().strip()
      except: pass
      try: b=row.find_all("div",{"class":"col_2"})[1].get_text().strip()
      except: pass
      if a == 'Status': Status=b
      if a == 'Token': Token=b
      if a == 'PreICO Price': PreICO_Price=b
      if a == 'Price': Price=b
      if a == 'Price in ICO': Price_in_ICO=b
      if a == 'Platform': Platform=b
      if a == 'Accepting': Accepting=b
      if a == 'Minimum investment': Minimum_investment=b
      if a == 'Soft cap': Soft_cap=b
      if a == 'Hard cap': Hard_cap=b
      if a == 'Country': Country=b
      if a == 'Whitelist/KYC': Whitelist_KYC=b
      if a == 'Restricted areas': Restricted_areas=b
      if a == 'preICO start': preICO_start=b
      if a == 'preICO end': preICO_end=b
      if a == 'ICO start': ICO_start=b
      if a == 'ICO end': ICO_end=b


   print (Token)
   print (PreICO_Price)
   print (Price)
   print (Price_in_ICO)
   print (Platform)
   print (Accepting)
   print (Minimum_investment)
   print (Soft_cap)
   print (Hard_cap)
   print (Country)
   print (Whitelist_KYC)
   print (Restricted_areas)
   print (preICO_start)
   print (preICO_end)
   print (ICO_start)
   print (ICO_end)


   print (Raised)

   print (Status)
   print (Time)

   with open ('icobench_data.csv','a') as outfile:
      csv_writer= csv.writer (outfile)
      csv_writer.writerow ([title,subtitle,categs,profile, team, vision, product,Token,PreICO_Price,Price,Price_in_ICO,Platform,Accepting,Minimum_investment,Soft_cap,Hard_cap,Country,Whitelist_KYC,Restricted_areas,preICO_start,preICO_end,ICO_start,ICO_end,Raised,Status,Time])
