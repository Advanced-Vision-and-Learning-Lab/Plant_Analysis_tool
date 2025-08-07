# upload_api.py

import logging
import sys
import os
import json
from datetime import datetime, date
from typing import List, Dict, Any
from pathlib import Path

import boto3
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# Add the backend directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from db.database import get_db
from db.models import Plant, ProcessedData, VegetationIndexTimeline, TextureTimeline
from services.db_service import PlantService, ProcessedDataService, VegetationIndexService, TextureService

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(levelname)s:%(name)s:%(message)s",
    force=True
)

logger = logging.getLogger(__name__)

# S3 Configuration
S3_BUCKET = "plant-analysis-data"
S3_REGION = "us-east-2"

router = APIRouter()

def get_species_from_filename(filename: str) -> str:
    """
    Extract species from filename.
    Examples:
    - "Sorghum_dataset" -> "Sorghum"
    - "Sorghum_results" -> "Sorghum"
    """
    if "_dataset" in filename:
        return filename.replace("_dataset", "")
    elif "_results" in filename:
        return filename.replace("_results", "")
    else:
        # If no suffix found, assume the whole name is the species
        return filename

def create_or_update_plant(db: Session, plant_id: str, species: str, capture_date: date) -> Plant:
    """
    Create a new plant entry or update existing one with new capture date.
    """
    try:
        return PlantService.create_or_update_plant(db, plant_id, species, capture_date)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

async def upload_file_to_s3(file: UploadFile, s3_key: str) -> bool:
    """Upload a file to S3."""
    try:
        s3 = boto3.client('s3', region_name='us-east-2')
        
        # Read file content
        content = await file.read()
        
        # Upload to S3
        s3.put_object(
            Bucket="plant-analysis-data",
            Key=s3_key,
            Body=content,
            ContentType=file.content_type
        )
        
        logger.info(f"Successfully uploaded {file.filename} to S3: {s3_key}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to upload {file.filename} to S3: {e}")
        return False

