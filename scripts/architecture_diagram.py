# # # from diagrams import Diagram, Cluster, Edge
# # # from diagrams.gcp.storage import GCS
# # # from diagrams.gcp.database import SQL
# # # from diagrams.gcp.compute import ComputeEngine
# # # from diagrams.onprem.workflow import Airflow
# # # from diagrams.onprem.client import Users
# # # from diagrams.onprem.container import Docker
# # # from diagrams.onprem.database import Mongodb
# # # from diagrams.custom import Custom

# # # output_path = "../assets/high_level_architecture_diagram"

# # # graph_attr = {
# # #     "splines": "polyline",
# # #     "nodesep": "0.8",
# # #     "ranksep": "1.0",
# # #     "fontsize": "14",
# # # }

# # # edge_attr = {
# # #     "penwidth": "2.0",
# # #     "fontsize": "11",
# # #     "fontcolor": "black"
# # # }

# # # with Diagram("PDF Extraction Pipeline - High-Level Architecture", filename=output_path, show=False, direction="LR", graph_attr=graph_attr):
# # #     user = Users("Developer")

# # #     with Cluster("Docker Environment"):
# # #         docker = Docker("Docker Compose")
# # #         airflow = Airflow("Airflow")

# # #         docker - Edge(style="dotted", **edge_attr) - airflow

# # #     hf_repo = Custom("Hugging Face Dataset", "../assets/icons/hf-logo.png")
    
# # #     with Cluster("Google Cloud Platform"):
# # #         gcp_logo = Custom("", "../assets/icons/gcp-logo.png")
# # #         gcs_bucket = GCS("Cloud Storage\nBucket")
# # #         cloud_sql = SQL("Cloud SQL")
# # #         vm_instance = ComputeEngine("VM Instance")
        
# # #         gcp_logo - Edge(style="invisible") - gcs_bucket
# # #         gcs_bucket - Edge(style="invisible") - cloud_sql
# # #         cloud_sql - Edge(style="invisible") - vm_instance

# # #     mongo_db = Mongodb("MongoDB Atlas")
# # #     pdfco = Custom("PDF.co API", "../assets/icons/pdfco.png")

# # #     user >> Edge(label="Trigger", **edge_attr) >> airflow
# # #     airflow << Edge(label="Clone", **edge_attr) << hf_repo
# # #     airflow >> Edge(label="Store/Retrieve", **edge_attr) >> gcs_bucket
# # #     airflow >> Edge(label="Store Data", **edge_attr) >> mongo_db
# # #     airflow << Edge(label="Process PDFs", **edge_attr) >> pdfco

# # from diagrams import Diagram, Cluster, Edge
# # from diagrams.gcp.storage import GCS
# # from diagrams.gcp.database import SQL
# # from diagrams.gcp.compute import ComputeEngine
# # from diagrams.onprem.workflow import Airflow
# # from diagrams.onprem.client import Users
# # from diagrams.onprem.container import Docker
# # from diagrams.custom import Custom
# # from diagrams.programming.framework import FastAPI

# # output_path = "../assets/high_level_architecture_diagram"
# # graph_attr = {
# #     "splines": "polyline",
# #     "nodesep": "0.8",
# #     "ranksep": "1.0",
# #     "fontsize": "14",
# # }
# # edge_attr = {
# #     "penwidth": "2.0",
# #     "fontsize": "11",
# #     "fontcolor": "black"
# # }

# # with Diagram("PDF Extraction Pipeline - High-Level Architecture", filename=output_path, show=False, direction="LR", graph_attr=graph_attr):
# #     user = Users("User/Developer")
    
# #     with Cluster("Docker Environment"):
# #         docker = Docker("Docker Compose")
# #         airflow = Airflow("Airflow")
# #         fastapi = FastAPI("FastAPI")
# #         docker - Edge(style="dotted", **edge_attr) - airflow

# #     hf_repo = Custom("Hugging Face Dataset", "../assets/icons/hf-logo.png")

# #     with Cluster("Google Cloud Platform"):
# #         gcp_logo = Custom("", "../assets/icons/gcp-logo.png")
# #         gcs_bucket = GCS("Cloud Storage\nBucket")
# #         cloud_sql = SQL("Cloud SQL\n(User Credentials)")
# #         vm_instance = ComputeEngine("VM Instance")
# #         gcp_logo - Edge(style="invisible") - gcs_bucket
# #         gcs_bucket - Edge(style="invisible") - cloud_sql
# #         cloud_sql - Edge(style="invisible") - vm_instance

# #     pdfco = Custom("PDF.co API", "../assets/icons/pdfco.png")

# #     # User interactions
# #     user >> Edge(label="Register/Login", **edge_attr) >> fastapi
# #     user >> Edge(label="Access APIs (with JWT)", **edge_attr) >> fastapi

# #     # FastAPI interactions
# #     fastapi >> Edge(label="Authenticate", **edge_attr) >> cloud_sql
# #     fastapi >> Edge(label="Store/Retrieve Data", **edge_attr) >> gcs_bucket

# #     # Airflow interactions
# #     airflow << Edge(label="Clone", **edge_attr) << hf_repo
# #     airflow >> Edge(label="Store/Retrieve", **edge_attr) >> gcs_bucket
# #     airflow << Edge(label="Process PDFs", **edge_attr) >> pdfco

