import recommendation
import dataloader
import sqlite3
import json



conn = sqlite3.connect('recommendation_engine.db')
products = open('bestbuy.json')
data = json.load(products)

#dataloader.load_products(conn,data)
#dataloader.fake_interactions(10000,data,conn)

results = recommendation.get_recommendations('1000592', 10,conn)
conn.commit()
conn.close()

for res in results:
    print 'Recommendation: Score:' + str(res[2]) + ' product: ' + str(res[0]) + ': ' + str(res[1])