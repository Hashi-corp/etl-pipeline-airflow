# ETL Pipeline with Apache Airflow

This repository focusses on building a basic ETL pipeline using **Apache Airflow** for monitoring and automating workflows.

---

## ✨ Features

- Weather monitoring for a given location
- Custom Airflow DAG for ETL operations
- Fully Dockerized setup with Airflow Web UI

---

## 📁 Project Structure

```
etl-pipeline-airflow/
├── dags/
│   └── etl_pipeline.py          
├── data/
│   ├── raw/                     
│   └── processed/               
├── plugins/
│   └── custom_operators/
│       ├── __init__.py
│       ├── extract_operator.py  
│       ├── transform_operator.py
│       └── load_operator.py    
├── docker-compose.yml          
├── requirements.txt            
└── README.md                    
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Hashi-corp/etl-pipeline-airflow.git
cd etl-pipeline-airflow
```

### 2. Start Airflow using Docker Compose

```bash
docker-compose up airflow-init
docker-compose up
```

- 🌐 Access Airflow UI: http://localhost:8080  
- 🔐 Default login:
  - Username: `airflow`
  - Password: `airflow`

### 3. Trigger the DAG

- Open the Airflow UI
- Enable and trigger the `etl_pipeline` DAG manually, or let it run on its schedule (daily)

---

## 📦 Requirements

If not using Docker, install dependencies manually:

```bash
pip install -r requirements.txt
```

Core dependencies:

- `apache-airflow`
- `docker` (optional for containerization)

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
