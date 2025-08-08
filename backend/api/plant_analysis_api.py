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
from backend.db.session import SessionLocal
from backend.db.models import ProcessedImage
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
    s3 = boto3.client('s3', region_name='us-east-2')
    bucket = "plant-analysis-data"
    prefix = f"results/{date}/{plant_id}/"
    try:
        paginator = s3.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix)
        files = []
        for page in page_iterator:
            if 'Contents' in page:
                files.extend([obj['Key'] for obj in page['Contents']])
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
                data = json.loads(obj['Body'].read().decode('utf-8'))
                result[clean_key] = data
                # If this is a *_result key, align vegetation_features and texture_features
                if clean_key.endswith('_result') and isinstance(data, dict):
                    # Vegetation features
                    if 'vegetation_indices' in data and isinstance(data['vegetation_indices'], list):
                        data['vegetation_features'] = data['vegetation_indices']
                    elif 'vegetation_indices_vegetation_features' in data and isinstance(data['vegetation_indices_vegetation_features'], list):
                        data['vegetation_features'] = data['vegetation_indices_vegetation_features']
                    # Texture features
                    if 'texture_features' in data and isinstance(data['texture_features'], list):
                        data['texture_features'] = data['texture_features']
                    elif 'texture_texture_features' in data and isinstance(data['texture_texture_features'], list):
                        data['texture_features'] = data['texture_texture_features']
                # Expose morphology traits as a flat dict for frontend compatibility
                if ('/morphology/' in file and file.endswith('_traits.json') and isinstance(data, dict)):
                    size_traits = data.get('size_traits', {}) if isinstance(data.get('size_traits', {}), dict) else {}
                    morph_traits = data.get('morphology_traits', {}) if isinstance(data.get('morphology_traits', {}), dict) else {}
                    merged = {}
                    merged.update(size_traits)
                    merged.update(morph_traits)
                    result['morphology_features'] = merged
        return result
    except Exception as e:
        logging.error(f"Error fetching results: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Error fetching results: {str(e)}")