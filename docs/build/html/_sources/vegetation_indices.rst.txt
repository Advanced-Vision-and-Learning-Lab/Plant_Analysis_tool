Vegetation Indices
==================

.. toctree::
   :maxdepth: 1

This page provides detailed explanations for each vegetation index supported by the pipeline, including formulas, descriptions, and interpretation.

NDVI (Normalized Difference Vegetation Index)
---------------------------------------------
**Formula:**

.. math::
   NDVI = \frac{NIR - Red}{NIR + Red}

**Description:**
NDVI quantifies vegetation greenness and health. High NDVI values indicate healthy, green vegetation; low values indicate stressed or sparse vegetation.

**Typical Range:** -1 to 1

**Interpretation:**
- NDVI > 0.5: Dense, healthy vegetation
- NDVI ~ 0: Bare soil or sparse vegetation
- NDVI < 0: Water, snow, or non-vegetated surfaces

**Image:**
.. image:: _static/NDVI.png
   :alt: NDVI
   :width: 300px

---

GNDVI (Green Normalized Difference Vegetation Index)
----------------------------------------------------
**Formula:**

.. math::
   GNDVI = \frac{NIR - Green}{NIR + Green}

**Description:**
GNDVI is sensitive to chlorophyll concentration and is useful for assessing plant health and nitrogen status.

**Typical Range:** -1 to 1

**Interpretation:**
- High GNDVI: High chlorophyll, healthy vegetation
- Low GNDVI: Stressed or sparse vegetation

**Image:**
.. image:: _static/GNDVI.png
   :alt: GNDVI
   :width: 300px

---

NDRE (Normalized Difference Red Edge Index)
-------------------------------------------
**Formula:**

.. math::
   NDRE = \frac{NIR - RedEdge}{NIR + RedEdge}

**Description:**
NDRE is sensitive to chlorophyll content and is useful for detecting plant stress before it is visible.

**Typical Range:** -1 to 1

**Interpretation:**
- High NDRE: Healthy, high-chlorophyll vegetation
- Low NDRE: Stressed or senescent vegetation

**Image:**
.. image:: _static/NDRE.png
   :alt: NDRE
   :width: 300px

---

GRNDVI (Green-Red Normalized Difference Vegetation Index)
---------------------------------------------------------
**Formula:**

.. math::
   GRNDVI = \frac{NIR - (Green + Red)}{NIR + Green + Red}

**Description:**
GRNDVI combines green and red bands for improved sensitivity to vegetation changes.

**Typical Range:** -1 to 1

**Interpretation:**
- High GRNDVI: Healthy, dense vegetation
- Low GRNDVI: Sparse or stressed vegetation

**Image:**
.. image:: _static/GRNDVI.png
   :alt: GRNDVI
   :width: 300px

---

TNDVI (Transformed NDVI)
------------------------
**Formula:**

.. math::
   TNDVI = \sqrt{NDVI + 0.5}

**Description:**
TNDVI is a transformed version of NDVI, often used to enhance contrast in vegetation mapping.

**Typical Range:** 0 to 1.5

**Interpretation:**
- Higher TNDVI: More vigorous vegetation

**Image:**
.. image:: _static/TNDVI.png
   :alt: TNDVI
   :width: 300px

---

MGRVI (Modified Green Red Vegetation Index)
-------------------------------------------
**Formula:**

.. math::
   MGRVI = \frac{Green^2 - Red^2}{Green^2 + Red^2}

**Description:**
MGRVI enhances the contrast between green and red reflectance, useful for vegetation discrimination.

**Typical Range:** -1 to 1

**Interpretation:**
- High MGRVI: Healthy, green vegetation
- Low MGRVI: Stressed or senescent vegetation

**Image:**
.. image:: _static/MGRVI.png
   :alt: MGRVI
   :width: 300px

---

GRVI (Green Red Vegetation Index)
---------------------------------
**Formula:**

.. math::
   GRVI = \frac{NIR}{Green}

