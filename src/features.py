import os
import numpy as np
from src.composite import convert_to_uint8
import cv2
import boto3
import io
import matplotlib.pyplot as plt


# Save image to S3 helper
s3_client = boto3.client('s3')

def save_index_to_s3(bucket, key, image_np):
    s3 = boto3.client('s3')
    success, encoded_img = cv2.imencode('.png', image_np)
    if success:
        s3.upload_fileobj(io.BytesIO(encoded_img.tobytes()), bucket, key)

def save_image_to_s3(bucket, key, img_np, cmap='YlGn', title=None):
    fig, ax = plt.subplots(figsize=(6, 6))
    im = ax.imshow(img_np, cmap=cmap)
    ax.axis('off')
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    if title:
        ax.set_title(title, fontsize=16)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    s3_client.upload_fileobj(buf, bucket, key)

# Vegetation Indices
VEG_INDEX_FORMULAS = {
    "ARI": lambda green, red_edge: (1.0 / (green + 1e-10)) - (1.0 / (red_edge + 1e-10)),
    # "ARI": lambda nir, red_edge, red: np.divide(nir-red_edge, red+1e-10, out=np.zeros_like(nir), where=red!=0),
    "MCARI": lambda red_edge, red, green: ((red_edge - red) - 0.2*(red_edge - green)) * np.divide(red_edge, red+1e-10, out=np.zeros_like(red_edge), where=red!=0),
    "GRNDVI": lambda nir, green, red: np.divide(nir-(green+red), nir+(green+red)+1e-10, out=np.zeros_like(nir), where=(nir+green+red)!=0),
    "CVI": lambda nir, red, green: np.divide(nir*red, (green**2.0)+1e-10, out=np.zeros_like(nir), where=(green**2.0)!=0),
    "ARI2": lambda nir, green, red_edge: nir*np.divide(1, green+1e-10, out=np.zeros_like(nir), where=green!=0) - nir*np.divide(1, red_edge+1e-10, out=np.zeros_like(nir), where=red_edge!=0),
    "CIRE": lambda nir, red_edge, epsilon=1e-10: (nir/(red_edge+epsilon))-1.0,
    "DSWI4": lambda green, red, epsilon=1e-10: green/(red+epsilon),
    "DVI": lambda nir, red, epsilon=1e-10: nir-red,
    "ExR": lambda red, green, epsilon=1e-10: 1.3 *red - green,
    "GEMI": lambda nir, red, epsilon=1e-10: (
        (
            (2 * (nir**2 - red**2) + 1.5 * nir + 0.5 * red) / (nir + red + 0.5 + epsilon)
        ) * (1 - 0.25 * (
            (2 * (nir**2 - red**2) + 1.5 * nir + 0.5 * red) / (nir + red + 0.5 + epsilon)
        )) - ((red - 0.125) / (1 - red + epsilon))
    ),
    "GNDVI": lambda nir, green, epsilon=1e-10: (nir-green)/(nir+green+epsilon),
    "GOSAVI": lambda nir, green, epsilon=1e-10: (nir-green)/(nir+green+0.16+epsilon),
    "GRVI": lambda nir, green, epsilon=1e-10: nir/(green+epsilon),
    "IPVI": lambda nir, red, epsilon=1e-10: nir/(nir+red+epsilon),
    "MCARI1": lambda nir, red, green, epsilon=1e-10: 1.2*(2.5*(nir-red)-1.3*(nir-green)),
    "MCARI2": lambda nir, red, green, epsilon=1e-10: (1.5*(2.5*(nir-red)-1.3*(nir-green)))/np.sqrt((2*nir+1)**2-(6*nir-5*np.sqrt(red+epsilon))),
    "MGRVI": lambda green, red, epsilon=1e-10: (green**2.0-red**2.0)/(green**2.0+red**2.0+epsilon),
    "MSAVI": lambda nir, red, epsilon=1e-10: 0.5*(2.0*nir+1-np.sqrt((2*nir+1)**2-8*(nir-red))),
    "MSR": lambda nir, red, epsilon=1e-10: (nir/(red+epsilon)-1)/np.sqrt(nir/(red+epsilon)+1),
    "MTVI1": lambda nir, green, red, epsilon=1e-10: 1.2*(1.2*(nir-green)-2.5*(red-green)),
    "MTVI2": lambda nir, green, red, epsilon=1e-10: (1.5*(1.2*(nir-green)-2.5*(red-green)))/np.sqrt((2*nir+1)**2-(6*nir-5*np.sqrt(red+epsilon))),
    "NDVI": lambda nir, red, epsilon=1e-10: (nir-red)/(nir+red+epsilon),
    "NDRE": lambda nir, red_edge, epsilon=1e-10: (nir-red_edge)/(nir+red_edge+epsilon),
    "NDWI": lambda green, nir, epsilon=1e-10: (green-nir)/(green+nir+epsilon),
    "NLI": lambda nir, red, epsilon=1e-10: ((nir**2)-red)/((nir**2)+red+epsilon),
    "OSAVI": lambda nir, red, soil_factor=0.16: np.divide(nir-red, nir+red+soil_factor+1e-10, out=np.zeros_like(nir), where=(nir+red+soil_factor)!=0),
    "RDVI": lambda nir, red, epsilon=1e-10: (nir-red)/np.sqrt(nir+red+epsilon),
    "PVI": lambda nir, red, a=0.5, b=0.3, epsilon=1e-10: (nir-a*red-b)/(np.sqrt(1+a**2)+epsilon),
    "SR": lambda nir, red, epsilon=1e-10: nir/(red+epsilon),
    "TCARIOSAVI": lambda red_edge, red, green, nir, epsilon=1e-10: (
    (3 * (red_edge - red) - 0.2 * (red_edge - green) * (red_edge / (red + epsilon))) /
    (1 + 0.16 * ((nir - red) / (nir + red + 0.16 + epsilon)))),
    "TNDVI": lambda nir, red, a=1.0, b=1.0, epsilon=1e-10: np.sqrt(np.clip(((a * nir - b * red) / (a * nir + b * red + epsilon)) + 0.5, 0, None)),
    "TSAVI": lambda nir, red, s=0.33, a=0.5, X=1.5, epsilon=1e-10: (s * (nir - s * red - a)) / (a * nir + red - a * s + X * (1 + s**2) + epsilon),
    "GSAVI": lambda nir, green, l=0.5: (1+l)*np.divide(nir-green, nir+green+l+1e-10, out=np.zeros_like(nir), where=(nir+green+l)!=0),
    "RI": lambda red, green, epsilon=1e-10: (red-green)/(red+green+epsilon),
    "TCARI": lambda red_edge, red, green: 3*((red_edge-red)-0.2*(red_edge-green)*np.divide(red_edge,red+1e-10, out=np.zeros_like(red_edge), where=red!=0)),
    # "IRECI": lambda nir, red_edge, red: np.divide(nir-red_edge, red_edge-red+1e-10, out=np.zeros_like(nir), where=(red_edge-red)!=0),
    "LCI": lambda nir, red_edge, epsilon=1e-10: (nir-red_edge)/(nir+red_edge+epsilon),
    "CIgreen": lambda nir, green, epsilon=1e-10: (nir/(green+epsilon))-1,
    "NGRDI": lambda green, red, epsilon=1e-10: (green-red)/(green+red+epsilon),
    "WDVI": lambda nir, red, a=0.5: nir - a * red,  # a is the soil line slope, typically ~0.5
    "EVI2": lambda nir, red, epsilon=1e-10: 2.5 * (nir - red) / (nir + red + 1 + epsilon),
    "AVI": lambda nir, red, epsilon=1e-10: np.cbrt(nir * (1.0 - red) * (nir - red + epsilon)),
    "SIPI2": lambda nir, green, red: (nir - green) / (nir - red + 1e-10),
    # "CIRE2": lambda nir, red_edge, epsilon=1e-10: (nir-red_edge)/(nir+red_edge+epsilon),
    "RRI1": lambda nir, red_edge, epsilon=1e-10: nir / (red_edge + epsilon),
    "CCCI": lambda nir, red_edge, red, epsilon=1e-10: (((nir - red_edge) * (nir + red)) /((nir + red_edge) * (nir - red) + epsilon)),
}
# --- 9b. Required bands for each index ---
# Keys must match VEG_INDEX_FORMULAS
# --- Mapping: Vegetation Index -> Required Spectral Bands ---
VEG_INDEX_CHANNELS = {
    "ARI": ["green", "red_edge"],
    "MCARI": ["red_edge", "red", "green"],
    "GRNDVI": ["nir", "green", "red"],
    "CVI": ["nir", "red", "green"],
    "ARI2": ["nir", "green", "red_edge"],
    "CIRE": ["nir", "red_edge"],
    "DSWI4": ["green", "red"],
    "DVI": ["nir", "red"],
    "ExR": ["red", "green"],
    "GEMI": ["nir", "red"],
    "GNDVI": ["nir", "green"],
    "GOSAVI": ["nir", "green"],
    "GRVI": ["nir", "green"],
    "IPVI": ["nir", "red"],
    "MCARI1": ["nir", "red", "green"],
    "MCARI2": ["nir", "red", "green"],
    "MGRVI": ["green", "red"],
    "MSAVI": ["nir", "red"],
    "MSR": ["nir", "red"],
    "MTVI1": ["nir", "green", "red"],
    "MTVI2": ["nir", "green", "red"],
    "NDVI": ["nir", "red"],
    "NDRE": ["nir", "red_edge"],
    "NDWI": ["green", "nir"],
    "NLI": ["nir", "red"],
    "OSAVI": ["nir", "red"],
    "RDVI": ["nir", "red"],
    "PVI": ["nir", "red"],
    "SR": ["nir", "red"],
    "TCARIOSAVI": ["red_edge", "red", "green", "nir"],
    "TNDVI": ["nir", "red"],
    "TSAVI": ["nir", "red"],
    "GSAVI": ["nir", "green"],
    "RI": ["red", "green"],
    "TCARI": ["red_edge", "red", "green"],
    "LCI": ["nir", "red_edge"],
    "CIgreen": ["nir", "green"],
    "NGRDI": ["green", "red"],
    "WDVI": ["nir", "red"],
    "EVI2": ["nir", "red"],
    "AVI": ["nir", "red"],
    "SIPI2": ["nir", "green", "red"],
    "RRI1": ["nir", "red_edge"],
    "CCCI": ["nir", "red_edge", "red"]
}

