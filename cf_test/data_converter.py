import pandas as pd
from scipy.spatial.distance import cosine

'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DATA LOADING ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
path = 'test_data_structure/'
users = pd.read_csv(path + 'users.csv')
products = pd.read_csv(path + 'products.csv')
products_bought = pd.read_csv(path + 'products_bought.csv')

print(products)
