Developer Guide
===============

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   docker_environment
   setup
   frontend_design
   database_design
   api_design
   environment_files
   testing
   collaboration_guidelines
   
Overview
--------
This project is a modular, containerized pipeline for plant image analysis. It uses FastAPI for the backend, Celery for background processing, Vue.js for the frontend, and Docker for orchestration. There is no Airflow or DAG-based orchestration in this version.

Architecture
------------
- **Frontend:** Vue.js SPA for user interaction, image upload, and result visualization
- **Backend:** FastAPI REST API for analysis requests, result retrieval, and orchestration
- **Worker:** Celery for running heavy image analysis tasks asynchronously
- **Database:** PostgreSQL for metadata and results
- **Storage:** AWS S3 for images and result files
- **Broker:** Redis for Celery
- **Containerization:** Docker Compose for easy setup and reproducibility

Developer Setup
---------------
1. **Clone the Repository**
   ```bash
   git clone https://github.com/Advanced-Vision-and-Learning-Lab/Plant_Analysis_tool.git
   cd Plant_Analysis_tool
   ```
2. **Configure Environment**
   - Copy and edit `.env` in `docker/common/` as needed (see README and environment_files.rst for details).
3. **Build and Start Services**
   ```bash
   cd docker/common
   docker-compose up --build
   ```
4. **Access Services**
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:8001
   - pgAdmin: http://localhost:5050

Development Workflow
--------------------
- **Backend:** Edit code in `backend/`, restart the backend container if needed.
- **Frontend:** Edit code in `frontend/`, use hot-reload for rapid development.
- **Celery Worker:** Code in `backend/` (tasks.py, pipeline_runner.py), restart worker if needed.
- **Database:** Use pgAdmin or psql for inspection.
- **Testing:** See the testing section for how to run and write tests for each component.

Contribution Guidelines
----------------------
- Use feature branches and pull requests.
- Write clear, modular, and well-documented code.
- Add or update tests in the `tests/` folder.
- Follow the collaboration guidelines in this documentation.

For more details on each component, see the following sections:
- :doc:`docker_environment`
- :doc:`setup`
- :doc:`frontend_design`
- :doc:`database_design`
- :doc:`api_design`
- :doc:`environment_files`
- :doc:`testing`
- :doc:`collaboration_guidelines`
- :doc:`collaboration_guidelines` (Usage and Supported Features, Technical Details)


