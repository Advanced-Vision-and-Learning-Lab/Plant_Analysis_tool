API Design
==========

The API layer is built using FastAPI, a modern Python web framework. It provides RESTful endpoints for all analysis and result retrieval operations, and integrates with Celery for background processing.

Key Features
------------
- RESTful endpoints for image upload, analysis, and result retrieval
- Asynchronous background processing using Celery
- Integration with AWS S3 for image storage
- Automatic API docs via Swagger UI (`/docs`)

Backend API
-----------
- Handles requests from the frontend for image analysis and result retrieval
- Triggers Celery tasks for heavy processing
- Stores and retrieves results from PostgreSQL and S3

Example Endpoints
-----------------
- `POST /api/analyze-plant/{plant_id}`: Start analysis for a plant image
- `GET /api/task-status/{task_id}`: Check the status of an analysis task
- `GET /api/plant-results/{plant_id}`: Retrieve analysis results for a plant

How to Use
----------
- Access the API docs at `http://localhost:8001/docs` for interactive testing and endpoint details.
- The frontend interacts with the backend API for all analysis and result retrieval operations.
- Developers can use tools like curl, Postman, or the Swagger UI to test endpoints.

Celery Task Flow
----------------
- When an analysis is triggered, the backend enqueues a Celery task.
- The Celery worker processes the image, runs the analysis pipeline, and stores results.
- Task status and results can be queried via the API.

Debugging Tips
--------------
- Use the Swagger UI to test endpoints and inspect responses.
- Check backend and worker logs for errors.
- Use pgAdmin to inspect the database.
