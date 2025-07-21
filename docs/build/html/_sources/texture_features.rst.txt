Texture Features
================

.. toctree::
   :maxdepth: 1

This page provides detailed explanations for each texture feature extracted by the pipeline.

LBP (Local Binary Pattern)
--------------------------
**Description:**
A texture descriptor that encodes the local spatial pattern of pixel intensities.

**Interpretation:**
LBP is useful for capturing fine texture details and is robust to illumination changes.

HOG (Histogram of Oriented Gradients)
-------------------------------------
**Description:**
A feature descriptor that counts occurrences of gradient orientation in localized portions of an image.

**Interpretation:**
HOG is effective for capturing edge and shape information.

Lacunarity
----------
**Description:**
A measure of texture heterogeneity and gap distribution at different scales.

- **Lac1:** Base window size
- **Lac2:** Multi-scale average
- **Lac3:** Deep learning-based lacunarity (DBC)

EHD (Edge Histogram Descriptor)
-------------------------------
**Description:**
Describes the distribution of edge directions in the image, useful for characterizing structure and texture. 