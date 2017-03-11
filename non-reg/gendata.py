import numpy as np
import numpy.random as rand
import cPickle

# Settings
ntrain = [1000, 10000, 100000] # , 100000]
data_dim = [10, 100, 1000]
links = ['cubic', 'sigmoid', 'exp']
beta = [rand.normal(size = n) for n in data_dim]
sigma = 10

# Save betas
cPickle.dump(beta, open("data/betas.p", "wb"))

# True function
def true_function(x, link):
	p = len(x)
	# x is data_dim vector

	# beta
	if p == 10:
		w = beta[0]
	elif p == 100:
		w = beta[1]
	else:
		w = beta[2]

	# link
	eps = rand.normal()
	lin_pred = np.dot(w, x) + eps
	if link == 'cubic':
		return lin_pred**3
	elif link == 'sigmoid':
		return 1/(1 + np.exp(-lin_pred))
	else: # exp
		return np.exp(lin_pred)

# Data generation
def gen_data(ntrain, data_dim, link):
	X_train = rand.normal(scale = sigma, size = (ntrain, data_dim))#(ntrain, data_dim,1))
	X_test = rand.normal(scale = sigma, size = (ntrain, data_dim))#(ntest, data_dim,1))
	Y_train = np.array([true_function(x, link) for x in X_train])
	Y_test = np.array([true_function(x, link) for x in X_test])
	return X_train, X_test, Y_train, Y_test

# Generate and save data
for n in ntrain:
	for p in data_dim:
		for link in links:
			X_train, X_test, Y_train, Y_test = gen_data(n, p, link)
			np.save("data/X_train_p" + str(p) + "_n" + str(n) + "_" + link, X_train)
			np.save("data/X_test_p" + str(p) + "_n" + str(n) + "_" + link, X_test)
			np.save("data/Y_train_p" + str(p) + "_n" + str(n) + "_" + link, Y_train)
			np.save("data/Y_test_p" + str(p) + "_n" + str(n) + "_" + link, Y_test)

