import numpy as np
import numpy.random as rand
import cPickle

# Settings
ntrain = [10**i for i in range(3,7)]
ntest = 10000
data_dim = 1000
beta = list(rand.uniform(0.5, 1, size = 10)) + list(rand.uniform(0.1, 0.3, size = 40)) + list(rand.uniform(-1,-0.5, size = 10)) + list(rand.uniform(-0.3, -0.1, size = 40)) + [0]*900

# Save betas
cPickle.dump(beta, open("data/betas.p", "wb"))

# True function (start with easy linear)
def true_function(x, type):
	eps = rand.normal()
	if type == "linear":
		return np.dot(beta, x) + eps
	else:
		return (np.dot(beta, x) + eps)**3

# Data generation
def gen_data(n, data_dim, type):
	X = rand.normal(size = (n, data_dim))#(ntrain, data_dim,1))
	Y = np.array([true_function(x, type) for x in X])
	return X, Y

# Generate and save data (linear)
for n in ntrain:
	print n
	X_train, Y_train = gen_data(n, data_dim, "linear")
	np.save("data/X_train_n" + str(n) + "_lin", X_train)
	np.save("data/Y_train_n" + str(n) + "_lin", Y_train)

X_test, Y_test = gen_data(ntest, data_dim, "linear")
np.save("data/X_test_n" + str(ntest) + "_lin", X_test)
np.save("data/Y_test_n" + str(ntest) + "_lin", Y_test)

# Generate and save data (nonlinear)
for n in ntrain:
	print n
	X_train, Y_train = gen_data(n, data_dim, "cubic")
	np.save("data/X_train_n" + str(n) + "_cub", X_train)
	np.save("data/Y_train_n" + str(n) + "_cub", Y_train)

X_test, Y_test = gen_data(ntest, data_dim, "cubic")
np.save("data/X_test_n" + str(ntest) + "_cub", X_test)
np.save("data/Y_test_n" + str(ntest) + "_cub", Y_test)
