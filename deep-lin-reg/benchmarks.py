import numpy as np
#from model import model
import csv
import sys
import os
import itertools
#import theano

from sklearn import linear_model

# Settings
ntrain = int(sys.argv[1])
ntest = 10000
p = 1000 # [10, 100, 1000]

# Training parameters
learning_rate = 0.001
nepochs = 200

data_prefix = os.path.expanduser("~/deep-stat/deep-lin-reg/data/")
output_prefix = "results/noreg_n" + str(ntrain)

def polyFeatures(x, d = 3):
	f_vector = []
	for feature in x:
		f_vector += [feature, feature**2, feature**3]
	return f_vector

def main():
	print("Data dim: %d" % p)
	print("Trainset size: %d" % ntrain)
	#print(theano.config.device)

	output = []

	# Data
	print("Loading data")
	X_train_lin = np.load(data_prefix + "X_train_n" + str(ntrain) + "_lin.npy")
	Y_train_lin = np.load(data_prefix + "Y_train_n" + str(ntrain) + "_lin.npy")
	X_test_lin = np.load(data_prefix + "X_test_n" + str(ntest) + "_lin.npy")
	Y_test_lin = np.load(data_prefix + "Y_test_n" + str(ntest) + "_lin.npy")

	X_train_cub = np.load(data_prefix + "X_train_n" + str(ntrain) + "_cub.npy")
	Y_train_cub = np.load(data_prefix + "Y_train_n" + str(ntrain) + "_cub.npy")
	X_test_cub = np.load(data_prefix + "X_test_n" + str(ntest) + "_cub.npy")
	Y_test_cub = np.load(data_prefix + "Y_test_n" + str(ntest) + "_cub.npy")

	# Compare to linear reg
	benchmarks = []

	# Linear
	print("Linear reg")
	linreg = linear_model.LinearRegression()
	linreg.fit(X_train_lin, Y_train_lin)
	benchmarks.append([np.mean((linreg.predict(X_train_lin) - Y_train_lin) ** 2), np.mean((linreg.predict(X_test_lin) - Y_test_lin) ** 2)])

	# Cubic
	print("Linear reg for cubic")
	cubreg = linear_model.LinearRegression()
	cubreg.fit(X_train_cub, Y_train_cub)
	benchmarks.append([np.mean((cubreg.predict(X_train_cub) - Y_train_cub) ** 2), np.mean((cubreg.predict(X_test_cub) - Y_test_cub) ** 2)])

	# Compare to poly reg (NO interaction terms for simplicity!)
	print("Poly features")
	X_train_poly = []
	X_test_poly = []
	for x in X_train_cub:
		X_train_poly.append(polyFeatures(x))
	X_train_poly = np.array(X_train_poly)

	for x in X_test_cub:
		X_test_poly.append(polyFeatures(x))
	X_test_poly = np.array(X_test_poly)

	# Cubic
	print("Cubic reg")
	cubreg = linear_model.LinearRegression()
	cubreg.fit(X_train_poly, Y_train_cub)
	benchmarks.append([np.mean((cubreg.predict(X_train_poly) - Y_train_cub) ** 2), np.mean((cubreg.predict(X_test_poly) - Y_test_cub) ** 2)])

	# Save
	with open(output_prefix + "_benchmarks.csv", "wb") as f:
		writer = csv.writer(f, delimiter = ",")
		for row in benchmarks:
			writer.writerow(row)





main()