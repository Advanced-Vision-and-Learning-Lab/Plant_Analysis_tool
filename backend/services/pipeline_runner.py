import os
import cv2
import yaml
import torch
import json
import boto3
import io
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt

import numpy as np
from src.data_loader import load_single_frame_from_s3
from src.composite import create_composites, convert_to_uint8
from src.features import compute_veg_indices, compute_veg_index_features, VEG_INDEX_CHANNELS
from src.morphology import detect_and_return_morphology
from src.feature_texture import analyze_texture_features, compute_texture_features

from torchvision import transforms
from transformers import AutoModelForImageSegmentation
from huggingface_hub import login
import os

hf_token = os.getenv("HF_TOKEN")
if hf_token:
    login(token=hf_token)
    
def save_json_to_s3(obj, bucket, key):
    s3 = boto3.client('s3')
    s3.upload_fileobj(io.BytesIO(json.dumps(obj, indent=2).encode("utf-8")), bucket, key)

def save_image_to_s3(bucket, key, image_np):
    s3 = boto3.client('s3')
    print(f"[DEBUG] save_image_to_s3: key={key}, image_np type={type(image_np)}, shape={getattr(image_np, 'shape', None)}, dtype={getattr(image_np, 'dtype', None)}")
    success, encoded_img = cv2.imencode('.png', image_np)
    if not success:
        print(f"[ERROR] cv2.imencode failed for {key} with image shape {getattr(image_np, 'shape', None)} and dtype {getattr(image_np, 'dtype', None)}")
        return
    s3.upload_fileobj(io.BytesIO(encoded_img.tobytes()), bucket, key)
    print(f"[DEBUG] Uploaded {key} to S3")



def save_index(idx, func, spec, mask, s3_bucket, s3_prefix):
    bands = VEG_INDEX_CHANNELS.get(idx)
    if bands is None:
        print(f"[WARN] No bands found for index {idx}, skipping.")
        return
    try:
        vals = [spec[b].squeeze(-1) for b in bands]
    except KeyError as e:
        print(f"[WARN] Missing band {e} for index {idx}, skipping.")
        return
    arr = func(*vals)
    masked = np.where(mask == 255, arr, np.nan)
    img8 = convert_to_uint8(masked)
    if img8 is None or not isinstance(img8, np.ndarray) or img8.size == 0 or np.all(img8 == 0):
        print(f"[WARN] img8 for {idx} is invalid or all zeros, skipping.")
        return
    fig = plt.figure(figsize=(8, 8))
    try:
        im = plt.imshow(img8, cmap='YlGn')
        plt.axis('off')
        cbar = plt.colorbar(im, fraction=0.046, pad=0.04)
        cbar.set_ticks([0, 255])
        cbar.set_ticklabels([f"{np.nanmin(masked):.2f}", f"{np.nanmax(masked):.2f}"])
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        buf.seek(0)
        s3 = boto3.client('s3')
        s3_key = f"{s3_prefix}/vegetation_indices/{idx}.png"
        s3.upload_fileobj(buf, s3_bucket, s3_key, ExtraArgs={'ContentType': 'image/png'})
    except Exception as e:
        print(f"[ERROR] Failed to plot/save index {idx}: {e}")
    finally:
        plt.close(fig)

