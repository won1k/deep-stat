from sklearn import linear_model
import numpy as np
import time

# p = data_dim, n = trainset size
def trainAndTest(X_train, Y_train, X_test, Y_test, hid_dim, p, n, learning_rate = 0.1, nepochs = 100):
	#print("Data dim: %d" % p)
	#print("Trainset size: %d" % n)

	# Define model
	from model import model
	model = model(hid_dim, learning_rate, p)

	# Training
	start_time = time.time()
	model.fit(X_train, Y_train, batch_size = 100, nb_epoch = nepochs, verbose = 0)
	train_time = time.time() - start_time

	# MSE
	start_time = time.time()
	test_preds = model.predict(X_test, verbose = 0).flatten()
	test_time = time.time() - start_time
	train_mse = model.evaluate(X_train, Y_train, batch_size = n, verbose = 0)
	test_mse = model.evaluate(X_test, Y_test, batch_size = n, verbose = 0)

	# R^2
	train_r2 = 1.0 - train_mse / np.var(Y_train)
	test_r2 = 1.0 - test_mse / np.var(Y_test)

	# Residuals
	train_preds = model.predict(X_train, verbose = 0).flatten()
	train_res = Y_train - train_preds
	test_res = Y_test - test_preds

	# Weights
	weights = model.get_weights()
	w_norm = sum([np.linalg.norm(x) for x in weights])

	#print("Mean squared error on train: %.2f"
	#      % np.mean((linreg.predict(X_train) - Y_train) ** 2))
	#print("Mean squared error on test: %.2f"
	#      % np.mean((linreg.predict(X_test) - Y_test) ** 2))

	# Return
	return train_mse, test_mse, train_r2, test_r2, train_time, test_time, w_norm, weights, test_preds, train_res, test_res