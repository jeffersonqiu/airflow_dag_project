from airflow import DAG
from datetime import timedelta, datetime
from airflow.utils.dates import days_ago
import json
import requests
import pendulum

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'jeqiu',
    'depends_on_past': False,
    'start_date': pendulum.today('UTC').add(days=-2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=15),
}

with open('/home/ubuntu/airflow/config_api.json', 'r') as config_file:
    api_host_key = json.load(config_file)

now = datetime.now()
dt_now_string = now.strftime("%d%m%Y%H%M%S")

def extract_from_api(**kwargs):
    url = kwargs['url']
    headers = kwargs['headers']
    querystring = kwargs['querystring']
    dt_string = kwargs['date_string']
    # return headers
    response = requests.get(url, headers=headers, params=querystring)
    response_data = response.json()
    

    # Specify the output file path
    output_file_path = f"/home/ubuntu/response_data_{dt_string}.json"
    file_str = f'response_data_{dt_string}.csv'

    # Write the JSON response to a file
    with open(output_file_path, "w") as output_file:
        json.dump(response_data, output_file, indent=4)  # indent for pretty formatting

    output_list = [output_file_path, file_str]
    return output_list  


with DAG(
    'my_first_dag',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 6, 1), # Change to your start date
    catchup=False,
) as dag:
    t1 = PythonOperator(
        task_id = 'tsk_extract_from_api', 
        python_collable=extract_from_api,
        op_kwargs = {'url': 'https://zillow56.p.rapidapi.com/search', 
                     'querystring': {'location': 'houston, tx'}, 
                     'headers': api_host_key
                     }
    )

t1

