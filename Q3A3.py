import sqlite3
import matplotlib.pyplot as plt
import time

connection = None
cursor = None
dbSmall = "./A3Small.db"
dbMedium = "./A3Medium.db"
dbLarge = "./A3Large.db"

def connectUniformed(path):
    # using global variables already defined in main method, not new variables
    global connection, cursor
    # create a connection to the sqlite3 database
    connection = sqlite3.connect(path)
    # create a cursor object which will be used to execute sql statements
    cursor = connection.cursor()

    
    # creating order_items table without foreign keys or primary keys
    cursor.execute("CREATE TABLE OrderItemsNew (order_id TEXT, order_item_id INTEGER, product_id TEXT, seller_id TEXT);")
    cursor.execute("INSERT INTO OrderItemsNew SELECT order_id, order_item_id, product_id, seller_id FROM Order_items;")

    # creating new tables without foreign keys or primary keys
    cursor.execute("CREATE TABLE 'CustomersNew' ('customer_id' TEXT, 'customer_postal_code' INTEGER);")
    cursor.execute("CREATE TABLE 'OrdersNew' ('order_id' TEXT, 'customer_id' TEXT);")
    cursor.execute("INSERT INTO CustomersNew SELECT customer_id, customer_postal_code FROM Customers;")
    cursor.execute("INSERT INTO OrdersNew SELECT order_id, customer_id FROM Orders;")
    # swap names of tables
    cursor.execute("ALTER TABLE Customers RENAME TO CustomersOriginal")
    cursor.execute("ALTER TABLE CustomersNew RENAME TO Customers")
    cursor.execute("ALTER TABLE Orders RENAME TO OrdersOriginal")
    cursor.execute("ALTER TABLE OrdersNew RENAME TO Orders")

    # disabling automatic indexing
    cursor.execute("PRAGMA automatic_index = FALSE")

    connection.commit()

    return

def connectSelfOptimized(path):
    # using global variables already defined in main method, not new variables
    global connection, cursor

    # create a connection to the sqlite3 database
    connection = sqlite3.connect(path)

    # create a cursor object which will be used to execute sql statements
    cursor = connection.cursor()
    cursor.execute(' PRAGMA automatic_index=TRUE; ')

    # commit the changes we have made so they are visible by any other connections
    connection.commit()
    return
    
def connectUserOptimizied(path):
    # using global variables already defined in main method, not new variables
    global connection, cursor

    # create a connection to the sqlite3 database
    connection = sqlite3.connect(path)

    # create a cursor object which will be used to execute sql statements
    cursor = connection.cursor()

    # Creating indexes for the customers and orders tables
    cursor.execute("CREATE INDEX IF NOT EXISTS CustomersIdx1 ON Customers(customer_postal_code, customer_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS OrdersIdx1 ON Orders(customer_id, order_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS Order_itemsIdx1 ON Order_items(order_id);")

    # commit the changes we have made so they are visible by any other connections
    connection.commit()
    return

def closeUniform():
    global connection, cursor

    # cleaning up the tables, views and resetting the database
    cursor.execute("DROP TABLE OrderItemsNew;")

    cursor.execute("DROP TABLE Customers;")
    cursor.execute("DROP TABLE Orders;")
    cursor.execute("ALTER TABLE CustomersOriginal RENAME TO Customers;")
    cursor.execute("ALTER TABLE OrdersOriginal RENAME TO Orders;")

    # commiting and closing the connection
    connection.commit()
    connection.close()

def close():
    global connection, cursor

    # commiting and closing the connection
    connection.commit()
    connection.close()

def executeQuery():
    global connection, cursor

    # query to execute
    query='''
    SELECT COUNT(O.order_id) as TotalOrders, SUM(OS.size) as TotalItems, SUM(OS.size)*1.0/COUNT(O.order_id) as AverageItemsPerOrder
    FROM Orders O, ( SELECT O.order_id as oid, COUNT(OI.order_id) as size
                    FROM Orders O LEFT OUTER JOIN Order_items OI ON O.order_id = OI.order_id -- match each order with associated items, null if there are no associated items
                    GROUP BY O.order_id) as OS
    WHERE (O.order_id = OS.oid)
	AND O.customer_id IN (SELECT C.customer_id
                            FROM Customers C
                            WHERE C.customer_postal_code = (SELECT C.customer_postal_code
                                                        FROM Customers C
                                                        ORDER BY RANDOM()
                                                        LIMIT 1))'''
    
    queryTime = 0
    secondsBefore = time.time()
    # running the query 50 times and getting the average runtime
    for x in range(50):
        cursor.execute(query)
    secondsAfter = time.time()
    queryTime += (secondsAfter-secondsBefore)*1000
    queryTime /= 50
    return queryTime


def query():
    # Uniformed Small
    connectUniformed(dbSmall)
    executionTimeUniformSmall = executeQuery()
    closeUniform()

    # Self-optimized Small
    connectSelfOptimized(dbSmall)
    executionTimeSelfSmall = executeQuery()
    close()

    # User-optimized Small
    connectUserOptimizied(dbSmall)
    executionTimeUserSmall = executeQuery()
    close()

     # Uniformed Medium
    connectUniformed(dbMedium)
    executionTimeUniformMedium = executeQuery()
    closeUniform()

    # Self-optimized Medium
    connectSelfOptimized(dbMedium)
    executionTimeSelfMedium = executeQuery()
    close()

    # User-optimized Medium
    connectUserOptimizied(dbMedium)
    executionTimeUserMedium = executeQuery()
    close()

    # Uniformed Large
    connectUniformed(dbLarge)
    executionTimeUniformLarge = executeQuery()
    closeUniform()

    # Self-optimized Large
    connectSelfOptimized(dbLarge)
    executionTimeSelfLarge = executeQuery()
    close()

    # User-optimized Large
    connectUserOptimizied(dbLarge)
    executionTimeUserLarge = executeQuery()
    close()

    smallVals = [executionTimeUniformSmall, executionTimeSelfSmall, executionTimeUserSmall]
    mediumVals = [executionTimeUniformMedium, executionTimeSelfMedium, executionTimeUserMedium]
    largeVals = [executionTimeUniformLarge, executionTimeSelfLarge, executionTimeUserLarge]

    # passing in the execution times to generate stacked graph
    stackedBar(smallVals, mediumVals, largeVals, "Q3")

def stackedBar(small, medium, large, title):
    # vals for the plots
    labels = ['SmallDB', 'MediumDB', 'LargeDB']
    uniformPlots = [small[0], medium[0], large[0]]
    selfPlots = [small[1], medium[1], large[1]]
    userPlots = [small[2], medium[2], large[2]]
    lastPlots = [selfPlots[0]+uniformPlots[0], selfPlots[1]+uniformPlots[1], selfPlots[2]+uniformPlots[2]]
    width = 0.35
    
    fig, ax = plt.subplots()
    
    ax.bar(labels, uniformPlots, width, label='Uniform')
    ax.bar(labels, selfPlots, width, bottom=uniformPlots, label='Self-Optimized')
    ax.bar(labels, userPlots, width, bottom=lastPlots, label='User-Optimized')

    ax.set_ylabel('Runtimes')
    ax.set_xlabel("Databases")
    ax.set_title('Database Runtimes for Q3 in ms')
    ax.legend()

    path = './{}A3chart.png'.format(title)
    plt.savefig(path)
    plt.close()
    return

def main():
    query()
    return

if __name__ == "__main__":
    main()