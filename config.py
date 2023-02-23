# Insert your own API token to perform the request through Twitter APIv2. If not specified, uses local text_source.
twitter_api_token = ''

# Source must be one of "twitter" or "news"
source = 'news'

# Local directories to which the script will point to for retrieving files
text_directory = f'./data/'
dataset_path = './data/gas_prices.csv'

# Specify which Neural Network to use for time series forecasting. Must be one of "BiLSTM" or "GRU"
nn = 'BiLSTM'

# Set to True if you want to include other features for predictions.
univariate = False
