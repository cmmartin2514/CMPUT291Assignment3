import sqlite3
import csv

# CREATES THE MAIN DATABASE WITH ALL INFO FROM THE CSV FILES, NOT THE SIZED DATABASES
conn = sqlite3.connect('./data.db')

c = conn.cursor()
#c.execute("SELECT NEIGHBOURHOOD FROM Census WHERE ((CAST(Female AS REAL)/CAST(MALE AS REAL)-1)*100 >=CAST(:percent AS REAL) OR (MALE = 0 AND FEMALE > 0)) AND AGE = CAST(:age as REAL) ORDER BY NEIGHBOURHOOD", {"age":age, "percent":percent})
#rows = c.fetchall()

# create tables
c.execute("CREATE TABLE 'Customers' ('customer_id' TEXT, 'customer_postal_code' INTEGER, PRIMARY KEY('customer_id'))")
c.execute("CREATE TABLE 'Sellers' ('seller_id' TEXT, 'seller_postal_code' INTEGER, PRIMARY KEY('seller_id'))")
c.execute("CREATE TABLE 'Orders' ('order_id' TEXT, 'customer_id' TEXT, PRIMARY KEY('order_id'), FOREIGN KEY('customer_id') REFERENCES 'Customers'('customer_id'))")
c.execute("CREATE TABLE 'Order_items' ('order_id' TEXT, 'order_item_id' INTEGER, 'product_id' TEXT, 'seller_id' TEXT, PRIMARY KEY('order_id', 'order_item_id', 'product_id', 'seller_id'), FOREIGN KEY('seller_id') REFERENCES 'Sellers'('seller_id'), FOREIGN KEY('order_id') REFERENCES 'Orders'('order_id'))")

# read each csv file and populate the respective table
with open("olist_customers_dataset.csv", 'r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['customer_id'],i['customer_zip_code_prefix']) for i in dr]

c.executemany("INSERT INTO 'Customers' ('customer_id', 'customer_postal_code') VALUES (?,?);", to_db)

with open("olist_sellers_dataset.csv", 'r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['seller_id'],i['seller_zip_code_prefix']) for i in dr]

c.executemany("INSERT INTO 'Sellers' ('seller_id', 'seller_postal_code') VALUES (?,?);", to_db)

with open("olist_orders_dataset.csv", 'r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['order_id'],i['customer_id']) for i in dr]

c.executemany("INSERT INTO 'Orders' ('order_id', 'customer_id') VALUES (?,?);", to_db)

with open("olist_order_items_dataset.csv", 'r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['order_id'],i['order_item_id'],i['product_id'],i['seller_id']) for i in dr]

c.executemany("INSERT INTO 'Order_items' ('order_id', 'order_item_id', 'product_id', 'seller_id') VALUES (?,?,?,?);", to_db)

# commit and close
conn.commit()
conn.close()