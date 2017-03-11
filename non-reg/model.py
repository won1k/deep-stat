import keras
import numpy as np

from keras.models import Model, Sequential
from keras.optimizers import SGD, Adam, RMSprop, Adagrad
from keras.regularizers import l1
from keras.layers import Input, Dense, Dropout, Flatten, Embedding, Reshape, Activation, Merge
from keras.layers.convolutional import Convolution1D, Convolution2D, MaxPooling1D, MaxPooling2D

# Hyperparameters
#learning_rate = 0.1
#nepochs = 10
#data_dim = 10

#hid_dim = 50

# Model (1-layer MLP)
def model(hid_dim, learning_rate, data_dim):
	inputs = Input(shape=(data_dim,), name='input', dtype='float32')

	# Dense layers (no dropout for now)
	h = Dense(hid_dim, activation='relu', name='hidden')(inputs)
	output = Dense(1, activation='linear', name='output')(h)
	#z = Dropout(0.5)(Dense(hid_dim, activation='relu')(conv3))

	# Model and loss
	model = Model(input=inputs, output=output)
	opt = Adam(lr=learning_rate)#, decay = learning_rate/100)
	model.compile(loss = 'mse', optimizer = opt)

	return model