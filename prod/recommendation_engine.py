__author__ = 'Alex Marion'

import pandas as pd
import copy

import data_loader
import data_converter
import collaborative_filtering
import HITON
import json_generator

def run_engine():
	#data_converter.init_fake_data()
	data_converter.init_test_data()
	conn = data_loader.get_connection()

	catalogs = data_loader.get_catalogs(conn)
	catalog_id = catalogs[0][0]  # TODO: PLACEHOLDER

	[data, user_map, product_map] = collaborative_filtering.collab_filter_load_data(catalog_id)

	recommendations = collaborative_filtering.user_collab_filter(data)
	print(recommendations)

	collaborative_filtering.print_recommendations(recommendations, user_map, product_map)

	user_id = data_loader.get_users(conn)[0][0]  # TODO: create ability to pass user
	user_idx = user_map[user_id][0]  # Get index at which user is stored

	# Get the product recommendations for the selected user
	recs_for_user = pd.DataFrame(recommendations.iloc[user_idx, 1:]).as_matrix()
	recs_for_user = [x for x_arr in recs_for_user for x in x_arr]

	# Pull context for current recommendation
	contexts = [data_loader.generate_context(recs_for_user[0])]  # Create the first context with the first product id
	for i in range(1, len(recs_for_user)):
		context_cpy = copy.deepcopy(contexts[0])
		context_cpy[0] = recs_for_user[i]
		contexts.append(context_cpy)

	# Copy user id
	user_ids = [user_id] * len(recs_for_user)

	# Insert recommendations into database and retrieve same items to test probabilities
	recommendations = data_loader.add_recommendation(conn, recs_for_user, user_ids, contexts)

	# Get all recommendations for products recommended to user
	prod_recs = []
	for prod_id in recs_for_user:
		prod_recs.append(data_loader.get_recommendations_by_product(conn, prod_id)[0])

	recommendations = set(recommendations + prod_recs)

	recommendation_header = data_converter.get_recommendation_header()
	context_header = data_converter.get_context_header()
	header = recommendation_header + context_header
	recommendation_fields = data_converter.get_recommendation_fields()

	rec_contexts = []
	for rec in recommendations:
		cur_context = {}
		for i in range(len(rec)):
			if header[i] in recommendation_fields:
				cur_context[header[i]] = rec[i]
		rec_contexts.append(cur_context)

	rec_list = list(recommendations)
	markov_blankets = []
	probabilities = []

	for i in range(0, len(rec_list) - 1):

		markov_blanket = HITON.hiton_mb(conn, rec_list[i], rec_contexts[i])
		markov_blankets.append({x: rec_contexts[i][x] for x in markov_blanket})
		probabilities.append(data_loader.get_probability(conn, {'product_id': rec_list[i][2]}, markov_blankets[i]))

		print('Recommendation: ', rec_list[i])
		print('Markov Blanket: ', markov_blankets[i])
		print('Probability: ', probabilities[i])

		print()


	zipped_probs_and_prods = zip(probabilities, recs_for_user)
	ordered_probs_and_prods = sorted(zipped_probs_and_prods, key = lambda p: p[0], reverse=True)

	#ordered_recs_for_user = [prod for (prob, prod) in sorted(zip(probabilities, recs_for_user), key=lambda x: x[0], reverse=True)]
	ordered_recs_for_user = [x[1] for x in ordered_probs_and_prods]
	ordered_probabilities = [x[0] for x in ordered_probs_and_prods]

	print(ordered_recs_for_user)
	print(json_generator.generate_json_from_product_ids(catalog_id, ordered_recs_for_user, ordered_probabilities))

if __name__ == '__main__':
	run_engine()
