-- Create a CUBE query to analyze total orders revenue by different dimensions
SELECT 
    date_key,
    menu_category_key,
    menu_item_key,
    SUM(item_price) AS total_revenue
FROM 
    restaurant.fact_orders
GROUP BY 
    CUBE (date_key, menu_category_key, menu_item_key);



-- Create a CUBE query to analyze the count of orders for each date
SELECT 
    date_key,
	order_date,
    COUNT(order_id) AS total_orders,
	SUM(item_price) AS total_revenue
FROM 
    restaurant.fact_orders
GROUP BY 
    CUBE (date_key, order_date);