# db_service.py

import logging
from datetime import date
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.db.models import Plant, ProcessedData, VegetationIndexTimeline, TextureTimeline

logger = logging.getLogger(__name__)

class PlantService:
    """Service class for plant-related database operations."""
    
    @staticmethod
    def create_or_update_plant(db: Session, plant_id: str, species: str, capture_date: date) -> Plant:
        """
        Create a new plant entry or update existing one with new capture date.
        
        Args:
            db: Database session
            plant_id: Unique plant identifier
            species: Plant species name
            capture_date: Date when the plant was captured
            
        Returns:
            Plant object
            
        Raises:
            IntegrityError: If there's a database constraint violation
        """
        try:
            # Check if plant already exists
            plant = db.query(Plant).filter(Plant.id == plant_id).first()
            
            if plant:
                # Update existing plant - add new date if not already present
                if capture_date not in plant.dates_captured:
                    plant.dates_captured.append(capture_date)
                    logger.info(f"Added date {capture_date} to existing plant {plant_id}")
            else:
                # Create new plant
                plant = Plant(
                    id=plant_id,
                    species=species,
                    dates_captured=[capture_date]
                )
                db.add(plant)
                logger.info(f"Created new plant {plant_id} for species {species}")
            
            db.commit()
            return plant
            
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Database integrity error for plant {plant_id}: {e}")
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating/updating plant {plant_id}: {e}")
            raise
    
    @staticmethod
    def get_plant_by_id(db: Session, plant_id: str) -> Optional[Plant]:
        """Get plant by ID."""
        return db.query(Plant).filter(Plant.id == plant_id).first()
    
    @staticmethod
    def get_plants_by_species(db: Session, species: str) -> List[Plant]:
        """Get all plants for a specific species."""
        return db.query(Plant).filter(Plant.species == species).all()
    
    @staticmethod
    def get_all_plants(db: Session) -> List[Plant]:
        """Get all plants."""
        return db.query(Plant).all()
    
    @staticmethod
    def get_plant_statistics(db: Session) -> Dict[str, Any]:
        """Get plant statistics."""
        total_plants = db.query(Plant).count()
        total_species = db.query(Plant.species).distinct().count()
        species_counts = db.query(Plant.species, db.func.count(Plant.id)).group_by(Plant.species).all()
        
        return {
            "total_plants": total_plants,
            "total_species": total_species,
            "species_breakdown": {species: count for species, count in species_counts}
        }

class ProcessedDataService:
    """Service class for processed data operations."""
    
    @staticmethod
    def create_processed_data_entry(
        db: Session,
        plant_id: str,
        date_captured: date,
        image_key: Optional[str] = None,
        vegetation_features: Optional[Dict[str, Any]] = None,
        morphology_features: Optional[Dict[str, Any]] = None,
        texture_features: Optional[Dict[str, Any]] = None
    ) -> ProcessedData:
        """
        Create a new processed data entry.
        
        Args:
            db: Database session
            plant_id: Plant identifier
            date_captured: Date when the image was captured
            image_key: S3 key for the image
            vegetation_features: Vegetation analysis features
            morphology_features: Morphology analysis features
            texture_features: Texture analysis features
            
        Returns:
            ProcessedData object
        """
        try:
            # Create unique ID for the processed data entry
            processed_data_id = f"{plant_id}_{date_captured}"
            
            processed_data = ProcessedData(
                id=processed_data_id,
                plant_id=plant_id,
                date_captured=date_captured,
                image_key=image_key,
                vegetation_features=vegetation_features,
                morphology_features=morphology_features,
                texture_features=texture_features
            )
            
            db.add(processed_data)
            db.commit()
            
            logger.info(f"Created processed data entry: {processed_data_id}")
            return processed_data
            
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Database integrity error for processed data {processed_data_id}: {e}")
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating processed data entry: {e}")
            raise
    
    @staticmethod
    def get_processed_data_by_plant_and_date(
        db: Session, 
        plant_id: str, 
        date_captured: date
    ) -> Optional[ProcessedData]:
        """Get processed data for a specific plant and date."""
        return db.query(ProcessedData).filter(
            ProcessedData.plant_id == plant_id,
            ProcessedData.date_captured == date_captured
        ).first()
    
    @staticmethod
    def get_processed_data_by_plant(db: Session, plant_id: str) -> List[ProcessedData]:
        """Get all processed data for a specific plant."""
        return db.query(ProcessedData).filter(ProcessedData.plant_id == plant_id).all()

class VegetationIndexService:
    """Service class for vegetation index timeline operations."""
    
    @staticmethod
    def create_vegetation_index_entry(
        db: Session,
        plant_id: str,
        date_captured: date,
        index_type: str,
        mean: float,
        median: float,
        std: float,
        q25: float,
        q75: float,
        min_val: float,
        max_val: float,
        index_image_key: str
    ) -> VegetationIndexTimeline:
        """
        Create a new vegetation index timeline entry.
        """
        try:
            entry = VegetationIndexTimeline(
                plant_id=plant_id,
                date_captured=date_captured,
                index_type=index_type,
                mean=mean,
                median=median,
                std=std,
                q25=q25,
                q75=q75,
                min=min_val,
                max=max_val,
                index_image_key=index_image_key
            )
            
            db.add(entry)
            db.commit()
            
            logger.info(f"Created vegetation index entry: {plant_id}_{date_captured}_{index_type}")
            return entry
            
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Database integrity error for vegetation index entry: {e}")
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating vegetation index entry: {e}")
            raise

class TextureService:
    """Service class for texture timeline operations."""
    
    @staticmethod
    def create_texture_entry(
        db: Session,
        plant_id: str,
        date_captured: date,
        band_name: str,
        texture_type: str,
        mean: float,
        median: float,
        std: float,
        q25: float,
        q75: float,
        min_val: float,
        max_val: float,
        texture_image_key: str
    ) -> TextureTimeline:
        """
        Create a new texture timeline entry.
        """
        try:
            entry = TextureTimeline(
                plant_id=plant_id,
                date_captured=date_captured,
                band_name=band_name,
                texture_type=texture_type,
                mean=mean,
                median=median,
                std=std,
                q25=q25,
                q75=q75,
                min=min_val,
                max=max_val,
                texture_image_key=texture_image_key
            )
            
            db.add(entry)
            db.commit()
            
            logger.info(f"Created texture entry: {plant_id}_{date_captured}_{band_name}_{texture_type}")
            return entry
            
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Database integrity error for texture entry: {e}")
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating texture entry: {e}")
            raise 