import math

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense
import akshare as ak
import matplotlib.pyplot as plt
from tensorflow import keras

plt.style.use('fivethirtyeight')

stock_hfq_df = ak.stock_zh_a_hist(symbol="601012", adjust='hfq').iloc[:, :6]
stock_hfq_df.columns = [
    'date',
    'open',
    "close",
    "high",
    'low',
    'volume'
]
stock_hfq_df.index = pd.to_datetime(stock_hfq_df['date'])

print(stock_hfq_df.shape)

# visualise 收盘价
# plt.figure(figsize=(16, 8))
# plt.title("price history")
# plt.plot(stock_hfq_df['close'])
# plt.xlabel('date', fontsize=18)
# plt.ylabel('close price for 隆基股份', fontsize=18)
# plt.show()

data = stock_hfq_df.filter(['close'])
dataset = data.values

# 0.8 train set 0.2 test set
training_data_len = math.ceil(len(dataset) * 0.8)

# data normalizer
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_dataset = scaler.fit_transform(dataset)

# training dataset
train_data = scaled_dataset[0:training_data_len, :]
x_train = []
y_train = []

print(train_data.shape)
for i in range(60, len(train_data)):
    x_train.append(train_data[i-60:i, 0])
    y_train.append(train_data[i, 0])
    if i <= 60:
        print(x_train)
        print(y_train)

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = x_train.reshape((x_train.shape[0], x_train.shape[1], 1))

# LSTM model
# model = Sequential()
# model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
# model.add(LSTM(50, return_sequences=False))
# model.add(Dense(25))
# model.add(Dense(1))
# model.compile(optimizer='adam', loss='mean_squared_error')

#model.fit(x_train, y_train, batch_size=1, epochs=1)
#model.save('LSTM_predictor')

model = load_model('LSTM_predictor')

# test set
test_data = scaled_dataset[training_data_len - 60:, :]
x_test = []
y_test = dataset[training_data_len:, :]

for i in range(60, len(test_data)):
    x_test.append(test_data[i-60:i, 0])

x_test = np.array(x_test)
x_test = x_test.reshape((x_test.shape[0], x_test.shape[1], 1))

# predict
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

# compare actual close price to my predictions, by root mean squared error(RMSE)
rmse = np.sqrt(np.mean(predictions-y_test)**2)

print(rmse)

