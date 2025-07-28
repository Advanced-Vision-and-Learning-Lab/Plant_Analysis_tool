import os
import re
import json
from datetime import datetime
import pandas as pd
import sys

project_root = "/home/grads/n/nazaro/Desktop/Github_repo/Plant_Analysis_tool"
sys.path.insert(0, project_root)

from backend.db.models import Plant, ProcessedData, VegetationIndexTimeline, TextureTimeline, VALID_VEGETATION_INDICES, TEXTURE_FEATURES
from backend.db.database import SessionLocal

# --- Config ---
save_folder = "/home/grads/n/nazaro/Desktop/Github_repo/Plant_Analysis_tool/backend/db/resources"
save_path = os.path.join(save_folder, "Sorghum_veg_texture_combined.csv")

# Helper to parse the naming convention
def parse_plant_id(raw_id):
    # Example: 2025_01_13_plant12_frame9
    match = re.match(r"(\d{4})_(\d{2})_(\d{2})_(plant\d+)_frame(\d+)", raw_id)
    if not match:
        raise ValueError(f"Invalid plant_id format: {raw_id}")
    year, month, day, plant_id, frame = match.groups()
    date_str = f"{year}-{month}-{day}"
    return plant_id, date_str, frame

def extract_vegetation_features(row, veg_cols):
    """
    Extract vegetation features and organize them by index type and statistic.
    
    Args:
        row: pandas Series containing the row data
        veg_cols: list of vegetation column names
    
    Returns:
        dict: Organized vegetation features by index type
    """
    # Statistical identifiers to look for
    stat_identifiers = ['_mean', '_std', '_max', '_min', '_median', '_q25', '_q75', '_nan_fraction']
    
    # Dictionary to store organized features
    organized_features = {}
    
    for col in veg_cols:
        if col in row and col != 'plant_id':
            # Extract the base vegetation index name (before the statistic identifier)
            base_index = None
            stat_type = None
            
            for stat in stat_identifiers:
                if col.endswith(stat):
                    base_index = col[:-len(stat)]  # Remove the statistic suffix
                    stat_type = stat[1:]  # Remove the leading underscore
                    break
            
            # If no statistic identifier found, use the full column name
            if base_index is None:
                base_index = col
                stat_type = 'raw'
            
            # Initialize the base index if not exists
            if base_index not in organized_features:
                organized_features[base_index] = {}
            
            # Store the value with its statistic type
            organized_features[base_index][stat_type] = row[col]
    
    return organized_features

def extract_texture_features(row, texture_cols):
    """
    Extract texture features and organize them by band and texture type.
    
    Args:
        row: pandas Series containing the row data
        texture_cols: list of texture column names
    
    Returns:
        dict: Organized texture features by band and texture type
    """
    # Statistical identifiers to look for
    stat_identifiers = ['_mean', '_std', '_max', '_min', '_median', '_q25', '_q75', '_nan_fraction']
    
    # Texture types from the texture analysis
    texture_types = ['orig','lbp', 'hog', 'lac1', 'lac2', 'lac3']
    
    # Dictionary to store organized features
    organized_features = {}
    
    for col in texture_cols:
        if col in row and col != 'plant_id':
            # Parse the column name to extract band, texture type, and statistic
            # Format: {band}_{texture-type}_{stat}
            # Example: "nir_lbp_mean", "color_hog_std", etc.
            
            parts = col.split('_')
            if len(parts) >= 3:
                # Find the texture type in the middle
                texture_type = None
                stat_type = None
                band_parts = []
                
                for i, part in enumerate(parts):
                    if part in texture_types:
                        texture_type = part
                        # Everything before texture_type is the band
                        band_parts = parts[:i]
                        # Everything after texture_type is the statistic
                        remaining_parts = parts[i+1:]
                        break
                
                if texture_type and remaining_parts:
                    # Reconstruct the band name
                    band = '_'.join(band_parts)
                    
                    # Check if the remaining parts form a valid statistic
                    stat_suffix = '_'.join(remaining_parts)
                    for stat in stat_identifiers:
                        if stat_suffix == stat[1:]:  # Remove leading underscore
                            stat_type = stat[1:]
                            break
                    
                    if stat_type:
                        # Initialize band if not exists
                        if band not in organized_features:
                            organized_features[band] = {}
                        
                        # Initialize texture type if not exists
                        if texture_type not in organized_features[band]:
                            organized_features[band][texture_type] = {}
                        
                        # Store the value with its statistic type
                        organized_features[band][texture_type][stat_type] = row[col]
    
    return organized_features

