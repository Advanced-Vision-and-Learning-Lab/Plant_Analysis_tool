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
# from backend.db.session import SessionLocal
# from backend.db.models import ProcessedImage
from fastapi.responses import JSONResponse
from backend.tasks import analyze_plant_task
from backend.celery_worker import celery_app
import boto3
import json
from backend.db.session import get_db
from backend.db.models import Plant, ProcessedData, VegetationIndexTimeline, TextureTimeline, VEGETATION_INDICES, TEXTURE_FEATURES

router = APIRouter()

S3_BUCKET = "plant-analysis-data"  
S3_IMAGE_PATH_TEMPLATE = "{species}_dataset/{date}/{plant_id}/{plant_id}_frame8.tif" 
S3_RESULTS_PATH = "results/{species}_results/{plant_id}/{date}/" 

@router.post("/analyze-plant/{species}/{plant_id}")
async def analyze_plant(species: str, plant_id: str, date: str):
    # Construct the S3 key for the plant image
    key = S3_IMAGE_PATH_TEMPLATE.format(species=species, date=date, plant_id=plant_id)
    task = analyze_plant_task.delay(S3_BUCKET, key, species)
    return {"task_id": task.id, "status": "processing started"}

@router.get("/task-status/{task_id}")
def get_task_status(task_id: str):
    task = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "state": task.state,
        "result": task.result if task.state == 'SUCCESS' else None
    }

@router.get("/plant-results/{species}/{plant_id}")
def get_plant_results(species: str, plant_id: str, date: str):
    s3 = boto3.client('s3', region_name='us-east-2')
    bucket = "plant-analysis-data"
    prefix = S3_RESULTS_PATH.format(species=species, plant_id=plant_id, date=date)
    
    print(f"🔍 Looking for files in S3: bucket={bucket}, prefix={prefix}")
    
    try:
        paginator = s3.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix)
        files = []
        for page in page_iterator:
            if 'Contents' in page:
                files.extend([obj['Key'] for obj in page['Contents']])
        
        print(f"📁 Found {len(files)} files: {files}")
        
        if not files:
            print(f"⚠️ No files found for {species}_{plant_id} on {date}")
            return {"error": "No analysis results found for this plant and date"}
        
        result = {}
        for file in files:
            rel_path = file[len(prefix):] if file.startswith(prefix) else file
            clean_key = rel_path.replace('/', '_').replace('.png', '').replace('.json', '')
            region = 'us-east-2'
            url = f"https://{bucket}.s3.{region}.amazonaws.com/{file}"
            
            print(f"📄 Processing file: {file} -> clean_key: {clean_key}")
            
            if file.endswith('.png'):
                result[clean_key] = url
                print(f"🖼️ Added image: {clean_key} = {url}")
            elif file.endswith('.json'):
                obj = s3.get_object(Bucket=bucket, Key=file)
                data = json.loads(obj['Body'].read().decode('utf-8'))
                result[clean_key] = data
                print(f"📊 Added JSON data: {clean_key}")
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
        
        print(f"✅ Returning result with {len(result)} items: {list(result.keys())}")
        return result
    except Exception as e:
        print(f"❌ Error fetching results: {str(e)}")
        logging.error(f"Error fetching results: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Error fetching results: {str(e)}")


@router.get("/plant-database-data/{species}/{plant_id}")
def get_plant_database_data(species: str, plant_id: str, date: str):
    """
    Get Actual Data from Database to use in the frontend

    TODO: ADD MORPHOLOGY DATA
    """
    try:
        db = next(get_db())
        
        # Convert date string to date object
        from datetime import datetime
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        
        # Get processed data
        processed_id = f"{species}_{plant_id}_{date}"
        processed_data = db.query(ProcessedData).filter(
            ProcessedData.id == processed_id
        ).first()
        
        if not processed_data:
            raise HTTPException(status_code=404, detail="No data found for this plant and date")
        
        base_path = processed_data.image_key

        # Get main images
        main_images = {
            'original': f"{base_path}/original.png",
            'mask': f"{base_path}/mask.png", 
            'overlay': f"{base_path}/overlay.png",
            'segmented': f"{base_path}/segmented.png"
        }
        
        # Get texture data from timeline on specific date
        texture_data = db.query(TextureTimeline).filter(
            TextureTimeline.plant_id == f"{species}_{plant_id}",
            TextureTimeline.date_captured == date_obj
        ).all()

        # Get texture images
        texture_images = {}
        for texture in texture_data:
            texture_images[f"{texture.band_name}_{texture.texture_type}"] = texture.texture_image_key
        
        # Get vegetation index data from timeline on specific date
        veg_data = db.query(VegetationIndexTimeline).filter(
            VegetationIndexTimeline.plant_id == f"{species}_{plant_id}",
            VegetationIndexTimeline.date_captured == date_obj
        ).all()
        
        # Get vegetation indices images
        veg_images = {}
        for veg in veg_data:
            veg_images[veg.index_type] = veg.index_image_key
        
        # Get vegetation indices table data
        veg_table = []
        for veg in veg_data:
            veg_table.append({
                'index': veg.index_type,
                'mean': veg.mean,
                'std': veg.std,
                'min': veg.min,
                'max': veg.max,
                'q25': veg.q25,
                'median': veg.median,
                'q75': veg.q75
            })
        
        # Get texture features table data
        texture_table = []
        for texture in texture_data:
            texture_table.append({
                'feature': f"{texture.band_name}_{texture.texture_type}",
                'band': texture.band_name,
                'texture_type': texture.texture_type,
                'mean': texture.mean,
                'std': texture.std,
                'min': texture.min,
                'max': texture.max,
                'q25': texture.q25,
                'median': texture.median,
                'q75': texture.q75
            })
        
        return {
            "images": main_images,
            "texture_images": texture_images,
            "vegetation_indices_images": veg_images,
            "vegetation_indices_table": veg_table,
            "texture_features_table": texture_table
        }
        
    except Exception as e:
        print(f"Error getting plant tab data: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving tab data: {str(e)}")

