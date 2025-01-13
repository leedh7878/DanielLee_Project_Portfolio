
-- 1. How many customers have a first name that starts with the letter 'J'?

SELECT * FROM Customers
WHERE first_name ILike'J%';

-- 2. What is the total number of products in each category?

SELECT category_name, COUNT(Products.category_id) AS product_count
FROM Categories LEFT JOIN Products ON Products.category_id = Categories.category_id	
GROUP BY category_name;

-- 3. What is the total number of unique products available in each store?

SELECT Stocks.store_id, COUNT(DISTINCT Stocks.product_id) AS unique_products
FROM Stocks JOIN Stores ON Stores.store_id = Stocks.store_id
WHERE Stocks.quantity > 0
GROUP BY Stocks.store_id
ORDER BY Stocks.store_id;

-- 4. Which staff members are managers, and how many staff members report to each manager?

SELECT 
    manager.staff_id AS manager_id, 
    COUNT(staff.staff_id) AS team_size
FROM Staffs AS staff JOIN Staffs AS manager ON staff.manager_id = manager.staff_id
GROUP BY manager.staff_id
HAVING COUNT(staff.staff_id) > 0
ORDER BY team_size DESC, manager_id;
 





