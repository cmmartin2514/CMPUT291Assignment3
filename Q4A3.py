import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import sqlite3
import time

conn = None
c = None

def connect(size):
    global conn, c
    # connect to database of given size
    conn = sqlite3.connect('./A3' + size + '.db')
    c = conn.cursor()
    return

def uninformed():
    global c, conn
    # uninformed scenario
    # create new tables without keys
    c.execute("CREATE TABLE 'CustomersNew' ('customer_id' TEXT, 'customer_postal_code' INTEGER)")
    c.execute("CREATE TABLE 'SellersNew' ('seller_id' TEXT, 'seller_postal_code' INTEGER)")
    c.execute("CREATE TABLE 'OrdersNew' ('order_id' TEXT, 'customer_id' TEXT)")
    c.execute("CREATE TABLE 'Order_itemsNew' ('order_id' TEXT, 'order_item_id' INTEGER, 'product_id' TEXT, 'seller_id' TEXT)")

    # populate new tables with contents of original
    c.execute("INSERT INTO CustomersNew SELECT customer_id, customer_postal_code FROM Customers")
    c.execute("INSERT INTO SellersNew SELECT seller_id, seller_postal_code FROM Sellers")
    c.execute("INSERT INTO OrdersNew SELECT order_id, customer_id FROM Orders")
    c.execute("INSERT INTO Order_itemsNew SELECT order_id, order_item_id, product_id, seller_id FROM Order_items")

    # swap names of tables
    c.execute("ALTER TABLE Customers RENAME TO CustomersOriginal")
    c.execute("ALTER TABLE CustomersNew RENAME TO Customers")
    c.execute("ALTER TABLE Sellers RENAME TO SellersOriginal")
    c.execute("ALTER TABLE SellersNew RENAME TO Sellers")
    c.execute("ALTER TABLE Orders RENAME TO OrdersOriginal")
    c.execute("ALTER TABLE OrdersNew RENAME TO Orders")
    c.execute("ALTER TABLE Order_items RENAME TO Order_itemsOriginal")
    c.execute("ALTER TABLE Order_itemsNew RENAME TO Order_items")

    # disable auto-indexing
    c.execute("PRAGMA automatic_index = FALSE")

    conn.commit()
    return


def self_optimized():
    global c, conn
    # self-optimized scenario
    # enable auto-indexing
    c.execute("PRAGMA automatic_index = TRUE")

    # drop altered table and rename original
    c.execute("DROP TABLE Customers")
    c.execute("ALTER TABLE CustomersOriginal RENAME TO Customers")
    c.execute("DROP TABLE Sellers")
    c.execute("ALTER TABLE SellersOriginal RENAME TO Sellers")
    c.execute("DROP TABLE Orders")
    c.execute("ALTER TABLE OrdersOriginal RENAME TO Orders")
    c.execute("DROP TABLE Order_items")
    c.execute("ALTER TABLE Order_itemsOriginal RENAME TO Order_items")

    conn.commit()

def user_optimized():
    global conn, c
    # user-optimized scenario
    # create my own indices
    c.execute("CREATE INDEX IF NOT EXISTS idx_order_items\
                ON Order_items(order_id, seller_id)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_sellers\
                ON Sellers(seller_id, seller_postal_code)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_orders\
                ON Orders(order_id)")

    conn.commit()
    return

def execute(query):
    global c, conn
    start = time.time()
    for i in range(50):
        c.execute(query)
    end = time.time()
    conn.commit()
    return (end - start)/50

def bar_chart(sc_1_values, sc_2_values, sc_3_values):
    # see matplotlib website for more details
    # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html

    width = 0.35
    labels = ["Small", "Medium", "Large"]
    
    
    fig, ax = plt.subplots()
    
    ax.bar(labels, sc_1_values, width, label='Uninformed')
    ax.bar(labels, sc_2_values, width, bottom=sc_1_values, label='Self-Optimized')
    ax.bar(labels, sc_3_values, width, bottom=[sc_1_values[i] + sc_2_values[i] for i in range(len(sc_1_values))], label='User-Optimized')
    
    ax.set_ylabel("Time in ms")
    ax.set_title("Query 4 Times by Database Size and Optimization Scenario")
    ax.legend()
    
    # save plot to file
    # we'll use passed title to give file name
    path = './Q4A3chart.png'
    plt.savefig(path)
    print('Chart saved to file {}'.format(path))
    
    # close figure so it doesn't display
    plt.close()
    return

def main():
    global conn, c
    sizes = ["Small", "Medium", "Large"]
    query = "SELECT COUNT(DISTINCT S.seller_postal_code)" \
    + " FROM Order_items I, Sellers S" \
    + " WHERE I.order_id = (SELECT order_id FROM Orders ORDER BY RANDOM() LIMIT 1)" \
    + " AND I.seller_id = S.seller_id"
    times = {"Small":[0]*3, "Medium":[0]*3, "Large":[0]*3}

    for size in sizes:
        print("Connection to the " + size + " database open")
        connect(size)
        # start with uninformed scenario
        print("Uninformed scenario " + size)
        uninformed()
        times[size][0] = execute(query)
        conn.commit()
        conn.close()
        connect(size)
        print("Self-Optimized scenario " + size)
        self_optimized()
        times[size][1] = execute(query)
        conn.commit()
        conn.close()
        connect(size)
        print("User-Optimized scenario " + size)
        user_optimized()
        times[size][2] = execute(query)
        print("Connection to the " + size + " database closed.")
        conn.commit()
        conn.close()


    print("Small: ")
    print([i for i in times["Small"]])
    print("Medium: ")
    print([i for i in times["Medium"]])
    print("Large: ")
    print([i for i in times["Large"]])

    sc_1_values = [times[i][0]*1000 for i in sizes]
    sc_2_values = [times[i][1]*1000 for i in sizes]
    sc_3_values = [times[i][2]*1000 for i in sizes]

    bar_chart(sc_1_values, sc_2_values, sc_3_values)

if __name__ == "__main__":
    main()
