# pipeline_runner.py

import os
import tempfile
import boto3
from src.pipeline import run_pipeline  # Assuming your pipeline has a callable method


def download_image_from_s3(bucket: str, key: str, local_path: str):
    s3 = boto3.client('s3')
    s3.download_file(bucket, key, local_path)
    return local_path


def process_plant_image(bucket: str, key: str) -> dict:
    with tempfile.TemporaryDirectory() as tmpdir:
        local_image_path = os.path.join(tmpdir, os.path.basename(key))
        download_image_from_s3(bucket, key, local_image_path)

        # Call your pipeline here
        results = run_pipeline(local_image_path)

        # results should be a dictionary of:
        # {
        #     "vegetation_indices": ...,  # filepath or image array
        #     "morphology_features": ...,  # dict or json
        #     "texture_features": ...,  # dict or json
        #     "segmented_image": ...,  # filepath or image array
        # }

        return results
