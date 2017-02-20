import pandas as pd
import data_loader
from scipy.spatial.distance import cosine

'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DATA LOADING ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
'''
path = 'test_data_structure/'
users = pd.read_csv(path + 'users.csv')
products = pd.read_csv(path + 'products.csv')
products_bought = pd.read_csv(path + 'products_bought.csv')

print(products)
'''
conn = data_loader.get_connection()
data_loader.init_database(conn)
data_loader.load_fake_data(conn)
#data_loader.get_users(conn)

print(data_loader.get_all_data(conn))

data_loader.conn.commit()
data_loader.conn.close()
