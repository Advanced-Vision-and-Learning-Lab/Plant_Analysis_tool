Morphological Features
======================

.. toctree::
   :maxdepth: 1

This page provides detailed explanations for each morphological feature extracted by the pipeline.

Area
----
**Description:**
Total area of the plant region in pixels.

Perimeter
---------
**Description:**
Length of the boundary of the plant region.

Width & Height
--------------
**Description:**
Width and height of the bounding box around the plant region.

Hull Area
---------
**Description:**
Area of the convex hull enclosing the plant region.

Solidity
--------
**Description:**
Ratio of the area of the plant region to the area of its convex hull.

Extent
------
**Description:**
Ratio of the region area to the bounding box area.

Aspect Ratio
------------
**Description:**
Ratio of the major axis length to the minor axis length.

Eccentricity
------------
**Description:**
Eccentricity of the plant shape (0 = circle, 1 = line).

Major/Minor Axis Length
-----------------------
**Description:**
Lengths of the major and minor axes of the best-fit ellipse.

Circularity
-----------
**Formula:**

.. math::
   Circularity = \frac{4\pi \times Area}{Perimeter^2}

**Description:**
A measure of how close the shape is to a perfect circle.

Center of Mass
--------------
**Description:**
X and Y coordinates of the center of mass of the plant region.

Bounding Box Properties
-----------------------
**Description:**
X, Y, width, and height of the bounding box enclosing the plant region. 