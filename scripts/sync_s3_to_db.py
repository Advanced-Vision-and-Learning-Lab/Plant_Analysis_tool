import boto3
import pymysql
import json
import re
import os
from datetime import datetime

# --- CONFIGURATION ---
S3_BUCKET = os.environ.get('S3_BUCKET_NAME', 'plant-analysis-data')
DB_CONN_STRING = os.environ.get('DB_DEV_CONNECTION_STRING')  # e.g. mysql+pymysql://user:pass@host:port/db

# --- S3 & DB SETUP ---
s3 = boto3.client('s3')

# Parse DB_CONN_STRING for pymysql
if DB_CONN_STRING:
    # Remove the dialect prefix for pymysql.connect
    # Example: mysql+pymysql://user:password@host:3306/dbname
    import sqlalchemy.engine.url as sa_url
    url = sa_url.make_url(DB_CONN_STRING)
    conn = pymysql.connect(
        host=url.host,
        user=url.username,
        password=url.password,
        database=url.database,
        port=url.port or 3306,
        charset='utf8mb4',
        autocommit=True
    )
else:
    # Fallback to manual env vars
    conn = pymysql.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'dev_user'),
        password=os.environ.get('DB_PASSWORD', 'dev_password'),
        database=os.environ.get('DB_NAME', 'plant_dev_db'),
        port=int(os.environ.get('DB_PORT', 3306)),
        charset='utf8mb4',
        autocommit=True
    )
cur = conn.cursor()

# --- REGEX TO MATCH FOLDERS ---
prefix = 'results/{species}_results/{plant_id}/{date}/'
folder_re = re.compile(r'results/(\d{4}-\d{2}-\d{2})/([^/]+)/')

# # --- PAGINATE ALL FOLDERS ---
# paginator = s3.get_paginator('list_objects_v2')
# for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=prefix, Delimiter='/'):
#     for folder in page.get('CommonPrefixes', []):
#         match = folder_re.match(folder['Prefix'])
#         if match:
#             date_str, plant_id = match.groups()
#             date_obj = datetime.strptime(date_str, '%Y-%m-%d')
#             # Check if record exists
#             cur.execute(
#                 "SELECT 1 FROM processed_images WHERE plant_id=%s AND date=%s",
#                 (plant_id, date_obj)
#             )
#             if not cur.fetchone():
#                 # Try to load features from S3
#                 def load_json_from_s3(key):
#                     try:
#                         obj = s3.get_object(Bucket=S3_BUCKET, Key=key)
#                         return json.loads(obj['Body'].read())
#                     except Exception:
#                         return None

#                 veg_features = load_json_from_s3(f"{prefix}/vegetation_indices/vegetation_features.json")
#                 morph_features = load_json_from_s3(f"{prefix}/morphology_features.json")
#                 texture_features = load_json_from_s3(f"{prefix}/texture/texture_features.json")

#                 # Insert new record
#                 cur.execute(
#                     """
#                     INSERT INTO processed_images
#                     (plant_id, image_key, date, vegetation_features, morphology_features, texture_features)
#                     VALUES (%s, %s, %s, %s, %s, %s)
#                     """,
#                     (
#                         plant_id,
#                         f"{prefix}/original.png",
#                         date_obj,
#                         json.dumps(veg_features) if veg_features else None,
#                         json.dumps(morph_features) if morph_features else None,
#                         json.dumps(texture_features) if texture_features else None
#                     )
#                 )
#                 print(f"Inserted record for {plant_id} on {date_str}")

conn.commit()
cur.close()
conn.close()
print("Sync complete!")