**Description:**
GRVI is used to assess vegetation vigor using NIR and green bands.

**Typical Range:** 0 to 10

**Interpretation:**
- High GRVI: Vigorous vegetation
- Low GRVI: Sparse or stressed vegetation

**Image:**
.. image:: _static/GRVI.png
   :alt: GRVI
   :width: 300px

---

NGRDI (Normalized Green Red Difference Index)
---------------------------------------------
**Formula:**

.. math::
   NGRDI = \frac{Green - Red}{Green + Red}

**Description:**
NGRDI is sensitive to vegetation cover and is used for crop monitoring.

**Typical Range:** -1 to 1

**Interpretation:**
- High NGRDI: Dense, healthy vegetation
- Low NGRDI: Sparse or stressed vegetation

**Image:**
.. image:: _static/NGRDI.png
   :alt: NGRDI
   :width: 300px

---

MSAVI (Modified Soil Adjusted Vegetation Index)
-----------------------------------------------
**Formula:**

.. math::
   MSAVI = 0.5 \times \left[2 \times NIR + 1 - \sqrt{(2 \times NIR + 1)^2 - 8 \times (NIR - Red)}\right]

**Description:**
MSAVI reduces the influence of soil brightness in areas with low vegetation cover.

**Typical Range:** 0 to 1

**Interpretation:**
- High MSAVI: Dense, healthy vegetation
- Low MSAVI: Sparse vegetation or bare soil

**Image:**
.. image:: _static/MSAVI.png
   :alt: MSAVI
   :width: 300px

---

OSAVI (Optimized Soil Adjusted Vegetation Index)
-----------------------------------------------
**Formula:**

.. math::
   OSAVI = \frac{NIR - Red}{NIR + Red + 0.16}

**Description:**
OSAVI is similar to SAVI but optimized for better performance in areas with moderate vegetation cover.

**Typical Range:** 0 to 1

**Interpretation:**
- High OSAVI: Dense, healthy vegetation
- Low OSAVI: Sparse vegetation or bare soil

**Image:**
.. image:: _static/OSAVI.png
   :alt: OSAVI
   :width: 300px

---

TSAVI (Transformed Soil Adjusted Vegetation Index)
--------------------------------------------------
**Formula:**

.. math::
   TSAVI = \frac{s (NIR - s \times Red - a)}{a \times NIR + Red - a \times s + X (1 + s^2)}

**Description:**
TSAVI further reduces soil background effects, especially in arid regions.

**Typical Range:** 0 to 1

**Interpretation:**
- High TSAVI: Dense, healthy vegetation
- Low TSAVI: Sparse vegetation or bare soil

**Image:**
.. image:: _static/TSAVI.png
   :alt: TSAVI
   :width: 300px

---

GSAVI (Green Soil Adjusted Vegetation Index)
--------------------------------------------
**Formula:**

.. math::
   GSAVI = (1 + l) \times \frac{NIR - Green}{NIR + Green + l}

**Description:**
GSAVI is a soil-adjusted index using the green band, useful for certain crops.

**Typical Range:** 0 to 1

**Interpretation:**
- High GSAVI: Dense, healthy vegetation
- Low GSAVI: Sparse vegetation or bare soil

**Image:**
.. image:: _static/GSAVI.png
   :alt: GSAVI
   :width: 300px

---

NDWI (Normalized Difference Water Index)
----------------------------------------
**Formula:**

.. math::
   NDWI = \frac{Green - NIR}{Green + NIR}

**Description:**
NDWI is used to monitor changes in water content of leaves and detect water bodies.

**Typical Range:** -1 to 1

**Interpretation:**
- High NDWI: Water bodies or high leaf water content
- Low NDWI: Dry or non-vegetated areas

**Image:**
.. image:: _static/NDWI.png
   :alt: NDWI
   :width: 300px

---

DSWI4 (Drought Stress Water Index 4)
-------------------------------------
**Formula:**

.. math::
   DSWI4 = \frac{Green}{Red}

**Description:**
DSWI4 is used for drought stress detection in plants.

