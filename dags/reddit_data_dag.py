from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime , timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id="reddit_data_dag",
    default_args=default_args,
    start_date=datetime(2024, 10, 20),
    schedule_interval= "* * * * *",  #"@daily", #  #"None",#
    catchup=False
) as dag:
    send_message_task = BashOperator(
        task_id="send_message_task",
        bash_command="cd /opt/airflow/reddit_data_pipeline && python kafka_streaming.py"
    )
    consume_message_task = BashOperator(
        task_id="consume_message_task",
        bash_command="cd /opt/airflow/reddit_data_pipeline && python cassandra_sink.py"
    )
    send_message_task >> consume_message_task

    