def process_raw_files_upload(db: Session, species: str, files_info: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Process raw files upload and create database entries.
    """
    try:
        processed_plants = set()
        total_files = 0
        
        for file_info in files_info:
            file_path = file_info['path']
            file_size = file_info['size']
            
            # Parse path: Sorghum_dataset/{date}/{plant_id}/{plant_id}_frame#.tiff
            path_parts = file_path.split('/')
            if len(path_parts) < 4:
                logger.warning(f"Invalid file path format: {file_path}")
                continue
                
            try:
                capture_date = datetime.strptime(path_parts[1], '%Y-%m-%d').date()
                plant_id = path_parts[2]
                filename = path_parts[3]
                
                # Create or update plant in database
                plant = create_or_update_plant(db, plant_id, species, capture_date)
                processed_plants.add(plant_id)
                total_files += 1
                
                logger.info(f"Processed raw file: {file_path} for plant {plant_id} on {capture_date}")
                
            except ValueError as e:
                logger.error(f"Invalid date format in path {file_path}: {e}")
                continue
            except Exception as e:
                logger.error(f"Error processing file {file_path}: {e}")
                continue
        
        return {
            "message": "Raw files upload processed successfully",
            "species": species,
            "plants_processed": len(processed_plants),
            "total_files": total_files,
            "plant_ids": list(processed_plants)
        }
        
    except Exception as e:
        logger.error(f"Error in process_raw_files_upload: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing raw files: {str(e)}")

def process_result_files_upload(db: Session, species: str, files_info: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Process result files upload and save data to database.
    """
    try:
        processed_plants = set()
        total_files = 0
        
        for file_info in files_info:
            file_path = file_info['path']
            file_size = file_info['size']
            
            # Parse path: Sorghum_results/{plant_id}/{date}/{plant_id}_frame#_result.json
            path_parts = file_path.split('/')
            if len(path_parts) < 4:
                logger.warning(f"Invalid result file path format: {file_path}")
                continue
                
            try:
                plant_id = path_parts[1]
                capture_date = datetime.strptime(path_parts[2], '%Y-%m-%d').date()
                filename = path_parts[3]
                
                # Create or update plant in database
                plant = create_or_update_plant(db, plant_id, species, capture_date)
                processed_plants.add(plant_id)
                total_files += 1
                
                logger.info(f"Processed result file: {file_path} for plant {plant_id} on {capture_date}")
                
            except ValueError as e:
                logger.error(f"Invalid date format in path {file_path}: {e}")
                continue
            except Exception as e:
                logger.error(f"Error processing result file {file_path}: {e}")
                continue
        
        return {
            "message": "Result files upload processed successfully",
            "species": species,
            "plants_processed": len(processed_plants),
            "total_files": total_files,
            "plant_ids": list(processed_plants)
        }
        
    except Exception as e:
        logger.error(f"Error in process_result_files_upload: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing result files: {str(e)}")

@router.post("/upload/raw-files")
async def upload_raw_files(
    files: List[UploadFile] = File(...)
):
    """
    Upload raw plant image files.
    
    Expected file structure: Sorghum_dataset/{date}/{plant_id}/{plant_id}_frame#.tiff
    
    If species is not provided, it will be extracted from the first filename.
    """
    try:
        if not files:
            raise HTTPException(status_code=400, detail="No files provided")
        
        # Extract species from first filename 
        first_filename = files[0].filename
        species = get_species_from_filename(first_filename)
        logger.info(f"Extracted species '{species}' from filename: {first_filename}")
        
        # Get database session
        db = next(get_db())
        
        # Process file information
        files_info = []
        for file in files:
            s3_key = f"uploaded_files/{file.filename}"
            await upload_file_to_s3(file, s3_key)
            files_info.append({
                "path": file.filename,
                "size": file.size,
                "content_type": file.content_type
            })
        
        # Process the upload
        result = process_raw_files_upload(db, species, files_info)
        
        return JSONResponse(content=result, status_code=200)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in upload_raw_files: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/upload/result-files")
async def upload_result_files(
    files: List[UploadFile] = File(...)
):
    """
    Upload result files from plant analysis.
    
    Expected file structure: Sorghum_results/{plant_id}/{date}/{plant_id}_frame#_result.json
    
    If species is not provided, it will be extracted from the first filename.
    """
    try:
        if not files:
            raise HTTPException(status_code=400, detail="No files provided")
        
        # Extract species from first filename if not provided
        first_filename = files[0].filename
        species = get_species_from_filename(first_filename)
        logger.info(f"Extracted species '{species}' from filename: {first_filename}")
        
        # Get database session
        db = next(get_db())
        
        # Process file information
        files_info = []
        for file in files:
            s3_key = f"uploaded_files/{file.filename}"
            await upload_file_to_s3(file, s3_key)
            files_info.append({
                "path": file.filename,
                "size": file.size,
                "content_type": file.content_type
            })
        
        # Process the upload
        result = process_result_files_upload(db, species, files_info)
        
        return JSONResponse(content=result, status_code=200)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in upload_result_files: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/upload/status")
async def get_upload_status():
    """
    Get upload status and statistics.
    """
    try:
        db = next(get_db())
        
        # Get basic statistics using the service
        return PlantService.get_plant_statistics(db)
        
    except Exception as e:
        logger.error(f"Error getting upload status: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/plants/{species}")
async def get_plants_by_species(species: str):
    """
    Get all plants for a specific species.
    """
    try:
        db = next(get_db())
        
        plants = PlantService.get_plants_by_species(db, species)
        
        return {
            "species": species,
            "plants": [
                {
                    "id": plant.id,
                    "name": plant.name,
                    "dates_captured": plant.dates_captured
                }
                for plant in plants
            ]
        }
        
    except Exception as e:
        logger.error(f"Error getting plants for species {species}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
