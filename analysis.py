from sklearn.preprocessing import MinMaxScaler
from keras.preprocessing.sequence import TimeseriesGenerator
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import numpy as np 
import tensorflow as tf 

scaler = MinMaxScaler()

def forecast(train):
    train_data = train.iloc[-120:].values
    scaler.fit(train_data)
    train_data = scaler.transform(train_data)
    n_input = 5
    generator = TimeseriesGenerator(train_data, train_data, 
                                    length=n_input, batch_size=1)
    n_features = 1
    model = Sequential()
    model.add(LSTM(100, activation='relu', input_shape=(n_input, n_features)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=3)
    model.fit(generator, epochs=20, callbacks=[callback])
    test_predictions = []
    first_eval_batch = train_data[-n_input:]
    current_batch = first_eval_batch.reshape((1, n_input, n_features))
    for i in range(10): 
        # get the prediction value for the first batch
        current_pred = model.predict(current_batch)[0]
        # append the prediction into the array
        test_predictions.append(current_pred) 
        # use the prediction to update the batch and remove the first value
        current_batch = np.append(current_batch[:,1:,:],[[current_pred]],axis=1)
    true_predictions = scaler.inverse_transform(test_predictions)
    print(true_predictions)
    