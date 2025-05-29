API Design
==========

The API layer of the plant phenotyping application is built using FastAPI, a modern Python web framework for building APIs with Python 3.12 based on standard Python type hints. FastAPI provides high performance, easy integration with frontend frameworks, and automatic interactive API documentation.

FAST API provides a simple way to define API endpoints, request and response models, and input validation. It also supports asynchronous operations, making it suitable for handling I/O-bound tasks efficiently.

It provides a Swagger UI interface for interactive documentation and testing of the API endpoints. To access the Swagger UI, navigate to ``http://localhost:<port>/docs`` after starting the API service.

Backend API
-----------

Responsible for handling requests from the frontend and Airflow services, the backend API interacts with the storage layer to access and update data. It abstracts the data access layer and provides a single entry point for other services to interact with the storage layer.

The backend API is built using FastAPI and follows RESTful principles for defining endpoints and handling requests. It provides endpoints for CRUD operations on plant images, analysis results, and segmentation models. 

This API service comes with Pytest to allow running unit tests and integration tests for the API endpoints. The tests are located in the ``tests`` folder and can be run using the ``pytest`` command.

The backend API service is deployed as a Docker container and can be accessed at ``http://localhost:<backend_port>/api/v1`` after starting the Docker environment.

From other docker containers, the backend API can be accessed using the service name defined in the ``docker-compose.yml`` file. For example, the frontend API service can access the backend API using the URL ``http://backend-api:8000/api/v1``.

The folder ``src/api/backend`` contains the FastAPI application, routers, and models for the backend API. The ``main.py`` file defines the FastAPI application and includes the routers for different endpoints. 

For list of available routes and their descriptions, refer to the Swagger UI documentation at ``http://localhost:<backend_port>/docs``.

Frontend API
------------

The frontend API service acts as a proxy between the frontend and backend services to avoid CORS issues and provide a single entry point for the frontend to interact with the backend services. It receives requests from the frontend and forwards them to the backend API or the Airflow webserver.

The frontend API is built using FastAPI and provides endpoints for handling requests from the frontend. It includes routes for uploading plant images, fetching analysis results, and triggering plant phenotyping tasks.

The frontend API service is deployed as a Docker container and can be accessed at ``http://localhost:<frontend_port>/api/v1`` after starting the Docker environment.

From other docker containers, the frontend API can be accessed using the service name defined in the ``docker-compose.yml`` file. For example, the frontend service can access the frontend API using the URL ``http://frontend-api:8000/api/v1``.

Pay attention to the fact that when testing on the host machine, the frontend API should be accessed using the URL ``http://localhost:<frontend_port>/api/v1``. 

The folder ``src/api/frontend`` contains the FastAPI application, routers, and models for the frontend API. The ``main.py`` file defines the FastAPI application and includes the routers for different endpoints.

For list of available routes and their descriptions, refer to the Swagger UI documentation at ``http://localhost:<frontend_port>/docs``.

Helpful debugging tips:
-----------------------

- You can use curl or Postman to test the API endpoints and verify the responses.
- You can log into the backend API container using:

  .. code-block:: bash

      docker exec -it <container-name> bash

- You can check the logs of the backend API service using:

  .. code-block:: bash

      docker logs <container-name>

- You can run the tests for the backend API using:

  .. code-block:: bash

      ENVIRONMENT=test pytest src/tests/api/backend --cov=src/api/backend --cov-report=term-missing --cov-report=html
