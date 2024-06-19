# Restaurant Data Warehouse Simulation

This repository contains a simulation of a Data Warehouse (DWH) for a restaurant, including Python scripts and SQL files to set up the database and populate it with sample data. The solution shows my design thinking, tool selection, and proficiency in building a functional data infrastructure. The project includes the following operations:

- **Operational Database (OLTP):** An operational database designed to handle the restaurant's transactional data.
- **Data Ingestion Service:** A service that regularly populates the operational database with data.
- **Analytical Database (OLAP):** An analytical database set up to support complex queries and data analysis.
- **Data Replication Solution:** A batch that replicates data from the operational database to the analytical database with a preferred delay.
- **Data Transformation:** Regular transformations of operational data into analytical data, including the creation and updating of fact and dimensional tables.
- **Replication Process Monitoring:** A monitoring solution to track the last runs of the replication process, displaying success/failure status and other relevant metrics.

This project is realized with PostgreSQL and Python, deployed using Docker. While not production-ready, it demonstrates a structured approach to building a functional data infrastructure within a reasonable timeframe.

## Getting Started

To set up and run the simulation on your local machine, follow these steps:

### Prerequisites

- Docker
- Python
- Git

### Clone the Repository

```bash
git clone https://github.com/rviktoria/restaurant-dwh.git
cd restaurant-dwh
```

### Docker Configuration
Navigate to the docker directory:
```bash
cd docker
```

### Start the Docker containers:
```bash
docker-compose up -d
```
This will start a PostgreSQL database instance and a Python application.
Python and SQL scripts run automatically and create the necessary databases, tables and data in the PostgreSQL databases.

### Accessing the Database
You can connect to the PostgreSQL database using any SQL client or command-line interface. Use the following connection details:

- Host: `db`
- Port: `5432`
- Username: `postgres`
- Password: `Admin!234`

### Cleaning Up
After you are done with the simulation, you can stop and remove the Docker containers:

```bash
docker-compose down
```

## Dataset Sources
The "restaurant_orders_dataset_sources" directory contains original sources from external free dataset warehouses.

- Source: https://mavenanalytics.io/data-playground 
- Title: Restaurant Orders
