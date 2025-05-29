# Cell 4: Composite & Spectral Stack
import numpy as np
from itertools import product

def convert_to_uint8(arr):
    a = np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0)
    norm = (a - a.min()) / (np.ptp(a) + 1e-6) * 255
    return norm.astype(np.uint8)


def process_raw_image(pil_img):
    # split the 4-band RAW into tiles and stack them
    d = pil_img.size[0] // 2
    boxes = [(j, i, j + d, i + d)
             for i, j in product(range(0, pil_img.height, d),
                                range(0, pil_img.width,  d))]
    stack = np.stack([np.array(pil_img.crop(b), float) for b in boxes], axis=-1)
    # bands come in order: [green, red, red_edge, nir]
    #green = stack[:, :, 0] 
    #red = stack[:, :, 1]
    #red_edge = stack[:, :, 2]
    #nir = stack[:, :, 3]
    green, red, red_edge, nir = np.split(stack, 4, axis=-1)
    # build pseudo-RGB as (nir, red_edge, red)
    comp = np.concatenate([green, red_edge, red], axis=-1)
    return convert_to_uint8(comp), {"green": green, "red": red, "red_edge": red_edge, "nir": nir}

# def create_composites(plants):
#     """
#     For each plant, take the first raw image (frame5), generate a pseudo-RGB composite
#     and store both the 8-bit composite and the full spectral stack.
#     """
#     for p, d in plants.items():
#         if not d.get("raw_images"):  # skip if no images
#             continue
#         im, _ = d["raw_images"][0]
#         comp, spec = process_raw_image(im)
#         d["composite"] = comp           # pseudo-RGB BGR-ready composite
#         d["spectral_stack"] = spec      # dict of raw bands
#     return plants
def create_composites(plants):
    """
    For each item in `plants` (whether flat or grouped),
    grab exactly one raw image and produce:
      pdata["composite"]      = 8-bit BGR numpy array
      pdata["spectral_stack"] = whatever your process_raw_image returns
    """
    for key, pdata in plants.items():
        # 1) find the PIL.Image in either flat or grouped fields
        if "raw_image" in pdata:
            im, _ = pdata["raw_image"]
        elif pdata.get("raw_images"):
            im, _ = pdata["raw_images"][0]
        else:
            # nothing to do here
            continue

        # 2) process it
        comp, spec = process_raw_image(im)

        # 3) attach exactly these two keys
        pdata["composite"]      = comp
        pdata["spectral_stack"] = spec

    return plants
