#!/usr/bin/env python

import splitData
import keras
from keras.layers.core import Dense, Activation, Dropout
from keras.models import Sequential
from keras import regularizers
import time
import numpy as np
import os

X_train, X_crossVal, X_test, y_train, y_crossVal, y_test = splitData.splitData('data/allData.csv')

assert not (np.any(np.isnan(X_train))), 'NaN in training data'
assert not (np.any(np.isnan(y_train))), 'NaN in training labels'
assert not (np.any(np.isnan(X_crossVal))), 'NaN in cross validation data'
assert not (np.any(np.isnan(y_crossVal))), 'NaN in cross validation labels'
assert not (np.any(np.isnan(X_test))), 'NaN in test data'
assert not (np.any(np.isnan(y_test))), 'NaN in test labels'

inputSize = np.shape(X_train)[1]
outputSize = np.shape(y_train)[1]

print('Number of species: ', outputSize)
print('Number of training examples: ', np.shape(y_train)[0])

if os.path.isfile('dinoModel.h5'):
    model = keras.models.load_model('dinoModel.h5')
else:
    # reg = keras.layers.ActivityRegularization(l1=1.0, l2=1.0)
    
    model = Sequential([
        Dense(input_dim=inputSize,output_dim=inputSize,use_bias=True,activity_regularizer=regularizers.l1(0)),
        Activation('sigmoid'),
        Dense(inputSize,use_bias=True,activity_regularizer=regularizers.l1(0)),
        Activation('sigmoid'),
        Dense(outputSize,use_bias=True,activity_regularizer=regularizers.l1(0)),
        Activation('sigmoid'),
    ])
    
    opt = keras.optimizers.Adagrad(lr=.01, epsilon=None, decay=0.001)

model.compile(loss='mean_squared_logarithmic_error', optimizer=opt, metrics=['acc'])

start = time.time()
model.fit(
    X_train,
    y_train,
    batch_size=1,
    epochs=10000,
    validation_data=(X_crossVal,y_crossVal))
print('training time : ', time.time() - start)

model.save_weights('dinoModel.h5')
