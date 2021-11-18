SELECT COUNT(*)
FROM Sellers S, Order_items I
WHERE S.seller_id = I.seller_id