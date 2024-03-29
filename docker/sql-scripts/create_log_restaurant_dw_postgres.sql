-- DROP DATABASE IF EXISTS restaurant_dwh;
-- CREATE DATABASE restaurant_dwh;


-- DROP SCHEMA IF EXISTS restaurant;
-- CREATE SCHEMA restaurant;
SET SCHEMA 'restaurant';


DROP TABLE IF EXISTS restaurant.replication_logs;
CREATE TABLE restaurant.replication_logs (
    log_id SERIAL PRIMARY KEY,
    run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
	task_name TEXT,
    status VARCHAR, -- Success/Failure/Running
    records_processed INT,
    error_message TEXT
);

/*
SELECT * FROM restaurant.replication_logs;
*/