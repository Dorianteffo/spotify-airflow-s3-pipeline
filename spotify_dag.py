from spotify_etl import etl_track, etl_album
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'dorianteffo',
    'depends_on_past': False,
    'start_date': datetime(2023, 8, 12),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'spotify_lilbaby_dag', 
    default_args = default_args, 
    description = "Extract the lil baby tracks and albums data", 
    schedule_interval='@monthly'
)

run_etl_track = PythonOperator(
    task_id = "etl_tracks_data", 
    python_callable = etl_track,
    dag = dag
)

run_etl_album = PythonOperator(
    task_id = 'etl_albums_data',
    python_callable = etl_album,
    dag=dag
)

run_etl_track >> run_etl_album