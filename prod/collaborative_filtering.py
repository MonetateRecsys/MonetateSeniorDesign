__author__ = 'Alex Marion'

import pandas as pd
from scipy.spatial.distance import cosine
from data_converter import get_data


def get_score(history, similarities):
	'''
	Return the a score of a history (purchase) vector by a vector of similarities
	:param history: Vector of purchase history
	:param similarities: Vector of computed similarities
	:return: score
	'''
	return sum(history * similarities)/sum(similarities)


'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DATA LOADING ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
def collab_filter_load_data(catalog_id):
	'''
	Load the data into a pandas data frame
	:param catalog_id: Catalog id to load data from
	:return: Pandas data frame
	'''
	[user_names, user_map, product_names, product_map, data_raw] = get_data(catalog_id)
	data = pd.DataFrame(data_raw)
	data.columns = product_names
	data.insert(0,'user',user_names)

	return [data, user_map, product_map]


def item_collab_filter(data):
	'''
	Perform item based collaborative filtering using cosine difference of observations
	:param data: Matrix of product to product interactions
	:return: Data Frame of products by products ordered by cosine similarity
	'''
	data_raw = data.drop('user',1)

	# Create placeholder data frame listing item vs. item
	data_ibs = pd.DataFrame(index = data_raw.columns, columns = data_raw.columns)

	# Fill placeholder with cosine similarities
	for i in range(0,len(data_ibs.columns)):
		for j in range(0,len(data_ibs.columns)):
			data_ibs.iloc[i,j] = 1 - cosine(data_raw.iloc[:,i], data_raw.iloc[:,j])

	# Create a placeholder dataframe for closest neighbours to an item
	num_cols = len(data_ibs.columns)
	data_neighbours = pd.DataFrame(index = data_ibs.columns, columns=range(1,num_cols + 1))

	# Loop through similarity dataframe and fill in neighbouring item names
	for i in range(0,len(data_ibs.columns)):
		data_neighbours.iloc[i,:num_cols] = data_ibs.iloc[0:,i].sort_values(ascending=False)[:num_cols].index

	return [data_neighbours, data_ibs]


def user_collab_filter(data):
	'''
	Perform user based collaborative filtering using cosine difference of observations
	:param data: Matrix of user to product interactions
	:return: Data Frame of users by products ordered by cosine similarity
	'''
	data_raw = data.drop('user',1)
	[data_neighbours, data_ibs] = item_collab_filter(data)

	# Create a placeholder for similarities and fill in user names
	data_sims = pd.DataFrame(index=data.index,columns=data.columns)
	data_sims.ix[:,:1] = data.ix[:,:1]

	#num_users = len(data_sims.ix[:,:1])
	num_products = len(data_sims.columns.values) - 1

	# Fill similarity scores (skipping user column)
	for i in range(0,len(data_sims.index)):
		for j in range(1,len(data_sims.columns)):
			user = data_sims.index[i]
			product = data_sims.columns[j]

			if data.ix[i][j] == 1:
				data_sims.ix[i][j] = 0
			else:
				product_top_names = data_neighbours.ix[product][1:]	# Index 0 will be self
				product_top_sims = data_ibs.ix[product].sort_values(ascending=False)
				user_purchases = data_raw.ix[user,product_top_names]
				data_sims.ix[i][j] = get_score(user_purchases,product_top_sims)

	# Get top products
	user_column_label = ['user'] + [str(x) for x in range(1, num_products)]
	data_recommend = pd.DataFrame(index = data_sims.index, columns = user_column_label)
	data_recommend.ix[0:,0] = data_sims.ix[:,0]

	# Assign product names to top scores
	for i in range(0,len(data_sims.index)):
		data_recommend.iloc[i,1:] = data_sims.iloc[i,1:].sort_values(ascending=False).iloc[1:num_products,].index.transpose()

	return data_recommend

def print_recommendations(recs, user_map, product_map):
	'''
	Print recommendations from collaborative filtering matrix by replacing the id's with string names
	:param recs: Pandas Data Frame of collaborative filtering recommendations
	:param user_map: Map of user ids to positions in matrix and user names {id: (pos, name)}
	:param product_map: Map of product ids to positions in matrix and product names {id: (pos, name)}
	:return: print recommendations with string names instead of int ids
	'''
	recommendations = pd.DataFrame.copy(recs)
	# Reassign ids to users
	for i in range(0, len(recommendations.ix[:,0])):
		user_id = recommendations.ix[i,0]
		recommendations.ix[i,0] = user_map[user_id][1]

	for i in range(0, len(recommendations.ix[:,1])):
		for j in range(1, len(recommendations.ix[0,:])):
			prod_name = recommendations.ix[i, j]
			recommendations.ix[i, j] = product_map[prod_name][1]

	print(recommendations)
