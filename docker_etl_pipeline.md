# Detailed Plan to Build an ETL Pipeline with Docker and Persistent Storage

## Overview
### **Workflow**:
1. **Extract**:
   - Fetch raw JSON data from API endpoints using a Python script.
   - Store raw JSON data in persistent storage (e.g., local directory).

2. **Transform**:
   - Process nested JSON data into structured CSV files using a Python script.
   - Store the processed CSV files in persistent storage.

3. **Load**:
   - Load the CSV files into a PostgreSQL table using Python scripts.

4. **Containerization**:
   - Package all Python scripts into a Docker image for deployment.

---

## **1. Extract Phase**

### Python Script to Fetch Data from APIs
Create a Python script to extract data from APIs and store it in a persistent storage location.

#### **`extract.py`**:
```python
import requests
import os
import json

# API Configuration
API_URL = "https://api.example.com/data"
RAW_JSON_DIR = "./data/raw"
os.makedirs(RAW_JSON_DIR, exist_ok=True)

# Fetch data from API
def fetch_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        output_file = os.path.join(RAW_JSON_DIR, "raw_data.json")
        with open(output_file, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Raw JSON data saved to {output_file}")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

if __name__ == "__main__":
    fetch_data()
```

---

## **2. Transform Phase**

### Python Script to Process Nested JSON and Save as CSV
Process the fetched JSON data into a structured CSV format.

#### **`transform.py`**:
```python
import json
import pandas as pd
import os

RAW_JSON_DIR = "./data/raw"
PROCESSED_CSV_DIR = "./data/processed"
os.makedirs(PROCESSED_CSV_DIR, exist_ok=True)

# Transform JSON to CSV
def transform_json_to_csv():
    input_file = os.path.join(RAW_JSON_DIR, "raw_data.json")
    output_file = os.path.join(PROCESSED_CSV_DIR, "processed_data.csv")

    with open(input_file, "r") as f:
        data = json.load(f)

    # Flatten nested JSON (adjust based on API structure)
    df = pd.json_normalize(data, sep="_")

    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"Processed CSV saved to {output_file}")

if __name__ == "__main__":
    transform_json_to_csv()
```

---

## **3. Load Phase**

### Python Script to Load CSV into PostgreSQL
Use the `psycopg2` library to load the processed CSV data into a PostgreSQL table.

#### **`load.py`**:
```python
import psycopg2
import pandas as pd
import os

# Configuration
PROCESSED_CSV_DIR = "./data/processed"
POSTGRES_CONFIG = {
    "dbname": "your_database_name",
    "user": "your_username",
    "password": "your_password",
    "host": "localhost",
    "port": 5432
}
TABLE_NAME = "your_table_name"

# Load CSV into PostgreSQL
def load_to_postgresql():
    input_file = os.path.join(PROCESSED_CSV_DIR, "processed_data.csv")
    df = pd.read_csv(input_file)

    connection = psycopg2.connect(**POSTGRES_CONFIG)
    cursor = connection.cursor()

    # Create table if not exists (basic example, adjust for your schema)
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        {', '.join([f'{col} TEXT' for col in df.columns])}
    );
    """)

    # Insert data
    for row in df.itertuples(index=False):
        cursor.execute(f"""
        INSERT INTO {TABLE_NAME} ({', '.join(df.columns)})
        VALUES ({', '.join(['%s'] * len(row))});
        """, tuple(row))

    connection.commit()
    cursor.close()
    connection.close()
    print(f"Data loaded into PostgreSQL table {TABLE_NAME}")

if __name__ == "__main__":
    load_to_postgresql()
```

---

## **4. Containerization**

### Dockerfile to Package Scripts
Create a `Dockerfile` to package the Python scripts and dependencies.

#### **`Dockerfile`**:
```dockerfile
FROM python:3.9-slim

# Set work directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set default command
CMD ["python", "entrypoint.py"]
```

### **`requirements.txt`**:
```
requests
pandas
psycopg2-binary
```

---

## **5. Persistent Storage Setup**

### Docker Compose File
Update the `docker-compose.yml` to use local storage for persistent storage and load data into PostgreSQL.

