import pandas as pd
import data_loader
from scipy.spatial.distance import cosine

def get_data():
	conn = data_loader.get_connection()
	data_loader.init_database(conn)
	data_loader.load_fake_data(conn)

	#data_loader.get_users(conn)
	#print(data_loader.get_all_data(conn))

	#print(pd.DataFrame(data_loader.get_all_data(conn)))
	#users = data_loader.get_users(conn)
	#products = data_loader.get_products(conn)

	users_with_products = data_loader.get_products_bought(conn)

	user_ids = [trans[1] for trans in users_with_products]
	product_ids = [trans[2] for trans in users_with_products]

	product_offset =max(product_ids) - min(product_ids)+1
	user_offset = max(user_ids) - min(user_ids)+1

	print(product_offset)
	print(user_offset)
	print(data_loader.get_products(conn))
	print(product_ids)

	matrix = [[0 for x in range(product_offset)] for y in range(user_offset)]
	for trans in users_with_products:
		matrix[trans[1]-min(user_ids)][trans[2]-min(product_ids)] = 1

	conn.commit()
	conn.close()

	return matrix
