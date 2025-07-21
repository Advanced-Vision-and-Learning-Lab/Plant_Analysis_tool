Environment Files
=================

Environment files (`.env`) are used to:
- Store sensitive information like database credentials, API keys, and region settings.
- Avoid hardcoding configuration variables in the codebase.
- Ensure portability across different environments (development, testing, production).

The main `.env` file should be placed at `docker/common/.env`.

Example `.env` file:

.. code-block:: text

    ENVIRONMENT=development

    # PostgreSQL Database
    POSTGRES_USER=dev_user
    POSTGRES_PASSWORD=dev_password
    POSTGRES_DB=pheno_dev
    DB_CONNECTION_STRING=postgresql+psycopg2://dev_user:dev_password@postgres_app_dev:5432/pheno_dev

    # pgAdmin Credentials
    PGADMIN_DEFAULT_EMAIL=admin@admin.com
    PGADMIN_DEFAULT_PASSWORD=admin

    # General Settings
    BACKEND_API_URL=http://backend-api:8001
    VUE_APP_API_BASE_URL=http://localhost:8080

    # AWS 
    AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
    AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
    S3_BUCKET_NAME=<S3_BUCKET_NAME>
    REGION=<REGION>
    AWS_DEFAULT_REGION=us-east-2

    # Redis
    REDIS_URL=redis://redis:6379/0

    # HuggingFace Token (if using models from HuggingFace Hub)
    HUGGINGFACE_TOKEN=<your_token_here>

Required Variables by Service
-----------------------------
- **Backend API:** DB_CONNECTION_STRING, AWS credentials, REDIS_URL
- **Frontend:** VUE_APP_API_BASE_URL
- **Celery Worker:** DB_CONNECTION_STRING, AWS credentials, REDIS_URL, HUGGINGFACE_TOKEN
- **pgAdmin:** PGADMIN_DEFAULT_EMAIL, PGADMIN_DEFAULT_PASSWORD