-- DROP DATABASE IF EXISTS restaurant_dwh;
-- CREATE DATABASE restaurant_dwh;


-- DROP SCHEMA IF EXISTS restaurant;
-- CREATE SCHEMA restaurant;
SET SCHEMA 'restaurant';


DROP TABLE IF EXISTS restaurant.staging_menu_category CASCADE;
CREATE TABLE restaurant.staging_menu_category (
  menu_category_id SMALLINT,
  menu_category_name VARCHAR,
  created_date DATE,
  created_time TIME(0)
);


DROP TABLE IF EXISTS restaurant.staging_menu_items CASCADE;
CREATE TABLE restaurant.staging_menu_items (
  menu_item_id SMALLINT,
  item_name VARCHAR,
  menu_category_id SMALLINT,
  price DECIMAL(5,2),
  created_date DATE,
  created_time TIME(0)
);


DROP TABLE IF EXISTS restaurant.staging_orders CASCADE;
CREATE TABLE restaurant.staging_orders (
  order_id SMALLINT,
  order_date DATE,
  order_time TIME(0),
  created_date DATE,
  created_time TIME(0)
);


DROP TABLE IF EXISTS restaurant.staging_order_details CASCADE;
CREATE TABLE restaurant.staging_order_details (
  order_details_id SMALLINT,
  order_id SMALLINT NOT NULL,
  item_id SMALLINT,
  created_date DATE,
  created_time TIME(0)
);



-- v_pre_dim_date

DROP VIEW IF EXISTS restaurant.v_pre_dim_date;
CREATE OR REPLACE VIEW restaurant.v_pre_dim_date AS

SELECT 
   d.date	
  ,DATE_PART('year', d.date)::int AS year
  ,DATE_PART('month', d.date)::int AS month
  ,DATE_PART('day', d.date)::int AS day
  ,TO_CHAR(d.date, 'Month') AS month_name_eng
  ,TO_CHAR(d.date, 'Day') AS day_name_of_week_eng
  
FROM (SELECT generate_series('2023-01-01'::date, CURRENT_DATE, '1 day')::date AS date) d;


-- v_pre_dim_menu_category

DROP VIEW IF EXISTS restaurant.v_pre_dim_menu_category;
CREATE OR REPLACE VIEW restaurant.v_pre_dim_menu_category AS

SELECT 
   menu_category_id AS menu_category_name_id
  ,COALESCE(menu_category_name, 'unknown') AS menu_category_name_eng
FROM restaurant.staging_menu_category;


-- v_pre_dim_menu_items

DROP VIEW IF EXISTS restaurant.v_pre_dim_menu_items;
CREATE OR REPLACE VIEW restaurant.v_pre_dim_menu_items AS

SELECT 
   smi.menu_item_id AS menu_item_name_id
  ,COALESCE(smi.item_name, 'unknown') AS item_name_eng
  ,COALESCE(smi.price, '0.00'::DECIMAL(5,2)) AS item_price  
  ,COALESCE(smc.menu_category_name, 'unknown') AS menu_category_name_eng
  
FROM restaurant.staging_menu_items smi
LEFT JOIN restaurant.staging_menu_category smc ON smi.menu_category_id = smc.menu_category_id;



DROP TABLE IF EXISTS restaurant.dim_date CASCADE;
CREATE TABLE restaurant.dim_date (
    date_key SERIAL PRIMARY KEY,
    date DATE,
    year INTEGER,
    month INTEGER,
    day INTEGER,
	month_name_eng VARCHAR,
    day_name_of_week_eng VARCHAR,
    created_date DATE,
    created_time TIME(0),
    modified_date DATE,
    modified_time TIME(0)
);
-- Reset the sequence to start from 0
ALTER SEQUENCE restaurant.dim_date_date_key_seq MINVALUE 0;
ALTER SEQUENCE restaurant.dim_date_date_key_seq RESTART WITH 0;

INSERT INTO restaurant.dim_date (date, year, month, day, month_name_eng, day_name_of_week_eng, created_date, created_time, modified_date, modified_time)
VALUES ('9999-01-01', 9999, 0, 0, 'unknown', 'unknown', CURRENT_DATE, CURRENT_TIME, '9999-01-01', '00:00:00');



DROP TABLE IF EXISTS restaurant.dim_menu_category CASCADE;
CREATE TABLE restaurant.dim_menu_category (
    menu_category_key SERIAL PRIMARY KEY,
	menu_category_name_id INTEGER,
    menu_category_name_eng VARCHAR,
	created_date DATE,
    created_time TIME(0),
    modified_date DATE,
    modified_time TIME(0)	
);
-- Reset the sequence to start from 0
ALTER SEQUENCE restaurant.dim_menu_category_menu_category_key_seq MINVALUE 0;
ALTER SEQUENCE restaurant.dim_menu_category_menu_category_key_seq RESTART WITH 0;

