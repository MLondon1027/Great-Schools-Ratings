# Imports
from pymongo import MongoClient
import pandas as pd
from flatten_json import flatten

# Run Mongo - do I do this?
#client = MongoClient('localhost', 27017)
#db = client['schools']
#clean = db['clean']

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

# Drop duplicates
df_h_0['id'].drop_duplicates(inplace=True)
df_h_1['id'].drop_duplicates(inplace=True)
df_h_2['id'].drop_duplicates(inplace=True)
df_h_3['id'].drop_duplicates(inplace=True)
df_h_4['id'].drop_duplicates(inplace=True)

# Concatenate the 5 dataframes
dataframes = [df_h_0, df_h_1, df_h_2, df_h_3, df_h_4]
combined_df = pd.concat(dataframes)

# Drop duplicates of concatenated dataframe
combined_df['id'].drop_duplicates(inplace=True)

# Check for duplicates
combined_df['id'].duplicated().value_counts()

# Save to csv
combined_df.to_csv('combined_df.csv')