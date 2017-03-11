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
nsims = 1000

# Hyperparameters
hid_dim = 50

# Training parameters
learning_rate = 0.005
nepochs = 800

data_prefix = "~/deep-stat/data/"
output_prefix = "results/noreg_p" + str(p) + "_n" + str(ntrain) + "_l" + str(learning_rate) + "_T" + str(nepochs)

def main():
	print("Data dim: %d" % p)
	print("Trainset size: %d" % ntrain)
	#print(theano.config.device)

	output = []

	# Data
	X_train = np.load(data_prefix + "X_train_p" + str(p) + "_n" + str(ntrain) + ".npy")
	Y_train = np.load(data_prefix + "Y_train_p" + str(p) + "_n" + str(ntrain) + ".npy")
	X_test = np.load(data_prefix + "X_test_p" + str(p) + "_n" + str(ntrain) + ".npy")
	Y_test = np.load(data_prefix + "Y_test_p" + str(p) + "_n" + str(ntrain) + ".npy")

	# Compare to linear reg (can do this separately)
	#linreg = linear_model.LinearRegression()
	#linreg.fit(X_train, Y_train)
	#linreg_train_loss = np.mean((linreg.predict(X_train) - Y_train) ** 2)
	#linreg_test_loss = np.mean((linreg.predict(X_test) - Y_test) ** 2)

	# Simulations
	#test_preds = []
	train_residuals = []
	test_residuals = []
	with open(output_prefix + "_metrics.csv", "wb") as f:
		writer = csv.writer(f, delimiter = ",")
		for i in range(nsims):
			print("Simulation: %d" % i)
			#trainAndTest(X_train, Y_train, X_test, Y_test, hid_dim, p, ntrain, learning_rate, nepochs)
			# no w_norm, weights for now
			train_mse, test_mse, train_r2, test_r2, train_time, test_time, train_res, test_res = trainAndTest(X_train, Y_train, X_test, Y_test, hid_dim, p, ntrain, learning_rate, nepochs)
			writer.writerow([train_mse, test_mse, train_r2, test_r2, train_time, test_time, w_norm])
			#test_preds.append(test_pred)
			train_residuals.append(train_res)
			test_residuals.append(test_res)

	#with open(output_prefix + "_test_preds.csv", "wb") as f:
	#	writer = csv.writer(f, delimiter = ",")
	#	for i in range(nsims):
	#		writer.writerow(test_preds[i])

	with open(output_prefix + "_test_res.csv", "wb") as f:
		writer = csv.writer(f, delimiter = ",")
		for i in range(nsims):
			writer.writerow(test_residuals[i])

	with open(output_prefix + "_train_res.csv", "wb") as f:
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
	with open(output_prefix + "_pred_var.csv", "wb") as f:
		writer = csv.writer(f, delimiter = ",")
		for i in range(ntrain):
			writer.writerow(list(pred_var[i,:]))


main()