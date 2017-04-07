__author__ = 'tomer'
import sqlite3
from random import randint
import test_data

def init_database(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS catalogs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, catalog_name TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS products
             (id INTEGER PRIMARY KEY AUTOINCREMENT, sku_id INTEGER, catalog_id INTEGER,  product_name TEXT, price FLOAT, description TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, user_name TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS products_bought
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,product_id INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS product_context
             (id INTEGER PRIMARY KEY AUTOINCREMENT,recommendation_id INTEGER, product_id INTEGER, device TEXT, os TEXT, time_of_day TEXT, day_of_week TEXT, latitude float, longitude float,num_items_in_cart INTEGER, purchases_in_last_month INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS recommendations
             (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER, product_id INTEGER, interacted BOOLEAN)''')


def load_fake_data(conn):

    c = conn.cursor()
    c.execute('''DELETE FROM catalogs''')
    c.execute('''DELETE FROM products''')
    c.execute('''DELETE FROM users''')
    c.execute('''DELETE FROM products_bought''')
    c.execute('''DELETE FROM product_context''')
    c.execute('''DELETE FROM recommendations''')

    catalogs = []
    c.execute('''INSERT INTO catalogs (catalog_name) VALUES (?)''',('BestBuy',))
    catalogs.append(c.lastrowid)
    c.execute('''INSERT INTO catalogs (catalog_name) VALUES (?)''',('RiteAid',))
    catalogs.append(c.lastrowid)


    ppl = []
    c.execute('''INSERT INTO users (user_name) VALUES (?)''',('Tomer',))
    ppl.append(c.lastrowid)
    c.execute('''INSERT INTO users (user_name) VALUES (?)''',('Alex',))
    ppl.append(c.lastrowid)
    c.execute('''INSERT INTO users (user_name) VALUES (?)''',('Matt',))
    ppl.append(c.lastrowid)
    c.execute('''INSERT INTO users (user_name) VALUES (?)''',('Rachael',))
    ppl.append(c.lastrowid)
    c.execute('''INSERT INTO users (user_name) VALUES (?)''',('Sam',))
    ppl.append(c.lastrowid)
    c.execute('''INSERT INTO users (user_name) VALUES (?)''',('Joey',))
    ppl.append(c.lastrowid)

    products = []
    # Load fake products
    for i in range(1,20):
        c.execute('''INSERT INTO products (id,sku_id,catalog_id, product_name, price,description) VALUES (NULL,?,?,?,?,?)''',(randint(1,2000),catalogs[randint(0,len(catalogs)-1)],'Movie' + str(i),randint(1,2000),'Title' + str(i)))
        products.append(c.lastrowid)

    # Load fake transactions
    for i in range(1,50):
        c.execute('''INSERT INTO products_bought (id,user_id, product_id) VALUES (NULL,?,?)''',(ppl[randint(0,len(ppl)-1)],products[randint(0,len(products)-1)]))
        values = (c.lastrowid,device[randint(0,len(device)-1)],oses[randint(0,len(oses)-1)], times[randint(0,len(times)-1)], days[randint(0,len(days)-1)], lats[randint(0,len(lats)-1)], lons[randint(0,len(lons)-1)],randint(0,5),randint(0,30))
        c.execute('''INSERT INTO product_context (id,recommendation_id , device , os , time_of_day , day_of_week , latitude , longitude ,num_items_in_cart , purchases_in_last_month) VALUES (NULL,?,?,?,?,?,?,?,?,?)''',values)

    # Load fake recommendations
    for i in range(1,1000):
       product_id = products[randint(0, len(products) - 1)]
       c.execute('''INSERT INTO recommendations (id,user_id, product_id, interacted) VALUES (NULL,?,?,'true')''',(ppl[randint(0,len(ppl)-1)],product_id))
       values = (c.lastrowid,product_id,device[randint(0,len(device)-1)],oses[randint(0,len(oses)-1)], times[randint(0,len(times)-1)], days[randint(0,len(days)-1)], lats[randint(0,len(lats)-1)], lons[randint(0,len(lons)-1)],randint(0,3),randint(0,3))
       c.execute('''INSERT INTO product_context (id,recommendation_id , product_id , device , os , time_of_day , day_of_week , latitude , longitude ,num_items_in_cart , purchases_in_last_month) VALUES (NULL,?,?,?,?,?,?,?,?,?,?)''',values)
    conn.commit()


oses = ['IOS', 'Android']#, 'Windows10', 'macOS']
device = ['mobile']#, 'computer']
'''
times = ['10:33 AM',
'2:38 PM',
'3:01 AM',
'12:31 AM',
'2:56 PM',
'8:01 AM',
'5:00 PM',
'9:38 PM',
'3:01 AM']
'''
times = ['morning', 'afternoon', 'night']

days = ['M']#['M', 'T', 'W', 'R', 'F', 'S', 'Su']

'''
lats = ['-149.8935557',
'-149.9054948',
'-149.7522',
'-149.8643361',
'-149.8379726',
'-149.9092788',
'-149.7364877',
'-149.8211',
'-149.8445832',
'-149.9728678']
'''
lats = ['north']#, 'south']

'''
lons = ['61.21759217',
'61.19533942',
'61.2297',
'61.19525062',
'61.13751355',
'61.13994658',
'61.19533265',
'61.2156',
'61.13806145',
'61.176693']
'''
lons = ['east']#, 'west']


def get_users(conn):
    c = conn.cursor()
    c.execute('''select * from users''')
    return c.fetchall()


def get_catalogs(conn):
    c = conn.cursor()
    c.execute('''select * from catalogs''')
    return c.fetchall()


def get_products(conn, catalog_id):
    c = conn.cursor()
    c.execute('''select * from products where catalog_id = ?''',(catalog_id,))
    return c.fetchall()


def get_product_by_id(conn, catalog_id, product_id):
    c = conn.cursor()
    c.execute('''SELECT * FROM products WHERE catalog_id = ? AND id = ?''',(catalog_id,product_id))
    return c.fetchall()


def get_products_bought(conn, catalog_id):
    c = conn.cursor()
    c.execute('''select pb.* from products_bought pb, catalogs cat, products p where pb.product_id = p.id and p.catalog_id = ?''',(catalog_id,))
    return c.fetchall()


def get_all_data(conn):
    c = conn.cursor()
    c.execute('''select u.*, p.*, c.* from users u, products p, products_bought pb, catalogs c where p.id = pb.product_id and p.catalog_id == c.id and u.id = pb.user_id''')
    return c. fetchall()


def get_data_for_user(conn,userid):
    c = conn.cursor()
    c.execute('''select u.*, p.*, c.* from users u, products p, products_bought pb, catalogs c where p.id = pb.product_id and p.catalog_id == c.id and u.id = pb.user_id and u.id = ?''',(userid,))
    return c.fetchall()


def get_data_for_user_and_catalog(conn, userid, catalogid):
    c = conn.cursor()
    c.execute('''select u.*, p.*, c.* from users u, products p, products_bought pb, catalogs c where p.id = pb.product_id and p.catalog_id == c.id and u.id = pb.user_id and u.id = ? and c.id = ?''',(userid,catalogid))
    return c.fetchall()


def get_transactions_for_catalog(conn,catalogid):
    c = conn.cursor()
    c.execute('''select u.*, p.*, c.* from users u, products p, products_bought pb, catalogs c where p.id = pb.product_id and p.catalog_id == c.id and u.id = pb.user_id and c.id = ?''',(catalogid,))
    return c.fetchall()


def get_recommendations_by_user(conn,userId):
    c = conn.cursor()
    c.execute('''select r.*, c.* from recommendations r, product_context c where r.id = c.recommendation_id and r.user_id = ?''',(userId,))
    return c.fetchall()


def get_recommendations_by_product(conn,productId):
    c = conn.cursor()
    c.execute('''select r.*, c.* from recommendations r, product_context c where r.id = c.recommendation_id and r.product_id = ?''',(productId,))
    return c.fetchall()


def get_connection():
    return sqlite3.connect('recommendation_engine.db')


def generate_context(product_id):
    return [product_id, device[randint(0, len(device) - 1)], oses[randint(0, len(oses) - 1)],
              times[randint(0, len(times) - 1)], days[randint(0, len(days) - 1)], lats[randint(0, len(lats) - 1)],
              lons[randint(0, len(lons) - 1)], randint(0, 3), randint(0, 3)]


def add_recommendation(conn, product_ids,user_ids,contexts):
    ids = []
    c = conn.cursor()
    for i in range(0,len(product_ids)):
        product_id = product_ids[i]
        user_id = user_ids[i]
        context = contexts[i]
        c.execute('''INSERT INTO recommendations (id,user_id, product_id, interacted) VALUES (NULL,?,?,'false')''',
                  (user_id, product_id))
        context.insert(0,c.lastrowid)
        ids.append(c.lastrowid)
        c.execute( '''INSERT INTO product_context (id,recommendation_id , product_id , device , os , time_of_day , day_of_week , latitude , longitude ,num_items_in_cart , purchases_in_last_month) VALUES (NULL,?,?,?,?,?,?,?,?,?,?)''',
            context)
    conn.commit()
    c.execute('select r.*, c.* from recommendations r, product_context c where r.id = c.recommendation_id and r.id in  (%s)' %
                           ','.join('?'*len(ids)), ids)
    return c.fetchall()


def get_probability(conn, x, giveny):
    c = conn.cursor()
    query = '''select count(*) from product_context where '''
    first = True
    params = []
    for key,val in x.items():
        if not first:
            query += ' and '
        else:
            first = False
        query += str(key) + '=?'
        params.append(str(val))
    c.execute(query,params)
    total = c.fetchone()[0]

    for key,val in giveny.items():
        query += ' and ' + str(key) + '=?'
        params.append(str(val))
    c.execute(query,params)
    smaller = c.fetchone()[0]
    if total == 0:
        return 0
    else:
        return smaller/float(total)


def load_test_data(conn):
    c = conn.cursor()

    # Clear database
    c.execute('''DELETE FROM catalogs''')
    c.execute('''DELETE FROM products''')
    c.execute('''DELETE FROM users''')
    c.execute('''DELETE FROM products_bought''')
    c.execute('''DELETE FROM product_context''')
    c.execute('''DELETE FROM recommendations''')

    # Initialize users
    user_names = test_data.USER_NAMES

    # Initialize movie names
    product_names = test_data.PRODUCT_NAMES

    # Initialize Prices
    prices = test_data.POSSIBLE_PRICES

    # Load test catalog
    catalog_ids = []
    c.execute('''INSERT INTO catalogs (catalog_name) VALUES (?)''', ('MovieDatabase',))
    catalog_ids.append(c.lastrowid)

    # Load test users
    user_ids = []
    for user in user_names:
        c.execute('''INSERT INTO users (user_name) VALUES (?)''', (user,))
        user_ids.append(c.lastrowid)

    # Load test products
    product_ids = []
    for product in product_names:
        values = (randint(1, 2000), catalog_ids[0], product, prices[randint(0, len(prices)-1)], 'desc')
        c.execute('''INSERT INTO products (id, sku_id, catalog_id, product_name, price, description) VALUES (NULL,?,?,?,?,?)''', values)
        product_ids.append(c.lastrowid)

    # Load fake transactions
    for i in range(1, 50):
        values = (user_ids[randint(0, len(user_ids)-1)], product_ids[randint(0, len(product_ids)-1)])
        c.execute('''INSERT INTO products_bought (id,user_id,product_id) VALUES (NULL,?,?)''', values)

        values = (c.lastrowid,
                  device[randint(0, len(device) - 1)],
                  oses[randint(0, len(oses) - 1)],
                  times[randint(0, len(times) - 1)],
                  days[randint(0, len(days) - 1)],
                  lats[randint(0, len(lats) - 1)],
                  lons[randint(0, len(lons) - 1)],
                  randint(0, 3),
                  randint(0, 3))
        c.execute('''INSERT INTO product_context (id,recommendation_id,device,os,time_of_day,day_of_week,latitude,longitude,num_items_in_cart,purchases_in_last_month) VALUES (NULL,?,?,?,?,?,?,?,?,?)''', values)

    # Load fake recommendations
    for i in range(1, 1000):
        product_id = product_ids[randint(0, len(product_ids)-1)]
        values = (user_ids[randint(0, len(user_ids)-1)], product_id,)
        c.execute('''INSERT INTO recommendations (id,user_id,product_id,interacted) VALUES (NULL,?,?,'True')''', values)

        values =(c.lastrowid,
                 product_id,
                 device[randint(0, len(device) - 1)],
                 oses[randint(0, len(oses) - 1)],
                 times[randint(0, len(times) - 1)],
                 days[randint(0, len(days) - 1)],
                 lats[randint(0, len(lats) - 1)],
                 lons[randint(0, len(lons) - 1)],
                 randint(0, 3),
                 randint(0, 3))
        c.execute('''INSERT INTO product_context (id,recommendation_id,product_id,device,os,time_of_day,day_of_week,latitude,longitude,num_items_in_cart,purchases_in_last_month) VALUES (NULL,?,?,?,?,?,?,?,?,?,?)''', values)

    conn.commit()

