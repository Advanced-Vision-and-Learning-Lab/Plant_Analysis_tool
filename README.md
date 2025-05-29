# Automated Plant Phenotyping Analysis

Automated Plant Phenotyping Analysis is a modular pipeline for plant image analysis, leveraging advanced workflows, image segmentation, and statistical insights to simplify phenotyping tasks.

---

## How to Start (Step-by-Step for First-Time Users)

Follow these steps to get the project running for the first time. This guide assumes you are starting from scratch on a Linux system, but the steps are similar for Mac/Windows (see Docker/Podman docs for details).

### 1. **Check Prerequisites**
Before you begin, make sure you have the following installed:
- **Git** (for cloning the repository)
- **Docker** and **Docker Compose** (or **Podman** and **Podman Compose**)
- **Internet connection** (for downloading images and dependencies)

Check each with:
```bash
git --version
docker --version
docker-compose --version
# Or for Podman
podman --version
podman-compose --version
```
If any are missing, install them using your package manager (e.g., `sudo apt install git docker.io docker-compose`).

### 2. **Clone the Repository**
Open your terminal and run:
```bash
git clone git@github.com:Advanced-Vision-and-Learning-Lab/Plant_Analysis_tool.git
```

### 3. **Navigate to the Project Directory**
```bash
cd Plant_Analysis_tool
```

### 4. **Navigate to the Docker Compose Directory**
All Docker-related files are in `docker/common`:
```bash
cd docker/common
```

### 5. **Check Your Network and Proxy Settings**
- Ensure you have a stable internet connection.
- If you are behind a proxy or firewall, make sure Docker can access the internet (see your institution's IT guide if needed).

### 6. **Prepare Environment Variables**
Check if a `.env` file exists in `docker/common/`. If not, copy the example:
```bash
cp .env.example .env
```
- **Edit `.env****: Open `.env` in a text editor and fill in all required values:
  - Database credentials (user, password, db name)
  - AWS keys (if using S3)
  - Any other required tokens or settings
- **Double-check**: Make sure there are no blank or placeholder values left in `.env`.

### 6a. **Using the Provided env.txt File**
A template file `env.txt` is provided in `docker/common/`. To set up your environment variables:

1. Copy `env.txt` to `.env` in the same directory:
   ```bash
   cp env.txt .env
   ```
2. Open `.env` in a text editor and fill in your own values for each variable.
   - **Do NOT share your `.env` file if it contains sensitive information!**
   - The `HUGGINGFACE_TOKEN` variable is commented out for security. See below for instructions on generating your own token.

### 6b. **How to Generate a HuggingFace Token**
Some features may require a HuggingFace API token (for example, if using models from the HuggingFace Hub).

To create your own HuggingFace token:
1. Go to [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) and log in or create an account.
2. Click **New token**, give it a name, and select the appropriate scopes (usually "Read").
3. Copy the generated token.
4. In your `.env` file, add:
   ```bash
   HUGGINGFACE_TOKEN=your_huggingface_token_here
   ```
5. **Never share your HuggingFace token publicly!**

Continue with the next steps once your `.env` file is ready.

### 7. **Verify Docker Permissions**
Make sure your user can run Docker without `sudo` (optional but recommended):
```bash
docker info
```
If you get a permissions error, add your user to the docker group:
```bash
sudo usermod -aG docker $USER
# Log out and back in for changes to take effect
```

### 8. **Check for Existing Containers or Ports in Use**
- Make sure ports 8080 (frontend), 8001 (backend), 5050 (pgAdmin), and 6379 (Redis) are not already in use.
- You can check with:
```bash
sudo lsof -i :8080
sudo lsof -i :8001
sudo lsof -i :5050
sudo lsof -i :6379
```
- If any are in use, stop the conflicting service or change the port in `docker-compose.yml` and `.env`.

### 9. **(Optional) Clean Up Old Docker Containers/Images**
If you have run this project before, you may want to clean up old containers and images:
```bash
docker-compose down -v --remove-orphans
docker system prune -f
```

### 10. **Build and Start All Services**
From inside `docker/common`, run:
```bash
docker-compose up --build
# Or, if using Podman:
podman-compose up --build
```
This will build and start all services (backend, frontend, database, Redis, workers, etc.).

### 11. **Access the Application**
- **Frontend GUI:** [http://localhost:8080](http://localhost:8080)
- **Backend API:** [http://localhost:8001](http://localhost:8001)
- **pgAdmin (DB Admin):** [http://localhost:5050](http://localhost:5050) (default: admin@admin.com/admin)

### 12. **Stopping the Services**
To stop all running containers, press `Ctrl+C` in the terminal where they are running, then:
```bash
docker-compose down
# Or
podman-compose down
```

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
