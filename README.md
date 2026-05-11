# Dutch TTF Price Prediction with News and Tweet Embeddings

Machine learning project for short-term Dutch TTF natural gas price forecasting using historical time series data combined with textual embeddings extracted from news articles and tweets.

The project was developed for the Artificial Intelligence and Machine Learning course at Politecnico di Bari, A.Y. 2021/2022.

## Project Overview

The goal of this project is to evaluate whether textual information from news articles and tweets can improve short-term natural gas price forecasting.

The project combines:

- historical Dutch TTF gas price data;
- news articles related to natural gas, energy and geopolitics;
- tweets related to gas prices and energy topics;
- BERT-based textual embeddings;
- an attention mechanism for daily textual feature aggregation;
- recurrent neural networks for time series forecasting;
- BiLSTM and GRU architectures;
- Prophet as a baseline model.

The experimental results show that recurrent neural networks can provide accurate short-term predictions for Dutch TTF prices. However, adding textual embeddings from news and tweets did not significantly improve performance compared to using the historical time series alone.

## Dataset

The historical price dataset contains daily Dutch TTF gas price data from Yahoo Finance.

The available features include:

- Date
- Open
- High
- Low
- Close
- Volume

The target variable used for forecasting is the daily closing price.

The dataset covers the period from `2019-06-19` to `2023-01-30`.

Textual data includes:

- news articles scraped from OilPrice.com;
- tweets collected through Twitter API v2 and processed into local CSV/JSON files.

The processed datasets are stored inside the `data/` directory.

## Methodology

The project follows this pipeline:

1. Load and preprocess Dutch TTF historical price data.
2. Load textual data from either news articles or tweets.
3. Generate textual embeddings using BERT.
4. Aggregate daily textual information through an attention mechanism.
5. Merge historical time series data with textual attention features.
6. Train either a BiLSTM or GRU forecasting model.
7. Evaluate predictions using MAE and RMSE.
8. Export predictions to CSV.

The main configuration is handled through `config.py`.

## Repository Structure

```text
.
├── ScrapingOilPrice/
│   ├── function/
│   └── news_scraper.py
│
├── ScrapingTweet/
│   ├── function/
│   ├── json_file/
│   ├── json_result/
│   └── twitter_scraper.py
│
├── data/
│   ├── all_news.csv
│   ├── gas_news.csv
│   ├── gas_prices.csv
│   ├── geopolitcs_news.csv
│   └── twitter.csv
│
├── models/
│   ├── BERT.py
│   └── networks.py
│
├── notebooks/
│   ├── BERT.ipynb
│   ├── BiLSTM_& _GRU.ipynb
│   └── Prophet.ipynb
│
├── output/
│   └── predictions.csv
│
├── utils/
│   └── preprocessing_commons.py
│
├── config.py
├── main.py
└── README.md
```

## Configuration

Before running the project, edit the `config.py` file.

Available configuration options:

```python
twitter_api_token = ''
source = 'news'
text_directory = './data/'
dataset_path = './data/gas_prices.csv'
nn = 'BiLSTM'
univariate = False
```

### Text source

Choose the textual source:

```python
source = 'news'
```

or:

```python
source = 'twitter'
```

### Neural network model

Choose the forecasting model:

```python
nn = 'BiLSTM'
```

or:

```python
nn = 'GRU'
```

### Univariate mode

To use only the historical price series and skip textual processing:

```python
univariate = True
```

To include textual embeddings:

```python
univariate = False
```

### Twitter API token

The project can process local tweet files without an API token.

To perform new Twitter API requests, insert a valid Twitter API v2 Bearer Token:

```python
twitter_api_token = 'YOUR_TOKEN_HERE'
```

Do not commit real API tokens to GitHub.

## Installation

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install the main dependencies:

```bash
pip install pandas numpy scikit-learn tensorflow keras torch transformers scipy matplotlib prophet
```

Depending on the local Python version and hardware configuration, TensorFlow or PyTorch installation may require additional setup.

## Usage

Run the main script:

```bash
python main.py
```

The script will:

1. load the Dutch TTF price dataset;
2. preprocess the time series;
3. load either news or tweet data;
4. compute textual embeddings;
5. train the selected neural network;
6. evaluate the predictions;
7. export the results.

The output file is saved to:

```text
output/predictions.csv
```

## Notebooks

The `notebooks/` directory contains three notebooks used for experimentation and model analysis:

- `Prophet.ipynb`: baseline forecasting model;
- `BERT.ipynb`: textual embedding generation;
- `BiLSTM_& _GRU.ipynb`: recurrent neural network experiments.

## Experimental Setup

The dataset was split into:

- training set: `2019-06-19` to `2022-11-30`;
- test set: `2022-12-01` to `2023-01-31`.

The forecasting task was formulated as a supervised learning problem using a lookback window of 5 days to predict the following day.

The following configurations were evaluated:

- univariate time series;
- multivariate time series with additional market features;
- multivariate time series with date-based features;
- multivariate time series with news embeddings;
- multivariate time series with tweet embeddings.

## Results

The models were evaluated using:

- Mean Absolute Error (MAE);
- Root Mean Square Error (RMSE).

The recurrent neural network models significantly outperformed the Prophet baseline.

Among the tested models:

- GRU achieved the best result in the univariate setting;
- BiLSTM showed stronger performance across most multivariate configurations;
- textual embeddings from news and tweets did not significantly improve forecasting accuracy.

## Conclusions

The project shows that BiLSTM and GRU models can effectively model the short-term dynamics of Dutch TTF natural gas prices.

However, the integration of BERT-based textual embeddings from news and tweets did not provide a clear performance improvement over the use of historical price data alone.

Future work may explore:

- alternative NLP models;
- sentiment analysis;
- larger and more diverse textual sources;
- more advanced attention mechanisms;
- transformer-based time series models.

## Authors

- Michele Abbaticchio
- Stefano Battista
- Domenico Catucci

## Academic Context

Project work for the Artificial Intelligence and Machine Learning course at Politecnico di Bari.

## License

This repository is intended for academic and portfolio purposes.