def process_plant_image(bucket, key):
    # print("▶ Starting pipeline for:", key)

    parts = key.split("/")
    # if len(parts) < 4:
    #     raise ValueError("Invalid S3 key format. Expected format: Sorghum_dataset/date/plant_id/file.tif")

    date = parts[1]
    plant_id = parts[2]
    frame_str = parts[3].split("_")[-1].replace(".tif", "")
    date_key = date.replace('-', '_')
    flat_key = f"{date_key}_{plant_id}_{frame_str}"

    # Use a consistent prefix for all outputs
    prefix = f"results/{date}/{plant_id}"

    image = load_single_frame_from_s3(bucket, key)
    # if image is None:
    #     print(f"[ERROR] Failed to load image from S3: {key}")
    #     return
    # print("[DEBUG] Image loaded successfully.")
    flats = {flat_key: {'raw_image': (image, os.path.basename(key))}}

    flats = create_composites(flats)
    # if not flats or flat_key not in flats or 'composite' not in flats[flat_key]:
    #     print(f"[ERROR] create_composites failed for {key}")
    #     return
    # print("[DEBUG] Composite created successfully.")
    # print("[DEBUG] About to set up bounding box variables")

    # print(f"[DEBUG] type(flats): {type(flats)}, len(flats): {len(flats)}")
    # if len(flats) > 0:
    #     print(f"[DEBUG] First key in flats: {next(iter(flats))}")
    # print(f"[DEBUG] Entering loop for plant_id={plant_id}, date={date}")
    for _, pdata in flats.items():
        comp = pdata['composite']
        H, W = comp.shape[:2]

        bbox_bucket = bucket
        bbox_key = f"bouningbox/{plant_id}.json"
        s3 = boto3.client('s3')
        # print("[DEBUG] About to fetch bounding box from S3")
        try:
            bbox_data = s3.get_object(Bucket=bbox_bucket, Key=bbox_key)['Body'].read()
            # eprint("[DEBUG] Finished fetching bounding box from S3")
            jd = json.loads(bbox_data)
            rect = next((s for s in jd.get('shapes', []) if s.get('shape_type') == 'rectangle'), None)
            bbox = (
                int(rect['points'][0][0]),
                int(rect['points'][0][1]),
                int(rect['points'][1][0]),
                int(rect['points'][1][1])
            ) if rect else None
        except Exception:
            bbox = None
        # print("[DEBUG] Finished bbox try/except block")

        x1, y1, x2, y2 = bbox if bbox else (0, 0, W, H)
        x1, x2 = max(0, x1), min(W, x2)
        y1, y2 = max(0, y1), min(H, y2)

        mask_box = np.zeros((H, W), dtype=np.uint8)
        mask_box[y1:y2, x1:x2] = 255
        # print(f"[DEBUG] comp shape: {comp.shape}, dtype: {comp.dtype}")
        # print(f"[DEBUG] mask_box shape: {mask_box.shape}, dtype: {mask_box.dtype}, unique values: {np.unique(mask_box)}")
        try:
            masked = cv2.bitwise_and(comp, comp, mask=mask_box)
        except Exception as e:
            # print(f"[ERROR] Exception during cv2.bitwise_and: {e}")
            return
        # Move model loading to module level so it is loaded only once
        print("▶ Loading segmentation model...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = (
            AutoModelForImageSegmentation
            .from_pretrained("briaai/RMBG-2.0", trust_remote_code=True)
            .eval()
            .to(device)
        )
        transform_image = transforms.Compose([
            transforms.Resize((1024, 1024)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        # print("[DEBUG] About to convert masked image to PIL")
        pil = Image.fromarray(cv2.cvtColor(masked, cv2.COLOR_BGR2RGB))

        # print("[DEBUG] About to transform PIL image")
        inp = transform_image(pil).unsqueeze(0).to(device)

        # print("[DEBUG] About to run segmentation model forward pass")
        with torch.no_grad():
            preds = model(inp)[-1].sigmoid().cpu()[0].squeeze(0).numpy()
        # print("[DEBUG] Segmentation model forward pass completed")

        mask_pred = (preds > 0.5).astype(np.uint8) * 255
        mask_full = cv2.resize(mask_pred, (W, H), interpolation=cv2.INTER_NEAREST)

        n_lbl, labels, stats, _ = cv2.connectedComponentsWithStats(mask_full, 8)
        if n_lbl > 1:
            largest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
            mask_full = (labels == largest).astype(np.uint8) * 255

        pdata['mask'] = mask_full

        # print("[DEBUG] Segmentation model finished.")
        # print(f"[DEBUG] Mask shape: {mask_full.shape}, dtype: {mask_full.dtype}")
        # print(f"[DEBUG] Composite shape: {comp.shape}, dtype: {comp.dtype}")

        try:
            # print(f"[DEBUG] About to save original.png for {plant_id} on {date}")
            save_image_to_s3(bucket, f"{prefix}/original.png", comp)
            # print(f"[DEBUG] Saved original.png for {plant_id} on {date}")
        except Exception as e:
            # print(f"[ERROR] Exception during saving original.png: {e}")
            pass
        try:
            # print(f"[DEBUG] About to save mask.png for {plant_id} on {date}")
            save_image_to_s3(bucket, f"{prefix}/mask.png", mask_full)
            # print(f"[DEBUG] Saved mask.png for {plant_id} on {date}")
        except Exception as e:
            # print(f"[ERROR] Exception during saving mask.png: {e}")
            pass

        bright = cv2.convertScaleAbs(comp, alpha=1.2, beta=15)
        overlay = bright.copy()
        overlay[mask_full == 255] = (0, 255, 0)
        overlay = cv2.addWeighted(bright, 1.0, overlay, 0.5, 0)
        save_image_to_s3(bucket, f"{prefix}/overlay.png", overlay)

        segmented = cv2.bitwise_and(comp, comp, mask=mask_full)
        save_image_to_s3(bucket, f"{prefix}/segmented.png", segmented)

        spec = pdata.get("spectral_stack")  # or whatever key holds your spectral data
        mask = pdata.get("mask")
        if spec is None or mask is None:
            print(f"[WARN] spec or mask is None for {plant_id} on {date}, skipping feature extraction.")
            continue

        # --- Compute and save vegetation indices sequentially (old method) ---
    flats = compute_veg_indices(flats, bucket, prefix)

    veg_features = compute_veg_index_features(flats)
    save_json_to_s3(veg_features, bucket, f"{prefix}/vegetation_indices/vegetation_features.json")

    print("▶ Analyzing texture features")
    analyze_texture_features(
            pdata,
            key=plant_id,
            s3_bucket=bucket,
            s3_prefix=prefix
        )
    print("Texture features analyzed")
    texture_features = compute_texture_features(flats)
    print("Texture features computed")
    save_json_to_s3(texture_features, bucket, f"{prefix}/texture/texture_features.json")

    # Morphology features
    print("▶ Extracting morphology features")
    def extract_and_save_morphology(pdata, bucket, prefix):
        img = pdata.get("composite")
        mask = pdata.get("mask")
        if img is not None and mask is not None:
            features = detect_and_return_morphology(img, mask)
            save_json_to_s3(features, bucket, f"{prefix}/morphology_features.json")
            return features
        return None
    morphology_features = {}
    with ThreadPoolExecutor(max_workers=4) as executor:
        morph_futures = []
        for _, pdata in flats.items():
            morph_futures.append(executor.submit(extract_and_save_morphology, pdata, bucket, prefix))
        for f in morph_futures:
            result = f.result()
            if result:
                morphology_features = result
    print("→ Done.")
    return {
        "vegetation_indices": veg_features,
        "texture_features": texture_features,
        "morphology_features": morphology_features,
        "mask_path": f"{prefix}/mask.png"
    }
