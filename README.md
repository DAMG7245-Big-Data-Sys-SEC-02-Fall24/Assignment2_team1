
# Automating Text Extraction and Client-Facing Application Development

This project automates text extraction from PDF files and provides a client-facing application for user interaction using FastAPI and Streamlit. The project is modular, containerized, and deployed using Docker Compose. The backend handles user authentication, text extraction queries, and stores data in a PostgreSQL database, while the frontend provides an interface for users to interact with the system.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Features

- Automated text extraction from PDF files using open-source and API-based tools.
- Modular structure with separate backend (FastAPI) and frontend (Streamlit) services.
- JWT authentication for secure access to protected resources.
- PostgreSQL database integration for data storage.
- Docker Compose setup for easy containerization and deployment.

## Technologies Used

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: Streamlit
- **Text Extraction**: pypdf2 (open-source), Docparser(API-based)
- **Orchestration**: Docker, Docker Compose
- **Cloud Storage**: Google Cloud Storage (GCP Bucket)
- **Workflow Automation**: Airflow

## Project Structure

```bash
AutomatingTextExtraction/
├── airflow_pipelines/          # Airflow DAGs and text extraction scripts
├── backend/                    # FastAPI backend
├── frontend/                   # Streamlit frontend
├── database/                   # Database scripts and migrations
├── docker-compose.yml          # Docker Compose for container orchestration
└── README.md                   # Project documentation
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/AutomatingTextExtraction.git
cd AutomatingTextExtraction
```

### 2. Install dependencies with Poetry

#### Backend:

```bash
cd backend
poetry install
```

#### Frontend:

```bash
cd frontend
poetry install
```

### 3. Set up Environment Variables

Create an `.env` file in the root directory with the following environment variables:

```bash
# PostgreSQL settings
POSTGRES_USER=youruser
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=yourdatabase
POSTGRES_HOST=localhost

# FastAPI JWT settings
JWT_SECRET_KEY=yourjwtsecret

# GCP settings
GCP_BUCKET_NAME=your-gcp-bucket-name
```

### 4. Set up Google Cloud Credentials

Add your GCP credentials in the `backend/secrets/gcp_creds.json` file (make sure this file is ignored by Git).

## Usage

### 1. Run the Application with Docker Compose

```bash
docker-compose up --build
```

This will start the FastAPI backend, Streamlit frontend, and PostgreSQL database in separate containers.

### 2. Access the Application

- **FastAPI Backend**: `http://localhost:8000`
- **Streamlit Frontend**: `http://localhost:8501`

## Deployment

This project is containerized using Docker and can be deployed on any cloud platform. To deploy on a cloud platform, follow the cloud provider's instructions to deploy Docker containers.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. Make sure to follow the project's coding standards and ensure that all tests pass before submitting your PR.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
