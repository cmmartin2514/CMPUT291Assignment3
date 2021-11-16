import sqlite3
import csv

# changes any instance of "Large" to make different sizes
# this code is bad but oh well it works
# change numbers in SELECT statements to select differnt numbers of rows

# open/create the new database
conn = sqlite3.connect('./A3Large.db')

# create its tables
c = conn.cursor()
c.execute("CREATE TABLE 'Customers' ('customer_id' TEXT, 'customer_postal_code' INTEGER, PRIMARY KEY('customer_id'))")
c.execute("CREATE TABLE 'Sellers' ('seller_id' TEXT, 'seller_postal_code' INTEGER, PRIMARY KEY('seller_id'))")
c.execute("CREATE TABLE 'Orders' ('order_id' TEXT, 'customer_id' TEXT, PRIMARY KEY('order_id'), FOREIGN KEY('customer_id') REFERENCES 'Customers'('customer_id'))")
c.execute("CREATE TABLE 'Order_items' ('order_id' TEXT, 'order_item_id' INTEGER, 'product_id' TEXT, 'seller_id' TEXT, PRIMARY KEY('order_id', 'order_item_id', 'product_id', 'seller_id'), FOREIGN KEY('seller_id') REFERENCES 'Sellers'('seller_id'), FOREIGN KEY('order_id') REFERENCES 'Orders'('order_id'))")
conn.commit()
conn.close()

# open main database
conn = sqlite3.connect('./data.db')
c = conn.cursor()

# select random customers and sellers since they don't matter
c.execute("SELECT * FROM Customers ORDER BY RANDOM() LIMIT 33000")
rows_customer = c.fetchall()
c.execute("SELECT * FROM Sellers ORDER BY RANDOM() LIMIT 1000")
rows_seller = c.fetchall()
conn.close()

# open sample database again
conn = sqlite3.connect('./A3Large.db')
c = conn.cursor()
# insert chosen customer and seller rows
c.executemany("INSERT INTO 'Customers' ('customer_id', 'customer_postal_code') VALUES (?,?);", rows_customer)
c.executemany("INSERT INTO 'Sellers' ('seller_id', 'seller_postal_code') VALUES (?,?);", rows_seller)
conn.commit()
conn.close()

# open main database again
conn = sqlite3.connect('./data.db')
# attach our sample database so we can reference it
conn.execute("ATTACH DATABASE './A3Large.db' AS Large")
c = conn.cursor()
# select random rows from Orders ensuring foreign key references are still valid
c.execute("SELECT order_id, O.customer_id FROM main.Orders O, Large.Customers C WHERE C.customer_id = O.customer_id ORDER BY RANDOM() LIMIT 33000")
rows_order = c.fetchall()
conn.close()

# open sample database again
conn = sqlite3.connect('./A3Large.db')
c = conn.cursor()
# insert chosen orders
c.executemany("INSERT INTO 'Orders' ('order_id', 'customer_id') VALUES (?,?);", rows_order)
conn.commit()
conn.close()

# open main database again and attach sample database
conn = sqlite3.connect('./data.db')
conn.execute("ATTACH DATABASE './A3Large.db' AS Large")
c = conn.cursor()
# select random rows from Order_items such that foreign key references are still valid
c.execute("SELECT I.order_id, order_item_id, product_id, I.seller_id FROM main.Order_items I, Large.Orders O, Large.Sellers S WHERE I.order_id = O.order_id AND I.seller_id = S.seller_ID ORDER BY RANDOM() LIMIT 10000")
rows_order_item = c.fetchall()
conn.close()

# open sample database again
conn = sqlite3.connect('./A3Large.db')
c = conn.cursor()
# insert chosen order items
c.executemany("INSERT INTO 'Order_items' ('order_id', 'order_item_id', 'product_id', 'seller_id') VALUES (?,?,?,?);", rows_order_item)
conn.commit()
conn.close()