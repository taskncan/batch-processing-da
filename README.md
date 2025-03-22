# Yelp Data Processing Pipeline

This project implements a batch-processing-based data architecture for a data-intensive machine learning application, ensuring scalable, automated, and secure data handling. The system ingests, processes, aggregates, and delivers large-scale Yelp business datasets to prepare data for downstream ML applications.

## Architecture Overview

The pipeline is built as a set of isolated microservices running in Docker containers:

1. **Ingestion Service**  
   Streams raw JSON data from Yelp datasets into Kafka for scalable, real-time ingestion.

2. **Storage Service**  
   Persists data in PostgreSQL for structured queries, with S3/HDFS as a backup and scalable data lake.

3. **Processing Service**  
   Uses Apache Spark for distributed batch processing, cleaning, and aggregating data (e.g., grouping by city). Processed outputs are stored in the `data/processed/` directory. Batch jobs are orchestrated using Airflow.

4. **Delivery Service**  
   Provides a Flask-based REST API to securely serve processed data to downstream ML applications, using SSL/TLS and authentication.

## Project Structure
	├── airflow/                        
	│   ├── dags					 # DAG File (data_pipeline_dag.py)
	├── data/                        
	│   ├── raw/                     # Raw dataset files
	├── docker/                      
	│   ├── ingestion/               # Ingestion service Dockerfile
	│   ├── processing/              # Processing service Dockerfile
	│   └── delivery/                # Delivery service Dockerfile
	├── src/                         
	│   ├── common/                  # Shared utilities
	│   ├── ingestion/               # Ingestion service source code
	│   ├── processing/              # Processing service source code
	│   └── delivery/                # Delivery (API) service source code
	├── config/                      
	│   ├── kafka_config.yml         # Kafka configuration
	│   └── spark_config.yml         # Spark configuration
	├── docker-compose.yml           # Orchestrates all services
	├── .env                         # Environment variables (secrets, config)
	├── requirements.txt             # Unified Python dependencies
	└── README.md                    # R

## Getting Started

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/taskncan/batch-processing-da.git
   cd batch-processing-da
   ```
2.	Configure Environment Variables:
  Create and Update the .env file with your secrets and configuration (DB credentials, SSL keys, etc.). Do not commit this file to version control.

4.	Build and Run Containers:
     ```bash
    docker-compose up --build
    ```
5.	Access the Services:
   • API Service: http://localhost:5000/data
   • Airflow UI: http://localhost:8080 (if enabled)

Security & Best Practices
	• Secrets Management: Sensitive settings are stored in the .env file.
	• Service Isolation: Each microservice runs in its own Docker container.
	• Orchestration: Airflow automates batch processing, ensuring efficient scheduling and reproducibility.
	• Version Control: All code and infrastructure definitions are maintained via Git.
