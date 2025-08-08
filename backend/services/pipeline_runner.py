# src/process_plant.py  (or wherever this lives)

import os
import io
import json
import cv2
import boto3
import torch
import yaml  # if you need it elsewhere; safe to remove if unused
import numpy as np
import matplotlib
matplotlib.use("Agg")  # safe for headless servers
import matplotlib.pyplot as plt

from PIL import Image
from torchvision import transforms
from transformers import AutoModelForImageSegmentation
from huggingface_hub import login

from src.data_loader import load_single_frame_from_s3
from src.composite import create_composites, convert_to_uint8
from src.features import compute_veg_indices, compute_veg_index_features, VEG_INDEX_CHANNELS
from src.feature_texture import analyze_texture_features, compute_texture_features
from src.morphology import create_morphology_outputs  # NEW

# -----------------------------
# Auth: Hugging Face (if token present)
# -----------------------------
hf_token = os.getenv("HF_TOKEN")
if hf_token:
    try:
        login(token=hf_token)
    except Exception:
        # non-fatal
        pass

# -----------------------------
# Global: S3 helpers
# -----------------------------
def save_json_to_s3(obj, bucket, key, content_type="application/json"):
    s3 = boto3.client('s3')
    s3.upload_fileobj(io.BytesIO(json.dumps(obj, indent=2).encode("utf-8")), bucket, key,
                      ExtraArgs={"ContentType": content_type})

def save_image_to_s3(bucket, key, image_np):
    s3 = boto3.client('s3')
    success, encoded_img = cv2.imencode('.png', image_np)
    if not success:
        print(f"[ERROR] cv2.imencode failed for {key} with image shape {getattr(image_np, 'shape', None)} and dtype {getattr(image_np, 'dtype', None)}")
        return
    s3.upload_fileobj(io.BytesIO(encoded_img.tobytes()), bucket, key, ExtraArgs={'ContentType': 'image/png'})

def save_morph_images_to_s3(images_dict, bucket, prefix):
    """images_dict: name -> np.uint8 image; returns name->s3_key"""
    out = {}
    for name, im in images_dict.items():
        key = f"{prefix}/morphology/images/{name}.png"
        save_image_to_s3(bucket, key, im)
        out[name] = key
    return out

def save_morph_csv(morph_results, bucket, key):
    """Write a simple CSV across plants with size + morphology traits."""
    import csv
    # gather columns
    all_size, all_morph = set(), set()
    for _, r in morph_results.items():
        all_size |= set(r.get("size_traits", {}).keys())
        all_morph |= set(r.get("morphology_traits", {}).keys())
    size_cols = sorted(all_size)
    morph_cols = sorted(all_morph)
    cols = ["plant_id"] + [f"size.{c}" for c in size_cols] + [f"morph.{c}" for c in morph_cols]

    bio = io.StringIO()
    w = csv.writer(bio)
    w.writerow(cols)
    for pid, r in morph_results.items():
        size = r.get("size_traits", {})
        morph = r.get("morphology_traits", {})
        row = [pid] + [size.get(c, "") for c in size_cols] + [morph.get(c, "") for c in morph_cols]
        w.writerow(row)
    data = bio.getvalue().encode("utf-8")
    s3 = boto3.client('s3')
    s3.upload_fileobj(io.BytesIO(data), bucket, key, ExtraArgs={"ContentType":"text/csv"})

# -----------------------------
# Global: RMBG segmentation model (load ONCE)
# -----------------------------
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
try:
    RMBG = (AutoModelForImageSegmentation
            .from_pretrained("briaai/RMBG-2.0", trust_remote_code=True)
            .eval()
            .to(DEVICE))
except Exception as e:
    RMBG = None
    print(f"[WARN] Could not load RMBG-2.0 model: {e}")

