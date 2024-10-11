from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from task1 import run_task
from task2 import run_extraction_task 
from task3 import run_upload_task
from task4 import run_data_extraction_task  
from task5 import run_data_extraction_task_closed

# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'Pdf_Extraction_Pipeline_test',
    default_args=default_args,
    description='A DAG to clone Hugging Face repo, extract PDFs, and process data',
)

# Define the first task (clone Hugging Face repo)
task1_operator = PythonOperator(
    task_id='clone_huggingface_repo',
    python_callable=run_task,
    dag=dag,
)

# Define the second task (extract PDFs)
task2_operator = PythonOperator(
    task_id='extract_pdfs',
    python_callable=run_extraction_task,
    dag=dag,
)

# Define the third task (upload to GCS bucket)
task3_operator = PythonOperator(
    task_id="upload_gcs_bucket",
    python_callable=run_upload_task,
    dag=dag,
)

# Define the fourth task (process and extract data)
task4_operator = PythonOperator(
    task_id="process_and_extract_data_via_opensource_tool",
    python_callable=run_data_extraction_task,
    dag=dag,
)

# Define the fourth task (process and extract data)
task5_operator = PythonOperator(
    task_id="process_and_extract_data_via_closedsource_tool",
    python_callable=run_data_extraction_task_closed,
    dag=dag,
)


# Task dependencies
task1_operator >> task2_operator >> task3_operator >> task4_operator >> task5_operator 

