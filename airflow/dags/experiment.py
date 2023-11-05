import os

from airflow import DAG
from airflow.operators.bash import BashOperator

import datetime as dt 

args = {
    "owner": "admin",
    "start_date": dt.datetime(2023, 11, 5),
    "retries": 1,
    "retry_delays": dt.timedelta(minutes=1),
    "depends_on_past": False
}

BASE_DIR = '/home/pyretttt/repos/mlops4'
with DAG(
    dag_id='experiment', 
    default_args=args, 
    schedule_interval=None, 
    tags=['experiment', 'mobile_price']
) as dag:
    get_data = BashOperator(
        task_id='get_data',
        bash_command=f'python3 {os.path.join(BASE_DIR, "scripts", "get_data.py")}',
        dag=dag
    )
    prepare_data = BashOperator(
            task_id='prepare_data',
            bash_command=f'python3 {os.path.join(BASE_DIR, "scripts", "prepare_data.py")}',
            dag=dag
    )
    experiment = BashOperator(
            task_id='experiment',
            bash_command=f'python3 {os.path.join(BASE_DIR, "scripts", "experiment.py")}',
            dag=dag
    )
                

    get_data >> prepare_data >> experiment
