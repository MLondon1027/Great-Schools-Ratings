# Imports
from bs4 import BeautifulSoup
import requests
import json
from pymongo import MongoClient
import time
import re
import pandas as pd

def scrape_district_names(site):
    '''
    Scrape school district names from greatschools.org
    Parse school districts with BeautifulSoup and create a list of urls
    Return only urls that are school districts

    Parameters
    ----------
    site: website of district names

    Returns
    -------
    list of cleaned school district urls
    '''
    dist_page = requests.get(site)
    dist_soup = BeautifulSoup(dist_page.content, 'html.parser')
    dist_html = list(dist_soup.children)[3]
    dist_urls = []
    for a in dist_soup.find_all('a', href=True):
        dist_urls.append(a['href'])
    txt = '/texas/'
    dist_urls_cleaned = [x for x in dist_urls if x.startswith(txt)]
    return dist_urls_cleaned

def school_scraper(collection, dist_urls_cleaned):
    '''
    get raw html for each individual school district and put in mongodb
    turn scripts into json dictionaries
    '''
    script = db[collection] # 'script'
    for district in dist_urls_cleaned:
        url = 'http://www.greatschools.org' + district
        page = requests.get(url)
        script.insert_one({district:page.content})
        soup = BeautifulSoup(page.content, 'html.parser')
        html = list(soup.children)[3]
        tags= soup.find_all('script')
        time.sleep(2)
        print(url)
    # turn scripts into json dictionaries
    clean = db['clean']
    for document in db[collection].find():
        try:
            soup = BeautifulSoup(document[list(document.keys())[1]], 'html.parser')
            script_w_json = soup.find('script', {'class':'js-react-on-rails-component', 'data-component-name':"TopSchoolsStatefulWrapper"})
            print(list(document.keys())[1])
            json_dict = json.loads(script_w_json.contents[0])
            clean.insert_one(json_dict)
        except:
            continue

if __name__ =="__main__":
    client = MongoClient('localhost', 27017)
    db = client['schools']
    dist_urls_cleaned = scrape_district_names('https://www.greatschools.org/schools/districts/texas/tx/')
    school_scraper('script', dist_urls_cleaned)





