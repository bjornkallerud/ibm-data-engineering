## import packages for DAG --------------------------------------------------------------------
# DAG object to instantiate DAG
from airflow.models import DAG
# operators to write tasks
from airflow.operators.bash_operator import BashOperator
# extras to make workflow smoother
from airflow.utils.dates import days_ago
from datetime import timedelta

# define default args for the DAG -----------------------------------------------------------
default_args = {
    'owner': 'Olai',
    'start_date': days_ago(0),
    'email': ['olai@morningandevening.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# define DAG
dag = DAG(
    'ETL_toll_data',
    schedule_interval=timedelta(days=1),
    default_args=default_args,
    description='Apache Airflow Final Assignment'
)

## define tasks ---------------------------------------------------------------------------------
# unzip
unzip_data = BashOperator(
    task_id='unzip_data',
    bash_command=(
        'tar -xvzf /home/project/airflow/dags/finalassignment/tolldata.tgz '
        '-C /home/project/airflow/dags/finalassignment/staging'
    ),
    dag=dag
)

extract_data_from_csv = BashOperator(
    task_id='extract_data_from_csv',
    bash_command=(
        'cut -d"," -f1,2,3,4 '
        '/home/project/airflow/dags/finalassignment/staging/vehicle-data.csv '
        '> /home/project/airflow/dags/finalassignment/staging/csv_data.csv'
    ),
    dag=dag
)

extract_data_from_tsv = BashOperator(
    task_id='extract_data_from_tsv',
    bash_command=(
        'cut -d$\'\\t\' -f5,6,7 '
        '/home/project/airflow/dags/finalassignment/staging/tollplaza-data.tsv '
        '> /home/project/airflow/dags/finalassignment/staging/tsv_data.csv'
    ),
    dag=dag
)

extract_data_from_fixed_width = BashOperator(
    task_id='extract_data_from_fixed_width',
    bash_command=(
        'cut -c$56-58,60-65 '
        '/home/project/airflow/dags/finalassignment/staging/payment-data.txt '
        '> /home/project/airflow/dags/finalassignment/staging/fixed_width_data.csv'
    ),
    dag=dag
)

consolidate_data = BashOperator(
    task_id='consolidate_data',
    bash_command=(
        'paste -d"," '
        '/home/project/airflow/dags/finalassignment/staging/csv_data.csv '
        '/home/project/airflow/dags/finalassignment/staging/tsv_data.csv '
        '/home/project/airflow/dags/finalassignment/staging/fixed_width_data.csv '
        '> /home/project/airflow/dags/finalassignment/staging/extracted_data.csv'
    ),
    dag=dag
)

transform_data = BashOperator(
    task_id='transform_data',
    bash_command=(
        "cut -d',' -f1-3 /home/project/airflow/dags/finalassignment/staging/extracted_data.csv > /tmp/first3.csv && "
        "cut -d',' -f4 /home/project/airflow/dags/finalassignment/staging/extracted_data.csv | tr '[:lower:]' '[:upper:]' > /tmp/vehicle.csv && "
        "cut -d',' -f5- /home/project/airflow/dags/finalassignment/staging/extracted_data.csv > /tmp/lastcols.csv && "
        "paste -d',' /tmp/first3.csv /tmp/vehicle.csv /tmp/lastcols.csv > /home/project/airflow/dags/finalassignment/staging/transformed_data.csv"
    ),
    dag=dag
)

# define pipeline
unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data >> transform_data