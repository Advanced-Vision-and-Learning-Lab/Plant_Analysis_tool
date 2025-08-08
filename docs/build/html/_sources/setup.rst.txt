Setting up the Development Environment
=====================================

This section describes how to set up a development environment for the Plant Analysis Tool pipeline. The stack uses Docker Compose to orchestrate all services, including FastAPI (backend), Celery (worker), Vue.js (frontend), PostgreSQL, Redis, and pgAdmin. There is no Airflow or DAG-based orchestration in this version.

Pre-requisites
--------------
- Docker
- Docker Compose
- [Optional] Node.js (> 22.0) for local frontend development

Environment Variables
---------------------
- Copy the provided `.env.example` in `docker/common/` to `.env` and fill in the required values (see :doc:`environment_files`).
- This file configures database credentials, AWS keys, API URLs, and other settings for all services.

Backend Development
-------------------
1. Start all backend services (API, worker, database, Redis, pgAdmin) with Docker Compose:
   ```bash
   cd docker/common
   docker-compose up --build
   ```
2. The backend API will be available at `http://localhost:8001`.
3. The Celery worker will run in a separate container and process analysis jobs.
4. Use pgAdmin at `http://localhost:5050` to inspect the database.
5. Source code changes in `backend/` will be reflected automatically (except for dependency changes, which require a container restart).

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
   ```
   or use Docker Compose for a containerized dev server:
   ```bash
   cd ../docker/common
   docker-compose up frontend
   ```
3. Access the frontend at `http://localhost:8080` (or mapped port).
4. Source code changes in `frontend/` will be reflected automatically.

Live Code Reloading & Debugging
-------------------------------
- The Docker Compose setup mounts source code folders for live reloading and easy debugging.
- Changes to frontend or backend code will be reflected without restarting containers (except for dependency changes).
- Use browser developer tools and backend logs for troubleshooting.

Testing
-------
- See the :doc:`testing` section for how to write and run tests for each component.

Troubleshooting
---------------
- Ensure all required environment variables are set in `.env`.
- If a service fails to start, check the logs with:
  ```bash
  docker-compose logs <service-name>
  ```
- For persistent issues, rebuild containers:
  ```bash
  docker-compose down -v
  docker-compose up --build
  ```


