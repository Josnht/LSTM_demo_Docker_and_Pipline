# -*- coding: utf-8 -*-
"""LSTM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14tlhpiSjNSZ4N190UGTKut-mkOvlyKDB

# Import Libaries and file csv
Import Libaries
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd 
from pandas import Series
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline
from sklearn.model_selection import GridSearchCV 
from keras.wrappers.scikit_learn import KerasRegressor
from keras.models import Sequential
from keras.layers import Dense,LSTM
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
import sklearn.metrics as metrics
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing
import math
import os.path
from os import path
from pylab import rcParams
from random import randrange
from pandas import Series
from matplotlib import pyplot
import pickle
import os
import joblib


dulieu = "./data.csv"
data = pd.read_csv(dulieu)
data

"""#Prepare the Data"""

data.Date = pd.to_datetime(data.Date, dayfirst = False)
data.set_index("Date", inplace = True)

data = data[['Close']] # Just use the close price
data

data.index

data.describe()

data.info()

data.count()

"""Display Close Price into 2 plot below"""

import matplotlib.ticker as ticker

data['Close'].plot(figsize=(17, 8))

plt.ylabel('Price', fontsize=16)
plt.xlabel('Date', fontsize=16)

plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)

plt.show()

"""#Test-Train split
We need to split the data into two set of data: training data and testing data
Using eighty percent of data for training and the remaining twenty percent for testing. This 80/20 split is the most common approach 

"""

size_train = int(len(data)*0.80) 
train_data = data[0:size_train] 
test_data = data[size_train:]

pd_train = pd.DataFrame(train_data['Close']) 
pd_test = pd.DataFrame(test_data['Close'])
print("Tập train:")
print(pd_train.describe())
print("") 
print("Tập test:")
print(pd_test.describe())

"""Display the training-set and the testing set as plot"""

fig, ax = plt.subplots(figsize=(18,8)) # 4.5, 2
sns.lineplot(x = data.index[:size_train], y = data['Close'][:size_train], color = 'red')
sns.lineplot(x = data.index[size_train:], y = data['Close'][size_train:], color = 'blue')
ax.set_title('Train & Test data', fontsize = 20, loc='center', fontdict=dict(weight='bold'))
ax.set_xlabel('Date', fontsize = 16, fontdict=dict(weight='bold'))
ax.set_ylabel('Price [Close] ($)', fontsize = 16, fontdict=dict(weight='bold'))
plt.tick_params(axis='y', which='major', labelsize=16)
plt.tick_params(axis='x', which='major', labelsize=16)
plt.legend(loc='upper right' ,labels = ('train', 'test'))
plt.show()

"""Create x_train, y_train, x_test, y_test"""

def create_dataset(dataset, time_step=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-time_step-1):
        a = dataset[i:(i+time_step)]
        dataX.append(a)
        dataY.append(dataset[i + time_step])
    return np.array(dataX), np.array(dataY)

time_step = 30
X_train, y_train = create_dataset(train_data['Close'], time_step)
X_test, y_test = create_dataset(test_data['Close'], time_step)

"""Create a copy variables for review the model"""

X_train_copy = X_train
y_train_copy = y_train
X_test_copy = X_test
y_test_copy = y_test

"""Normalize data"""

scaler_test = MinMaxScaler(feature_range=(0,1))
scaler_train = MinMaxScaler(feature_range=(0,1))

X_train = scaler_train.fit_transform(X_train)
X_test  = scaler_test.fit_transform(X_test)
y_train = scaler_train.fit_transform(y_train.reshape(-1,1))
y_test = scaler_test.fit_transform(y_test.reshape(-1,1))

"""#Building the model

####Long Short Term Memory Model
"""

hidden_nodes = 20

model_LSTM = Sequential()
model_LSTM.add(LSTM(hidden_nodes, activation="relu", recurrent_dropout=0.1, return_sequences = True, input_shape = (X_train.shape[1],1)))
model_LSTM.add(LSTM(hidden_nodes, return_sequences =False))
model_LSTM.add(Dense(20))
model_LSTM.add(Dense(1))
model_LSTM.compile(optimizer = 'adam', loss = 'mean_squared_error')

