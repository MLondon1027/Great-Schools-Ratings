# Imports
from bs4 import BeautifulSoup
import requests
import json
from pymongo import MongoClient
import time
import re
import pandas as pd

# Run Mongo
client = MongoClient('localhost', 27017)
db = client['schools']
script = db['script']

# Scrape district names and append to list
dist_page = requests.get('https://www.greatschools.org/schools/districts/texas/tx/')
dist_soup = BeautifulSoup(dist_page.content, 'html.parser')
dist_html = list(dist_soup.children)[3]
dist_urls = []
for a in dist_soup.find_all('a', href=True):
    dist_urls.append(a['href'])

# Remove urls that are not disticts
txt = '/texas/'
dist_urls_cleaned = [x for x in dist_urls if x.startswith(txt)]

# Run scraper by district
for district in dist_urls_cleaned:
    url = 'http://www.greatschools.org' + district
    page = requests.get(url)
    script.insert_one({district:page.content})
    soup = BeautifulSoup(page.content, 'html.parser')
    html = list(soup.children)[3]
    tags= soup.find_all('script')
    time.sleep(2)
    print(url)

# Turn scripts into json dictionaries
problem_dists = ['/texas/houston/a-plus-unlimited-potential/', 
                 '/texas/league-city/bay-area-charter-inc/', 
                 '/texas/leakey/big-springs-charter-school/',
                 '/texas/mountain-home/divide-independent-school-district']
clean = db['clean']
for document in db['script'].find():
    if list(document.keys())[1] not in problem_dists:
        try:
            soup = BeautifulSoup(document[list(document.keys())[1]], 'html.parser')
            script_w_json = soup.find('script', {'class':'js-react-on-rails-component', 'data-component-name':"TopSchoolsStatefulWrapper"})
            print(list(document.keys())[1])
            json_dict = json.loads(script_w_json.contents[0])
            clean.insert_one(json_dict)
        except:
            continue