def compute_veg_indices(plants, s3_bucket=None, s3_prefix=None):

    for p, d in plants.items():
        spec, mask = d.get("spectral_stack"), d.get("mask")
        if spec is None or mask is None:
            continue

        raw, disp = {}, {}

        for idx, func in VEG_INDEX_FORMULAS.items():
            bands = VEG_INDEX_CHANNELS.get(idx)
            if bands is None:
                continue
            try:
                vals = [spec[b].squeeze(-1) for b in bands]
            except KeyError:
                continue

            arr = func(*vals)
            masked = np.where(mask == 255, arr, np.nan)
            img8 = convert_to_uint8(masked)
            raw[idx], disp[idx] = masked, img8

            if s3_bucket and s3_prefix:
                s3_key = f"{s3_prefix}/vegetation_indices/{idx}.png"
                save_image_to_s3(s3_bucket, s3_key, img8, cmap='YlGn', title=idx)

        d["vegetation_indices"] = disp
        d["original_index_values"] = raw

    return plants

def compute_veg_index_features(plants):
    feature_table = []
    for plant_id, data in plants.items():
        mask = data.get("mask")
        indices = data.get("original_index_values")
        if mask is None or indices is None:
            continue
        mask = (mask == 255)
        for idx_name, idx_array in indices.items():
            if idx_array is None:
                continue
            values = idx_array[mask]
            if values.size == 0:
                continue
            feature_table.append({
                "index": idx_name,
                "mean": float(np.nanmean(values)),
                "std": float(np.nanstd(values)),
                "max": float(np.nanmax(values)),
                "min": float(np.nanmin(values)),
                "median": float(np.nanmedian(values)),
                "q25": float(np.nanpercentile(values, 25)),
                "q75": float(np.nanpercentile(values, 75)),
                "nan_fraction": float(np.isnan(values).sum() / values.size)
            })
    return feature_table
