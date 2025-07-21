Morphological Features
======================

.. toctree::
   :maxdepth: 1

This page provides detailed explanations for each morphological feature extracted by the pipeline, including description, formula (if applicable), interpretation, and example images.

Area
----
**Description:**
Total area of the plant region in pixels.

**Interpretation:**
- Larger area: Bigger plant or leaf
- Smaller area: Smaller plant or leaf

**Image:**
.. image:: _static/area_example.png
   :alt: Area Example
   :width: 300px

---

Perimeter
---------
**Description:**
Length of the boundary of the plant region.

**Interpretation:**
- Larger perimeter: More complex or larger shape
- Smaller perimeter: Simpler or smaller shape

**Image:**
.. image:: _static/perimeter_example.png
   :alt: Perimeter Example
   :width: 300px

---

Width & Height
--------------
**Description:**
Width and height of the bounding box around the plant region.

**Interpretation:**
- Indicates the spread of the plant in horizontal and vertical directions

**Image:**
.. image:: _static/width_height_example.png
   :alt: Width and Height Example
   :width: 300px

---

Hull Area
---------
**Description:**
Area of the convex hull enclosing the plant region.

**Interpretation:**
- Used to assess compactness and shape regularity

**Image:**
.. image:: _static/hull_area_example.png
   :alt: Hull Area Example
   :width: 300px

---

Solidity
--------
**Formula:**

.. math::
   Solidity = \frac{Area}{Hull\ Area}

**Description:**
Ratio of the area of the plant region to the area of its convex hull.

**Interpretation:**
- Solidity close to 1: Compact, solid shape
- Lower solidity: More holes or irregularities

**Image:**
.. image:: _static/solidity_example.png
   :alt: Solidity Example
   :width: 300px

---

Extent
------
**Formula:**

.. math::
   Extent = \frac{Area}{Bounding\ Box\ Area}

**Description:**
Ratio of the region area to the bounding box area.

**Interpretation:**
- High extent: Region fills most of the bounding box
- Low extent: Region is small relative to bounding box

**Image:**
.. image:: _static/extent_example.png
   :alt: Extent Example
   :width: 300px

---

Aspect Ratio
------------
**Formula:**

.. math::
   Aspect\ Ratio = \frac{Major\ Axis\ Length}{Minor\ Axis\ Length}

**Description:**
Ratio of the major axis length to the minor axis length.

**Interpretation:**
- High aspect ratio: Elongated shape
- Low aspect ratio: More circular shape

**Image:**
.. image:: _static/aspect_ratio_example.png
   :alt: Aspect Ratio Example
   :width: 300px

---

Eccentricity
------------
**Description:**
Eccentricity of the plant shape (0 = circle, 1 = line).

**Interpretation:**
- High eccentricity: Elongated or irregular shape
- Low eccentricity: More circular shape

**Image:**
.. image:: _static/eccentricity_example.png
   :alt: Eccentricity Example
   :width: 300px

---

Major/Minor Axis Length
-----------------------
**Description:**
Lengths of the major and minor axes of the best-fit ellipse.

**Interpretation:**
- Major axis: Longest dimension
- Minor axis: Shortest dimension

**Image:**
.. image:: _static/axis_length_example.png
   :alt: Axis Length Example
   :width: 300px

---

Circularity
-----------
**Formula:**

.. math::
   Circularity = \frac{4\pi \times Area}{Perimeter^2}

**Description:**
A measure of how close the shape is to a perfect circle.

**Interpretation:**
- Circularity close to 1: Nearly circular
- Lower circularity: More elongated or irregular

**Image:**
.. image:: _static/circularity_example.png
   :alt: Circularity Example
   :width: 300px

---

Center of Mass
--------------
**Description:**
X and Y coordinates of the center of mass of the plant region.

**Interpretation:**
- Indicates the geometric center of the region

**Image:**
.. image:: _static/center_of_mass_example.png
   :alt: Center of Mass Example
   :width: 300px

---

Bounding Box Properties
-----------------------
**Description:**
X, Y, width, and height of the bounding box enclosing the plant region.

**Interpretation:**
- Useful for locating and cropping the region of interest

**Image:**
.. image:: _static/bounding_box_example.png
   :alt: Bounding Box Example
   :width: 300px

--- 