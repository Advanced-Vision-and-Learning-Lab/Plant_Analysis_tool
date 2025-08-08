Docker Environment
=============================

Docker is used to create a consistent and reproducible environment for the plant phenotyping application. It simplifies the deployment process by encapsulating all dependencies and services within containers.

Architecture Overview
---------------------
This project uses a multi-container architecture managed by Docker Compose. The main services are:

1. **Backend API (FastAPI):**
   - Handles all API requests from the frontend and manages communication with the database and S3.
   - Exposes endpoints for image analysis, result retrieval, and task management.

2. **Celery Worker:**
   - Processes heavy image analysis tasks asynchronously in the background.
   - Communicates with the backend API and uses Redis as a message broker.

3. **Frontend (Vue.js):**
   - Provides a modern, user-friendly web interface for uploading images, starting analysis, and viewing results.

4. **PostgreSQL Database:**
   - Stores metadata and analysis results.

5. **Redis:**
   - Serves as the message broker for Celery task queues.

6. **pgAdmin:**
   - Web-based interface for managing and inspecting the PostgreSQL database.

7. **AWS S3 (external):**
   - Used for storing raw and processed images and result files.

Service Orchestration
---------------------
- All services are defined in `docker/common/docker-compose.yml`.
- Each service has its own Dockerfile and configuration files for modularity and encapsulation.
- The stack can be started or stopped with a single command:

  ```bash
  docker-compose up --build
  # To stop:
  docker-compose down
  ```

- Environment variables (DB credentials, AWS keys, etc.) are managed via `.env` in `docker/common/`.

Key Notes
---------
- The default ports are:
  - Frontend: 8080
  - Backend API: 8001
  - pgAdmin: 5050
  - Redis: 6379
- Make sure to configure your `.env` file before starting the stack.
- For more details about the Docker environment setup, refer to the :doc:`setup` part of this documentation.