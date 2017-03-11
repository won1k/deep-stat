import numpy as np
from model import model
import csv
import sys
#import theano

from sklearn import linear_model

from train_test import trainAndTest

# Settings
ntrain = int(sys.argv[1]) #[100, 1000, 10000, 100000]
p = int(sys.argv[2]) # [10, 100, 1000]
link_no = int(sys.argv[3])
nsims = 1000

# Hyperparameters
hid_dim = 50

# Training parameters
learning_rate = 0.005
nepochs = 800

links = ["cubic", "sigmoid", "exp"]
link = links[link_no]
output_prefix = "noreg_" + link + "_p" + str(p) + "_n" + str(ntrain) + "_l" + str(learning_rate) + "_T" + str(nepochs)

def link_fn(y, link):
	if link == 'cubic':
		return y**3
	elif link == 'sigmoid':
		return 1/(1 + np.exp(-y))
	else: # exp
		return np.exp(y)

def main():
	print("Data dim: %d" % p)
	print("Trainset size: %d" % ntrain)
	print("Link function: %s" % link)
	#print(theano.config.device)

	output = []

	# Data
	X_train = np.load("data/X_train_p" + str(p) + "_n" + str(ntrain) + ".npy")
	Y_train = np.load("data/Y_train_p" + str(p) + "_n" + str(ntrain) + ".npy")
	Y_train = np.array([link_fn(y, link) for y in Y_train])
	X_test = np.load("data/X_test_p" + str(p) + "_n" + str(ntrain) + ".npy")
	Y_test = np.load("data/Y_test_p" + str(p) + "_n" + str(ntrain) + ".npy")
	Y_test = np.array([link_fn(y, link) for y in Y_test])

	# Compare to linear reg (can do this separately)
	#linreg = linear_model.LinearRegression()
	#linreg.fit(X_train, Y_train)
	#linreg_train_loss = np.mean((linreg.predict(X_train) - Y_train) ** 2)
	#linreg_test_loss = np.mean((linreg.predict(X_test) - Y_test) ** 2)

	# Simulations
	test_preds = []
	train_residuals = []
	test_residuals = []
	with open("results/" + output_prefix + "_metrics.csv", "wb") as f:
		writer = csv.writer(f, delimiter = ",")
		for i in range(nsims):
			print("Simulation: %d" % i)
			#trainAndTest(X_train, Y_train, X_test, Y_test, hid_dim, p, ntrain, learning_rate, nepochs)
			train_mse, test_mse, train_r2, test_r2, train_time, test_time, w_norm, weights, test_pred, train_res, test_res = trainAndTest(X_train, Y_train, X_test, Y_test, hid_dim, p, ntrain, learning_rate, nepochs)
			writer.writerow([train_mse, test_mse, train_r2, test_r2, train_time, test_time, w_norm])
			test_preds.append(test_pred)
			train_residuals.append(train_res)
			test_residuals.append(test_res)

	with open("results/" + output_prefix + "_test_preds.csv", "wb") as f:
		writer = csv.writer(f, delimiter = ",")
		for i in range(nsims):
			writer.writerow(test_preds[i])

	with open("results/" + output_prefix + "_test_res.csv", "wb") as f:
		writer = csv.writer(f, delimiter = ",")
		for i in range(nsims):
			writer.writerow(test_residuals[i])

	with open("results/" + output_prefix + "_train_res.csv", "wb") as f:
		writer = csv.writer(f, delimiter = ",")
		for i in range(nsims):
			writer.writerow(train_residuals[i])

	# Other statistics
	X_train_mean = np.mean(X_train, axis = 0)
	test_norms = np.linalg.norm(X_test - X_train_mean, axis = 1)
	test_residuals = np.array(test_residuals)
	test_mses = np.mean(test_residuals**2, axis = 0)
	test_preds = np.array(test_preds)
	test_vars = np.var(test_preds, axis = 0)
	pred_var = np.array([list(test_vars), list(test_mses), list(test_norms)]).transpose()
	with open("results/" + output_prefix + "_pred_var.csv", "wb") as f:
		writer = csv.writer(f, delimiter = ",")
		for i in range(ntrain):
			writer.writerow(list(pred_var[i,:]))


main()