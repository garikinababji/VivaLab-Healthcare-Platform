from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator


def start():
    print("Pipeline Started")


def process():
    print("Processing Patient Data")


def end():
    print("Pipeline Completed")


with DAG(
    dag_id="hello_airflow",
    start_date=datetime(2026, 8, 3),
    schedule=None,
    catchup=False,
    tags=["training"],
) as dag:

    start_task = PythonOperator(
        task_id="start_task",
        python_callable=start,
    )

    process_task = PythonOperator(
        task_id="process_task",
        python_callable=process,
    )

    end_task = PythonOperator(
        task_id="end_task",
        python_callable=end,
    )

    start_task >> process_task >> end_task