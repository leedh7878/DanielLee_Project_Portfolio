
--1.Total Sales by Product Category:

SELECT c.category_name, SUM(oi.quantity * p.list_price) AS total_sales
FROM Orders o
JOIN Order_Items oi ON o.order_id = oi.order_id
JOIN Products p ON oi.product_id = p.product_id
JOIN Categories c ON p.category_id = c.category_id
GROUP BY c.category_name;

--2. Average Order Value by Store:

SELECT s.store_name, AVG(total_order_value) AS avg_order_value
FROM (
    SELECT o.store_id, SUM(oi.quantity * oi.list_price) AS total_order_value
    FROM Orders o
    JOIN Order_Items oi ON o.order_id = oi.order_id
    GROUP BY o.store_id
) AS order_totals
JOIN Stores s ON order_totals.store_id = s.store_id
GROUP BY s.store_name;

--3. Total Stock Quantity by Product Brand:

SELECT b.brand_name, SUM(s.quantity) AS total_stock_quantity
FROM Stocks s
JOIN Products p ON s.product_id = p.product_id
JOIN Brands b ON p.brand_id = b.brand_id
GROUP BY b.brand_name;

--4. 


