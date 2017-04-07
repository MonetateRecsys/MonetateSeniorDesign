__author__ = 'Alex Marion'

import data_loader


def init_fake_data():
	'''
	Initialize fake testing data from database
	:return:
	'''
	conn = data_loader.get_connection()
	data_loader.init_database(conn)
	data_loader.load_fake_data(conn)

def init_test_data():
	'''
	Initialize testing data from database
	:return:
	'''
	conn = data_loader.get_connection()
	data_loader.init_database(conn)
	data_loader.load_test_data(conn)

def get_data(catalog_id):
	'''
	Convert data from catalog to a matrix of users by products
	:param catalog_id: The catalog id to pull data from
	:return:
		:user_names: A list of ordered user names parallel to the matrix column for users
		:user_map: A map from user id to (position in matrix, user name)
		:product_names: A list of ordered product names parallel to the matrix row for products
		:product_map: A map from product id to (position in matrix, product_id)
		:matrix: A matrix of user to product interactions (in this case, purchases from transaction data)
	'''
	conn = data_loader.get_connection()

	transactions = data_loader.get_transactions_for_catalog(conn, catalog_id)
	product_names = []
	product_map = {}
	user_names = []
	user_map = {}
	max_user = 0
	max_product = 0

	user_ids = set([trans[0] for trans in transactions])
	product_ids = set([trans[2] for trans in transactions])

	matrix = [[0 for x in range(len(product_ids))] for y in range(len(user_ids))]
	for trans in transactions:
		if(trans[0] in user_map):
			user_tuple = user_map[trans[0]] # User tuple = (new_id, name)
			user_index = user_tuple[0]
		else:
			user_map[trans[0]] = (max_user, trans[1])   # Assign the user to {old_id: (new_id, name)}
			user_names.append(trans[0])
			user_index = max_user
			max_user += 1

		if(trans[2] in product_map):
			product_tuple = product_map[trans[2]]   # Product tuple = (new_id, name)
			prod_index = product_tuple[0]
		else:
			product_map[trans[2]] = (max_product, trans[5]) # Assign the product to {old_id: (new_id, name)}
			product_names.append(trans[2])
			prod_index = max_product
			max_product += 1


		matrix[user_index][prod_index] = 1

	conn.commit()
	conn.close()

	return [user_names, user_map, product_names, product_map, matrix]


def get_recommendation_header():
	'''
	:return: The header for the recommendation table
	'''
	return ['recommendation_id',
			'user_id',
			'product_id',
			'interacted']


def get_context_header():
	'''
	:return: The header for the context table
	'''
	return ['context_id',
			'recommendation_id',
			'product_id',
			'device',
			'os',
			'time_of_day',
			'day_of_week',
			'latitude',
			'longitude',
			'num_items_in_cart',
			'purchases_in_last_month']


def get_recommendation_fields():
	'''
	:return: All fields in context (header without ids)
	'''
	return ['device',
			'os',
			'time_of_day',
			'day_of_week',
			'latitude',
			'longitude',
			'num_items_in_cart',
			'purchases_in_last_month']


def get_product_header():
	'''
	:return: The header for the product table
	'''
	return ['id',
			'sku_id',
			'catalog_id',
			'product_name',
			'price',
			'description']