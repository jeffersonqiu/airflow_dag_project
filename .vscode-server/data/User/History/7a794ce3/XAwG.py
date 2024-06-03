from airflow import DAG
from datetime import timedelta, datetime
from airflow.utils.dates import days_ago
import json

from airflow.operators.bash_operator import BashOperator
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'jeqiu',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=15),
}

with open('/home/ubuntu/airflow/config_api.json', 'r') as config_file:
    api_host_key = json.load(config_file)
    print(api_host_key)

# def extract_from_api(**kwargs):



# with DAG(
#     'my_first_dag',
#     default_args=default_args,
#     description='A simple tutorial DAG',
#     schedule_interval=timedelta(days=1),
#     start_date=datetime(2024, 6, 1), # Change to your start date
#     catchup=False,
# ) as dag:
#     t1 = PythonOperator(
#         task_id = 'tsk_extract_from_api', 
#         python_collable=extract_from_api,
#         op_kwargs = {'url': 'https://zillow56.p.rapidapi.com/search', 
#                      'querystring': {'location': 'houston, tx'}, 

#                      }
#     )