import os
import glob
import json
import numpy as np
import cv2
import boto3
from PIL import Image
import io

def load_single_frame_from_s3(bucket, key):
    """
    Load a single image from S3 and return it as a PIL Image (without converting color).
    """
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket, Key=key)
    image_data = response['Body'].read()
    image = Image.open(io.BytesIO(image_data))
    return image

# # Plants to ignore completely
# _IGNORE = {2, 3, 15, 36, 44}

# # Plants where you want exactly one frame from their own folder
# _EXACT_FRAME = {
#     4:  7,
#     5:  5,
#     7:  5,
#     12: 5,
#     13: 5,
#     18: 7,
#     19: 2,
#     20: 3,
#     24: 6,
#     25: 5,
#     26: 5,
#     30: 8,
#     37: 7,
# }

# # Plants where you want to borrow a frame from a *different* plant folder
# # format: target_pid: (source_pid, source_frame)
# _BORROW = {
#     14: (13, 5),
#     15: (14, 5),
#     16: (15, 5),
#     33: (34, 7),
#     34: (35, 7),
#     35: (35, 8),
#     36: (36, 6),  # if you really still want plant36 frame6
# }
# def load_raw_images_one(input_root_folder, DEBUG=False):
#     """
#     Load exactly the 2025-02-05 plant1 frame8 image.
#     Returns a dict keyed by "2025-02-05_plant1" → {"raw_images":[(PIL Image, filename)]}.
#     """
#     plants = {}
#     date_name   = "2025-02-05"
#     plant_name  = "plant1"
#     frame_num   = 8

#     # build paths
#     date_path        = os.path.join(input_root_folder, date_name)
#     plant_folder     = plant_name
#     filename         = f"{plant_folder}_frame{frame_num}.tif"
#     full_image_path  = os.path.join(date_path, plant_folder, filename)

#     if os.path.exists(full_image_path):
#         try:
#             im = Image.open(full_image_path)
#             key = f"{date_name}_{plant_name}"
#             plants[key] = {"raw_images": [(im, filename)]}
#             if DEBUG:
#                 print(f"✅ Loaded {key}: {filename}")
#         except Exception as e:
#             if DEBUG:
#                 print(f"❌ Failed to open {full_image_path}: {e}")
#     else:
#         if DEBUG:
#             print(f"⚠ File not found: {full_image_path}")

#     return plants

# def load_raw_images(input_root_folder, DEBUG=False):
#     """
#     Load exactly one frame per plant according to your custom rules.
#     Returns a dict keyed by "YYYY-MM-DD_plantX" → {"raw_images":[(PIL Image, filename)]}.
#     """
#     plants = {}

#     for date_name in sorted(os.listdir(input_root_folder)):
#         date_path = os.path.join(input_root_folder, date_name)
#         if not os.path.isdir(date_path):
#             continue

#         for plant_name in sorted(os.listdir(date_path)):
#             plant_path = os.path.join(date_path, plant_name)
#             if not os.path.isdir(plant_path):
#                 continue

#             # extract numeric ID
#             try:
#                 pid = int(plant_name.replace("plant",""))
#             except:
#                 continue

#             # 1) ignore?
#             if pid in _IGNORE:
#                 if DEBUG:
#                     print(f"🔹 Ignoring plant{pid}")
#                 continue

#             # decide which frame to load
#             if pid in _EXACT_FRAME:
#                 frame_num = _EXACT_FRAME[pid]
#                 src_plant, src_frame = pid, frame_num

#             elif pid in _BORROW:
#                 src_plant, src_frame = _BORROW[pid]
#             else:
#                 # fallback to frame9 (original behavior)
#                 src_plant, src_frame = pid, 9

#             # build source path
#             src_plant_folder = f"plant{src_plant}"
#             src_filename     = f"{src_plant_folder}_frame{src_frame}.tif"
#             src_path         = os.path.join(date_path, src_plant_folder, src_filename)

#             if os.path.exists(src_path):
#                 try:
#                     im = Image.open(src_path)
#                     key = f"{date_name}_{plant_name}"
#                     plants[key] = {"raw_images": [(im, src_filename)]}
#                 except Exception as e:
#                     if DEBUG:
#                         print(f"❌ Failed to open {src_path}: {e}")
#             else:
#                 if DEBUG:
#                     print(f"⚠ Missing {src_filename} for plant{pid} on {date_name}")

