from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 3, 20),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_pipeline',
    default_args=default_args,
    description='A DAG for batch processing Yelp data',
    schedule_interval=None,  # Runs every hour
    catchup=False,  # Optional: prevents backfilling
)

ingest = BashOperator(
    task_id='ingest_data',
    bash_command='docker-compose run ingestion',
    dag=dag,
)

process = BashOperator(
    task_id='process_data',
    bash_command='docker-compose run processing',
    dag=dag,
)

deliver = BashOperator(
    task_id='deliver_data',
    bash_command='docker-compose run delivery',
    dag=dag,
)

ingest >> process >> deliver