Vegetation Indices
==================

.. toctree::
   :maxdepth: 1

This page provides detailed explanations for each vegetation index supported by the pipeline, including formulas and interpretation.

NDVI (Normalized Difference Vegetation Index)
---------------------------------------------
**Formula:**

.. math::
   NDVI = \frac{NIR - Red}{NIR + Red}

**Description:**
NDVI is a widely used index for quantifying vegetation greenness and health. High NDVI values indicate healthy, green vegetation.

**Image:**
.. image:: _static/ndvi_example.png
   :alt: NDVI Example
   :width: 300px

---

GNDVI (Green Normalized Difference Vegetation Index)
----------------------------------------------------
**Formula:**

.. math::
   GNDVI = \frac{NIR - Green}{NIR + Green}

**Description:**
GNDVI is sensitive to chlorophyll concentration and is useful for assessing plant health and nitrogen status.

**Image:**
.. image:: _static/gndvi_example.png
   :alt: GNDVI Example
   :width: 300px

---

# Add similar sections for each index (NDRE, EVI, SAVI, etc.) 