#     return plants
# def load_hand_labeled_mask(json_file, shape):

#     with open(json_file) as f:
#         data = json.load(f)
#     mask = np.zeros(shape, dtype=np.uint8)
#     for shp in data.get('shapes', []):
#         pts = np.array(shp['points'], dtype=np.int32).reshape(-1,1,2)
#         cv2.fillPoly(mask, [pts], 255)
#     return mask


# def overlay_mask(img, mask, color=(0,255,0), alpha=0.5):
#     overlay = img.copy()
#     overlay[mask==255] = color
#     return cv2.addWeighted(img, 1-alpha, overlay, alpha, 0)


# def apply_hand_masks(plants, labels_folder):
#     """
#     Apply each JSON mask named e.g. plant1_frame5.json
#     to every stitched image whose raw_images[0][1] was plant1_frame5.tif.
#     """
#     # build { "plant1_frame5": "/…/plant1_frame5.json", … }
#     jsons = glob.glob(os.path.join(labels_folder, "*.json"))
#     jm = {os.path.splitext(os.path.basename(j))[0]: j for j in jsons}

#     for pname, data in plants.items():
#         stitched = data.get("stitched")
#         if stitched is None:
#             if DEBUG: print(f"⚠ No stitched image for {pname}")
#             continue

#         # extract base name from the original TIFF
#         raw = data.get("raw_images", [])
#         if not raw:
#             if DEBUG: print(f"⚠ No raw_images entry for {pname}")
#             continue
#         _, fn = raw[0]                   # e.g. "plant1_frame5.tif"
#         base = os.path.splitext(fn)[0]   # "plant1_frame5"

#         # load the matching JSON (or blank mask)
#         jfile = jm.get(base)
#         if jfile:
#             m = load_hand_labeled_mask(jfile, stitched.shape[:2])
#             mask = (m > 127).astype(np.uint8) * 255
#         else:
#             if DEBUG: print(f"⚠ No JSON annotation for {base}")
#             mask = np.zeros(stitched.shape[:2], dtype=np.uint8)

#         data["mask"]    = mask
#         data["overlay"] = overlay_mask(stitched, mask)

#     return plants
# def load_raw_images_all_frames(input_root_folder, DEBUG=False):
#     """
#     Load every frame per plant, except:
#       • ignore plants in _IGNORE
#       • for plants in _BORROW, only load the specified source frame
#     Returns a dict keyed by "YYYY-MM-DD_plantX_frameY".
#     """
#     plants = {}

#     for date_name in sorted(os.listdir(input_root_folder)):
#         date_path = os.path.join(input_root_folder, date_name)
#         if not os.path.isdir(date_path):
#             continue

#         for plant_name in sorted(os.listdir(date_path)):
#             plant_path = os.path.join(date_path, plant_name)
#             if not os.path.isdir(plant_path):
#                 continue

#             # extract numeric ID
#             try:
#                 pid = int(plant_name.replace("plant", ""))
#             except ValueError:
#                 continue

#             # skip ignored plants
#             if pid in _IGNORE:
#                 if DEBUG: print(f"Ignoring plant{pid}")
#                 continue

#             # Are we borrowing?
#             if pid in _BORROW:
#                 src_pid, src_frame = _BORROW[pid]
#                 src_folder = f"plant{src_pid}"
#                 fname = f"{src_folder}_frame{src_frame}.tif"
#                 fpath = os.path.join(date_path, src_folder, fname)
#                 key   = f"{date_name}_{plant_name}_frame{src_frame}"
#                 if os.path.exists(fpath):
#                     try:
#                         img = Image.open(fpath)
#                         plants[key] = {"raw_images": [(img, fname)]}
#                     except Exception as e:
#                         if DEBUG: print(f"Failed to load borrow {fpath}: {e}")
#                 else:
#                     if DEBUG: print(f"Missing borrow file {fpath}")
#                 continue

#             # Otherwise, load ALL frames for this plant
#             pattern = os.path.join(plant_path, f"{plant_name}_frame*.tif")
#             for fpath in sorted(glob.glob(pattern)):
#                 fname = os.path.basename(fpath)
#                 # derive frame id for key
#                 frame_id = fname.split("_frame")[-1].split(".tif")[0]
#                 key = f"{date_name}_{plant_name}_frame{frame_id}"
#                 try:
#                     img = Image.open(fpath)
#                     plants[key] = {"raw_images": [(img, fname)]}
#                 except Exception as e:
#                     if DEBUG: print(f"Failed to load {fpath}: {e}")

