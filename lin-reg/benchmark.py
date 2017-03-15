import numpy as np
import csv
import sys
import os
import time
import gc

from sklearn import linear_model
from sklearn import metrics
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from pyearth import Earth

# Settings
ntrain = int(sys.argv[1]) #[100, 1000, 10000, 100000]
p = int(sys.argv[2]) # [10, 100, 1000]
gc.enable()

# Hyperparameters
hid_dim = 50

# Training parameters
learning_rate = 0.005
nepochs = 800

data_prefix = os.path.expanduser("~/deep-stat/data/")
output_file = "results/benchmarks" + "_p" + str(p) + "_n" + str(ntrain) + ".csv"

def main():
	if ntrain < 50*p:
		return

	print("Data dim: %d" % p)
	print("Trainset size: %d" % ntrain)
	#print(theano.config.device)

	output = []

	# Data
	X_train = np.load(data_prefix + "X_train_p" + str(p) + "_n" + str(ntrain) + ".npy")
	Y_train = np.load(data_prefix + "Y_train_p" + str(p) + "_n" + str(ntrain) + ".npy")
	X_test = np.load(data_prefix + "X_test_p" + str(p) + "_n" + str(ntrain) + ".npy")
	Y_test = np.load(data_prefix + "Y_test_p" + str(p) + "_n" + str(ntrain) + ".npy")

	# Linear regression
	print("LinearRegression")
	linreg = linear_model.LinearRegression()
	start_time = time.time()
	linreg.fit(X_train, Y_train)
	linreg_train_time = time.time() - start_time
	linreg_train_mse = np.mean((linreg.predict(X_train) - Y_train) ** 2)
	linreg_test_mse = np.mean((linreg.predict(X_test) - Y_test) ** 2)
	linreg_train_r2 = linreg.score(X_train, Y_train)
	linreg_test_r2 = linreg.score(X_test, Y_test)
	output.append(["LinearRegression", 0, linreg_train_mse, linreg_test_mse, linreg_train_r2, linreg_test_r2, linreg_train_time])
	del linreg
	gc.collect()
	del gc.garbage[:]

	# Splines
	print("MARS")
	spline = Earth(enable_pruning = True)
	start_time = time.time()
	spline.fit(X_train, Y_train)
	spline_train_time = time.time() - start_time
	spline_train_mse = metrics.mean_squared_error(Y_train, spline.predict(X_train))
	spline_test_mse = metrics.mean_squared_error(Y_test, spline.predict(X_test))
	spline_train_r2 = metrics.r2_score(Y_train, spline.predict(X_train))
	spline_test_r2 = metrics.r2_score(Y_test, spline.predict(X_test))
	output.append(["MARS", 0, spline_train_mse, spline_test_mse, spline_train_r2, spline_test_r2, spline_train_time])
	del spline
	gc.collect()
	del gc.garbage[:]


	# Poly. regression
	print("Polynomial")
	polyreg = Pipeline([('poly', PolynomialFeatures(degree=3)),
	                   ('linear', linear_model.LinearRegression(fit_intercept=False))])
	start_time = time.time()
	polyreg.fit(X_train, Y_train)
	polyreg_train_time = time.time() - start_time
	polyreg_train_mse = np.mean((polyreg.predict(X_train) - Y_train) ** 2)
	polyreg_test_mse = np.mean((polyreg.predict(X_test) - Y_test) ** 2)
	polyreg_train_r2 = polyreg.score(X_train, Y_train)
	polyreg_test_r2 = polyreg.score(X_test, Y_test)
	output.append(["Polynomial", 0, polyreg_train_mse, polyreg_test_mse, polyreg_train_r2, polyreg_test_r2, polyreg_train_time])
	del polyreg
	gc.collect()
	del gc.garbage[:]

	# Linear + L1
	print("Lasso")
	for lamb in [0.1, 1.0, 10.0]:
		l1reg = linear_model.Lasso(alpha = lamb)
		start_time = time.time()
		l1reg.fit(X_train, Y_train)
		l1reg_train_time = time.time() - start_time
		l1reg_train_mse = np.mean((l1reg.predict(X_train) - Y_train) ** 2)
		l1reg_test_mse = np.mean((l1reg.predict(X_test) - Y_test) ** 2)
		l1reg_train_r2 = l1reg.score(X_train, Y_train)
		l1reg_test_r2 = l1reg.score(X_test, Y_test)
		output.append(["Lasso", lamb, l1reg_train_mse, l1reg_test_mse, l1reg_train_r2, l1reg_test_r2, l1reg_train_time])
		del l1reg
		gc.collect()
		del gc.garbage[:]

	# Linear + L2
	print("Ridge")
	for lamb in [0.1, 1.0, 10.0]:
		l2reg = linear_model.Ridge(alpha = lamb)
		start_time = time.time()
		l2reg.fit(X_train, Y_train)
		l2reg_train_time = time.time() - start_time
		l2reg_train_mse = np.mean((l2reg.predict(X_train) - Y_train) ** 2)
		l2reg_test_mse = np.mean((l2reg.predict(X_test) - Y_test) ** 2)
		l2reg_train_r2 = l2reg.score(X_train, Y_train)
		l2reg_test_r2 = l2reg.score(X_test, Y_test)
		output.append(["Ridge", lamb, l2reg_train_mse, l2reg_test_mse, l2reg_train_r2, l2reg_test_r2, l2reg_train_time])
		del l2reg
		gc.collect()
		del gc.garbage[:]

	# Poly. + L1
	print("PolyLasso")
	for lamb in [0.1, 1.0, 10.0]:
		polyreg = Pipeline([('poly', PolynomialFeatures(degree=3)),
	                   ('lasso', linear_model.Lasso(fit_intercept=False, alpha = lamb))])
		start_time = time.time()
		polyreg.fit(X_train, Y_train)
		polyreg_train_time = time.time() - start_time
		polyreg_train_mse = np.mean((polyreg.predict(X_train) - Y_train) ** 2)
		polyreg_test_mse = np.mean((polyreg.predict(X_test) - Y_test) ** 2)
		polyreg_train_r2 = polyreg.score(X_train, Y_train)
		polyreg_test_r2 = polyreg.score(X_test, Y_test)
		output.append(["PolyLasso", lamb, polyreg_train_mse, polyreg_test_mse, polyreg_train_r2, polyreg_test_r2, polyreg_train_time])
		del polyreg
		gc.collect()
		del gc.garbage[:]

	# Poly. + L2
	print("PolyRidge")
	for lamb in [0.1, 1.0, 10.0]:
		polyreg = Pipeline([('poly', PolynomialFeatures(degree=3)),
	                   ('ridge', linear_model.Ridge(fit_intercept=False, alpha = lamb))])
		start_time = time.time()
		polyreg.fit(X_train, Y_train)
		polyreg_train_time = time.time() - start_time
		polyreg_train_mse = np.mean((polyreg.predict(X_train) - Y_train) ** 2)
		polyreg_test_mse = np.mean((polyreg.predict(X_test) - Y_test) ** 2)
		polyreg_train_r2 = polyreg.score(X_train, Y_train)
		polyreg_test_r2 = polyreg.score(X_test, Y_test)
		output.append(["PolyRidge", lamb, polyreg_train_mse, polyreg_test_mse, polyreg_train_r2, polyreg_test_r2, polyreg_train_time])
		del polyreg
		gc.collect()
		del gc.garbage[:]

	# Save output
	with open(output_file, "wb") as f:
		writer = csv.writer(f, delimiter = ",")
		for row in output:
			writer.writerow(row)

main()