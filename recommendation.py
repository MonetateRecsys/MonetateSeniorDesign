def new_action(prod1,prod2, action, conn):
    c = conn.cursor()
    c.execute('''INSERT INTO actions (productId1, productId2, action) VALUES (?,?,?)''', (prod1,prod2,action))


def get_recommendations(product, limit, conn):
    c = conn.cursor()
    c.execute('''SELECT * FROM  INTO actions (productId1, productId2, action) VALUES (?,?,?)''', (prod1, prod2, action))




###
# SELECT PRODUCTS.*, COUNT(actions.id) as action_count FROM PRODUCTS left join ACTIONs on PRODUCTS.id = actions.productId1
# where actions.productId1 = 1019005
# group by PRODUCTS.id
# order by action_count desc
#
#
# select * from ACTIONS where productId1 = 1019005
#
#
# select * from (
#     select * , count(1) N from ACTIONS
# 	where productId1 = 1019005
#     group by productId1) t
# order by N desc