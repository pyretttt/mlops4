import os
import sys

from airflow import DAG
from airflow.operators.bash import BashOperator

import datetime as dt 

sys.path.append('/home/pyretttt/repos/mlops4')
from scripts import get_data, prepare_data, experiment

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
    get_data = get_data.run(dag_instance=dag)
    prepare_data = prepare_data.run(dag_instance=dag)
    experiment = experiment.run(dag_instance=dag)

    get_data >> prepare_data >> experiment
