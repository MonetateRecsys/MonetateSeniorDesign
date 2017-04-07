from numpy import asmatrix, asarray, ones, zeros, mean, sum, arange, prod, dot, loadtxt
from numpy.random import random, randint
import pickle

MISSING_VAL = -1 # This denotes values which don't have data

def infer_hidden_node(E, I, theta, sample_hidden):
	theta_T, theta_E = theta

	# Calculate unnormalized probability associated with hidden node being 0
	theta_E_wide = asarray(ones([E.shape[0],1]) * asmatrix(theta_E[:,0])) 
	p_vis_0 = I * (theta_E_wide * E + (1-theta_E_wide) * (1-E)) + (I==0)*1	
	prob_0_unnorm = (1-theta_T) * prod(p_vis_0, 1)

	# Calculate unnormalized probability associated with hidden node being 1
	theta_E_wide = asarray(ones([E.shape[0],1]) * asmatrix(theta_E[:,1]))
	p_vis_1 = I * (theta_E_wide * E + (1-theta_E_wide) * (1-E)) + (I==0)*1	
	prob_1_unnorm = theta_T * prod(p_vis_1, 1)

	# Probability of hidden node being 1
	hidden = prob_1_unnorm/(prob_0_unnorm + prob_1_unnorm)

	if sample_hidden:
		# Set hidden node to 0 or 1 instead of probability
		hidden = (hidden > random(hidden.shape)) * 1
	
	return hidden

def simulate(theta, n_samples):
	theta_T, theta_E = theta
	T = (theta_T > random(n_samples))

	E = (asmatrix(1-T).transpose() * theta_E[:,0] > random([n_samples,theta_E.shape[0]])) \
	+ (asmatrix(T).transpose() * theta_E[:,1] > random([n_samples, theta_E.shape[0]]))

	E = asarray(E*1)

	return T, E

def compute_theta(T, E):
	theta_T = mean(T)
	theta_E = zeros([E.shape[1], 2])

	for e in range(E.shape[1]):
		E_col = E[:,e]
		ix = E_col != MISSING_VAL	# Evidence row indices 
		theta_E[e,0] = sum(E_col[ix] * (1-T[ix]))/float(sum(1-T[ix]))	# Average of E when T = 0
		theta_E[e,1] = sum(E_col[ix] * T[ix])/float(sum(T[ix]))			# Average of E when T = 1

	return [theta_T, theta_E]

def print_theta(theta):
	theta_T, theta_E = theta
	
	print("T\t0: %f\t1:%f" % (1-theta_T, theta_T))
	for i in range( theta_E.shape[0] ):
		print("E%d T=0\t0: %f\t1:%f" % (i, 1-theta_E[i,0], theta_E[i,0]))
		print("E%d T=1\t0: %f\t1:%f" % (i, 1-theta_E[i,1], theta_E[i,1]))

def learn(T, E, max_iter, sample_hidden):
	I = (E != MISSING_VAL) * 1

	theta = compute_theta(T,E)

	for i in range(max_iter):
		T = infer_hidden_node(E, I, theta, sample_hidden)	# E-step

		if mean(T) < 0.5:
			T = 1 - T

		theta = compute_theta(T, E)		# M-step

		print("Run %d produced theta of: " % i)
		print_theta(theta)

	return theta

def simulate():
	E = loadtxt('bnet.csv', dtype=int, delimiter=',', skiprows=1)
	T = randint(2, size=E.shape[0])

	theta_learned = learn(T, E, 200, sample_hidden=True)

	print('Starting State:')
	print_theta(compute_theta(T, E))
	print('Ending State:')
	print_theta(theta_learned)

	pickle.dump([theta_learned[0], theta_learned[1].tolist()], open('theta.pickle', 'wb'))

if __name__ == '__main__':
	simulate()
