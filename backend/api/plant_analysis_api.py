# plant_analysis_api.py

import logging
import sys
logging.basicConfig(
    level=logging.WARNING,
    stream=sys.stdout,
    format="%(levelname)s:%(name)s:%(message)s",
    force=True
)

from fastapi import APIRouter, HTTPException, Query
from services.pipeline_runner import process_plant_image
from backend.db.session import SessionLocal
from backend.db.models import ProcessedImage
import datetime
from fastapi.responses import JSONResponse
from backend.tasks import analyze_plant_task
from backend.celery_worker import celery_app
import boto3
import json

router = APIRouter()

S3_BUCKET = "plant-analysis-data"  
S3_IMAGE_PATH_TEMPLATE = "Sorghum_dataset/{date}/{plant_id}/{plant_id}_frame8.tif" 

@router.post("/analyze-plant/{plant_id}")
async def analyze_plant(plant_id: str, date: str):
    # Construct the S3 key for the plant image
    key = S3_IMAGE_PATH_TEMPLATE.format(date=date, plant_id=plant_id)
    task = analyze_plant_task.delay(S3_BUCKET, key)
    return {"task_id": task.id, "status": "processing started"}

@router.get("/task-status/{task_id}")
def get_task_status(task_id: str):
    task = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "state": task.state,
        "result": task.result if task.state == 'SUCCESS' else None
    }

@router.get("/plant-results/{plant_id}")
def get_plant_results(plant_id: str, date: str):
    print("REACHED /plant-results endpoint")
    s3 = boto3.client('s3', region_name='us-east-2')
    bucket = "plant-analysis-data"
    prefix = f"results/{date}/{plant_id}/"
    try:
        logging.warning(f"Listing S3 prefix: {prefix}")
        paginator = s3.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix)
        files = []
        for page in page_iterator:
            if 'Contents' in page:
                files.extend([obj['Key'] for obj in page['Contents']])
        logging.warning(f"Files found: {files}")
        result = {}
        for file in files:
            rel_path = file[len(prefix):] if file.startswith(prefix) else file
            clean_key = rel_path.replace('/', '_').replace('.png', '').replace('.json', '')
            region = 'us-east-2'
            url = f"https://{bucket}.s3.{region}.amazonaws.com/{file}"
            if file.endswith('.png'):
                result[clean_key] = url
            elif file.endswith('.json'):
                obj = s3.get_object(Bucket=bucket, Key=file)
                result[clean_key] = json.loads(obj['Body'].read().decode('utf-8'))
        return result
    except Exception as e:
        logging.error(f"Error fetching results: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Error fetching results: {str(e)}")