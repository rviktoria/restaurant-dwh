# Restaurant Data Warehouse Simulation

This repository contains a simulation of a Data Warehouse (DWH) for a restaurant, including Python scripts and SQL files to set up the database and populate it with sample data.

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

- Source: https://mavenanalytics.io/data-playground?page=3&pageSize=5 
- Title: Restaurant Orders