#     return plants
# def load_all_raw_images(input_root_folder, DEBUG=False):
#     """
#     Load every .tif frame per plant from all date folders, without skipping or borrowing.
#     Returns a dict keyed by "YYYY-MM-DD_plantX_frameY".
#     """
#     plants = {}

#     for date_name in sorted(os.listdir(input_root_folder)):
#         date_path = os.path.join(input_root_folder, date_name)
#         if not os.path.isdir(date_path):
#             continue

#         for plant_name in sorted(os.listdir(date_path)):
#             plant_path = os.path.join(date_path, plant_name)
#             if not os.path.isdir(plant_path):
#                 continue

#             # Load ALL .tif frames for this plant
#             pattern = os.path.join(plant_path, f"{plant_name}_frame*.tif")
#             for fpath in sorted(glob.glob(pattern)):
#                 fname = os.path.basename(fpath)
#                 try:
#                     # extract frame number from filename
#                     frame_id = fname.split("_frame")[-1].split(".tif")[0]
#                     key = f"{date_name}_{plant_name}_frame{frame_id}"

#                     img = Image.open(fpath)
#                     plants[key] = {"raw_images": [(img, fname)]}

#                 except Exception as e:
#                     if DEBUG:
#                         print(f"Failed to load {fpath}: {e}")

#     return plants
# def load_frame8_per_plant(input_root_folder):
#     """
#     Load only frame8 for each plant across all dates.
#     Returns dict of 'YYYY-MM-DD_plantX' → {'raw_images': [(image, filename)]}
#     """
#     from PIL import Image
#     plants = {}
#     for date in sorted(os.listdir(input_root_folder)):
#         date_path = os.path.join(input_root_folder, date)
#         if not os.path.isdir(date_path):
#             continue

#         for plant in sorted(os.listdir(date_path)):
#             plant_path = os.path.join(date_path, plant)
#             if not os.path.isdir(plant_path):
#                 continue

#             frame_path = os.path.join(plant_path, f"{plant}_frame8.tif")
#             if os.path.exists(frame_path):
#                 try:
#                     img = Image.open(frame_path)
#                     key = f"{date}_{plant}"
#                     plants[key] = {"raw_images": [(img, f"{plant}_frame8.tif")]}
#                 except Exception as e:
#                     print(f"❌ Failed to load {frame_path}: {e}")
#     return plants


# def load_selected_frame_per_plant(input_root_folder):
#     """
#     Load one frame per plant across all dates, with these rules:
    
#     1. Folder-substitution mapping (which plant folder to pull from):
#        • plant16 → plant15
#        • plant15 → plant14
#        • plant14 → plant13
#        • plant13 → plant13
#        • plant33 → plant34
#        • plant34 → plant35
#        • plant24 → plant25
#        • plant25 → plant25
#        • plant35 → plant36
#        • plant36 → plant37
#        • plant37 → plant37
#        • plant44 → plant43
#        • plant45 → plant44

#     2. Frame-number overrides (use frame9 instead of frame8) for:
#        plant1,  plant2,  plant12, plant13, plant15,
#        plant25, plant32, plant38, plant39, plant42,
#        plant43, plant44, plant45, plant47, plant48

#     All other plants default to frame8 of their (possibly substituted) folder.
#     Returns dict of 'YYYY-MM-DD_plantX' → {'raw_images': [(PIL.Image, filename)]}
#     """
#     substitutes = {
#         'plant16': 'plant15',
#         'plant15': 'plant14',
#         'plant14': 'plant13',   # now uses image13
#         'plant13': 'plant13',
#         'plant33': 'plant34',
#         'plant34': 'plant35',
#         'plant24': 'plant25',
#         'plant25': 'plant25',
#         'plant35': 'plant36',
#         'plant36': 'plant37',
#         'plant37': 'plant37',
#         'plant44': 'plant43',   # use image43
#         'plant45': 'plant44',   # use image44
#     }

