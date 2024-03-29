SET SCHEMA 'restaurant';

---------------------------------------------------------
-------------- LOAD Dimensional tables-------------------

-- load dim_date

MERGE INTO restaurant.dim_date AS target
USING restaurant.v_pre_dim_date AS source
ON target.date = source.date
WHEN MATCHED 
AND (target.year <> source.year OR
	target.month <> source.month OR
	target.day <> source.day OR
	target.month_name_eng <> source.month_name_eng OR
	target.day_name_of_week_eng <> source.day_name_of_week_eng) 
THEN
	UPDATE
	SET 
		year = source.year,
		month = source.month,
		day = source.day,
		month_name_eng = source.month_name_eng,
		day_name_of_week_eng = source.day_name_of_week_eng,
		modified_date = CURRENT_DATE,
		modified_time = CURRENT_TIME

WHEN NOT MATCHED THEN
	INSERT (date, year, month, day, month_name_eng, day_name_of_week_eng, created_date, created_time, modified_date, modified_time)
	VALUES (source.date, source.year, source.month, source.day, source.month_name_eng, source.day_name_of_week_eng, CURRENT_DATE, CURRENT_TIME, '9999-01-01', '00:00:00');


-- load dim_menu_category	
	
MERGE INTO restaurant.dim_menu_category AS target
USING restaurant.v_pre_dim_menu_category AS source 
ON target.menu_category_name_id = source.menu_category_name_id
WHEN MATCHED 
AND (target.menu_category_name_eng <> source.menu_category_name_eng)
THEN
	UPDATE 
	SET 
		menu_category_name_eng = source.menu_category_name_eng,
		modified_date = CURRENT_DATE,
		modified_time = CURRENT_TIME
		
WHEN NOT MATCHED THEN
	INSERT (menu_category_name_id, menu_category_name_eng, created_date, created_time, modified_date, modified_time)
	VALUES (source.menu_category_name_id, source.menu_category_name_eng, CURRENT_DATE, CURRENT_TIME, '9999-01-01', '00:00:00');	
	

-- load dim_menu_items		
	
MERGE INTO restaurant.dim_menu_items AS target
USING restaurant.v_pre_dim_menu_items AS source 
ON target.menu_item_name_id = source.menu_item_name_id
WHEN MATCHED 
AND (target.item_name_eng <> source.item_name_eng OR
	target.menu_category_name_eng <> source.menu_category_name_eng) 
THEN
	UPDATE 
	SET 
		item_name_eng = source.item_name_eng,
		menu_category_name_eng = source.menu_category_name_eng,
		modified_date = CURRENT_DATE,
		modified_time = CURRENT_TIME
		
WHEN NOT MATCHED THEN
	INSERT (menu_item_name_id, item_name_eng, item_price, menu_category_name_eng, created_date, created_time, modified_date, modified_time)
	VALUES (source.menu_item_name_id, source.item_name_eng, source.item_price, source.menu_category_name_eng, CURRENT_DATE, CURRENT_TIME, '9999-01-01', '00:00:00');	
	
	
---------------------------------------------------------
--------------------- LOAD Fact tables-------------------	

-- load fact_orders	
	
INSERT INTO restaurant.fact_orders (order_id, order_line, menu_category_key, menu_item_key, item_price, order_total_lines, order_total_price, date_key, order_date, created_date, created_time)
SELECT 
    pfo.order_id,
    pfo.order_line,
    pfo.menu_category_key,
    pfo.menu_item_key,
    pfo.item_price,
    pfo.order_total_lines,
    pfo.order_total_price,
    pfo.order_date_key,
    pfo.order_date,
    CURRENT_DATE,
    CURRENT_TIME
FROM 
    restaurant.v_pre_fact_orders AS pfo