**Typical Range:** 0 to 10

**Interpretation:**
- High DSWI4: Well-watered vegetation
- Low DSWI4: Drought-stressed vegetation

**Image:**
.. image:: _static/DSWI4.png
   :alt: DSWI4
   :width: 300px

---

CIRE (Chlorophyll Index Red Edge)
----------------------------------
**Formula:**

.. math::
   CIRE = \frac{NIR}{RedEdge} - 1

**Description:**
CIRE is sensitive to chlorophyll content and is useful for precision agriculture.

**Typical Range:** 0 to 10

**Interpretation:**
- High CIRE: High chlorophyll, healthy vegetation
- Low CIRE: Stressed or senescent vegetation

**Image:**
.. image:: _static/CIRE.png
   :alt: CIRE
   :width: 300px

---

LCI (Leaf Chlorophyll Index)
----------------------------
**Formula:**

.. math::
   LCI = \frac{NIR - RedEdge}{NIR + RedEdge}

**Description:**
LCI is used to estimate leaf chlorophyll content.

**Typical Range:** 0 to 5

**Interpretation:**
- High LCI: High chlorophyll content
- Low LCI: Low chlorophyll content

**Image:**
.. image:: _static/LCI.png
   :alt: LCI
   :width: 300px

---

CIgreen (Chlorophyll Index Green)
----------------------------------
**Formula:**

.. math::
   CIgreen = \frac{NIR}{Green} - 1

**Description:**
CIgreen is sensitive to chlorophyll content in the green band.

**Typical Range:** 0 to 5

**Interpretation:**
- High CIgreen: High chlorophyll content
- Low CIgreen: Low chlorophyll content

**Image:**
.. image:: _static/CIgreen.png
   :alt: CIgreen
   :width: 300px

---

MCARI (Modified Chlorophyll Absorption Ratio Index)
---------------------------------------------------
**Formula:**

.. math::
   MCARI = [(RedEdge - Red) - 0.2 \times (RedEdge - Green)] \times \frac{RedEdge}{Red}

**Description:**
MCARI is used to estimate chlorophyll content and reduce soil background effects.

**Typical Range:** 0 to 1.5

**Interpretation:**
- High MCARI: High chlorophyll content
- Low MCARI: Low chlorophyll content

**Image:**
.. image:: _static/MCARI.png
   :alt: MCARI
   :width: 300px

---

MCARI1 (Modified Chlorophyll Absorption Ratio Index 1)
------------------------------------------------------
**Formula:**

.. math::
   MCARI1 = 1.2 \times [2.5 \times (NIR - Red) - 1.3 \times (NIR - Green)]

**Description:**
MCARI1 is a variant of MCARI for improved sensitivity to chlorophyll.

**Typical Range:** 0 to 1.5

**Interpretation:**
- High MCARI1: High chlorophyll content
- Low MCARI1: Low chlorophyll content

**Image:**
.. image:: _static/MCARI1.png
   :alt: MCARI1
   :width: 300px

---

MCARI2 (Modified Chlorophyll Absorption Ratio Index 2)
------------------------------------------------------
**Formula:**

.. math::
   MCARI2 = \frac{1.5 \times [2.5 \times (NIR - Red) - 1.3 \times (NIR - Green)]}{\sqrt{(2 \times NIR + 1)^2 - (6 \times NIR - 5 \times \sqrt{Red})}}

**Description:**
MCARI2 is another variant of MCARI for improved sensitivity to chlorophyll.

**Typical Range:** 0 to 1.5

**Interpretation:**
- High MCARI2: High chlorophyll content
- Low MCARI2: Low chlorophyll content

**Image:**
.. image:: _static/MCARI2.png
   :alt: MCARI2
   :width: 300px

---

CVI (Chlorophyll Vegetation Index)
----------------------------------
**Formula:**

.. math::
   CVI = \frac{NIR \times Red}{Green^2}

**Description:**
CVI is used to estimate chlorophyll content and vegetation vigor.