model_LSTM.fit(X_train,y_train, epochs= 100, batch_size= 26)

"""#Predict on test data and visualize """

y_pred_test_LSTM = model_LSTM.predict(X_test)

y_pred_test_LSTM = scaler_test.inverse_transform(y_pred_test_LSTM.reshape(-1,1))

plt.figure(figsize=(18,8))
plt.plot(data.index[2815:], y_test_copy, color="red", label=f"Real Value (test data)")
plt.plot(data.index[2815:], y_pred_test_LSTM, color="blue", label = 'LSTM Prediction')
plt.title('Prediction VN-Index on test data', fontsize=18)
plt.xlabel('Date')
plt.ylabel("Prices")
plt.legend()
plt.savefig('Prediction_VN-Index_on_test_data.png')

"""#Visualize train data"""

y_pred_train_LSTM = model_LSTM.predict(X_train)

y_pred_train_LSTM = scaler_train.inverse_transform(y_pred_train_LSTM.reshape(-1,1))

plt.figure(figsize=(18,8))
plt.plot(data.index[31:2784],y_train_copy, color="red", label = 'Real Prices(train data)')
plt.plot(data.index[31:2784],y_pred_train_LSTM, color="blue", label = 'LSTM Prediction')
plt.title('Prediction VN-Index on train data', fontsize=18)
plt.tick_params(axis='y', which='major', labelsize=10)
plt.tick_params(axis='x', which='major', labelsize=10)
plt.legend()
plt.savefig('Prediction_VN-Index_on_train_data.png')


"""#Review model"""

print("TẬP TEST                           TẬP TRAIN")
print("LSTM")
print("MSE  : " + str(mean_squared_error(y_test_copy, y_pred_test_LSTM))                
+"  ||  "  + str(mean_squared_error(y_train_copy, y_pred_train_LSTM)))
print("MAE  : " + str(mean_absolute_error(y_test_copy, y_pred_test_LSTM))               
+"  ||  " + str(mean_absolute_error(y_train_copy, y_pred_train_LSTM)))
print("MAPE : " + str(mean_absolute_percentage_error(y_test_copy, y_pred_test_LSTM)*100)
+" ||  "  + str(mean_absolute_percentage_error(y_train_copy, y_pred_train_LSTM)*100))
print("R2   : " + str(round(metrics.r2_score(y_test_copy, y_pred_test_LSTM), 15))
+"  ||  "  + str(round(metrics.r2_score(y_train_copy, y_pred_train_LSTM), 15)))

"""#Predicting index in next 30 days"""

x_input=test_data[667:].values.reshape(1, -1)
x_input.shape

temp_input=list(x_input)
temp_input=temp_input[0].tolist()

lst_output=[]
n_steps=30
i=0
while(i<30):
    
    if(len(temp_input)>30):
        #(temp_input)
        x_input=np.array(temp_input[1:])
        x_input=x_input.reshape(1,-1)
        x_input = x_input.reshape((1, n_steps, 1))
        #(x_input)
        yhat = model_LSTM.predict(x_input, verbose=0)
        temp_input.extend(yhat[0].tolist())
        temp_input=temp_input[1:]
        #(temp_input)
        lst_output.extend(yhat.tolist())
        i=i+1
    else:
        x_input = x_input.reshape((1, n_steps,1))
        yhat = model_LSTM.predict(x_input, verbose=0)
        temp_input.extend(yhat[0].tolist())
        lst_output.extend(yhat.tolist())
        i=i+1

Prediction_LSTM = scaler_test.inverse_transform(lst_output)

plt.figure(figsize= (18, 8))
plt.plot(Prediction_LSTM,color='blue', label ="LSTM")
plt.title('Prediction VN-Index in next 30days future', fontsize=18)
plt.legend()
plt.savefig('Prediction_VN-Index_on_next_30days.png')


