# Automated Plant Phenotyping Analysis

Automated Plant Phenotyping Analysis is a modular pipeline for plant image analysis, leveraging advanced workflows, image segmentation, and statistical insights to simplify phenotyping tasks.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Quick Start (Recommended: Docker/Podman)](#quick-start-recommended-dockerpodman)
- [Manual Setup (Advanced)](#manual-setup-advanced)
- [Service URLs](#service-urls)
- [Frontend: What Results to Expect](#frontend-what-results-to-expect)
- [Backend: Processes and Modules](#backend-processes-and-modules)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Contributing](#contributing)

---

## Project Overview

This project provides a full-stack solution for analyzing plant images:
- **Frontend**: A Vue.js web app for uploading images, viewing results, and interacting with the pipeline.
- **Backend**: A FastAPI server that exposes endpoints for image analysis, result retrieval, and background task management.
- **Worker**: Celery workers for running heavy image analysis tasks asynchronously.
- **Database**: PostgreSQL for storing metadata and results.
- **Redis**: Message broker for Celery.
- **Sync Service**: Periodically syncs data from S3 to the database.

---

## Project Structure

- **frontend/**: Vue.js app (user interface).
- **backend/**: FastAPI app (API endpoints, Celery tasks, DB models).
  - **api/**: FastAPI routes for plant analysis.
  - **services/**: Main image processing pipeline.
  - **db/**: Database models and session management.
- **src/**: Core image processing, feature extraction, and data loading modules.
- **services/**: Pipeline runner script for orchestrating analysis.
- **scripts/**: Utility scripts (e.g., syncing S3 data to DB).
- **docker/**: Dockerfiles and compose files for backend, frontend, and shared services.

---

## Quick Start (Recommended: Docker/Podman)

### 1. Clone the Repository
```bash
git clone git@github.com:Advanced-Vision-and-Learning-Lab/Plant_Analysis_tool.git
cd Plant_Analysis_tool/docker/common
```

### 2. Prepare Environment Variables
- Copy the provided `.env.example` (or create a `.env` file) in `docker/common/` and fill in the required values (DB credentials, AWS keys, etc).

### 3. Install Docker and Docker Compose (or Podman)
- On Ubuntu:
  ```bash
  sudo apt update
  sudo apt install docker.io docker-compose
  # Or for Podman:
  sudo apt install podman podman-compose
  ```
- For other OS, see [Docker Install Guide](https://docs.docker.com/get-docker/) and [Podman Install Guide](https://podman.io/getting-started/installation).

### 4. Build and Start All Services
```bash
docker-compose up --build
# Or, if using Podman:
podman-compose up --build
```

### 5. Access the Services
- **Frontend GUI:** [http://localhost:8080](http://localhost:8080)
- **Backend API:** [http://localhost:8001](http://localhost:8001)
- **pgAdmin (DB Admin):** [http://localhost:5050](http://localhost:5050) (default: admin@admin.com/admin)

### 6. Stopping the Services
```bash
docker-compose down
# Or
podman-compose down
```

---

## Manual Setup (Advanced)
If you prefer not to use containers, you can set up each component manually. This is only recommended for advanced users.

### 1. Prerequisites
- [Node.js 22.12+](https://nodejs.org/) (for frontend)
- [Python 3.10+](https://www.python.org/) (for backend)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)

### 2. Database Setup
- Install and start PostgreSQL.
- Create a database and user as specified in your backend config.

### 3. Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### 4. Celery Worker Setup
```bash
cd backend
source venv/bin/activate
celery -A backend.tasks worker --loglevel=info
```

### 5. Frontend Setup
```bash
cd frontend
npm install
npm run serve
```

### 6. Redis Setup
- Start Redis server (default port 6379).

### 7. (Optional) Sync Service
- To periodically sync S3 data to the database:
```bash
python scripts/sync_s3_to_db.py
```

---

## Service URLs
- **Frontend GUI:** [http://localhost:8080](http://localhost:8080) — Main user interface for uploading images and viewing results.
- **Backend API:** [http://localhost:8001](http://localhost:8001) — FastAPI endpoints for analysis and results.
- **pgAdmin:** [http://localhost:5050](http://localhost:5050) — Web UI for managing the PostgreSQL database.

---

## Frontend: What Results to Expect

When you use the frontend, you will experience:

- **Intuitive Upload & Analysis:**
  - Upload plant images for analysis (biotic/abiotic stress, plant type selection).
  - Start analysis jobs and track their progress.

- **Results Dashboard:**
  - **Image Previews:** See original, composite, mask, overlay, and segmented images for each plant.
  - **Vegetation Indices:** Visualizations (color maps) and downloadable data for indices like NDVI, GNDVI, etc.
  - **Texture Features:** Tables and charts summarizing texture analysis results.
  - **Morphology Features:** Key plant shape and size metrics, displayed in tables or charts.
  - **Downloadable Results:** Download processed images and result files (JSON, PNG) for further analysis.

- **User Experience:**
  - Responsive, modern interface with clear navigation.
  - Step-by-step workflow from upload to results.
  - Error messages and status updates for each analysis job.

---

## Backend: Processes and Modules

The backend is responsible for all data processing, analysis, and orchestration. It consists of several key modules and processes:

- **API Layer (`backend/api/`):**
  - Exposes REST endpoints for:
    - Submitting new plant image analysis jobs.
    - Checking the status of analysis tasks.
    - Retrieving results (images, features, metrics) for each plant.

- **Task Queue & Worker (`backend/tasks.py`, `backend/celery_worker.py`):**
  - Uses Celery and Redis to run heavy analysis jobs in the background.
  - Handles job queuing, progress tracking, and result storage.

- **Image Processing Pipeline (`backend/services/pipeline_runner.py`):**
  - **Image Loading:** Downloads plant images from S3.
  - **Composite Creation:** Generates composite images from raw data.
  - **Segmentation:** Uses deep learning models to segment plant regions.
  - **Vegetation Indices:** Computes and visualizes indices (NDVI, GNDVI, etc.).
  - **Texture Analysis:** Extracts texture features from segmented regions.
  - **Morphology Analysis:** Measures plant shape, size, and other morphological features.
  - **Result Storage:** Uploads processed images and feature data back to S3.

- **Database Layer (`backend/db/`):**
  - Manages metadata and links to processed results.
  - Uses SQLAlchemy for ORM and PostgreSQL as the database.

- **Sync Service (`scripts/sync_s3_to_db.py`):**
  - Periodically syncs new data from S3 to the local database for up-to-date results.

- **Configuration & Environment:**
  - All sensitive and environment-specific settings are managed via `.env` files.

---

## Features
- **Image Processing**: Color image generation, stitching, segmentation, and feature extraction.
- **Statistical Analysis**: Insightful calculations for phenotyping metrics.
- **Frontend GUI**: Intuitive interface for monitoring and interacting with the pipeline.
- **Scalable Architecture**: Modular design for ease of maintenance and scaling.
- **Async Processing**: Heavy tasks are run in the background using Celery and Redis.

---

## Tech Stack
- **Backend**: Python (FastAPI, Celery, SQLAlchemy)
- **Frontend**: Vue.js (CLI 4+)
- **Database**: PostgreSQL
- **Broker**: Redis
- **Containerization**: Docker or Podman

---

## Contributing
Refer to the [Developer Guide](https://automatedplantphenotypinganalysisdocs.readthedocs.io/en/latest/collaboration_guidelines.html) for detailed collaboration guidelines.
