# Setting Up and Explaining Airflow Pipeline


# Fetching `docker-compose.yaml`

To deploy Airflow on Docker Compose, fetch the `docker-compose.yaml` file using the following command:

```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.10.2/docker-compose.yaml'
```

## Services

This `docker-compose.yaml` defines several services:

- **airflow-scheduler**: Monitors tasks and DAGs, triggering task instances when dependencies are complete.
- **airflow-webserver**: Accessible at [http://localhost:8080](http://localhost:8080).
- **airflow-worker**: Executes tasks scheduled by the scheduler.
- **airflow-triggerer**: Runs an event loop for deferrable tasks.
- **airflow-init**: Initialization service.
- **postgres**: The database.
- **redis**: The broker that forwards messages from the scheduler to workers.


- **flower**: The monitoring app, available at [http://localhost:5555](http://localhost:5555).

All these services enable running Airflow with the `CeleryExecutor`. For more information, refer to the [Architecture Overview](https://airflow.apache.org/docs/apache-airflow/stable/overview.html).

## Directory Mounts

Some directories in the container are mounted, meaning their contents are synchronized between your computer and the container:

- `./dags` - Place your DAG files here.
- `./logs` - Contains task execution and scheduler logs.
- `./config` - Add custom log parsers or configure settings.
- `./plugins` - Place custom plugins here.

This file uses the latest Airflow image (`apache/airflow`). If you need additional Python or system libraries, you can build your own image.

## Initializing Environment

Before starting Airflow for the first time, you need to prepare your environment by creating necessary files, directories, and initializing the database.

### Setting the Airflow User

On Linux, ensure your host user ID is set, and the group ID is set to `0` to avoid creating files with `root` ownership in `dags`, `logs`, and `plugins` directories.

```bash
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

For other operating systems, you may see a warning that `AIRFLOW_UID` is not set. You can ignore this or manually create an `.env` file with the following content:

```bash
AIRFLOW_UID=50000
```

### Initialize the Database

On all operating systems, run database migrations and create the first user account:

```bash
docker compose up airflow-init
```

Once the initialization is complete, you should see a message like:

```
airflow-init_1       | Upgrades done
airflow-init_1       | Admin user airflow created
airflow-init_1       | 2.10.2
start_airflow-init_1 exited with code 0
```

The default account is:

- **Username**: `airflow`
- **Password**: `airflow`

## Cleaning up the Environment

This Docker Compose setup is a "quick-start" environment and not suited for production. The best way to recover from any issues is to clean up and restart from scratch:

1. Run the following command to stop and clean the environment:

    ```bash
    docker compose down --volumes --remove-orphans
    ```

2. Remove the directory containing the `docker-compose.yaml` file:

    ```bash
    rm -rf '<DIRECTORY>'
    ```

3. Re-download the `docker-compose.yaml` file and follow the guide from the beginning.

## Running Airflow

To start all services:

```bash
docker compose up -d
```

# Explaination of Project 


# PDF Extraction Pipeline with Airflow (Docker Compose)

This project implements a pipeline using Apache Airflow, Docker Compose, and Google Cloud Storage (GCS) to automate the process of downloading a dataset from Hugging Face, extracting PDF files, uploading them to GCS, and processing them to extract tables, text, and images. The extracted data is stored in MongoDB.

## Table of Contents
- [Project Structure](#project-structure)
- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
  - [1. Environment Variables](#1-environment-variables)
  - [2. Docker Setup](#2-docker-setup)
  - [3. Setup GCP and MongoDB](#3-setup-gcp-and-mongodb)
- [DAG Overview](#dag-overview)
- [Tasks](#tasks)
- [Usage](#usage)
- [License](#license)

## Project Structure

```bash
.
├── dags/
│   ├── task1.py          # Clone Hugging Face repository
│   ├── task2.py          # Extract PDFs from dataset
│   ├── task3.py          # Upload PDFs to GCS
│   ├── task4.py          # Process PDFs using open-source tools
│   └── task5.py          # Process PDFs using closed-source tools
├── config/
│   └── gcp.json          # Google Cloud credentials for GCS
├── docker-compose.yaml   # Docker Compose setup for Airflow
└── .env                  # Environment variables
```

## Features
- Clone dataset repository from Hugging Face.
- Extract PDFs from the dataset, including handling zip files.
- Upload extracted PDFs to a GCP bucket.
- Extract text, images, and tables from PDFs.
- Store extracted data in MongoDB.
- Two data extraction pipelines: open-source and closed-source API (PDF.co).

## Requirements
- Docker
- Docker Compose
- Google Cloud Storage (GCS) and a service account
- Hugging Face account with an API token
- `pdf.co` account with an API key for the closed-source tool

## Setup

### Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
AIRFLOW_UID=50000

# Hugging Face token
HF_TOKEN=your_huggingface_token

# MongoDB connection URI
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/db_name

# GCP credentials
GOOGLE_APPLICATION_CREDENTIALS=/opt/airflow/config/gcp.json

# PDF.co API Key
PDFCO_API_KEY=your_pdfco_api_key
```

### Setup GCP and MongoDB

- [Create a GCP bucket](https://cloud.google.com/storage/docs/creating-buckets).
- Ensure you have a MongoDB cluster running, either locally or on MongoDB Atlas.
- Upload your GCP service account key to `config/gcp.json`.

## Airflow Pipeline Overview

![](/assets/airflow_architecture_diagram.png)

The DAG `Pdf_Extraction_Pipeline` consists of five tasks:

1. **Clone Hugging Face Repository**  
   Downloads the dataset from Hugging Face.

2. **Extract PDFs**  
   Extracts PDFs from the dataset, including handling zip files.

3. **Upload PDFs to GCS**  
   Uploads the extracted PDFs to Google Cloud Storage.

4. **Process PDFs with Open-Source Tools**  
   Extracts text, images, and tables from PDFs using `pymupdf` and uploads them to GCS.

5. **Process PDFs with Closed-Source Tools**  
   Extracts text, tables from PDFs using the PDF.co API.

## Tasks

- **`task1.py`**: Logs in to Hugging Face, clones the dataset repository.
- **`task2.py`**: Extracts PDF files from the dataset, handling zip files.
- **`task3.py`**: Uploads extracted PDFs to a GCS bucket.
- **`task4.py`**: Processes PDFs using open-source tools to extract text, images, and tables, and saves them to GCS and MongoDB.
- **`task5.py`**: Processes PDFs using PDF.co to extract tables and text.

## Usage

Once Airflow is running in Docker, you can trigger the `Pdf_Extraction_Pipeline_test` DAG manually from the Airflow UI or schedule it to run daily. 

Monitor the task progress in the UI and check GCS and MongoDB for the uploaded data.
