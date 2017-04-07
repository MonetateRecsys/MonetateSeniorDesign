__author__ = 'Alex Marion'

import data_loader
import data_converter
import itertools as it
import sys
import time
import math

ALL_VARS = data_converter.get_recommendation_fields()
EPS = 0.005  # Probability threshold


def get_field_key(d):
	'''
	Gets the key from a dictionary as a literal
	:param d: Input dictionary
	:return: Literal key of dictionary
	'''
	return list(d.items())[0][0]


def get_probs(conn, context, given):
	'''
	Get the probability of a context given a set of variables and values
	:param conn: Connection to the database
	:param context: Context to test probability for
	:param given: Given set of variables and values
	:return:
	'''
	probs = {}
	given_key = list(given)[0]
	for var in context:
		if var != given_key:
			probs[var] = data_loader.get_probability(conn, {var: context[var]}, given)
	return probs


def bayes_independent(conn, x, y, z):
	'''
	Test if x is independent of y given z, P(x | y, z) = P(x | z)
	:param conn: Connection to the database
	:param x: Context to test the independence of y
	:param y: Field to test independence of
	:param z: Context under which to test for independence
	:return: True if x is independent of y given z, false otherwise
	'''
	yz = dict(y)
	yz.update(z)

	p_xz = data_loader.get_probability(conn, x, z)  # Probability of x given z
	p_xyz = data_loader.get_probability(conn, x, yz)  # Probability of x given y and z

	if abs(p_xz - p_xyz) < EPS:
		return True
	return False


def power_set(lst):
	'''
	Get a power set of elements in lst not including the empty set
	:param lst: List of items
	:return: Power set of the list
	'''
	res = list(lst)
	return it.chain.from_iterable(it.combinations(res, r) for r in range(1, len(res) + 1))


def hiton_mb(conn, recommendation, rec_context):
	'''
	Return the markov blanket of the given recommendation and context
	:param conn: Connection to the database
	:param recommendation: Recommendation to find the markov blanket for
	:param rec_context: Context of the recommendation
	:return: Markov blanket of recommendation
	'''
	product_id = recommendation[2]  # Product ID is the second field in recommendation
	product_field = {'product_id': product_id}
	parent_child_list = {}
	parent_child_list = hiton_pc(conn, parent_child_list, rec_context, product_field)
	parent_child_list[product_id] = parent_child_list.pop(
		'product_id')  # Replace string 'product_id' with real product id

	# Get the parents and children of every parent and child of the product id
	index = 1
	print('')
	for var in parent_child_list[product_id]:
		parent_child_list = hiton_pc(conn, parent_child_list, rec_context, {var: rec_context[var]})
		printProgressBar(math.floor(100*(index / float(len(parent_child_list[product_id])))))
		index +=1
	print('')
	# Initialize the markov blanket candidates to all items in parent/child list
	markov_blanket_candidates = set(it.chain.from_iterable(parent_child_list.values()))

	markov_blanket = set(markov_blanket_candidates)
	while markov_blanket_candidates:  # For all potential X in markov blanket
		X = markov_blanket_candidates.pop()
		x_dict = {X: rec_context[X]}

		for Y in parent_child_list:  # For all Y in the parent child list where Y != X
			if Y != X:
				S = [Y] + [x for x in ALL_VARS if x != X]  # Create a set of Y union (ALL_VARS - X)
				s_dict = {key: rec_context[key] for key in S if key != product_id}  # Create dictionary from keys in S

				# If the recommendation is dependent on X add it to the markov blanket
				if bayes_independent(conn, product_field, x_dict, s_dict):
					markov_blanket.remove(X)
					break

	return markov_blanket


def hiton_pc(conn, parent_child_list, context, field):
	'''
	hiton_pc returns the parent child list of the input field by testing conditional bayesian probabilities
	:param conn: Connection to the database
	:param parent_child_list: Existing parent child dictionary with string keys and array values
	:param context: Recommendation context (dictionary with one to many values)
	:param field: Field for which the parent child list is being generated (single entry dictionary with key/value)
	:return: Parent child list (dictionary of arrays) of field
	'''
	probs = get_probs(conn, context, field)  # Get the probabilities of the context given the variable value
	var = get_field_key(field)  # Get the key of the variable value

	if not var in parent_child_list:
		parent_child_list[var] = []  # Initialize empty parent child list

	open = [x for x in ALL_VARS if x != var and x not in parent_child_list[var]]  # Get all vars not equal to cur var
	open.sort(key=lambda x: probs[x], reverse=True)  # Sort by probability of x given variable value
	while open:
		parent_child_list[var].append(open.pop())
		for x in parent_child_list[var]:
			for z in power_set([var for var in parent_child_list[var] if var != x]):
				# Construct fields for bayesian independence test
				z_dict = {key: context[key] for key in z if key != x}
				x_dict = {x: context[x]}

				# If x and the current variable value are conditionally independent, remove x from the list
				if bayes_independent(conn, x_dict, field, z_dict):
					parent_child_list[var].remove(x)
					break

	return parent_child_list

def printProgressBar(iter):
	sys.stdout.write(("\r%d%% [" + '█' * math.floor(iter/2) + ' ' * (50 - math.floor(iter/2)) + ']') % iter)
	sys.stdout.flush()


def test():
	'''
	Testing code for markov blanket generation
	:return:
	'''

	conn = data_loader.get_connection()
	#data_loader.init_database(conn)
	#data_loader.load_fake_data(conn)

	catalog_id = data_loader.get_catalogs(conn)[0][0]
	product_id = data_loader.get_products(conn, catalog_id)[0][0]
	user_id = data_loader.get_users(conn)[0][0]

	user_recs = data_loader.get_recommendations_by_user(conn, user_id)
	prod_ids = set()
	for rec in user_recs:
		prod_ids.add(rec[2])

	# Get all recommendations for products recommended to user
	prod_recs = []
	for prod_id in prod_ids:
		prod_recs.append(data_loader.get_recommendations_by_product(conn, prod_id)[0])

	# Concatenate all recs and assign to dictionary values via the headers
	recommendations = set(user_recs + prod_recs)

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
	for i in range(0, len(rec_list) - 1):
		markov_blanket = hiton_mb(conn, rec_list[i], rec_contexts[i])
		print('Recommendation: ', rec_list[i])
		print('Markov Blanket: ', markov_blanket)


if __name__ == '__main__':
	test()
