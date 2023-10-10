import logging
import os
import sys
from datetime import datetime

from airflow import DAG
from airflow.operators.email import EmailOperator
from airflow.operators.python import PythonOperator

sys.path.append(f"{os.environ['HOME']}/PycharmProjects/Vikings")  # noqa: E402
from Data_process.jobs.scrap.norsemen import main_norsemen
from Data_process.jobs.scrap.vikings_serial import main_vikings
from Data_process.jobs.load.load_norsemen import main_load_norsemen
from Data_process.jobs.load.load_vikings import main_load_vikings

# get the airflow.task logger
task_logger = logging.getLogger("airflow.task")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 6, 27),
    'email': ['iam@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'home': f"{os.environ['HOME']}/PycharmProjects/Data_process/sample/"
}
for k, v in os.environ.items():
    task_logger.info(f'{k}={v}')

with DAG(dag_id="dag_scrap_and_load_actors",
         default_args=default_args,
         schedule_interval=None,
         tags=["my_dags"],
         ) as dag:
    task1 = PythonOperator(
        task_id="pars_norsemen",
        python_callable=main_norsemen,
        dag=dag,
    )
    task2 = PythonOperator(
        task_id="pars_vikings",
        python_callable=main_vikings,
        dag=dag,
    )
    task3 = PythonOperator(
        task_id="csv_to_parquet_processing_university",
        python_callable=main_load_norsemen,
        do_xcom_push=True,
        dag=dag,
    )
    task4 = PythonOperator(
        task_id="csv_to_parquet_processing_geo",
        python_callable=main_load_vikings,
        do_xcom_push=True,
        dag=dag,
    )

    email = EmailOperator(
        task_id='send_email',
        to='my_mail@gmail.com',
        subject='Airflow Alert',
        html_content=""" <h3>Email Test</h3> """,
        dag=dag
    )

    task1 >> task3 >> email
    task2 >> task4 >> email

