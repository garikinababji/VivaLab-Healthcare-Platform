from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

from vivalab.main import main

default_args = {
    "owner": "babji",
    "retries": 1,
}


def run_pipeline():
    main()


with DAG(
    dag_id="patient_etl",
    description="VivaLab Healthcare Patient ETL Pipeline",
    start_date=datetime(2026, 8, 3),
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["vivalab", "healthcare", "patient"],
) as dag:

    patient_pipeline = PythonOperator(
        task_id="run_patient_pipeline",
        python_callable=run_pipeline,
    )