from diagrams import Diagram, Cluster, Edge
from diagrams.gcp.storage import GCS
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.client import Users
from diagrams.onprem.container import Docker
from diagrams.onprem.database import Mongodb
from diagrams.programming.language import Python
from diagrams.custom import Custom

output_path = "../assets/airflow_architecture_diagram"

graph_attr = {
    "splines": "polyline",  # Changed from ortho to polyline to reduce arrow rendering issues
    "nodesep": "0.8",
    "ranksep": "1.0",
    "fontsize": "14",
}

edge_attr = {
    "penwidth": "2.5",
    "fontsize": "11",
    "fontcolor": "black"
}

with Diagram("PDF Extraction Pipeline Architecture", filename=output_path,show=False, direction="LR", graph_attr=graph_attr):
    # User interaction
    user = Users("Developer")

    # Docker and Airflow Cluster
    with Cluster("Docker Compose with Airflow"):
        docker = Docker("Docker Compose")
        airflow = Airflow("Airflow")

        docker - Edge(style="dotted", color="black", **edge_attr) - airflow

    # Airflow DAG Tasks
    with Cluster("Airflow Tasks"):
        task1 = Python("1. Clone\nHugging Face Repo")
        task2 = Python("2. Extract PDFs")
        task3 = Python("3. Upload PDFs\nto GCS")
        task4 = Python("4. Process PDFs\nOpen Source")
        task5 = Python("5. Process PDFs\nClosed Source")

        task1 >> Edge(color="blue", penwidth="2.5", fontsize="11", fontcolor="black") >> task2
        task2 >> Edge(color="green", penwidth="2.5", fontsize="11", fontcolor="black") >> task3
        task3 >> Edge(color="purple", penwidth="2.5", fontsize="11", fontcolor="black") >> task4
        task3 >> Edge(color="red", penwidth="2.5", fontsize="11", fontcolor="black") >> task5

    # External Components
    hf_repo = Custom("Hugging Face Dataset","../assets/icons/hf-logo.png")
    terraform = Custom("Terraform (IaC)", "../assets/icons/terraform.png")

    # Google Cloud Platform Components
    with Cluster("Google Cloud Platform"):
        gcp_logo = Custom("", "../assets/icons/gcp-logo.png")
        gcs_bucket = GCS("Cloud Storage\nBucket")
        gcp_logo - Edge(style="invisible", color="black", **edge_attr) - gcs_bucket

    mongo_db = Mongodb("MongoDB Atlas")
    pdfco = Custom("PDF.co API","../assets/icons/pdfco.png")

    # Task dependencies
    user >> Edge(label="Trigger DAG", color="darkorange", penwidth="2.5", fontsize="11", fontcolor="black") >> airflow
    airflow >> Edge(color="brown", penwidth="2.5", fontsize="11", fontcolor="black") >> task1
    task1 << Edge(label="Clone Dataset", color="teal", penwidth="2.5", fontsize="11", fontcolor="black") << hf_repo
    terraform >> Edge(color="orange", style="dotted", label="Manage", penwidth="2.5", fontsize="11", fontcolor="black") >> gcs_bucket
    task3 >> Edge(label="Upload", color="darkgreen", penwidth="2.5", fontsize="11", fontcolor="black") >> gcs_bucket

    # Updated task4 interactions
    task4 >> Edge(label="Extract\nTables/Images", color="darkblue", penwidth="2.5", fontsize="11", fontcolor="black") >> gcs_bucket
    task4 >> Edge(label="Store JSON", color="darkblue", penwidth="2.5", fontsize="11", fontcolor="black") >> mongo_db

    # Updated task5 interactions
    task5 << Edge(label="Send PDFs", color="darkred", penwidth="2.5", fontsize="11", fontcolor="black") >> pdfco
    task5 << Edge(label="Receive\nExtracted Data", color="darkred", penwidth="2.5", fontsize="11", fontcolor="black") >> pdfco
    task5 >> Edge(label="Store Files", color="darkred", penwidth="2.5", fontsize="11", fontcolor="black") >> gcs_bucket
    task5 >> Edge(label="Store JSON", color="darkred", penwidth="2.5", fontsize="11", fontcolor="black") >> mongo_db