TRANSFORM_IMAGE = transforms.Compose([
    transforms.Resize((1024, 1024)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# -----------------------------
# Vegetation index helper (unchanged)
# -----------------------------
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

# -----------------------------
# Main pipeline for one plant-frame
# -----------------------------
def process_plant_image(bucket, key):
    """
    Runs the full pipeline for a single plant image in S3:
    - load frame
    - create composites
    - crop to bbox (if available)
    - segment RMBG -> mask (largest CC)
    - save original/mask/overlay/segmented
    - compute vegetation indices + JSON
    - compute texture features (maps + JSON)
    - compute morphology (traits + diagnostic images + CSV)

    Returns a dict with veg, texture, morphology, and mask path.
    """
    parts = key.split("/")
    date = parts[1]
    plant_id = parts[2]
    frame_str = parts[3].split("_")[-1].replace(".tif", "")
    date_key = date.replace('-', '_')
    flat_key = f"{date_key}_{plant_id}_{frame_str}"

    prefix = f"results/{date}/{plant_id}"

    # 1) Load
    image = load_single_frame_from_s3(bucket, key)
    flats = {flat_key: {'raw_image': (image, os.path.basename(key))}}

    # 2) Composite
    flats = create_composites(flats)

    # 3) For this plant (single entry), build bbox crop + RMBG mask
    for _, pdata in flats.items():
        comp = pdata['composite']
        H, W = comp.shape[:2]

        # bbox from S3 (keep their existing path name 'bouningbox/')
        bbox_bucket = bucket
        bbox_key = f"bouningbox/{plant_id}.json"
        s3 = boto3.client('s3')
        try:
            bbox_data = s3.get_object(Bucket=bbox_bucket, Key=bbox_key)['Body'].read()
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

        x1, y1, x2, y2 = bbox if bbox else (0, 0, W, H)
        x1, x2 = max(0, x1), min(W, x2)
        y1, y2 = max(0, y1), min(H, y2)

        mask_box = np.zeros((H, W), dtype=np.uint8)
        mask_box[y1:y2, x1:x2] = 255

        masked = cv2.bitwise_and(comp, comp, mask=mask_box)

        # RMBG segmentation (using global model)
        if RMBG is None:
            print("[ERROR] RMBG model not available; cannot segment.")
            return None

        pil = Image.fromarray(cv2.cvtColor(masked, cv2.COLOR_BGR2RGB))
        inp = TRANSFORM_IMAGE(pil).unsqueeze(0).to(DEVICE)
        with torch.no_grad():
            preds = RMBG(inp)[-1].sigmoid().cpu()[0].squeeze(0).numpy()

        mask_pred = (preds > 0.5).astype(np.uint8) * 255
        mask_full = cv2.resize(mask_pred, (W, H), interpolation=cv2.INTER_NEAREST)

        # Largest connected component
        n_lbl, labels, stats, _ = cv2.connectedComponentsWithStats(mask_full, 8)
        if n_lbl > 1:
            largest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
            mask_full = (labels == largest).astype(np.uint8) * 255

        pdata['mask'] = mask_full

        # Save images
        try:
            save_image_to_s3(bucket, f"{prefix}/original.png", comp)
        except Exception:
            pass
        try:
            save_image_to_s3(bucket, f"{prefix}/mask.png", mask_full)
        except Exception:
            pass

        bright = cv2.convertScaleAbs(comp, alpha=1.2, beta=15)
        overlay = bright.copy()
        overlay[mask_full == 255] = (0, 255, 0)
        overlay = cv2.addWeighted(bright, 1.0, overlay, 0.5, 0)
        save_image_to_s3(bucket, f"{prefix}/overlay.png", overlay)

        segmented = cv2.bitwise_and(comp, comp, mask=mask_full)
        save_image_to_s3(bucket, f"{prefix}/segmented.png", segmented)

        # optional: texture visualization per-plant (uses pdata)
        print("▶ Analyzing texture features")
        try:
            analyze_texture_features(
                pdata,
                key=plant_id,
                s3_bucket=bucket,
                s3_prefix=prefix
            )
            print("Texture features analyzed")
        except Exception as e:
            print(f"[WARN] analyze_texture_features failed: {e}")

    # 4) Vegetation indices (over flats) + JSON
    flats = compute_veg_indices(flats, bucket, prefix)
    veg_features = compute_veg_index_features(flats)
    save_json_to_s3(veg_features, bucket, f"{prefix}/vegetation_indices/vegetation_features.json")

    # 5) Aggregate texture features (over flats) + JSON
    texture_features = compute_texture_features(flats)
    save_json_to_s3(texture_features, bucket, f"{prefix}/texture/texture_features.json")

    # 6) Morphology (new) — build refined_plants and run
    print("▶ Extracting morphology features")
    # We’ll use the single plant_id as the key in refined_plants
    # Pull composite/mask from the (only) flats entry:
    # NOTE: if you ever expand to multiple entries, extend this.
    any_pdata = next(iter(flats.values()))
    if "composite" in any_pdata and "mask" in any_pdata:
        refined_plants = {
            plant_id: {
                "composite": any_pdata["composite"],
                "mask": any_pdata["mask"],
            }
        }
    else:
        print("[WARN] Missing composite/mask; skipping morphology.")
        refined_plants = {}

    morph_results = {}
    if refined_plants:
        morph_results = create_morphology_outputs(refined_plants)

        # Save traits + images to S3
        for pid, mr in morph_results.items():
            # traits JSON
            save_json_to_s3(
                {
                    "size_traits": mr.get("size_traits", {}),
                    "morphology_traits": mr.get("morphology_traits", {})
                },
                bucket, f"{prefix}/morphology/{pid}_traits.json"
            )
            # images
            _ = save_morph_images_to_s3(mr.get("images", {}), bucket, prefix)

        # CSV across all (here: single plant)
        try:
            save_morph_csv(morph_results, bucket, f"{prefix}/morphology/morphology.csv")
        except Exception as e:
            print(f"[WARN] Could not save morphology.csv: {e}")

    print("→ Done.")
    return {
        "vegetation_indices": veg_features,
        "texture_features": texture_features,
        "morphology": morph_results,
        "mask_path": f"{prefix}/mask.png"
    }