#     frame_override = {
#         'plant1':  '9',
#         'plant2':  '10',
#         'plant3':  '9',
#         'plant5':  '9',
#         'plant6':  '9',
#         'plant7':  '9',
#         'plant10': '9',
#         'plant11': '9',
#         'plant12': '9',
#         'plant13': '10',
#         'plant14': '9',
#         'plant15': '11',
#         'plant19': '10',
#         'plant21': '9',
#         'plant22': '10',
#         'plant25': '9',
#         'plant27': '10',
#         'plant30': '9',
#         'plant31': '10',
#         'plant32': '9',
#         'plant33': '10',
#         'plant35': '9',
#         'plant38': '9',
#         'plant39': '9',
#         'plant41': '9',
#         'plant42': '10',
#         'plant43': '10',
#         'plant44': '9',
#         'plant45': '10',
#         'plant47': '10',
#         'plant48': '11',
#     }

#     plants = {}
#     for date in sorted(os.listdir(input_root_folder)):
#         date_path = os.path.join(input_root_folder, date)
#         if not os.path.isdir(date_path):
#             continue

#         for plant in sorted(os.listdir(date_path)):
#             plant_path = os.path.join(date_path, plant)
#             if not os.path.isdir(plant_path):
#                 continue

#             source = substitutes.get(plant, plant)
#             frame  = frame_override.get(plant, '8')
#             filename  = f"{source}_frame{frame}.tif"
#             frame_path = os.path.join(date_path, source, filename)

#             if os.path.exists(frame_path):
#                 try:
#                     img = Image.open(frame_path)
#                     key = f"{date}_{plant}"
#                     plants[key] = {"raw_images": [(img, filename)]}
#                 except Exception as e:
#                     print(f"❌ Failed to load {frame_path}: {e}")
#             else:
#                 print(f"⚠ Missing {filename} in {os.path.join(date_path, source)}")

#     return plants



# def load_selected_frame_per_plant(input_root_folder):
#     """
#     Load one (or multiple) frames per plant across all dates, with these rules:

#     1. Folder-substitution mapping:
#        plant16 → plant15  
#        plant15 → plant14  
#        plant14 → plant13  
#        plant13 → plant13  
#        plant33 → plant34  
#        plant34 → plant35  
#        plant24 → plant25  
#        plant25 → plant25  
#        plant35 → plant36  
#        plant36 → plant37  
#        plant37 → plant37  
#        plant44 → plant43  
#        plant45 → plant44  

#     2. Frame-number overrides (use frameX instead of frame8) for a single frame:
#        plant1,2,3,5,6,7,10,11,12,13,14,15,19,21,22,25,27,30,31,32,33,35,38,39,41,42,43,44,45,47,48

#     3. **Multi-frame plants** (load all 1…13) for:
#        plant8, plant19, plant28, plant29, plant33, plant35, plant36, plant42, plant44

#     Returns a dict:
#       'YYYY-MM-DD_plantX' → {'raw_images': [(PIL.Image, filename), …]}
#     """

#     substitutes = {
#         'plant16': 'plant15',
#         'plant15': 'plant14',
#         'plant14': 'plant13',
#         'plant13': 'plant13',
#         'plant33': 'plant34',
#         'plant34': 'plant35',
#         'plant24': 'plant25',
#         'plant25': 'plant25',
#         'plant35': 'plant36',
#         'plant36': 'plant37',
#         'plant37': 'plant37',
#         'plant44': 'plant43',
#         'plant45': 'plant44',
#     }

#     frame_override = {
#         'plant1':  '9',
#         'plant2':  '10',
#         'plant3':  '9',
#         'plant5':  '9',
#         'plant6':  '9',
#         'plant7':  '9',
#         'plant10': '9',
#         'plant11': '9',
#         'plant12': '9',
#         'plant13': '10',
#         'plant14': '9',
#         'plant15': '11',
#         'plant19': '10',
#         'plant21': '9',
#         'plant22': '10',
#         'plant25': '9',
#         'plant27': '10',
#         'plant30': '9',
#         'plant31': '10',
#         'plant32': '9',
#         'plant33': '10',
#         'plant35': '9',
#         'plant38': '9',
#         'plant39': '9',
#         'plant41': '9',
#         'plant42': '10',
#         'plant43': '10',
#         'plant44': '9',
#         'plant45': '10',
#         'plant47': '10',
#         'plant48': '11',
#     }

