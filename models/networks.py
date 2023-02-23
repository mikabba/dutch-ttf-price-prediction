from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, Bidirectional, GRU
import matplotlib.pyplot as plt
import numpy as np


class BiLSTM:

    def __init__(self, input_shape):
        self.history = None
        self.model = Sequential()
        # Input layer
        self.model.add(
            Bidirectional(LSTM(units=100, return_sequences=True), input_shape=(input_shape[1], input_shape[2])))
        self.model.add(Dropout(0.2))

        # Hidden layer
        self.model.add(Bidirectional(LSTM(units=50)))
        self.model.add(Dropout(0.25))

        self.model.add(Dense(units=1))

        # Compile model
        self.model.compile(optimizer='adam', loss='mean_squared_error')

    def info(self):
        # prints a summary of the model
        self.model.summary()

    def train(self, X_train, y_train):
        self.history = self.model.fit(X_train, y_train,
                                      epochs=50,
                                      batch_size=64,
                                      shuffle=False,
                                      validation_split=0.2,
                                      verbose=False
                                      )

    def plot_loss(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.history.history['loss'])
        plt.plot(self.history.history['val_loss'])
        plt.title('Model Train vs Validation Loss for BiLSTM')
        plt.ylabel('Loss')
        plt.xlabel('epoch')
        plt.legend(['Train loss', 'Validation loss'], loc='upper right')
        plt.tight_layout()

    def predict(self, X_test, scaler):
        prediction = self.model.predict(X_test, verbose=False)
        prediction = scaler.inverse_transform(prediction)
        return prediction

    def evaluate_predictions(self, predictions, actual):
        errors = predictions - actual
        mse = np.square(errors).mean()
        rmse = np.sqrt(mse)
        mae = np.abs(errors).mean()
        print('BiLSTM:')
        print('Mean Absolute Error: {:.4f}'.format(mae))
        print('Root Mean Square Error: {:.4f}'.format(rmse))


class Gru:

    def __init__(self, input_shape):
        self.history = None
        self.model = Sequential()
        # Input layer
        self.model.add(GRU(units=100, return_sequences=True, input_shape=[input_shape[1], input_shape[2]]))
        self.model.add(Dropout(0.2))

        # Hidden layer
        self.model.add(GRU(units=50))
        self.model.add(Dropout(0.25))

        self.model.add(Dense(units=1))

        # Compile model
        self.model.compile(optimizer='adam', loss='mean_squared_error')

    def info(self):
        self.model.summary()

    def train(self, X_train, y_train):
        self.history = self.model.fit(X_train, y_train,
                                      epochs=50,
                                      batch_size=64,
                                      shuffle=False,
                                      validation_split=0.2,
                                      verbose=False
                                      )

    def plot_loss(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.history.history['loss'])
        plt.plot(self.history.history['val_loss'])
        plt.title('Model Train vs Validation Loss for GRU')
        plt.ylabel('Loss')
        plt.xlabel('epoch')
        plt.legend(['Train loss', 'Validation loss'], loc='upper right')
        plt.tight_layout()

    def predict(self, X_test, scaler):
        prediction = self.model.predict(X_test, verbose=False)
        prediction = scaler.inverse_transform(prediction)
        return prediction

    def evaluate_predictions(self, predictions, actual):
        errors = predictions - actual
        mse = np.square(errors).mean()
        rmse = np.sqrt(mse)
        mae = np.abs(errors).mean()
        print('GRU:')
        print('Mean Absolute Error: {:.4f}'.format(mae))
        print('Root Mean Square Error: {:.4f}'.format(rmse))
