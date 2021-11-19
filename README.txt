Group 4, CCIDS: plekach, cmmartin, cfong. Names: Paige Lekach, Claire Martin, Celine Fong. 

We declare that we did not collaborate with anyone outside our own group in this assignment


Reasoning for choices made for each query under the “User Optimized” Scenario

Query #1:

We executed the following SQL query:

    SELECT COUNT(O.order_id)
    FROM Orders O
    WHERE O.customer_id IN (SELECT C.customer_id
                            FROM Customers C
                            WHERE C.customer_postal_code = (SELECT C.customer_postal_code
                                                        FROM Customers C
                                                        ORDER BY RANDOM()
                                                        LIMIT 1));

We chose to create the indices on Customers(customer_postal_code, customer_id) and Orders(customer_id, order_id) as these are cover 
the constraints used in the where clause with the cutsomer_postal_code comparison, the where clause with the customer_id  comparison, and the select clause.

Query #2:

We created the following view:
    CREATE VIEW IF NOT EXISTS OrderSize (
        oid,
        size
    )
    AS
    SELECT O.order_id, COUNT(OI.order_id)
    FROM Orders O LEFT OUTER JOIN Order_items OI ON O.order_id = OI.order_id -- match each order with associated items, null if there are no associated items
    GROUP BY O.order_id

Which gives the size of each order in the Orders table using the items noted under that order_id in the Order_items table. If there are no items in Order_items
with the corresponding order_id, then the size of the order is listed as 0.

And then executed the following query:
    SELECT COUNT(O.order_id) as TotalOrders, SUM(OS.size) as TotalItems, SUM(OS.size)*1.0/COUNT(O.order_id) as AverageItemsPerOrder
    FROM Orders O, OrderSize OS
    WHERE (O.order_id = OS.oid)
	AND O.customer_id IN (SELECT C.customer_id
                            FROM Customers C
                            WHERE C.customer_postal_code = (SELECT C.customer_postal_code
                                                        FROM Customers C
                                                        ORDER BY RANDOM()
                                                        LIMIT 1))

We chose to keep the same indices used for the first Query #1, and additionally to tune the query used to generate the view
we chose to index the order_id attribute of the Order_size table since it used in the left outer join, and the order_id attribute of the Orders table was already
indexed since it is a primary key.

Query #3:

We executed the following SQL query:
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
                                                        LIMIT 1))

We chose to keep all of the same indexes that were used in query #2, since we are essentially executing the same query. 

Query #4:

We executed the following SQL query:

    SELECT COUNT(DISTINCT S.seller_postal_code)
    FROM Order_items I, Sellers S
    WHERE I.order_id = (SELECT order_id
                        FROM Orders
                        ORDER BY RANDOM()
                        LIMIT 1)
    AND I.seller_id = S.seller_id

We chose to create the indices on Order_items(order_id, seller_id), Sellers(seller_id, seller_postal_code) and Orders(order_id) as these cover
the columns that were referenced in the query WHERE clause with the order_id from both Order_items and Orders, as well as the seller_id from
both Sellers and Order_items and the seller_postal_code in the SELECT clause. To confirm these indices were necessary, we used SQLite's EXPLAIN
QUERY PLAN method to check whether SQL would use our user-defined indices. When they were outlined as in the code for Query 4, SQL stated that
it would use all 3 indices in its query plan instead of its built-in automatic indices. This showed us that our user-defined indices were in fact
more efficient than those created by SQL.
