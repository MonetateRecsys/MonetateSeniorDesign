def new_action(prod1,prod2, action, conn):
    c = conn.cursor()
    c.execute('''INSERT INTO actions (productId1, productId2, action) VALUES (?,?,?)''', (prod1,prod2,action))


def get_recommendations(product, limit, conn):
    c = conn.cursor()
    c.execute('''SELECT p.*, (select count(*) from actions where actions.productId1= ? and  actions.productId2 = p.id) as score from products p order by score desc limit ?''', (product, limit))
    y=c.fetchall()
    return y



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