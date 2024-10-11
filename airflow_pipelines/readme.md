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
docker compose up
```
