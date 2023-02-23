import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler


def read_data(path, date_columns=None):
    if date_columns:
        df = pd.read_csv(path)
        for col in date_columns:
            df[col] = df[col].apply(lambda x: pd.Timestamp(x[:10]))
        df = df.sort_values(date_columns[0])
    else:
        df = pd.read_csv(path)
    return df


def preprocess(df, cut=None):
    df = df.rename(columns={'Close': 'Price'})
    df = df.drop('Adj Close', axis=1)
    if cut:
        df = df.loc[df.Date >= cut]
    return df


def split_train_test(df, perc=0.8, date=None, date_column=None):
    # Data can be split by providing a desired percent or by specifying the date of the split
    if date and date_column:
        date = pd.Timestamp(date)
        train = df.loc[df[date_column] < date]
        test = df.loc[df[date_column] >= date]
    else:
        train, test = train_test_split(df, test_size=(1-perc), train_size=perc, shuffle=False)
    return train, test


def convert_to_array(df):
    return df.set_index('Date').to_numpy()


def scale_data(df, scaler='minmax'):
    # Data is scaled through minmax scaled or standard scaler
    if scaler == 'standard':
        sc = StandardScaler()
    else:
        sc = MinMaxScaler()
    df_scaled = sc.fit_transform(df)
    return sc, df_scaled


def to_supervised(X, n_future, n_past):
    # Transforms the time series forecasting problem in a supervised one
    # creates a new dataframe where with each observation also the previous n_past and n_future ones are provided
        Xs, ys = [], []
        for i in range(n_past, len(X) - n_future + 1):
            Xs.append(X[i - n_past:i, 0:X.shape[1]])
            ys.append(X[i + n_future - 1:i + n_future, 0])
        return np.array(Xs), np.array(ys)

