import pandas as pd
import data_loader
from scipy.spatial.distance import cosine


def get_data():
    conn = data_loader.get_connection()
    data_loader.init_database(conn)
    data_loader.load_fake_data(conn)

    catalogs = data_loader.get_catalogs(conn)
    print(catalogs)
    catalog_id = catalogs[0][0]
    users_with_products = data_loader.get_products_bought(conn, catalog_id)

    user_ids = set([trans[1] for trans in users_with_products])
    product_ids = set([trans[2] for trans in users_with_products])

    userlookup = {}
    productlookup = {}
    productIdlookup = {}
    userIdlookup = {}

    maxUser = 0
    maxProduct = 0

    matrix = [[0 for x in range(len(product_ids))] for y in range(len(user_ids))]
    for trans in users_with_products:
        if(trans[1] in userlookup):
            user_index = userlookup[trans[1]]
        else:
            userlookup[trans[1]] = maxUser
            userIdlookup[maxUser] = trans[1]
            user_index = maxUser
            maxUser += 1

        if(trans[2] in productlookup):
            prod_index = productlookup[trans[2]]
        else:
            productlookup[trans[2]] = maxProduct
            productIdlookup[maxProduct] = trans[2]
            prod_index = maxProduct
            maxProduct += 1

        matrix[user_index][prod_index] = 1

    conn.commit()
    conn.close()

    return [userIdlookup, productIdlookup, matrix]
