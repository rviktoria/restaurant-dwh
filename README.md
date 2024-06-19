# Restaurant Data Warehouse Simulation

This repository contains a simulation of a Data Warehouse (DWH) for a restaurant, including Python scripts and SQL files to set up the database and populate it with sample data. The solution shows my design thinking, tool selection, and proficiency in building a functional data infrastructure. The project includes the following operations:

- **Operational Database (OLTP):** An operational database designed to handle the restaurant's transactional data.
- **Data Ingestion Service:** A service that regularly populates the operational database with data.
- **Analytical Database (OLAP):** An analytical database set up to support complex queries and data analysis.
- **Data Replication Solution:** A batch that replicates data from the operational database to the analytical database with a preferred delay.
- **Data Transformation:** Regular transformations of operational data into analytical data, including the update of fact and dimensional tables.
- **Replication Process Monitoring:** A monitoring solution to track the last runs of the replication process, displaying success/failure status.

This project is realized with PostgreSQL and Python, deployed using Docker. While not production-ready, it demonstrates a structured approach to building a functional data infrastructure within a reasonable timeframe.

## Getting Started

You can use 2 options: via Docker and Manually.

## 1. To set up and run the simulation on your local machine via Docker, follow these steps:

### 1.1. Prerequisites

- Docker
- Python
- Git

### 1.2. Clone the Repository

```bash
git clone https://github.com/rviktoria/restaurant-dwh.git
cd restaurant-dwh
```

### 1.3. Docker Configuration
Navigate to the docker directory:
```bash
cd docker
```

### 1.4. Start the Docker containers:
```bash
docker-compose up -d
```
This will start a PostgreSQL database instance and a Python application.
Python and SQL scripts run automatically and create the necessary databases, tables and data in the PostgreSQL databases.

### 1.5. Accessing the Database
You can connect to the PostgreSQL database using any SQL client or command-line interface. Use the following connection details:

- Host: `db`
- Port: `5432`
- Username: `postgres`
- Password: `Admin!234`

### 1.6. Cleaning Up
After you are done with the simulation, you can stop and remove the Docker containers:

```bash
docker-compose down
```

## 2. Manual Script Execution

If you are unable to set up Docker, you can execute all scripts manually by following the order described below. This will ensure the databases and processes are set up correctly.

### 2.1. Preparing Databases for Simulation

1. **Create Operational Database:**
   ```bash
   python create_database_restaurant_db_postgres.py
   ```
2. **Create Data Warehouse Database:**
   ```bash
   python create_database_restaurant_dwh_postgres.py
   ```
3. **Create Tables in Operational Database:**
   ```bash
   psql -f create_tables_restaurant_db_postgres.sql
   ```
4. **Create Tables in Data Warehouse Database:**
   ```bash
   psql -f create_tables_restaurant_dwh_postgres.sql
   ```
5. **Create Log Table in Data Warehouse Database:**
   ```bash
   psql -f create_log_restaurant_dwh_postgres.sql
   ```
### 2.2. Data Warehouse Processes
6. **Generate New Order in Operational Database:**
   ```bash
   python generate_new_order_into_restaurant_db.py
   ```
7. **Load Staging Menu Category:**
   ```bash
   python load_staging_menu_category.py
   ```
8. **Load Staging Menu Items:**
   ```bash
   python load_staging_menu_items.py
   ```
9. **Load Staging Orders:**
   ```bash
   python load_staging_orders.py
   ```
10. **Load Staging Order Details:**
   ```bash
   python load_staging_order_details.py
   ```   
11. **Load Tables into Data Warehouse:**
   ```bash
   psql -f load_tables_restaurant_dwh_postgres.sql
   ``` 
12. **Load Dimension Date:**
   ```bash
   python load_dim_date.py
   ``` 
13. **Load Dimension Menu Category:**
   ```bash
   python load_dim_menu_category.py
   ``` 
14. **Load Dimension Menu Items:**
   ```bash
   python load_dim_menu_items.py
   ```
15. **Load Fact Orders:**
   ```bash
   python load_fact_orders.py
   ```
Follow these steps to manually set up and run the project. Each script should be executed in the order listed above to ensure proper configuration and operation.

## Dataset Sources
The "restaurant_orders_dataset_sources" directory contains original sources from external free dataset warehouses.

- Source: https://mavenanalytics.io/data-playground 
- Title: Restaurant Orders
