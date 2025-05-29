Setting up the Development Environment
==================================================

The development environment is flexible to seperate the backend and frontend components. The backend is managed by Airflow and the Backend API, while the frontend is managed by Vue.js and the frontend API.

It also mount some folders from the host machine to the containers to allow for live code reloading and easy debugging. You can update the frontend code and see the changes reflected in the browser without restarting the containers.

Environment Variables
---------------------

Please make sure to define an ``.env`` file in the ``docker/common`` directory with the required environment variables. For detailed information about environment variables and their configuration, please refer to :doc:`environment_files`.

Pre-requisites
--------------

* Docker
* Docker Compose
* [Optional] Node.js (> 22.0). You don't need to install Node.js if you only want to work on the backend.

For GUI Development
-------------------

   Initialize the frontend environment

   .. code-block:: bash

       cd frontend
       npm install

   This will recreate the ``src/frontend/node_modules`` folder with the required dependencies. 

   You have the option to continue development using the local machine or within the Docker container. It is highly recommended to use the Docker container to ensure consistency across all environments.

   To start the frontend development server, run the following command:

   .. code-block:: bash

       docker-compose -d up frontend

   This will start the frontend service and make it available at ``http://localhost:<frontend_port>``. You can access the frontend at this URL and see the changes reflected in the browser without restarting the container.

   Currently, the frontend definition within the docker compose file has the following:
   
   .. code-block:: yaml

       ports:
         - "3000:8080"

   This maps port 8080 from the container to port 3000 on the host machine so the frontend can be accessed at ``http://localhost:3000``.

   Please note that it might takes sometime for the frontend to be available as the dependencies are being installed and the server is being started.

   Successful start of the frontend service will show the something like below in the docker logs:

   .. code-block:: text

       2025-01-24 12:37:39  INFO  Starting development server...
       DONE  Compiled successfully in 44482ms6:38:50 PM
       2025-01-24 12:38:50 

       2025-01-24 12:38:50   App running at:
       2025-01-24 12:38:50   - Local:   http://localhost:8080/ 
       2025-01-24 12:38:50 
       2025-01-24 12:38:50   It seems you are running Vue CLI inside a container.
       2025-01-24 12:38:50   Access the dev server via http://localhost:<your container's external mapped port>/
       2025-01-24 12:38:50 
       2025-01-24 12:38:50   Note that the development build is not optimized.
       2025-01-24 12:38:50   To create a production build, run npm run build.
       2025-01-24 12:38:50

For Backend Development
-----------------------

   Typically, you will need to spin both airflow containers, backend API, test and development database containers. Current dependencies managed by the docker compose file allow running all of them simply by:

   .. code-block:: bash

       docker-compose up -d airflow-webserver

   This will start the Airflow webserver and make it available at ``http://localhost:<airflow_port>``. You can access the Airflow webserver at this URL and see the changes reflected in the browser without restarting the container.

   Also, it will start the backend API and make it available at ``http://localhost:<backend_port>``. You can access the backend API at this URL and see the changes reflected in the browser without restarting the container.

   Besides, it will start the test and development database containers. You can access the pgAdmin at ``http://localhost:<pgadmin_port>`` to manage and monitor the PostgreSQL databases.


