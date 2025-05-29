#!/bin/bash

if [ ! -f /app/pytest.ini ]; then
    echo "[pytest]" > /app/pytest.ini
    echo "markers =" >> /app/pytest.ini
    echo "    asyncio: Mark a test as an asyncio test, requiring an event loop." >> /app/pytest.ini
    echo "pytest.ini created."
fi

# Check environment
if [ "$ENVIRONMENT" = "development" ]; then
    echo "Starting in development mode..."
    exec uvicorn src.frontend.api.main_frontend_api:app --host 0.0.0.0 --port 8000 --reload
else
    echo "Starting in production mode..."
    exec uvicorn src.frontend.api.main_frontend_api:app --host 0.0.0.0 --port 8000
fi
