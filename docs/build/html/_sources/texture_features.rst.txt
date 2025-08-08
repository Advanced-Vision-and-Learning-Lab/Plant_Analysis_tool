Texture Features
================

.. toctree::
   :maxdepth: 1

This page provides detailed explanations for each texture feature extracted by the pipeline, including algorithm, interpretation, and example images.

LBP (Local Binary Pattern)
--------------------------
**Description:**
A texture descriptor that encodes the local spatial pattern of pixel intensities by thresholding the neighborhood of each pixel and converting the result into a binary number.

**Algorithm:**
- For each pixel, compare its value to its neighbors (typically 8 neighbors in a 3x3 window).
- Assign 1 if the neighbor is greater than or equal to the center pixel, 0 otherwise.
- The resulting 8-bit binary number is the LBP value for that pixel.

**Interpretation:**
LBP is robust to illumination changes and captures fine texture details. High LBP values indicate complex textures; low values indicate uniform regions.

**Image:**
.. image:: _static/lbp_example.png
   :alt: LBP Example
   :width: 300px

---

HOG (Histogram of Oriented Gradients)
-------------------------------------
**Description:**
A feature descriptor that counts occurrences of gradient orientation in localized portions of an image, capturing edge and shape information.

**Algorithm:**
- Compute gradients (edge directions) for each pixel.
- Divide the image into small cells and compute a histogram of gradient directions for each cell.
- Normalize histograms across blocks of cells for illumination invariance.

**Interpretation:**
HOG is effective for capturing edge and shape information, useful for distinguishing structural patterns in plant images.

**Image:**
.. image:: _static/hog_example.png
   :alt: HOG Example
   :width: 300px

---

Lacunarity
----------
**Description:**
A measure of texture heterogeneity and gap distribution at different scales. The pipeline computes three variants:
- **Lac1:** Base window size
- **Lac2:** Multi-scale average
- **Lac3:** Deep learning-based lacunarity (DBC)

**Algorithm:**
- For each window size, compute the mean and variance of pixel intensities.
- Lacunarity is calculated as the ratio of variance to the square of the mean, plus 1.
- DBC Lacunarity uses a deep learning model to estimate lacunarity at multiple scales.

**Interpretation:**
- High lacunarity: More gaps/heterogeneity in texture (e.g., sparse or patchy regions)
- Low lacunarity: More uniform texture

**Image:**
.. image:: _static/lacunarity_example.png
   :alt: Lacunarity Example
   :width: 300px

---

EHD (Edge Histogram Descriptor)
-------------------------------
**Description:**
Describes the distribution of edge directions in the image, useful for characterizing structure and texture.

**Algorithm:**
- Apply a set of directional edge filters to the image.
- For each direction, count the number of edge responses above a threshold.
- The resulting histogram summarizes the edge orientation distribution.

**Interpretation:**
- High values in certain bins indicate dominant edge directions (e.g., leaf veins, stem orientation).
- Uniform histogram: Random or isotropic texture.

**Image:**
.. image:: _static/ehd_example.png
   :alt: EHD Example
   :width: 300px

---

Statistics Computed
-------------------
For each feature above (and for each band: color, green, nir, red_edge, red, pca), the following statistics are computed:
- Mean
- Standard deviation
- Max
- Min
- Median
- 25th percentile (q25)
- 75th percentile (q75)
- Fraction of NaN values 