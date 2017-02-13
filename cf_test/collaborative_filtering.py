import pandas as pd
from scipy.spatial.distance import cosine

'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DATA LOADING ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
data = pd.read_csv('test_data.csv')
#print(data.head(6).ix[:,2:8])

# Drop user column
data_raw = data.drop('user',1)

print('Raw Data')
print(data)
print()


'''~~~~~~~~~~~~~~~~~~~~~ ITEM BASED COLLABORATIVE FILTERING ~~~~~~~~~~~~~~~~~~~~'''
# Create placeholder dataframe listing item vs. item
data_ibs = pd.DataFrame(index=data_raw.columns,columns=data_raw.columns)

# Fill placeholder with cosine similarities
for i in range(0,len(data_ibs.columns)):
	for j in range(0,len(data_ibs.columns)):
		data_ibs.ix[i,j] = 1-cosine(data_raw.ix[:,i],data_raw.ix[:,j])

# Create a placeholder dataframe for closest neighbours to an item
num_cols = len(data_ibs.columns)
data_neighbours = pd.DataFrame(index=data_ibs.columns,columns=range(1,num_cols + 1))
#print(data_neighbours)

# Loop through similarity dataframe and fill in neighbouring item names
for i in range(0,len(data_ibs.columns)):
	data_neighbours.ix[i,:num_cols] = data_ibs.ix[0:,i].sort_values(ascending=False)[:num_cols].index

print('Item Based Collaborative Filtering')
print(data_neighbours);
print()


'''~~~~~~~~~~~~~~~~~~~~~ USER BASED COLLABORATIVE FILTERING ~~~~~~~~~~~~~~~~~~~~'''
# Helper function to get similarities
def getScore(history, similarities):
	return sum(history*similarities)/sum(similarities)

# Create a placeholder for similarities and fill in user names
data_sims = pd.DataFrame(index=data.index,columns=data.columns)
data_sims.ix[:,:1] = data.ix[:,:1]

# Fill similarity scores (skipping user column)
for i in range(0,len(data_sims.index)):
	for j in range(1,len(data_sims.columns)):
		user = data_sims.index[i]
		product = data_sims.columns[j]

		if data.ix[i][j] == 1:
			data_sims.ix[i][j] = 0
		else:
			product_top_names = data_neighbours.ix[product][1:10]		
			product_top_sims = data_ibs.ix[product].sort_values(ascending=False)
			user_purchases = data_raw.ix[user,product_top_names]

			data_sims.ix[i][j] = getScore(user_purchases,product_top_sims)

# Get top products
data_recommend = pd.DataFrame(index=data_sims.index,columns=['user','1','2','3','4','5','6'])
data_recommend.ix[0:,0] = data_sims.ix[:,0]

# Assign product names to top scores
for i in range(0,len(data_sims.index)):
	data_recommend.ix[i,1:] = data_sims.ix[i,:].sort_values(ascending=False).ix[1:7,].index.transpose()

print('User Based Collaborative Filtering')
print(data_recommend.ix[:10,:7])
