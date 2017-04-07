import numpy as np
import bayespy.plot as bpplt
from bayespy.nodes import Dirichlet, Categorical
from bayespy.nodes import Gaussian, Wishart
from bayespy.nodes import Mixture
from bayespy.inference import VB

y0 = np.random.multivariate_normal([0, 0], [[2, 0], [0, 0.1]], size=50)
y1 = np.random.multivariate_normal([0, 0], [[0.1, 0], [0, 2]], size=50)
y2 = np.random.multivariate_normal([2, 2], [[2, -1.5], [-1.5, 2]], size=50)
y3 = np.random.multivariate_normal([-2, -2], [[0.5, 0], [0, 0.5]], size=50)
y = np.vstack([y0, y1, y2, y3])

N = 200
D = 2
K = 10

alpha = Dirichlet(1e-5*np.ones(K), name='alpha')
Z = Categorical(alpha, plates=(N,),name='z')

mu = Gaussian(np.zeros(D),1e-5*np.identity(D),plates=(K,),name='mu')
Lambda = Wishart(D,1e-5*np.identity(D),plates=(K,),name='Lambda')

Y = Mixture(Z, Gaussian, mu, Lambda, name='Y')
Z.initialize_from_random()
Q = VB(Y, mu, Lambda, Z, alpha)

Y.observe(y)
Q.update(repeat=1000)

bpplt.gaussian_mixture_2d(Y, alpha=alpha, scale=2)

