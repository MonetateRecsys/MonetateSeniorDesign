import data_loader


def get_data():
    conn = data_loader.get_connection()
    data_loader.init_database(conn)
    data_loader.load_fake_data(conn)

    catalogs = data_loader.get_catalogs(conn)
    catalog_id = catalogs[0][0]

    transactions = data_loader.get_transactions_for_catalog(conn,catalog_id)
    products_names = []
    productMap = {}
    user_names = []
    userMap = {}
    maxUser = 0
    maxProduct = 0

    user_ids = set([trans[0] for trans in transactions])
    product_ids = set([trans[2] for trans in transactions])

    matrix = [[0 for x in range(len(product_ids))] for y in range(len(user_ids))]
    for trans in transactions:
        if(trans[0] in userMap):
            user_index = userMap[trans[0]]
        else:
            userMap[trans[0]] = maxUser
            user_names.append(trans[1])
            user_index = maxUser
            maxUser += 1

        if(trans[2] in productMap):
            prod_index = productMap[trans[2]]
        else:
            productMap[trans[2]] = maxProduct
            products_names.append(trans[5])
            prod_index = maxProduct
            maxProduct += 1

        matrix[user_index][prod_index] = 1

    conn.commit()
    conn.close()

    return [user_names, products_names, matrix]