# Collect the species name from the file name ex: Sorghum_veg_texture_combined.csv
species_name = os.path.basename(save_path).split("_")[0]

# Load the combined features CSV
df = pd.read_csv(save_path)

# Use the vegetation indices from models.py to match columns
veg_cols = [col for col in df.columns if any(index in col for index in VALID_VEGETATION_INDICES)]
tex_cols = [col for col in df.columns if any(index in col for index in TEXTURE_FEATURES) and 'CIgreen' not in col]

# Open a DB session
session = SessionLocal()
added_plants = set()
added_processed = 0
added_veg_timeline = 0
added_tex_timeline = 0  

for idx, row in df.iterrows():
    try:
        raw_id = row['plant_id']
        plant_id, date_str, frame = parse_plant_id(raw_id)
        date_captured = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        # Insert Plant if not exists
        if plant_id not in added_plants:
            plant = session.query(Plant).filter_by(id=plant_id).first()
            if not plant:
                plant = Plant(id=f"{species_name}_{plant_id}", name=None, species=species_name)
                session.add(plant)
                session.commit()
            added_plants.add(plant_id)
        
        # Compose ProcessedData primary key
        processed_id = f"{species_name}_{plant_id}_{date_str}"
        
        # Extract features by type
        veg_features = extract_vegetation_features(row, veg_cols)
        texture_features = extract_texture_features(row, tex_cols)
        
        # Insert ProcessedData with JSON features
        processed = ProcessedData(
            id=processed_id,
            name=None,
            plant_id=f"{species_name}_{plant_id}",
            image_key=None, #TODO: change to image_key
            date_captured=date_captured,
            vegetation_features=veg_features,  # This will be saved as JSON
            morphology_features=None,
            texture_features=texture_features if texture_features else None
        )
        session.merge(processed)
        
        # Populate VegetationIndexTimeline for each vegetation index
        for index_name, stats in veg_features.items():
            # Check if we have the required statistics for the timeline
            if all(stat in stats for stat in ['mean', 'median', 'std', 'q25', 'q75', 'min', 'max']):
                veg_timeline = VegetationIndexTimeline(
                    plant_id=f"{species_name}_{plant_id}",
                    date_captured=date_captured,
                    index_type=index_name,
                    mean=float(stats['mean']),
                    median=float(stats['median']),
                    std=float(stats['std']),
                    q25=float(stats['q25']),
                    q75=float(stats['q75']),
                    min=float(stats['min']),
                    max=float(stats['max']),
                    index_image_key=f"{processed_id}_{index_name}.png"  # Placeholder image key
                )
                session.merge(veg_timeline)
                added_veg_timeline += 1
            else:
                print(f"Warning: Missing required stats for {index_name} in row {idx}")

        # Populate TextureTimeline for each texture feature
        for band_name, texture_types in texture_features.items():
            for texture_type, stats in texture_types.items():
                if all(stat in stats for stat in ['mean', 'median', 'std', 'q25', 'q75', 'min', 'max']):
                    texture_timeline = TextureTimeline(
                        plant_id=f"{species_name}_{plant_id}",
                        date_captured=date_captured,
                        band_name=band_name,
                        texture_type=texture_type,
                        mean=float(stats['mean']),
                        median=float(stats['median']),
                        std=float(stats['std']),
                        q25=float(stats['q25']),
                        q75=float(stats['q75']),
                        min=float(stats['min']),
                        max=float(stats['max']),
                        texture_image_key=f"{processed_id}_{band_name}_{texture_type}.png"  # Placeholder image key
                    )
                    session.merge(texture_timeline)
                    added_tex_timeline += 1
                else:
                    print(f"Warning: Missing required stats for {band_name}_{texture_type} in row {idx}")
        
        session.commit()
        added_processed += 1
        
        if idx < 5:  # Print first 5 for debugging
            print(f"Row {idx}: Processed {processed_id}")
            print(f"  Vegetation indices: {list(veg_features.keys())}")
            print(f"  Texture features: {len(texture_features)} bands")
            print(f"  Timeline entries added: {len([k for k in veg_features.keys() if all(stat in veg_features[k] for stat in ['mean', 'median', 'std', 'q25', 'q75', 'min', 'max'])])}")
            
    except Exception as e:
        print(f"Error processing row {idx}: {e}")
        session.rollback()

session.close()
print(f"Database population complete!")
print(f"  Plants added/updated: {len(added_plants)}")
print(f"  ProcessedData records: {added_processed}")
print(f"  VegetationIndexTimeline entries: {added_veg_timeline}")
print(f"  TextureTimeline entries: {added_tex_timeline}")