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

# Create a dataframe

df = pd.DataFrame(list(clean.find({})))

# Only include schoolsData column

df.drop(['community', 'locality', 'schoolLevels', 'summaryType', '_id'], axis=1, 
inplace=True)

df = df['schoolsData'].apply(pd.Series)

# Only include high school data

df_h = df['high'].apply(pd.Series)

# Drop rows if all values are NaNs- this means district has no high school
df_h.dropna(axis=0, how='all', inplace=True)

# Flatten columns and drop NaNs
df_h_0 = pd.DataFrame([flatten(x) for x in df_h[0]])
df_h_1 = df_h[1].dropna(axis=0, inplace=True)
df_h_1 = pd.DataFrame([flatten(x) for x in df_h[1]])
df_h_2 = df_h[2].dropna(axis=0, inplace=True)
df_h_2 = pd.DataFrame([flatten(x) for x in df_h[2]])
df_h_3 = df_h[3].dropna(axis=0, inplace=True)
df_h_3 = pd.DataFrame([flatten(x) for x in df_h[3]])
df_h_4 = df_h[4].dropna(axis=0, inplace=True)
df_h_4 = pd.DataFrame([flatten(x) for x in df_h[4]])

# Remove unnecessary columns
def clean_round_one(dataframes):
    for df in dataframes:
        df.drop(cols_to_del, axis=1, inplace=True)

cols_to_del = ['assigned', 'address_street1', 'address_street2', 'address_city', 
               'lat', 'lon', 'pinned', 'testScoreRatingForEthnicity', 'highlighted']
dataframes = [df_h_0, df_h_1, df_h_2, df_h_3, df_h_4]
clean_round_one(dataframes)

# Remove charter schools
df_h_0 = df_h_0[df_h_0['schoolType'] == 'public']
df_h_1 = df_h_1[df_h_1['schoolType'] == 'public']
df_h_2 = df_h_2[df_h_2['schoolType'] == 'public']
df_h_3 = df_h_3[df_h_3['schoolType'] == 'public']
df_h_4 = df_h_4[df_h_4['schoolType'] == 'public']

# Concatenate the 5 dataframes
dataframes = [df_h_0, df_h_1, df_h_2, df_h_3, df_h_4]
combined_df = pd.concat(dataframes)

# Save to csv
combined_df.to_csv('combined_df.csv')
