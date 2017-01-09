
from random import randint
import random
import recommendation

def init_database(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products
             (id INTEGER PRIMARY KEY, name TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS actions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,productId1 INTEGER, productId2 INTEGER, action text, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS tags
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,productId INTEGER ,tag text)''')

    c.execute('''DELETE FROM products''')
    c.execute('''DELETE FROM tags''')
    c.execute('''DELETE FROM actions''')

def load_products(conn, data):

    init_database(conn)

    c = conn.cursor()
    for product in data['products']:
        c.execute('''INSERT INTO products (id, name) VALUES (?,?)''',(product['sku'],product['name']))
        c.execute('''INSERT INTO tags (productId, tag) VALUES (?,?)''',(product['sku'],product['genre']))







def fake_interactions(num, data, conn):
    c = conn.cursor()
    for i in range(0,num):
        type = randint(0, 5)
        if type <= 2:
            action = 'LOOK'
        elif type <=4:
            action = 'CART'
        else:
            action = 'BUY'

        prods = random.sample(range(1, 100), 2)
        recommendation.new_action(data['products'][prods[0]]['sku'],data['products'][prods[1]]['sku'],action,conn)
        recommendation.new_action(data['products'][prods[1]]['sku'], data['products'][prods[2]]['sku'], action, conn)
