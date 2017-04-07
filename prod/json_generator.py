__author__ = 'Alex Marion'

import json
from collections import OrderedDict

import data_loader
import data_converter

def generate_json_from_product_ids(catalog_id, product_ids, probabilites = None):
	'''
	Generate json from list of product ids
	:param catalog_id: Catalog id for which product ids belong
	:param product_ids: List of product ids (assumed to be sorted in order of highest probability to lowest)
	:return: JSON data for all products in order
	'''
	conn = data_loader.get_connection()
	product_header = data_converter.get_product_header()

	json_data = []

	sum_probs = 1
	if probabilites:
		sum_probs = sum(probabilites)

	for i in range(len(product_ids)):
		product = data_loader.get_product_by_id(conn, catalog_id, product_ids[i])[0]  # Only one product will be returned
		json_product = {}

		for j in range(len(product_header)):
			json_product[product_header[j]] = product[j]

		if probabilites:
			json_product['Probability'] = probabilites[i]/sum_probs

		json_data.append((product_ids[i], json_product))

	return json.dumps(json_data)