**Typical Range:** 0 to 10

**Interpretation:**
- High CVI: High chlorophyll content
- Low CVI: Low chlorophyll content

**Image:**
.. image:: _static/CVI.png
   :alt: CVI
   :width: 300px

---

TCARI (Transformed Chlorophyll Absorption Ratio Index)
------------------------------------------------------
**Formula:**

.. math::
   TCARI = 3 \times [(RedEdge - Red) - 0.2 \times (RedEdge - Green) \times \frac{RedEdge}{Red}]

**Description:**
TCARI is used to estimate chlorophyll content and reduce soil background effects.

**Typical Range:** 0 to 1

**Interpretation:**
- High TCARI: High chlorophyll content
- Low TCARI: Low chlorophyll content

**Image:**
.. image:: _static/TCARI.png
   :alt: TCARI
   :width: 300px

---

TCARIOSAVI (TCARI/OSAVI)
------------------------
**Formula:**

.. math::
   TCARIOSAVI = \frac{TCARI}{OSAVI}

**Description:**
TCARIOSAVI combines TCARI and OSAVI for improved chlorophyll estimation.

**Typical Range:** 0 to 1

**Interpretation:**
- High TCARIOSAVI: High chlorophyll content
- Low TCARIOSAVI: Low chlorophyll content

**Image:**
.. image:: _static/TCARIOSAVI.png
   :alt: TCARIOSAVI
   :width: 300px

---

AVI (Advanced Vegetation Index)
-------------------------------
**Formula:**

.. math::
   AVI = \sqrt[3]{NIR \times (1 - Red) \times (NIR - Red)}

**Description:**
AVI is used to estimate vegetation cover and vigor.

**Typical Range:** 0 to 1

**Interpretation:**
- High AVI: Dense, healthy vegetation
- Low AVI: Sparse or stressed vegetation

**Image:**
.. image:: _static/AVI.png
   :alt: AVI
   :width: 300px

---

SIPI2 (Structure Insensitive Pigment Index 2)
---------------------------------------------
**Formula:**

.. math::
   SIPI2 = \frac{NIR - Green}{NIR - Red}

**Description:**
SIPI2 is used to estimate pigment content, insensitive to structure.

**Typical Range:** 0 to 1

**Interpretation:**
- High SIPI2: High pigment content
- Low SIPI2: Low pigment content

**Image:**
.. image:: _static/SIPI2.png
   :alt: SIPI2
   :width: 300px

---

ARI (Anthocyanin Reflectance Index)
-----------------------------------
**Formula:**

.. math::
   ARI = \frac{1}{Green} - \frac{1}{RedEdge}

**Description:**
ARI is used to estimate anthocyanin content in leaves.

**Typical Range:** 0 to 1

**Interpretation:**
- High ARI: High anthocyanin content
- Low ARI: Low anthocyanin content

**Image:**
.. image:: _static/ARI.png
   :alt: ARI
   :width: 300px

---

ARI2 (Anthocyanin Reflectance Index 2)
--------------------------------------
**Formula:**

.. math::
   ARI2 = NIR \times \left(\frac{1}{Green} - \frac{1}{RedEdge}\right)

**Description:**
ARI2 is a variant of ARI for improved anthocyanin estimation.

**Typical Range:** 0 to 1

**Interpretation:**
- High ARI2: High anthocyanin content
- Low ARI2: Low anthocyanin content

**Image:**
.. image:: _static/ARI2.png
   :alt: ARI2
   :width: 300px

---

DVI (Difference Vegetation Index)
---------------------------------
**Formula:**

.. math::
   DVI = NIR - Red

**Description:**
DVI is a simple index for vegetation detection.

**Typical Range:** 0 to 1

**Interpretation:**
- High DVI: Dense, healthy vegetation
- Low DVI: Sparse or stressed vegetation

**Image:**
.. image:: _static/DVI.png
   :alt: DVI
   :width: 300px

---

WDVI (Weighted Difference Vegetation Index)
-------------------------------------------
**Formula:**

