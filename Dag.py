from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'tu_dag',
    default_args=default_args,
    description='Ejecución de script en Docker',
    schedule_interval=timedelta(days=1),  
)

# Definir la tarea que ejecuta tu script
run_script_task = PythonOperator(
    task_id='run_script',
    python_callable=your_python_function, 
    dag=dag,
)

# Definir una tarea ficticia de finalización
end_task = DummyOperator(
    task_id='end_task',
    dag=dag,
)

# Definir el orden de ejecución de las tareas
run_script_task >> end_task
