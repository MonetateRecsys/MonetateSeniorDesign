import recommendation
import dataloader
import sqlite3
import json



conn = sqlite3.connect('recommendation_engine.db')
products = open('bestbuy.json')
data = json.load(products)

#dataloader.load_products(conn,data)
dataloader.fake_interactions(1000,data,conn)

conn.commit()
conn.close()