Environment Files
============================

Environment files (`.env`) are used to:
- Store sensitive information like database credentials, API keys, and region settings.
- Avoid hardcoding configuration variables in the codebase.
- Ensure portability across different environments (development, testing, production).

Below is an example of an environment file for the plant phenotyping application. Please note that this file ``.env`` should be placed at ``docker/common/.env``.

.. code-block:: text

    ENVIRONMENT=development

    ## Airflow Settings

    # PostgreSQL Airflow Database (Airflow Metadata DB)
    POSTGRES_AIRFLOW_USER=airflow_user
    POSTGRES_AIRFLOW_PASSWORD=airflow_password
    POSTGRES_AIRFLOW_DB=airflow_db
    AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql://airflow_user:airflow_password@postgres_airflow:5432/airflow_db

    # Airflow Admin User
    AIRFLOW_ADMIN_USERNAME=admin
    AIRFLOW_ADMIN_FIRSTNAME=Admin
    AIRFLOW_ADMIN_LASTNAME=User
    AIRFLOW_ADMIN_EMAIL=admin@example.com
    AIRFLOW_ADMIN_PASSWORD=admin_password 
    AIRFLOW__CORE__DAGS_FOLDER=/opt/airflow/src/dags


    ## Database Settings

    # PostgreSQL App Development Database
    POSTGRES_DEV_USER=dev_user
    POSTGRES_DEV_PASSWORD=dev_password
    POSTGRES_DEV_DB=pheno_dev
    DB_DEV_CONNECTION_STRING=postgresql+psycopg2://dev_user:dev_password@postgres_app_dev:5432/pheno_dev

    # PostgreSQL App Test Database
    POSTGRES_TEST_USER=test_user
    POSTGRES_TEST_PASSWORD=test_password
    POSTGRES_TEST_DB=pheno_test
    DB_TEST_CONNECTION_STRING=postgresql+psycopg2://test_user:test_password@postgres_app_test:5432/pheno_test

    # PostgreSQL App Production Database
    POSTGRES_PROD_USER=prod_user
    POSTGRES_PROD_PASSWORD=prod_password
    POSTGRES_PROD_DB=pheno_prod
    DB_PROD_CONNECTION_STRING=postgresql+psycopg2://prod_user:prod_password@postgres_app_prod:5432/pheno_prod

    # pgAdmin Credentials
    PGADMIN_DEFAULT_EMAIL=admin@admin.com
    PGADMIN_DEFAULT_PASSWORD=admin


    ## General Settings
    API_HEALTHCHECK_URL=http://localhost:8002/health
    AIRFLOW_URL=http://airflow-webserver:8080
    PGADMIN_HEALTHCHECK_URL=http://pgadmin:5050
    BACKEND_API_URL=http://backend-api:8000
    VUE_APP_API_BASE_URL=http://localhost:8002

    # AWS 
    AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
    AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
    ROLE=<ROLE>
    S3_BUCKET_NAME=<S3_BUCKET_NAME>
    REGION=<REGION>