#     # these get *all* frames 1–13
#     multi_frame_plants = {
#         'plant8', 'plant19', 'plant28', 'plant29',
#         'plant33', 'plant35', 'plant36', 'plant42', 'plant44'
#     }

#     plants = {}
#     for date in sorted(os.listdir(input_root_folder)):
#         date_path = os.path.join(input_root_folder, date)
#         if not os.path.isdir(date_path):
#             continue

#         for plant in sorted(os.listdir(date_path)):
#             plant_path = os.path.join(date_path, plant)
#             if not os.path.isdir(plant_path):
#                 continue

#             source = substitutes.get(plant, plant)
#             key = f"{date}_{plant}"
#             plants[key] = {"raw_images": []}

#             if plant in multi_frame_plants:
#                 # load frames 1 through 13
#                 for i in range(1, 14):
#                     fname = f"{source}_frame{i}.tif"
#                     fpath = os.path.join(date_path, source, fname)
#                     if os.path.exists(fpath):
#                         try:
#                             img = Image.open(fpath)
#                             plants[key]["raw_images"].append((img, fname))
#                         except Exception as e:
#                             print(f"❌ Failed to load {fpath}: {e}")
#                     else:
#                         print(f"⚠ Missing {fname} in {os.path.join(date_path, source)}")

#             else:
#                 # single-frame case
#                 frame = frame_override.get(plant, '8')
#                 fname = f"{source}_frame{frame}.tif"
#                 fpath = os.path.join(date_path, source, fname)
#                 if os.path.exists(fpath):
#                     try:
#                         img = Image.open(fpath)
#                         plants[key]["raw_images"].append((img, fname))
#                     except Exception as e:
#                         print(f"❌ Failed to load {fpath}: {e}")
#                 else:
#                     print(f"⚠ Missing {fname} in {os.path.join(date_path, source)}")

#     return plants

def load_selected_frame_flat(input_root_folder):
    """
    Load frames per plant across all dates, flattening so each
    dict key is YYYY_MM_DD_plantX_frameY and each value is:
      {'raw_image': (PIL.Image, filename)}

    Respects your same substitutes, frame_overrides, and multi-frame sets.
    """
    substitutes = {
        'plant16': 'plant15', 'plant15': 'plant14', 'plant14': 'plant13',
        'plant13': 'plant13', 'plant33': 'plant34', 'plant34': 'plant35',
        'plant24': 'plant25', 'plant25': 'plant25', 'plant35': 'plant36',
        'plant36': 'plant37', 'plant37': 'plant37', 'plant44': 'plant43',
        'plant45': 'plant44',
    }
    frame_override = {
        'plant1':'9','plant2':'10','plant3':'9','plant5':'7','plant6':'9', 'plant8':'5',
        'plant7':'9','plant10':'9','plant11':'9','plant12':'9',
        'plant13':'10','plant14':'8','plant15':'11','plant19':'4','plant20':'7',
        'plant21':'9','plant22':'10','plant25':'4','plant26':'2','plant27':'10','plant28':'9','plant29':'2',
        'plant30':'9','plant31':'10','plant32':'9','plant33':'8',
        'plant35':'9','plant36':'4','plant38':'9','plant39':'9','plant41':'9',
        'plant42':'6','plant43':'10','plant44':'9','plant45':'7',
        'plant47':'10','plant48':'11',
    }
    

    flat = {}
    for date in sorted(os.listdir(input_root_folder)):
        date_path = os.path.join(input_root_folder, date)
        if not os.path.isdir(date_path):
            continue

        # switch dashes → underscores for key
        date_key = date.replace('-', '_')

        for plant in sorted(os.listdir(date_path)):
            plant_path = os.path.join(date_path, plant)
            if not os.path.isdir(plant_path):
                continue

            source = substitutes.get(plant, plant)

            
            frames = [int(frame_override.get(plant, '8'))]

            for f in frames:
                fn = f"{source}_frame{f}.tif"
                fp = os.path.join(date_path, source, fn)
                if os.path.exists(fp):
                    try:
                        img = Image.open(fp)
                        key = f"{date_key}_{plant}_frame{f}"
                        flat[key] = {'raw_image': (img, fn)}
                    except Exception as e:
                        print(f"❌ Failed to load {fp}: {e}")
                else:
                    print(f"⚠ Missing {fn} in {os.path.join(date_path, source)}")

    return flat