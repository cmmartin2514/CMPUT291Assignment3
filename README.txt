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
