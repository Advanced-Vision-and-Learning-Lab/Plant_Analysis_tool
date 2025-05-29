from plantcv import plantcv as pcv
import numpy as np
import cv2

def preprocess_mask(mask, kernel_size: int = 5, min_area: int = 500):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    opened = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(opened, connectivity=8)
    clean = np.zeros_like(opened)
    for lbl in range(1, num_labels):
        if stats[lbl, cv2.CC_STAT_AREA] >= min_area:
            clean[labels == lbl] = 255
    return clean

def detect_and_return_morphology(img, mask):
    # Set PlantCV global parameters (optional if not set elsewhere)
    pcv.params.debug = None
    pcv.params.text_size = 0.7
    pcv.params.text_thickness = 2
    pcv.params.line_thickness = 3
    pcv.params.dpi = 100

    mask_clean = preprocess_mask(mask, kernel_size=7, min_area=1000)
    skel = pcv.morphology.skeletonize(mask=mask_clean)
    pr1, _, edge = pcv.morphology.prune(skel_img=skel, size=50, mask=mask_clean)
    pr2, _, edge = pcv.morphology.prune(skel_img=pr1, size=10, mask=mask_clean)

    pcv.morphology.fill_segments(mask=mask_clean, objects=list(edge), label="default")
    pcv.morphology.find_branch_pts(skel_img=pr2, mask=mask_clean, label="default")
    pcv.morphology.find_tips(skel_img=pr2, mask=mask_clean, label="default")
    leaf, stem = pcv.morphology.segment_sort(skel_img=pr2, objects=list(edge), mask=mask_clean)
    pcv.morphology.segment_id(skel_img=pr2, objects=leaf, mask=mask_clean)

    lm, n = pcv.create_labels(mask=mask_clean)
    pcv.analyze.size(img=img, labeled_mask=lm, n_labels=n, label="default")

    # Get extracted values
    obs = pcv.outputs.observations.get("default_1", {})
    features = {k: v["value"] for k, v in obs.items()}
    return features
