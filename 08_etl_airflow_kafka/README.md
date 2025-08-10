# Course 08 — ETL and Data Pipelines with Shell, Airflow and Kafka

**Status:** ✅ Completed — August 2025

---

## 🗂 Modules
1. Data Processing Techniques  
2. ETL & Data Pipelines: Tools and Techniques  
3. Building Data Pipelines using Apache Airflow  
4. Building Streaming Pipelines using Apache Kafka  
5. Final Assignment  

---

## 📚 Key Topics / Skills
- ETL processes and data pipelines  
- Shell scripting for automation  
- Orchestrating workflows with Apache Airflow  
- Building streaming data pipelines with Apache Kafka  
- Data ingestion and transformation patterns  

---

## 🏁 Final Project

The Final Assignment brought together everything learned in the course by implementing ETL workflows in **three** ways:

1. **BashOperator in Apache Airflow** (final submission used this approach)  
2. **PythonOperator in Apache Airflow**  
3. **Kafka streaming pipeline feeding MySQL**  

All relevant Python source files are stored in the **src/** subfolder.

---

## 1️⃣ BashOperator Method — dag-bash DAG

**Scenario**  
Analyze road traffic data from various toll plazas—each providing data in different formats—and consolidate it into a single CSV for downstream analytics.

**Environment Setup**  
- Create staging directory: /home/project/airflow/dags/finalassignment/staging  
- Ensure write permissions for /home/project/airflow/dags/finalassignment  
- Download dataset: tolldata.tgz into the finalassignment directory

**Airflow DAG**  
- Use **BashOperator** for all tasks in this method  
- DAG id: ETL_toll_data  
- Schedule: Daily (once)  
- Description: Apache Airflow Final Assignment  
- Default args: owner, start_date (today), email (optional), email_on_failure=True, email_on_retry=True, retries=1, retry_delay=5 minutes

**Tasks**  
- **unzip_data** — Untar tolldata.tgz into staging  
- **extract_data_from_csv** — Select: Rowid, Timestamp, Anonymized Vehicle number, Vehicle type (→ csv_data.csv)  
- **extract_data_from_tsv** — Select: Number of axles, Tollplaza id, Tollplaza code (→ tsv_data.csv)  
- **extract_data_from_fixed_width** — Select: Type of Payment code, Vehicle Code (→ fixed_width_data.csv)  
- **consolidate_data** — Merge csv_data.csv, tsv_data.csv, fixed_width_data.csv (→ extracted_data.csv) with column order:  
  Rowid, Timestamp, Anonymized Vehicle number, Vehicle type, Number of axles, Tollplaza id, Tollplaza code, Type of Payment code, Vehicle Code  
- **transform_data** — Uppercase the Vehicle type column (→ transformed_data.csv in staging)

**Task Pipeline**  
unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data >> transform_data

---

## 2️⃣ PythonOperator Method

**Scenario**  
Same ETL objective as above but implemented with pure Python functions for flexibility and easier unit testing.

**Environment Setup**  
- Create staging directory: /home/project/airflow/dags/python_etl/staging  
- Ensure write permissions for /home/project/airflow/dags/python_etl

**Python Functions** (store in **src/** and import into the DAG)  
- **download_dataset()** — Download tolldata.tgz into staging  
- **untar_dataset()** — Extract archive contents  
- **extract_data_from_csv()** — Select: Rowid, Timestamp, Anonymized Vehicle number, Vehicle type (→ csv_data.csv)  
- **extract_data_from_tsv()** — Select: Number of axles, Tollplaza id, Tollplaza code (→ tsv_data.csv)  
- **extract_data_from_fixed_width()** — Select: Type of Payment code, Vehicle Code (→ fixed_width_data.csv)  
- **consolidate_data()** — Merge the three files (→ extracted_data.csv) with column order:  
  Rowid, Timestamp, Anonymized Vehicle number, Vehicle type, Number of axles, Tollplaza id, Tollplaza code, Type of Payment code, Vehicle Code  
- **transform_data()** — Uppercase Vehicle type column (→ transformed_data.csv in staging)

**Airflow DAG**  
- DAG id: ETL_toll_data  
- Schedule: Daily (once)  
- Description: Apache Airflow Final Assignment  
- Default args: owner, start_date (today), retries=1, retry_delay=5 minutes

**Task Pipeline**  
download_dataset >> untar_dataset >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data >> transform_data

---

## 3️⃣ Kafka Streaming Method

**Scenario**  
As vehicles pass a toll plaza, records (vehicle_id, vehicle_type, toll_plaza_id, timestamp) are streamed to Kafka. Build a pipeline that consumes from Kafka and writes to MySQL.

**Kafka Setup**  
- Download Kafka 3.7.0 and extract  
- Configure KRaft: generate cluster UUID, format storage, and start server  
- Create a topic: **toll**

**MySQL Setup**  
- Start MySQL server  
- Create database: **tolldata**  
- Create table: **livetolldata(timestamp DATETIME, vehicle_id INT, vehicle_type CHAR(15), toll_plaza_id SMALLINT)**

**Dependencies**  
- kafka-python  
- mysql-connector-python==8.0.31

**Data Flow**  
- **Producer**: Download toll_traffic_generator.py (configure topic = toll) and run it to stream data  
- **Consumer**: Download streaming-data-reader.py; set TOPIC, DATABASE, USERNAME, PASSWORD to connect to MySQL; run to persist the stream into **livetolldata**

**Validation**  
- In MySQL, query top rows from tolldata.livetolldata to verify streaming ingestion

---

## Notes
- Final submission used **Airflow BashOperator** with the **dag-bash** DAG.  
- All Python helpers/utilities are organized under **src/** for clarity and reuse.  
- Screenshots for DAG args/definition/tasks/pipeline/runs were captured as part of the assignment deliverables.
