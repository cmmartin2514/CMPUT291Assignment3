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
