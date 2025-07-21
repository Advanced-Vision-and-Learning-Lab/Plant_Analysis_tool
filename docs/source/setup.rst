Setting up the Development Environment
=====================================

The development environment is designed to separate the backend and frontend components, and to make development easy and reproducible using Docker Compose. There is no Airflow or DAG-based orchestration in this version.

Environment Variables
---------------------

Define an `.env` file in the `docker/common` directory with the required environment variables. For details, see :doc:`environment_files`.

Pre-requisites
--------------
- Docker
- Docker Compose
- [Optional] Node.js (> 22.0) for local frontend development

Frontend Development
--------------------
1. Initialize the frontend environment:
   ```bash
   cd frontend
   npm install
   ```
2. Start the frontend development server (hot-reload):
   ```bash
   npm run serve
   # or use Docker Compose for a containerized dev server
   cd ../docker/common
   docker-compose up frontend
   ```
3. Access the frontend at `http://localhost:8080` (or mapped port).

Backend Development
-------------------
1. Start the backend and all services:
   ```bash
   cd docker/common
   docker-compose up --build
   ```
2. The backend API will be available at `http://localhost:8001`.
3. The Celery worker will run in a separate container and process analysis jobs.
4. Use pgAdmin at `http://localhost:5050` to inspect the database.

Live Code Reloading
-------------------
- The Docker Compose setup mounts source code folders for live reloading and easy debugging.
- Changes to frontend or backend code will be reflected without restarting containers (except for dependency changes).


