
from sklearn import linear_model
import numpy as np

# p = data_dim, n = trainset size
def trainAndTest(X_train, Y_train, X_test, Y_test, hid_dim, p, n, learning_rate = 0.1, nepochs = 100):
	#print("Data dim: %d" % p)
	#print("Trainset size: %d" % n)

	# Define model
	from model import model
	model = model(hid_dim, learning_rate, p)

	# Training
	model.fit(X_train, Y_train, batch_size = 100, nb_epoch = nepochs)

	# Testing
	#print "\n"

	# Metrics
	train_loss = model.evaluate(X_train, Y_train, batch_size = n)
	test_loss = model.evaluate(X_test, Y_test, batch_size = n/10)

	#print("Mean squared error on train: %.2f"
	#      % np.mean((linreg.predict(X_train) - Y_train) ** 2))
	#print("Mean squared error on test: %.2f"
	#      % np.mean((linreg.predict(X_test) - Y_test) ** 2))

	# Return
	return train_loss, test_loss #, linreg_train_loss, linreg_test_loss