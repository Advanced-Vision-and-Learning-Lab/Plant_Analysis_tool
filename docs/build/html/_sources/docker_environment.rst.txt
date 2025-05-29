Docker Environment
=============================

Docker is used to create a consistent and reproducible environment for the plant phenotyping application. It simplifies the deployment process by encapsulating all dependencies and services within containers.

This setup follows three tier architecture, consisting of the following components:

Services and Their Purpose
---------------------------

1. **Airflow Services (Scheduler and Webserver):**

   - **Purpose:** These services manage the execution and monitoring of Directed Acyclic Graphs(DAGs) for plant phenotyping tasks.

   - **Rationale:** Airflow simplifies the automation of complex workflows and ensures scalability by using its scheduler and web interface.

   The ``start_airflow.sh`` creates a user and initializes the database for the Airflow services.

   The role of the scheduler is to trigger tasks based on defined schedules or dependencies. The webserver provides a user interface to monitor and manage DAGs, tasks, and logs.

2. **Backend API:**
   
   - **Purpose:** This backend service manage the interaction with the storage layer (Both S3 and PostgreSQL components). Both Airflow and Frontend interact with this service to access/update the data.
   
   - **Rationale:** This service is necessary to abstract the data access layer and provide a single entry point for the other services to interact with the storage layer.

3. **Frontend API:**
   
   - **Prupose:** Receives requests from the frontend and forwards them to the backend API or the Airflow Webserver.
   - **Rationale:** This service is necessary to avoid CORS issues and to provide a single entry point for the frontend to interact with the backend services.
  
4. **Frontend (Vue.js):**
   
   - **Purpose:** Provides a graphical user interface for users to interact with the application.
   
   - **Rationale:** Vue.js is chosen for its simplicity, reactivity, and strong ecosystem, which makes it ideal for building user-friendly Single Page Applications (SPA)).

   For more information about the options considered for the frontend, refer to the :doc:`frontend_design` chapter.


4. **Databases (Dev, Test, Prod):**
   
   - **Purpose:** Separate PostgreSQL instances for development, testing, and production ensure isolated environments.
   
   - **Rationale:** This separation minimizes the risk of data corruption and allows testing and development without interfering with production.

   PostgreSQL is chosen for its robust features, reliability, and compatibility with Airflow and FastAPI.

5. **pgAdmin:**
   
   - **Purpose:** Provides a web-based interface to manage and monitor PostgreSQL databases.
   
   - **Rationale:** Makes it easier to visualize database structures and execute queries during development.

Key Notes
-----------------------------

- Each service has its own Dockerfile and configuration files to ensure modularity and encapsulation. Also, it only gets access to the parts of the repo that it needs.

- The ``docker/common/docker-compose.yml`` file orchestrates the services, volumes, and networks to create a multi-container environment. This allows for easy setup and teardown of the application stack.

For more details about the Docker environment setup, refer to the :doc:`setup` part of this documentation.