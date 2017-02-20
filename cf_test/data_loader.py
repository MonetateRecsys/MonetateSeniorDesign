__author__ = 'tomer'
import sqlite3
from random import randint

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



def load_fake_data(conn):

    c = conn.cursor()
    c.execute('''DELETE FROM catalogs''')
    c.execute('''DELETE FROM products''')
    c.execute('''DELETE FROM users''')
    c.execute('''DELETE FROM products_bought''')

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
    c.execute('''INSERT INTO users (user_name) VALUES (?)''',('Joey',))
    ppl.append(c.lastrowid)

    products = []
    c.execute('''INSERT INTO products (id,sku_id,catalog_id, product_name, price,description) VALUES (NULL,?,?,?,?,?)''',(100,catalogs[randint(0,len(catalogs)-1)],'Movie1',51007,'Red and swollen'))
    products.append(c.lastrowid)
    c.execute('''INSERT INTO products (id,sku_id,catalog_id, product_name, price,description) VALUES (NULL,?,?,?,?,?)''',(200,catalogs[randint(0,len(catalogs)-1)],'Movie2',1337,'Bachelor trying to have it all'))
    products.append(c.lastrowid)
    c.execute('''INSERT INTO products (id,sku_id,catalog_id, product_name, price,description) VALUES (NULL,?,?,?,?,?)''',(300,catalogs[randint(0,len(catalogs)-1)],'Movie3',69.69,'Mid range model'))
    products.append(c.lastrowid)
    c.execute('''INSERT INTO products (id,sku_id,catalog_id, product_name, price,description) VALUES (NULL,?,?,?,?,?)''',(400,catalogs[randint(0,len(catalogs)-1)],'Movie4',234,'Absent'))
    products.append(c.lastrowid)
    c.execute('''INSERT INTO products (id,sku_id,catalog_id, product_name, price,description) VALUES (NULL,?,?,?,?,?)''',(500,catalogs[randint(0,len(catalogs)-1)],'Movie5',876,'Yall'))
    products.append(c.lastrowid)
    c.execute('''INSERT INTO products (id,sku_id,catalog_id, product_name, price,description) VALUES (NULL,?,?,?,?,?)''',(600,catalogs[randint(0,len(catalogs)-1)],'Movie6',45.56,'Handicapable'))
    products.append(c.lastrowid)

    for i in range(1,100):
        c.execute('''INSERT INTO products_bought (id,user_id, product_id) VALUES (NULL,?,?)''',(ppl[randint(0,len(ppl)-1)],products[randint(0,len(products)-1)]))


def get_users(conn):
    c = conn.cursor()
    c.execute('''select * from users''')
    return c.fetchall()

def get_products(conn):
    c = conn.cursor()
    c.execute('''select * from products''')
    return c.fetchall()

def get_products_bought(conn):
    c = conn.cursor()
    c.execute('''select * from products_bought''')
    return c.fetchall()

def get_all_data(conn):
    c = conn.cursor()
    c.execute('''select u.*, p.*, c.* from users u, products p, products_bought pb, catalogs c where p.id = pb.product_id and p.catalog_id == c.id and u.id = pb.user_id''')
    return c. fetchall()

def get_data_for_user(conn,userid):
    c = conn.cursor()
    c.execute('''select u.*, p.*, c.* from users u, products p, products_bought pb, catalogs c where p.id = pb.product_id and p.catalog_id == c.id and u.id = pb.user_id and u.id = ?''',(userid,))
    return c.fetchall()

def get_data_for_user_and_catalog(conn,userid,catalogid):
    c = conn.cursor()
    c.execute('''select u.*, p.*, c.* from users u, products p, products_bought pb, catalogs c where p.id = pb.product_id and p.catalog_id == c.id and u.id = pb.user_id and u.id = ? and c.id = ?''',(userid,catalogid))
    return c.fetchall()

def get_data_for_catalog(conn,catalogid):
    c = conn.cursor()
    c.execute('''select u.*, p.*, c.* from users u, products p, products_bought pb, catalogs c where p.id = pb.product_id and p.catalog_id == c.id and u.id = pb.user_id and c.id = ?''',(catalogid,))
    return c.fetchall()


def get_connection():
    return sqlite3.connect('recommendation_engine.db')