# from diagrams import Diagram, Cluster, Edge
# from diagrams.gcp.storage import GCS
# from diagrams.gcp.database import SQL
# from diagrams.gcp.compute import ComputeEngine
# from diagrams.onprem.workflow import Airflow
# from diagrams.onprem.client import Users
# from diagrams.onprem.container import Docker
# from diagrams.custom import Custom
# from diagrams.programming.framework import FastAPI

# output_path = "../assets/high_level_architecture_diagram"
# graph_attr = {
#     "splines": "polyline",
#     "nodesep": "0.8",
#     "ranksep": "1.0",
#     "fontsize": "14",
# }
# edge_attr = {
#     "penwidth": "2.0",
#     "fontsize": "11",
#     "fontcolor": "black"
# }

# with Diagram("PDF Extraction Pipeline - High-Level Architecture", filename=output_path, show=False, direction="LR", graph_attr=graph_attr):
#     user = Users("User/Developer")
    
#     hf_repo = Custom("Hugging Face Dataset", "../assets/icons/hf-logo.png")

#     with Cluster("Google Cloud Platform"):
#         gcp_logo = Custom("", "../assets/icons/gcp-logo.png")
#         gcs_bucket = GCS("Cloud Storage\nBucket")
#         cloud_sql = SQL("Cloud SQL\n(User Credentials)")
        
#         with Cluster("VM Instance"):
#             vm_instance = ComputeEngine("VM Instance")
#             with Cluster("Docker Environment"):
#                 docker = Docker("Docker Compose")
#                 airflow = Airflow("Airflow")
#                 fastapi = FastAPI("FastAPI")
#                 docker - Edge(style="dotted", **edge_attr) - airflow
#                 docker - Edge(style="dotted", **edge_attr) - fastapi

#         gcp_logo - Edge(style="invisible") - gcs_bucket
#         gcs_bucket - Edge(style="invisible") - cloud_sql
#         cloud_sql - Edge(style="invisible") - vm_instance

#     pdfco = Custom("PDF.co API", "../assets/icons/pdfco.png")

#     # User interactions
#     user >> Edge(label="Register/Login", **edge_attr) >> fastapi
#     user >> Edge(label="Access APIs (with JWT)", **edge_attr) >> fastapi

#     # FastAPI interactions
#     fastapi >> Edge(label="Authenticate", **edge_attr) >> cloud_sql
#     fastapi >> Edge(label="Store/Retrieve Data", **edge_attr) >> gcs_bucket

#     # Airflow interactions
#     airflow << Edge(label="Clone", **edge_attr) << hf_repo
#     airflow >> Edge(label="Store/Retrieve", **edge_attr) >> gcs_bucket
#     airflow << Edge(label="Process PDFs", **edge_attr) >> pdfco

from diagrams import Diagram, Cluster, Edge
from diagrams.gcp.storage import GCS
from diagrams.gcp.database import SQL
from diagrams.gcp.compute import ComputeEngine
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.client import Users
from diagrams.onprem.container import Docker
from diagrams.custom import Custom
from diagrams.programming.framework import FastAPI

output_path = "../assets/high_level_architecture_diagram"
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

with Diagram("PDF Extraction Pipeline - High-Level Architecture", filename=output_path, show=False, direction="LR", graph_attr=graph_attr):
    user = Users("User/Developer")
    
    hf_repo = Custom("Hugging Face Dataset", "../assets/icons/hf-logo.png")

    with Cluster("Google Cloud Platform"):
        gcp_logo = Custom("", "../assets/icons/gcp-logo.png")
        gcs_bucket = GCS("Cloud Storage\nBucket")
        cloud_sql = SQL("Cloud SQL\n(User Credentials)")
        
        with Cluster("VM Instance"):
            vm_instance = ComputeEngine("VM Instance")
            with Cluster("Docker Environment"):
                docker = Docker("Docker Compose")
                airflow = Airflow("Airflow")
                with Cluster("FastAPI"):
                    fastapi = FastAPI("FastAPI")
                    summary_endpoint = Custom("Summary Endpoint", "../assets/icons/summary.jpg")
                    query_endpoint = Custom("Query Endpoint", "../assets/icons/query.png")
                    fastapi - Edge(style="dotted", **edge_attr) - summary_endpoint
                    fastapi - Edge(style="dotted", **edge_attr) - query_endpoint
                docker - Edge(style="dotted", **edge_attr) - airflow
                docker - Edge(style="dotted", **edge_attr) - fastapi

        gcp_logo - Edge(style="invisible") - gcs_bucket
        gcs_bucket - Edge(style="invisible") - cloud_sql
        cloud_sql - Edge(style="invisible") - vm_instance

    pdfco = Custom("PDF.co API", "../assets/icons/pdfco.png")
    openai = Custom("OpenAI API", "../assets/icons/openai.png")

    # User interactions
    user >> Edge(label="Register/Login", **edge_attr) >> fastapi
    user >> Edge(label="Access APIs (with JWT)", **edge_attr) >> fastapi

    # FastAPI interactions
    fastapi >> Edge(label="Authenticate", **edge_attr) >> cloud_sql
    fastapi >> Edge(label="Store/Retrieve Data", **edge_attr) >> gcs_bucket

    # Endpoint interactions
    summary_endpoint >> Edge(label="Get Summary", **edge_attr) >> openai
    query_endpoint >> Edge(label="Get Answer", **edge_attr) >> openai

    # Airflow interactions
    airflow << Edge(label="Clone", **edge_attr) << hf_repo
    airflow >> Edge(label="Store/Retrieve", **edge_attr) >> gcs_bucket
    airflow << Edge(label="Process PDFs", **edge_attr) >> pdfco