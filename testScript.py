import splitData
import keras
from keras.layers.core import Dense, Activation, Dropout
from keras.models import Sequential
from keras import regularizers
import time
import numpy as np

X_train, X_crossVal, X_test, y_train, y_crossVal, y_test = splitData.splitData('dinoData/allData.csv')

inputSize = 47 #np.shape(X_train)[1]
outputSize = 803 #np.shape(y_train)[1]

print(outputSize)

# reg = keras.layers.ActivityRegularization(l1=1.0, l2=1.0)

model = Sequential([
    Dense(input_dim = 47, output_dim = 47,use_bias=True,activity_regularizer=regularizers.l1(0)),
    Activation('sigmoid'),
    Dense(425,use_bias=True,activity_regularizer=regularizers.l1(0)),
    Activation('sigmoid'),
    Dense(803,use_bias=True,activity_regularizer=regularizers.l1(0)),
    Activation('sigmoid'),
])

opt = keras.optimizers.Adagrad(lr=0.01, epsilon=None, decay=0.0)

model.compile(loss='mean_squared_logarithmic_error', optimizer=opt, metrics=['acc'])

start = time.time()
model.fit(
    X_train,
    y_train,
    batch_size=1,
    epochs=10000,
    validation_data=(X_crossVal,y_crossVal))
print('training time : ', time.time() - start)