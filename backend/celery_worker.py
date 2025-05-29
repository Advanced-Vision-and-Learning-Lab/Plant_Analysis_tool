from celery import Celery

celery_app = Celery(
    "plant_analysis",
    broker="redis://redis:6379/0",  # Use your Redis service name from docker-compose
    backend="redis://redis:6379/0"
)

