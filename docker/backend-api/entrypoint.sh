#!/bin/bash
set -e

echo "Current working directory: $(pwd)"
echo "Listing files in /app/backend:"
ls -l /app/backend || echo "Directory /app/backend not found."

echo "Listing files in /app/backend/db:"
ls -l /app/backend/db || echo "Directory /app/backend/db not found."

echo "Listing files in /app/backend/api:"
ls -l /app/backend/api || echo "Directory /app/backend/api not found."

echo "Listing Alembic versions (if exists):"
ls -l /app/backend/db/migrations/versions || echo "No Alembic version files found."

# Apply database migrations if needed
# echo "Running Alembic migrations..."
# alembic --config /app/backend/db/alembic.ini upgrade head

# Run the sync script before starting the backend
python /app/scripts/sync_s3_to_db.py

# Start the server
if [ "$ENVIRONMENT" = "development" ]; then
    echo "Starting in development mode..."
    exec uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
else
    echo "Starting in production mode..."
    exec uvicorn backend.main:app --host 0.0.0.0 --port 8000
fi