.. math::
   WDVI = NIR - a \times Red

**Description:**
WDVI is used to minimize soil background effects in vegetation detection.

**Typical Range:** 0 to 1

**Interpretation:**
- High WDVI: Dense, healthy vegetation
- Low WDVI: Sparse or stressed vegetation

**Image:**
.. image:: _static/WDVI.png
   :alt: WDVI
   :width: 300px

---

SR (Simple Ratio)
-----------------
**Formula:**

.. math::
   SR = \frac{NIR}{Red}

**Description:**
SR is a basic ratio for vegetation detection.

**Typical Range:** 0 to 10

**Interpretation:**
- High SR: Dense, healthy vegetation
- Low SR: Sparse or stressed vegetation

**Image:**
.. image:: _static/SR.png
   :alt: SR
   :width: 300px

---

MSR (Modified Simple Ratio)
---------------------------
**Formula:**

.. math::
   MSR = \frac{NIR/Red - 1}{\sqrt{NIR/Red + 1}}

**Description:**
MSR is a modified ratio for improved vegetation discrimination.

**Typical Range:** 0 to 10

**Interpretation:**
- High MSR: Dense, healthy vegetation
- Low MSR: Sparse or stressed vegetation

**Image:**
.. image:: _static/MSR.png
   :alt: MSR
   :width: 300px

---

PVI (Perpendicular Vegetation Index)
------------------------------------
**Formula:**

.. math::
   PVI = \frac{NIR - a \times Red - b}{\sqrt{1 + a^2}}

**Description:**
PVI is used to minimize soil background effects in vegetation detection.

**Typical Range:** 0 to 1

**Interpretation:**
- High PVI: Dense, healthy vegetation
- Low PVI: Sparse or stressed vegetation

**Image:**
.. image:: _static/PVI.png
   :alt: PVI
   :width: 300px

---

GEMI (Global Environmental Monitoring Index)
--------------------------------------------
**Formula:**

.. math::
   GEMI = \left[\frac{2(NIR^2 - Red^2) + 1.5NIR + 0.5Red}{NIR + Red + 0.5}\right] \times \left[1 - 0.25 \left(\frac{2(NIR^2 - Red^2) + 1.5NIR + 0.5Red}{NIR + Red + 0.5}\right)\right] - \frac{Red - 0.125}{1 - Red}

**Description:**
GEMI is used for global environmental monitoring and vegetation assessment.

**Typical Range:** 0 to 1

**Interpretation:**
- High GEMI: Dense, healthy vegetation
- Low GEMI: Sparse or stressed vegetation

**Image:**
.. image:: _static/GEMI.png
   :alt: GEMI
   :width: 300px

---

ExR (Excess Red)
-----------------
**Formula:**

.. math::
   ExR = 1.3 \times Red - Green

**Description:**
ExR is used to highlight red features, useful for certain crop and soil analyses.

**Typical Range:** -1 to 1

**Interpretation:**
- High ExR: High red reflectance
- Low ExR: Low red reflectance

**Image:**
.. image:: _static/ExR.png
   :alt: ExR
   :width: 300px

---

RI (Redness Index)
-------------------
**Formula:**

.. math::
   RI = \frac{Red - Green}{Red + Green}

**Description:**
RI is used to assess redness in vegetation or soil.

**Typical Range:** 0 to 1

**Interpretation:**
- High RI: High redness
- Low RI: Low redness

**Image:**
.. image:: _static/RI.png
   :alt: RI
   :width: 300px

---

RRI1 (Redness Ratio Index 1)
----------------------------
**Formula:**

.. math::
   RRI1 = \frac{NIR}{RedEdge}

**Description:**
RRI1 is used to assess redness using NIR and red edge bands.

**Typical Range:** 0 to 1

**Interpretation:**
- High RRI1: High NIR to red edge ratio
- Low RRI1: Low NIR to red edge ratio

**Image:**
.. image:: _static/RRI1.png
   :alt: RRI1
   :width: 300px

--- 