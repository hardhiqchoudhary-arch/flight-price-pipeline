# dags/flight_pipeline_dag.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import subprocess
import sys

# -----------------------------------------------
# DEFAULT SETTINGS FOR ALL TASKS
# -----------------------------------------------
default_args = {
    'owner': 'hardhiq',
    'retries': 3,                           # retry 3 times if task fails
    'retry_delay': timedelta(minutes=5),    # wait 5 mins between retries
    'email_on_failure': False,
}

# -----------------------------------------------
# DEFINE THE DAG
# -----------------------------------------------
with DAG(
    dag_id='flight_price_pipeline',
    description='Daily pipeline: fetch flights → load to DB → run dbt → retrain model',
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule_interval='0 8 * * *',    # run every day at 8am
    catchup=False,                    # don't backfill missed runs
    tags=['flights', 'dbt', 'ml'],
) as dag:

    # -----------------------------------------------
    # TASK 1: FETCH FLIGHTS FROM API
    # -----------------------------------------------
    fetch_flights = PythonOperator(
        task_id='fetch_flights',
        python_callable=lambda: subprocess.run(
            [sys.executable, '/opt/airflow/scripts/fetch_flights.py'],
            check=True
        ),
    )

    # -----------------------------------------------
    # TASK 2: LOAD DATA INTO POSTGRESQL
    # -----------------------------------------------
    load_to_db = PythonOperator(
        task_id='load_to_db',
        python_callable=lambda: subprocess.run(
            [sys.executable, '/opt/airflow/scripts/load_to_db.py'],
            check=True
        ),
    )

    # -----------------------------------------------
    # TASK 3: RUN DBT MODELS
    # -----------------------------------------------
    run_dbt = BashOperator(
        task_id='run_dbt_models',
        bash_command='cd /opt/airflow && dbt run --profiles-dir ~/.dbt',
    )

    # -----------------------------------------------
    # TASK 4: RUN DBT TESTS
    # -----------------------------------------------
    test_dbt = BashOperator(
        task_id='test_dbt_models',
        bash_command='cd /opt/airflow && dbt test --profiles-dir ~/.dbt',
    )

    # -----------------------------------------------
    # TASK ORDER — THIS IS THE MAGIC LINE
    # -----------------------------------------------
    fetch_flights >> load_to_db >> run_dbt >> test_dbt