import numpy as np
from model import model
import csv

from sklearn import linear_model

from train_test import trainAndTest


# Settings
ntrain = 1000 #[100, 1000, 10000, 100000]
p = 10 # [10, 100, 1000]
nsims = 1000

# Hyperparameters
hid_dim = 50

# Training parameters
learning_rate = 0.005
nepochs = 800

output_file = "noreg_p" + str(p) + "_n" + str(ntrain) + "_l" + str(learning_rate) + "_T" + str(nepochs) + ".csv"

def main():
	output = []

	# Data
	X_train = np.load("data/X_train_p" + str(p) + "_n" + str(ntrain) + ".npy")
	Y_train = np.load("data/Y_train_p" + str(p) + "_n" + str(ntrain) + ".npy")
	X_test = np.load("data/X_test_p" + str(p) + "_n" + str(ntrain) + ".npy")
	Y_test = np.load("data/Y_test_p" + str(p) + "_n" + str(ntrain) + ".npy")

	# Compare to linear reg (can do this separately)
	#linreg = linear_model.LinearRegression()
	#linreg.fit(X_train, Y_train)
	#linreg_train_loss = np.mean((linreg.predict(X_train) - Y_train) ** 2)
	#linreg_test_loss = np.mean((linreg.predict(X_test) - Y_test) ** 2)

	with open(output_file, "wb") as f:
		writer = csv.writer(f, delimiter = ",")
		for i in range(nsims):
			print("Simulation: %d" % i)
			#trainAndTest(X_train, Y_train, X_test, Y_test, hid_dim, p, ntrain, learning_rate, nepochs)
			writer.writerow(list(trainAndTest(X_train, Y_train, X_test, Y_test, hid_dim, p, ntrain, learning_rate, nepochs)))

main()