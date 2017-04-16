from sklearn import linear_model
import numpy as np
import time

# p = data_dim, n = trainset size
def trainAndTest(X_train, Y_train, X_test, Y_test, hid_dim, p, n, L, learning_rate = 0.0001, nepochs = 100):
	#print("Data dim: %d" % p)
	#print("Trainset size: %d" % n)

	# Define model
	from model import *
	s = model_shallow(learning_rate, p)
	d = model_deep(learning_rate, p)
	u = model_unif(hid_dim, learning_rate, p, L)
	p = model_pyr(hid_dim, learning_rate, p, L)
	models = [s,d,u,p]
	model_names = ["shallow","deep","unif","pyr"]

	# Training
	train_time = []
	for model in models:
		start_time = time.time()
		model.fit(X_train, Y_train, batch_size = 100, nb_epoch = nepochs, verbose = 1)
		train_time.append(time.time() - start_time)

	# MSE / R2
	#start_time = time.time()
	#test_preds = model.predict(X_test, verbose = 0).flatten()
	#test_time = time.time() - start_time
	train_mse = []
	train_r2 = []
	test_mse = []
	test_r2 = []
	for model in models:
		train_mse.append(model.evaluate(X_train, Y_train, batch_size = n, verbose = 0))
		train_r2.append(1.0 - train_mse/np.var(Y_train))
		test_mse.append(model.evaluate(X_test, Y_test, batch_size = n, verbose = 0))
		test_r2.append(1.0 - test_mse / np.var(Y_test))

	# Residuals
	# train_preds = model.predict(X_train, verbose = 0).flatten()
	# train_res = Y_train - train_preds
	# test_res = Y_test - test_preds

	# Weights
	#weights = model.get_weights()
	#w_norm = sum([np.linalg.norm(x) for x in weights])

	#print("Mean squared error on train: %.2f"
	#      % np.mean((linreg.predict(X_train) - Y_train) ** 2))
	#print("Mean squared error on test: %.2f"
	#      % np.mean((linreg.predict(X_test) - Y_test) ** 2))

	# Return
	return model_names, train_mse, test_mse, train_r2, test_r2, train_time#, test_time, train_res, test_res, test_preds#, w_norm, weights