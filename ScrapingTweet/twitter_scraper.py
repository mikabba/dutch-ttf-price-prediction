from ScrapingTweet.function import manageJson, tweetRequest
from ScrapingTweet.function.funzioni_date import *
import config
import glob
import re
import pandas as pd

def process_tweets():
    data = pd.DataFrame()

    for file in glob.glob("./ScrapingTweet/json_result/*.json"):
        t = pd.read_json(file, orient='index')
        data = data.append(t, ignore_index=True)

    data[0] = data[0].apply(lambda x: re.sub("https:\/\/([A-z\d.\/])*", "", str(x)))
    data[0] = data[0].apply(lambda x: re.sub("[^A-z\d,.$%\s€]+", "", x))
    data[1] = data[1].apply(lambda x: pd.to_datetime(x))
    data = data.rename(columns={0: 'CONTENT', 1: 'DATE'})
    data.to_csv("./data/twitter.csv", header=True, sep=',', index=None)

def scrape_tweets(start, end):
    end_date = np.datetime64(start)
    start_date = sum_date(end_date, -90)
    try:
        while start_date >= np.datetime64(end):
            if start_date >= end_date:
                raise ValueError("start_time must be before end_time")
            end_date = sum_date(start_date, +90)
            n_files = tweetRequest.fun(format_date(start_date), format_date(end_date),
                                       bearer_token=config.twitter_api_token)
            for n_file in n_files:
                manageJson.manage(f'{n_file}')
            start_date = sum_date(start_date, -90)
        process_tweets()
    except ValueError as e:
        print(e)


