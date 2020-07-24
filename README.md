# Great-Schools-Ratings

## Background

I discovered the greatschools.org website and rating system in an unorthodox way: through real estate. Zillow and other major home search apps show schools and their corresponding GreatSchools rating under each listing. Through my real estate experience I've learned the importance of schools in home values, and GreatSchools seems to have cornered the market in the K-12 rating market.

Back to the school ratings: I strongly believe in equality in the K-12 market. Children should receive an education up to state standards no matter which public school they attend. I was especially interested to compare the outcomes of schools with more lower income students to those with fewer low income students, specifically whether there is a difference between the mean test score rating of high schools with majority low income students (>50% low income) vs. high schools with minority low income students (<50% low income).

## Methodology

My methodology for the project is to build a web scraper to scrape the greatschools.org website, derive insights through exploratory data analysis, and form a consclusion via a statistical test. I will use a variety of tools including Python, Jupyter Notebooks, VSCode, Git, Docker, MongoDB, Requests, BeautifulSoup, Json, Matplotlib, Seaborn, Numpy, Pandas, and the stats module of Scipy.

## Data and Process

The data was all scraped from Greatschools.org. I first scraped a list of all the Texas school districts and appended their urls to a list. I then removed any urls that were not actual school districts. I then ran the scraper for each school district, scraping the entire page and inserting it into a MongoDB collection. I parsed it through BeautifulSoup and then turned the scripts into json dictionaries and saved each one as a document in a new MongoDB collection.

After creating a Pandas dataframe with the cleaned scripts, I subsetted the data to select just high school data. I used the flatten method from the flatten_json library to flatten columns and then dropped NaNs. I made the decision to drop charter schools because there was a small number of them and I wanted to focus exclusively on non application based schools. It would be interesting to do a separate study including charter schools.

There were five separate dataframes, because some districts had up to five high schools. I concatenated the five dataframes. I then changed string numbers to floats in the columns I was interested in analyzing. I saved the final dataframe to a csv file.

## Exploratory Data Analysis

[Test Score Rating Distribution](/Images/final_test_scores_dist.png)