INSERT INTO restaurant.dim_menu_category (menu_category_name_id, menu_category_name_eng, created_date, created_time, modified_date, modified_time)
VALUES (0, 'unknown', CURRENT_DATE, CURRENT_TIME, '9999-01-01', '00:00:00');



DROP TABLE IF EXISTS restaurant.dim_menu_items CASCADE;
CREATE TABLE restaurant.dim_menu_items (
	menu_item_key SERIAL PRIMARY KEY,
	menu_item_name_id INTEGER,
    item_name_eng VARCHAR,
    item_price DECIMAL(5,2),
    menu_category_name_eng VARCHAR,
	created_date DATE,
    created_time TIME(0),
    modified_date DATE,
    modified_time TIME(0)
);
-- Reset the sequence to start from 0
ALTER SEQUENCE restaurant.dim_menu_items_menu_item_key_seq MINVALUE 0;
ALTER SEQUENCE restaurant.dim_menu_items_menu_item_key_seq RESTART WITH 0;

INSERT INTO restaurant.dim_menu_items (menu_item_name_id, item_name_eng, item_price, menu_category_name_eng, created_date, created_time, modified_date, modified_time)
VALUES (0, 'unknown', 0.00, 'unknown', CURRENT_DATE, CURRENT_TIME, '9999-01-01', '00:00:00');



-- v_pre_fact_orders

DROP VIEW IF EXISTS restaurant.v_pre_fact_orders;
CREATE OR REPLACE VIEW restaurant.v_pre_fact_orders AS

WITH order_totals AS (
    SELECT 
        sod.order_id, 
        SUM(dmi.item_price) AS order_total_price,
		COUNT(sod.order_id) AS order_total_lines
    FROM 
        restaurant.staging_order_details sod
    LEFT JOIN 
        restaurant.dim_menu_items dmi ON sod.item_id = dmi.menu_item_name_id 
    GROUP BY 
        sod.order_id
)

SELECT 
   so.order_id
  ,ROW_NUMBER() OVER(PARTITION BY so.order_id ORDER BY so.order_id ASC) AS order_line
  ,COALESCE(dmc.menu_category_key, 0) AS menu_category_key
  ,COALESCE(dmi.menu_item_key, 0) AS menu_item_key
  ,COALESCE(dmi.item_price, '0.00'::DECIMAL(5,2)) AS item_price
  ,ot.order_total_price
  ,ot.order_total_lines
  ,COALESCE(dd.date_key, 0) AS order_date_key
  ,COALESCE(dd.date, '9999-01-01'::DATE) AS order_date

FROM restaurant.staging_order_details sod

LEFT JOIN restaurant.staging_orders so ON sod.order_id = so.order_id
LEFT JOIN restaurant.dim_menu_items dmi ON sod.item_id = dmi.menu_item_name_id
LEFT JOIN restaurant.dim_date dd ON so.order_date = dd.date
LEFT JOIN restaurant.dim_menu_category dmc ON dmi.menu_category_name_eng = dmc.menu_category_name_eng
LEFT JOIN order_totals ot ON sod.order_id = ot.order_id;



DROP TABLE IF EXISTS restaurant.fact_orders CASCADE;
CREATE TABLE restaurant.fact_orders (
    order_details_key SERIAL PRIMARY KEY,
	order_id INTEGER,
	order_line INTEGER,
	menu_category_key INTEGER REFERENCES restaurant.dim_menu_category(menu_category_key),
	menu_item_key INTEGER REFERENCES restaurant.dim_menu_items(menu_item_key),
	item_price DECIMAL(5,2),
	order_total_lines INTEGER,
	order_total_price DECIMAL(5,2),
	date_key INTEGER REFERENCES restaurant.dim_date(date_key),
	order_date DATE,
	created_date DATE,
	created_time TIME(0)
);


/*
SELECT * FROM restaurant.staging_menu_category;
SELECT * FROM restaurant.staging_menu_items;
SELECT * FROM restaurant.staging_orders;
SELECT * FROM restaurant.staging_order_details;

SELECT * FROM restaurant.v_pre_dim_date;
SELECT * FROM restaurant.v_pre_dim_menu_category;
SELECT * FROM restaurant.v_pre_dim_menu_items;

SELECT * FROM restaurant.dim_date;
SELECT * FROM restaurant.dim_menu_category;
SELECT * FROM restaurant.dim_menu_items;

SELECT * FROM restaurant.v_pre_fact_orders;
SELECT * FROM restaurant.fact_orders;

SELECT * FROM restaurant.replication_logs;
*/