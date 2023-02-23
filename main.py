import pandas as pd

from utils.preprocessing_commons import *
from models.networks import *
from ScrapingTweet.twitter_scraper import scrape_tweets, process_tweets
from ScrapingOilPrice.news_scraper import scrape_news
from models.BERT import process_text
import config

# TO ADJUST THIS SCRIPT CONFIGURATION, PLEASE USE THE config.py FILE

df = read_data(config.dataset_path, date_columns=['Date'])
df = preprocess(df, cut='2019-06-19')

# If univariate mode is selected, text retrieval and processing operations are skipped
if not config.univariate:
    if config.source == 'news':
        scrape_news()
        text_source = pd.read_csv(config.text_directory + "all_news.csv", sep=';', parse_dates=['DATE'])
    elif config.source == 'twitter':
        # If no twitter API token is provided, uses local files to process tweets
        if config.twitter_api_token != '':
            scrape_tweets(start='2019-06-19', end='2023-01-31')
        process_tweets()
        text_source = pd.read_csv(config.text_directory + "twitter.csv", parse_dates=['DATE'])

    df = process_text(df, text_source)
    df = df[['Date', 'Price', 'Attention']]
else:
    df = df[['Date', 'Price']]

train, test = split_train_test(df, date_column='Date', date='2022-12-01')
train = convert_to_array(train)
test = convert_to_array(test)

input_scaler, train_scaled = scale_data(train, 'minmax')
test_scaled = input_scaler.transform(test)

output_scaler, _ = scale_data(train[:, 0:1])

n_future = 1   # Number of days we want to predict into the future
n_past = 5     # Number of past days we want to use to predict the future

X_train, y_train = to_supervised(train_scaled, n_future, n_past)
X_test, y_test = to_supervised(test_scaled, n_future, n_past)

if config.nn == 'BiLSTM':
    model = BiLSTM(input_shape=X_train.shape)
elif config.nn == 'GRU':
    model = Gru(input_shape=X_train.shape)
model.info()
model.train(X_train, y_train)

predictions = model.predict(X_test, scaler=output_scaler)

# Evaluates predictions by computing MAE and RMSE
y_test_unscaled = output_scaler.inverse_transform(y_test)
model.evaluate_predictions(predictions, y_test_unscaled)

# Predictions are exported to a csv file
predictions_df = pd.DataFrame(columns=['Date', 'Prediction'])
predictions_df['Date'] = df.loc[df.Date >= '2022-12-01'].Date[5:]
predictions_df['Prediction'] = predictions
predictions_df.to_csv("./output/predictions.csv", header=True, index=None)