@router.get("/plant-timeline/{species}/{plant_id}")
def get_plant_timeline(species: str, plant_id: str):
    """
    Get timeline data for a specific plant including vegetation indices and texture features.
    """
    try:
        # Get database session
        db = next(get_db())
        
        # Get plant data
        plant = db.query(Plant).filter(Plant.id == f"{species}_{plant_id}").first()
        if not plant:
            raise HTTPException(status_code=404, detail=f"Plant {species}_{plant_id} not found")
        
        # Get vegetation indices timeline data
        veg_timeline = db.query(VegetationIndexTimeline).filter(
            VegetationIndexTimeline.plant_id == f"{species}_{plant_id}"
        ).order_by(VegetationIndexTimeline.date_captured).all()
        
        # Get texture timeline data
        texture_timeline = db.query(TextureTimeline).filter(
            TextureTimeline.plant_id == f"{species}_{plant_id}"
        ).order_by(TextureTimeline.date_captured).all()
        
        # Get available features
        available_veg_indices = list(set([v.index_type for v in veg_timeline]))
        available_texture_features = list(set([f"{t.band_name}_{t.texture_type}" for t in texture_timeline]))
        
        # Get available dates
        available_dates = list(set([v.date_captured for v in veg_timeline] + [t.date_captured for t in texture_timeline]))
        available_dates.sort()
        
        return {
            "plant_id": f"{species}_{plant_id}",
            "species": species,
            "available_dates": [str(date) for date in available_dates],
            "available_vegetation_indices": available_veg_indices,
            "available_texture_features": available_texture_features,
            "vegetation_timeline": [
                {
                    "date": str(v.date_captured),
                    "index_type": v.index_type,
                    "mean": v.mean,
                    "median": v.median,
                    "std": v.std,
                    "q25": v.q25,
                    "q75": v.q75,
                    "min": v.min,
                    "max": v.max,
                    "image_key": v.index_image_key
                } for v in veg_timeline
            ],
            "texture_timeline": [
                {
                    "date": str(t.date_captured),
                    "band_name": t.band_name,
                    "texture_type": t.texture_type,
                    "mean": t.mean,
                    "median": t.median,
                    "std": t.std,
                    "q25": t.q25,
                    "q75": t.q75,
                    "min": t.min,
                    "max": t.max,
                    "image_key": t.texture_image_key
                } for t in texture_timeline
            ]
        }
        
    except Exception as e:
        print(f"Error getting plant timeline: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving timeline data: {str(e)}")

@router.get("/plant-timeline/{species}/{plant_id}/vegetation/{index_type}")
def get_vegetation_timeline(species: str, plant_id: str, index_type: str):
    """
    Get timeline data for a specific vegetation index.
    """
    try:
        db = next(get_db())
        
        timeline_data = db.query(VegetationIndexTimeline).filter(
            VegetationIndexTimeline.plant_id == f"{species}_{plant_id}",
            VegetationIndexTimeline.index_type == index_type
        ).order_by(VegetationIndexTimeline.date_captured).all()
        
        return {
            "plant_id": f"{species}_{plant_id}",
            "index_type": index_type,
            "timeline": [
                {
                    "date": str(v.date_captured),
                    "mean": v.mean,
                    "median": v.median,
                    "std": v.std,
                    "q25": v.q25,
                    "q75": v.q75,
                    "min": v.min,
                    "max": v.max,
                    "image_key": v.index_image_key
                } for v in timeline_data
            ]
        }
        
    except Exception as e:
        print(f"Error getting vegetation timeline: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving vegetation timeline: {str(e)}")

@router.get("/plant-timeline/{species}/{plant_id}/texture/{band_name}/{texture_type}")
def get_texture_timeline(species: str, plant_id: str, band_name: str, texture_type: str):
    """
    Get timeline data for a specific texture feature.
    """
    try:
        db = next(get_db())
        
        timeline_data = db.query(TextureTimeline).filter(
            TextureTimeline.plant_id == f"{species}_{plant_id}",
            TextureTimeline.band_name == band_name,
            TextureTimeline.texture_type == texture_type
        ).order_by(TextureTimeline.date_captured).all()
        
        return {
            "plant_id": f"{species}_{plant_id}",
            "band_name": band_name,
            "texture_type": texture_type,
            "timeline": [
                {
                    "date": str(t.date_captured),
                    "mean": t.mean,
                    "median": t.median,
                    "std": t.std,
                    "q25": t.q25,
                    "q75": t.q75,
                    "min": t.min,
                    "max": t.max,
                    "image_key": t.texture_image_key
                } for t in timeline_data
            ]
        }
        
    except Exception as e:
        print(f"Error getting texture timeline: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving texture timeline: {str(e)}")