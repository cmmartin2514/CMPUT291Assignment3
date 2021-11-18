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

    # disabling automatic indexing
    cursor.execute(' PRAGMA automatic_index=FALSE; ')

    # creating new tables without foreign keys or primary keys
    cursor.execute("CREATE TABLE 'CustomersNew' ('customer_id' TEXT, 'customer_postal_code' INTEGER);")
    cursor.execute("CREATE TABLE 'OrdersNew' ('order_id' TEXT, 'customer_id' TEXT);")
    cursor.execute("INSERT INTO CustomersNew SELECT customer_id, customer_postal_code FROM Customers;")
    cursor.execute("INSERT INTO OrdersNew SELECT order_id, customer_id FROM Orders;")
    cursor.execute("ALTER TABLE Customers RENAME TO CustomersOriginal;")
    cursor.execute("ALTER TABLE CustomersNew RENAME TO Customers;")
    cursor.execute("ALTER TABLE Orders RENAME TO OrdersOriginal;")
    cursor.execute("ALTER TABLE OrdersNew RENAME TO Orders;")
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
    cursor.execute("CREATE INDEX CustomersIdx1 ON Customers(customer_id, customer_postal_code);")
    cursor.execute("CREATE INDEX OrdersIdx1 ON Orders(order_id, customer_id);")
    
    
    # commit the changes we have made so they are visible by any other connections
    connection.commit()
    return

def closeUniform(path):
    global connection, cursor
    connection = sqlite3.connect(path)
    cursor = connection.cursor()

    # cleaning up the tables and resetting the database
    cursor.execute("DROP TABLE Customers;")
    cursor.execute("DROP TABLE Orders;")
    cursor.execute("ALTER TABLE CustomersOriginal RENAME TO Customers;")
    cursor.execute("ALTER TABLE OrdersOriginal RENAME TO Orders;")
    
    # commiting and closing the connection
    connection.commit()
    connection.close()

def closeSelf():
    global connection, cursor

    # commiting and closing the connection
    connection.commit()
    connection.close()

def closeUser():
    global connection, cursor

    # cleaning up the indices created
    cursor.execute("DROP INDEX CustomersIdx1;")
    cursor.execute("DROP INDEX OrdersIdx1;")

    # commiting and closing the connection
    connection.commit()
    connection.close()

def executeQuery():
    global connection, cursor

    # query Q1 to execute
    query='''
    SELECT COUNT(O.order_id)
    FROM Orders O
    WHERE O.customer_id IN (SELECT C.customer_id
                            FROM Customers C
                            WHERE C.customer_postal_code = :Postal);'''
    
    # query to randomly generate 50 random postal codes
    queryRandom = '''
    SELECT C.customer_postal_code
    FROM Customers C
    ORDER BY RANDOM()
    LIMIT 50;
    '''
    queryTime = 0
    # running the query 50 times and getting the average runtime
    for x in range(50):
        cursor.execute(queryRandom)
        inputPostal = cursor.fetchall()
        secondsBefore = time.time()
        cursor.execute(query, {"Postal": inputPostal[x][0]})
        secondsAfter = time.time()
        queryTime += (secondsAfter-secondsBefore)*1000
    queryTime /= 50
    return queryTime
    
def query():
    # Uniformed Small
    connectUniformed(dbSmall)
    executionTimeUniformSmall = executeQuery()
    closeUniform(dbSmall)

    # Self-optimized Small
    connectSelfOptimized(dbSmall)
    executionTimeSelfSmall = executeQuery()
    closeSelf()

    # User-optimized Small
    connectUserOptimizied(dbSmall)
    executionTimeUserSmall = executeQuery()
    closeUser()

     # Uniformed Medium
    connectUniformed(dbMedium)
    executionTimeUniformMedium = executeQuery()
    closeUniform(dbMedium)

    # Self-optimized Medium
    connectSelfOptimized(dbMedium)
    executionTimeSelfMedium = executeQuery()
    closeSelf()

    # User-optimized Medium
    connectUserOptimizied(dbMedium)
    executionTimeUserMedium = executeQuery()
    closeUser()

     # Uniformed Large
    connectUniformed(dbLarge)
    executionTimeUniformLarge = executeQuery()
    closeUniform(dbLarge)

    # Self-optimized Large
    connectSelfOptimized(dbLarge)
    executionTimeSelfLarge = executeQuery()
    closeSelf()

    # User-optimized Large
    connectUserOptimizied(dbLarge)
    executionTimeUserLarge = executeQuery()
    closeUser()

    
    smallVals = [executionTimeUniformSmall, executionTimeSelfSmall, executionTimeUserSmall]
    mediumVals = [executionTimeUniformMedium, executionTimeSelfMedium, executionTimeUserMedium]
    largeVals = [executionTimeUniformLarge, executionTimeSelfLarge, executionTimeUserLarge]
    # passing in the execution times to generate stacked graph
    stackedBar(smallVals, mediumVals, largeVals, "Q1")

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
    ax.set_title('Database Runtimes for Q1 in ms')
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
