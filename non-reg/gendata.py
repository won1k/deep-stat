import numpy as np
import numpy.random as rand

# Settings
ntrain = [1000, 10000, 100000]
data_dim = [10, 100, 1000]
beta = [rand.normal(size = n) for n in data_dim]
sigma = 10

# Save betas
cPickle.dump(beta, open("data/betas.p", "wb"))

# True function (start with easy linear)
def true_function(x):
	p = len(x)
	# x is data_dim vector

	if p == 10:
		w = beta[0]
	elif p == 100:
		w = beta[1]
	else:
		w = beta[2]
	
	eps = rand.normal()
	return np.dot(w, x) + eps

# Data generation
def gen_data(ntrain, ntest, data_dim):
	X_train = rand.normal(scale = sigma, size = (ntrain, data_dim))#(ntrain, data_dim,1))
	X_test = rand.normal(scale = sigma, size = (ntest, data_dim))#(ntest, data_dim,1))
	Y_train = np.array([true_function(x) for x in X_train])
	Y_test = np.array([true_function(x) for x in X_test])
	return X_train, X_test, Y_train, Y_test

# Generate and save data
for n in ntrain:
	for p in data_dim:
		X_train, X_test, Y_train, Y_test = gen_data(n, n, p)
		np.save("data/X_train_p" + str(p) + "_n" + str(n), X_train)
		np.save("data/X_test_p" + str(p) + "_n" + str(n), X_test)
		np.save("data/Y_train_p" + str(p) + "_n" + str(n), Y_train)
		np.save("data/Y_test_p" + str(p) + "_n" + str(n), Y_test)