#### **`docker-compose.yml`**:
```yaml
version: '3.8'
services:
  etl_pipeline:
    build: .
    volumes:
      - ./data:/app/data
    depends_on:
      - postgres
    environment:
      - POSTGRES_USER=your_username
      - POSTGRES_PASSWORD=your_password
      - POSTGRES_DB=your_database_name
      - POSTGRES_HOST=postgres

  postgres:
    image: postgres:latest
    container_name: postgres_db
    environment:
      POSTGRES_USER: your_username
      POSTGRES_PASSWORD: your_password
      POSTGRES_DB: your_database_name
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## **6. Entrypoint Script**

### Python Entrypoint to Run All Scripts
Create an entrypoint script to call the `extract.py`, `transform.py`, and `load.py` scripts sequentially.

#### **`entrypoint.py`**:
```python
import subprocess

def run_script(script_name):
    try:
        subprocess.run(["python", script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")

if __name__ == "__main__":
    print("Starting ETL pipeline...")
    run_script("extract.py")
    run_script("transform.py")
    run_script("load.py")
    print("ETL pipeline completed successfully!")
```

---

## **7. Execution**

### Run the ETL Pipeline
1. **Build the Docker Image**:
   ```bash
   docker-compose build
   ```

2. **Run the Containers**:
   ```bash
   docker-compose up
   ```

---

This setup enables persistent storage using local storage and loads data into a PostgreSQL table. Let me know if you need further assistance! 🚀







------------------------------------------------------------------------------------



Understanding Persistent Volumes Using Local Storage
In Docker, a persistent volume ensures that data created or used by a container persists even after the container is stopped or removed. This is especially useful in an ETL pipeline to store raw data (e.g., JSON files) and processed data (e.g., CSV files). Here's how it works with local storage:

Key Components
Host Directory:

A directory on your local machine (e.g., ./data/) is mapped to a directory inside the container (e.g., /app/data/).
Data written to this directory inside the container is automatically stored on your local machine.
Docker Volume Mapping:

Use the -v option in docker run or the volumes key in docker-compose.yml to specify the mapping between the host and container directories.
How It Works
During Build:

The Docker container runs your Python scripts, saving raw JSON and processed CSV files to the /app/data directory.
Volume Mapping:

When you map a host directory (e.g., ./data) to /app/data in the container, all data written to /app/data is also saved to ./data on your host machine.
Benefits:

Data Persistence: If the container is removed, the data remains accessible in the host directory.
Easy Debugging: You can inspect the raw and processed data directly on your local machine.
Reusability: The same data can be used by other containers or applications.
Setup Example
Directory Structure
Create a data/ directory in your project to act as persistent storage:

graphql
Copy code
project/
├── data/
│   ├── raw/         # Stores raw JSON files
│   ├── processed/   # Stores processed CSV files
├── Dockerfile
├── docker-compose.yml
Docker Run Command
Use the -v flag to map the data/ directory on the host to /app/data in the container:

bash
Copy code
docker run -it -v $(pwd)/data:/app/data etl_pipeline
Docker Compose Configuration
In the docker-compose.yml file, the volumes section handles the mapping:

yaml
Copy code
services:
  etl_pipeline:
    build: .
    volumes:
      - ./data:/app/data
File Access Inside the Container
The raw JSON files are saved in /app/data/raw inside the container.
The processed CSV files are saved in /app/data/processed inside the container.
On the host machine, these files are accessible in:

./data/raw
./data/processed
Example Workflow
Run the Pipeline:

When the pipeline runs, extract.py writes raw JSON data to /app/data/raw.
transform.py reads raw JSON data from /app/data/raw and writes processed CSV data to /app/data/processed.
Inspect Data on Host:

After the container stops, you can view the raw JSON and processed CSV files directly in the data/ directory on your host machine:
bash
Copy code
ls ./data/raw
ls ./data/processed
Best Practices
Clean Directory Before Each Run:

Ensure the data/ directory is cleaned up before starting a new pipeline run to avoid overwriting or mixing old data.
bash
Copy code
rm -rf ./data/*
Use .gitignore:

Add the data/ directory to .gitignore to prevent raw and processed data files from being committed to version control.
Permission Management:

Ensure the Docker container has write permissions to the data/ directory on your host machine.