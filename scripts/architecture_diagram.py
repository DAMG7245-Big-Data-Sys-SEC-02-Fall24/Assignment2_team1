from diagrams import Diagram, Cluster, Edge
from diagrams.gcp.storage import GCS
from diagrams.gcp.database import SQL
from diagrams.gcp.compute import ComputeEngine
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.client import Users
from diagrams.onprem.container import Docker
from diagrams.onprem.database import MongoDB
from diagrams.custom import Custom

output_path = "../assets/high_level_architecture_diagram_1"
graph_attr = {
    "splines": "polyline",
    "nodesep": "0.8",
    "ranksep": "1.0",
    "fontsize": "14",
}
edge_attr = {
    "penwidth": "2.0",
    "fontsize": "11",
    "fontcolor": "black"
}

with Diagram("PDF Extraction Application - High-Level Architecture", filename=output_path, show=False, direction="LR", graph_attr=graph_attr):
    user = Users("User/Developer")
    hf_repo = Custom("Hugging Face Dataset", "../assets/icons/hf-logo.png")

    # Adding Terraform logo
    tf_logo = Custom("Terraform", "../assets/icons/terraform.png")

    with Cluster("Google Cloud Platform"):
        gcp_logo = Custom("", "../assets/icons/gcp-logo.png")
        gcs_bucket = GCS("Cloud Storage\nBucket")
        cloud_sql = SQL("Cloud SQL\n(User Credentials)")
        mongodb = MongoDB("MongoDB\n(Document Storage)")

        with Cluster("VM Instance"):
            vm_instance = ComputeEngine("VM Instance")

            with Cluster("Docker Environment (Airflow)"):
                docker_airflow = Docker("Docker Compose\n(Airflow)")
                airflow = Airflow("Airflow")

            with Cluster("Docker Environment (FastAPI & Streamlit)"):
                docker_fastapi_streamlit = Docker("Docker Compose\n(FastAPI & Streamlit)")
                with Cluster("FastAPI"):
                    fastapi = Custom("FastAPI", "../assets/icons/fastapi.png")
                    summary_endpoint = Custom("Summary Endpoint", "../assets/icons/summary.png")
                    query_endpoint = Custom("Query Endpoint", "../assets/icons/query.png")
                streamlit = Custom("Streamlit", "../assets/icons/streamlit.png")

    gcp_logo - Edge(style="invisible") - gcs_bucket
    gcs_bucket - Edge(style="invisible") - cloud_sql
    cloud_sql - Edge(style="invisible") - mongodb
    mongodb - Edge(style="invisible") - vm_instance

    pdfco = Custom("PDF.co API", "../assets/icons/pdfco.png")
    openai = Custom("OpenAI API", "../assets/icons/openai.png")

    # Adding Terraform connection
    tf_logo >> Edge(label="Manages Infra", **edge_attr) >> gcp_logo

    # User interactions
    user >> Edge(label="Access Web App", **edge_attr) >> streamlit

    # Streamlit interactions
    streamlit >> Edge(label="API Requests", **edge_attr) >> fastapi

    # FastAPI interactions
    fastapi >> Edge(label="Authenticate", **edge_attr) >> cloud_sql
    fastapi >> Edge(label="Retrieve Data", **edge_attr) >> gcs_bucket
    fastapi >> Edge(label="Retrieve Documents", **edge_attr) >> mongodb

    # Endpoint interactions
    summary_endpoint >> Edge(label="Get Summary", **edge_attr) >> openai
    query_endpoint >> Edge(label="Get Answer", **edge_attr) >> openai

    # Airflow interactions
    airflow << Edge(label="Clone", **edge_attr) << hf_repo
    airflow >> Edge(label="Store/Retrieve", **edge_attr) >> gcs_bucket
    airflow << Edge(label="Process PDFs", **edge_attr) >> pdfco
    airflow >> Edge(label="Store Processed Data", **edge_attr) >> mongodb

    # Docker compose relationships
    docker_airflow - Edge(style="dotted", **edge_attr) - airflow
    docker_fastapi_streamlit - Edge(style="dotted", **edge_attr) - fastapi
    docker_fastapi_streamlit - Edge(style="dotted", **edge_attr) - streamlit

    # FastAPI internal relationships
    fastapi - Edge(style="dotted", **edge_attr) - summary_endpoint
    fastapi - Edge(style="dotted", **edge_attr) - query_endpoint
