#KKday：the traveling packages for the countries and cities we offered

s_country = '日本' #Japan
s_city = '沖繩' #Okinawa

#The following are the country and city code in KKday, will be used in the web scraping process
country = {
    '日本': 'A01-003',
    '韓國': 'A01-004',
    '香港': 'A01-005',
    '泰國': 'A01-010',
    '新加坡': 'A01-013'
}

city = {
    'None': '',
    '東京': 'A01-003-00001',
    '大阪京都': 'A01-003-00003',
    '北海道': 'A01-003-00005',
    '沖繩': 'A01-003-00013',
    '首爾': 'A01-004-00001',
    '釜山': 'A01-004-00002',
    '曼谷': 'A01-010-00001',
    '普吉島': 'A01-010-00002',
    '芭達雅': 'A01-010-00007'  
}

country_id = country[s_country]
city_id = city[s_city]

print(country_id, city_id)

#KKday：web scraping 

import requests
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup

import re
import time

url = 'https://www.kkday.com/zh-tw/product/ajax_get_autocomplete_prod_data?keywords=&rows=2&country=' + country_id + '&city=' + city_id + '&csrf_token_name=e9a9e93c38556b46d08d9888f104d802'
res = requests.get(url)
data  = json.loads(res.text)

itineraries = []
for i, d in enumerate(data): #create title and id for the url
    itineraries.append({
        'id':d['id'],
        'title':d['name']})
print(itineraries)

#get all the itineraries for the cities from the database 

def getContentFromPage(dic_i):
    detail_id = 'https://www.kkday.com/zh-tw/product/' + dic_i['id']
    result = requests.get(detail_id)
     
    chrome_options = Options()
    chrome_options.add_argument("--headless")       # define headless
    driver = webdriver.Chrome(options=chrome_options) 
    
    #get the detail id
    driver.get(detail_id)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # find and clean up the info
    def toContent(raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html) 
        return cleantext
    
    info_class = soup.find_all('div', {"class": "info-section"})
    p = info_class[0].find('p')
    rawInfo = str(p)
    info = toContent(rawInfo)
    
    # find and clean up the price
    def toD(p_string):
        digit = ''.join(i for i in p_string if i.isdigit())
        return int(digit)
    price_class = soup.find_all('div', {"class": "product-pricing text-left"})[0].find("h2")
    price = toD(price_class.string)
    return info, price

for dic_i in itineraries:
    info, price = getContentFromPage(dic_i)
    dic_i.update({"price": price}) #increase price key into the dictionary
    dic_i.update({"info": info})

print(itineraries)
    



#change to pandas, print out as csv file
import csv

import numpy as np
import pandas as pd

df = pd.DataFrame(itineraries)
df.to_csv('./kkday/output.csv', encoding='utf-8')
