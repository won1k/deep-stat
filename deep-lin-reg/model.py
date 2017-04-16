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

# Model (N-layer MLP)
def model_unif(hid_dim, learning_rate, data_dim, num_layers):
	inputs = Input(shape=(data_dim,), name='input', dtype='float32')

	# Dense layers (no dropout for now)
	layers = []
	for i in range(num_layers):
		if i == 0:
			layers.append(Dense(hid_dim, activation='relu', name='hidden'+str(i))(inputs))
		else:
			layers.append(Dense(hid_dim, activation='relu', name='hidden'+str(i))(layers[i-1]))
	# Output
	output = Dense(1, activation='linear', name='output')(layers[num_layers-1])
	#z = Dropout(0.5)(Dense(hid_dim, activation='relu')(conv3))

	# Model and loss
	model = Model(input=inputs, output=output)
	opt = Adam(lr=learning_rate)#, decay = learning_rate/100)
	model.compile(loss = 'mse', optimizer = opt)

	return model

def model_pyr(hid_dim, learning_rate, data_dim, num_layers):
	inputs = Input(shape=(data_dim,), name='input', dtype='float32')

	# Dense layers (no dropout for now)
	layers = []
	for i in range(num_layers):
		if i == 0:
			layers.append(Dense(5*hid_dim, activation='relu', name='hidden'+str(i))(inputs))
		elif i == num_layers-1:
			layers.append(Dense(hid_dim/5, activation='relu', name='hidden'+str(i))(layers[i-1]))
		else:
			layers.append(Dense(hid_dim, activation='relu', name='hidden'+str(i))(layers[i-1]))
	# Output
	output = Dense(1, activation='linear', name='output')(layers[num_layers-1])
	#z = Dropout(0.5)(Dense(hid_dim, activation='relu')(conv3))

	# Model and loss
	model = Model(input=inputs, output=output)
	opt = Adam(lr=learning_rate)#, decay = learning_rate/100)
	model.compile(loss = 'mse', optimizer = opt)

	return model

# Shallow vs. deep (p = 1000)
def model_shallow(learning_rate, data_dim):
	hid_dim = 100
	inputs = Input(shape=(data_dim,), name='input', dtype='float32')

	# Dense layers (no dropout for now)
	hidden = Dense(hid_dim, activation='relu', name='hidden')(inputs)
	output = Dense(1, activation='linear', name='output')(hidden)
	#z = Dropout(0.5)(Dense(hid_dim, activation='relu')(conv3))

	# Model and loss
	model = Model(input=inputs, output=output)
	opt = Adam(lr=learning_rate)#, decay = learning_rate/100)
	model.compile(loss = 'mse', optimizer = opt)

	return model

def model_deep(learning_rate, data_dim):
	hid_dim = 50
	inputs = Input(shape=(data_dim,), name='input', dtype='float32')

	# Dense layers (no dropout for now)
	layers = []
	for i in range(20):
		if i == 0:
			layers.append(Dense(hid_dim, activation='relu', name='hidden'+str(i))(inputs))
		else:
			layers.append(Dense(hid_dim, activation='relu', name='hidden'+str(i))(layers[i-1]))
	# Output
	output = Dense(1, activation='linear', name='output')(layers[i-1])
	#z = Dropout(0.5)(Dense(hid_dim, activation='relu')(conv3))

	# Model and loss
	model = Model(input=inputs, output=output)
	opt = Adam(lr=learning_rate)#, decay = learning_rate/100)
	model.compile(loss = 'mse', optimizer = opt)

	return model



