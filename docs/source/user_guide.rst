User Guide
==========

Welcome to the Automated Plant Phenotyping Analysis application! This guide will help you understand the features and services offered by the app, as well as how to use it effectively.

Introduction
------------
Automated Plant Phenotyping Analysis is a web-based tool designed to simplify and automate the analysis of plant images. The platform provides a seamless workflow for uploading images, running advanced analyses (segmentation, feature extraction), and accessing results through a modern, user-friendly interface. The backend leverages FastAPI, Celery, and Docker for scalable, efficient processing.

Key Features
------------
- Upload plant images for automated analysis
- Deep learning-based image segmentation
- Extraction of vegetation indices, texture, and morphology features
- Downloadable results (images, JSON, CSV)
- Modern, responsive web interface
- API access for automation and integration

Analysis Outputs
----------------
The following tables summarize the types of features and indices supported by the pipeline.

Vegetation Indices Supported
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
+-------------------+-----------------------------------------------+
| Index             | Description                                   |
+===================+===============================================+
| NDVI              | Normalized Difference Vegetation Index        |
+-------------------+-----------------------------------------------+
| GNDVI             | Green Normalized Difference Vegetation Index  |
+-------------------+-----------------------------------------------+
| NDRE              | Normalized Difference Red Edge Index          |
+-------------------+-----------------------------------------------+
| GRNDVI            | Green-Red Normalized Difference Vegetation Index |
+-------------------+-----------------------------------------------+
| TNDVI             | Transformed NDVI                              |
+-------------------+-----------------------------------------------+
| MGRVI             | Modified Green Red Vegetation Index           |
+-------------------+-----------------------------------------------+
| GRVI              | Green Red Vegetation Index                    |
+-------------------+-----------------------------------------------+
| NGRDI             | Normalized Green Red Difference Index         |
+-------------------+-----------------------------------------------+
| MSAVI             | Modified Soil Adjusted Vegetation Index       |
+-------------------+-----------------------------------------------+
| OSAVI             | Optimized Soil Adjusted Vegetation Index      |
+-------------------+-----------------------------------------------+
| TSAVI             | Transformed Soil Adjusted Vegetation Index    |
+-------------------+-----------------------------------------------+
| GSAVI             | Green Soil Adjusted Vegetation Index          |
+-------------------+-----------------------------------------------+
| NDWI              | Normalized Difference Water Index             |
+-------------------+-----------------------------------------------+
| DSWI4             | Drought Stress Water Index 4                  |
+-------------------+-----------------------------------------------+
| CIRE              | Chlorophyll Index Red Edge                    |
+-------------------+-----------------------------------------------+
| LCI               | Leaf Chlorophyll Index                        |
+-------------------+-----------------------------------------------+
| CIgreen           | Chlorophyll Index Green                       |
+-------------------+-----------------------------------------------+
| MCARI             | Modified Chlorophyll Absorption Ratio Index   |
+-------------------+-----------------------------------------------+
| MCARI1            | Modified Chlorophyll Absorption Ratio Index 1 |
+-------------------+-----------------------------------------------+
| MCARI2            | Modified Chlorophyll Absorption Ratio Index 2 |
+-------------------+-----------------------------------------------+
| CVI               | Chlorophyll Vegetation Index                  |
+-------------------+-----------------------------------------------+
| TCARI             | Transformed Chlorophyll Absorption Ratio Index|
+-------------------+-----------------------------------------------+
| TCARIOSAVI        | TCARI/OSAVI                                   |
+-------------------+-----------------------------------------------+
| AVI               | Advanced Vegetation Index                     |
+-------------------+-----------------------------------------------+
| SIPI2             | Structure Insensitive Pigment Index 2         |
+-------------------+-----------------------------------------------+
| ARI               | Anthocyanin Reflectance Index                 |
+-------------------+-----------------------------------------------+
| ARI2              | Anthocyanin Reflectance Index 2               |
+-------------------+-----------------------------------------------+
| DVI               | Difference Vegetation Index                   |
+-------------------+-----------------------------------------------+
| WDVI              | Weighted Difference Vegetation Index          |
+-------------------+-----------------------------------------------+
| SR                | Simple Ratio                                  |
+-------------------+-----------------------------------------------+
| MSR               | Modified Simple Ratio                         |
+-------------------+-----------------------------------------------+
| PVI               | Perpendicular Vegetation Index                |
+-------------------+-----------------------------------------------+
| GEMI              | Global Environmental Monitoring Index         |
+-------------------+-----------------------------------------------+
| ExR               | Excess Red                                    |
+-------------------+-----------------------------------------------+
| RI                | Redness Index                                 |
+-------------------+-----------------------------------------------+
| RRI1              | Redness Ratio Index 1                         |
+-------------------+-----------------------------------------------+

Texture Features Supported
^^^^^^^^^^^^^^^^^^^^^^^^^^
+-------------------+---------------------------------------------------------------+
| Feature           | Description                                                   |
+===================+===============================================================+
| LBP               | Local Binary Pattern (texture descriptor)                      |
+-------------------+---------------------------------------------------------------+
| HOG               | Histogram of Oriented Gradients (edge/orientation descriptor)  |
+-------------------+---------------------------------------------------------------+
| Lacunarity (Lac1) | Lacunarity at base window size (texture heterogeneity)         |
+-------------------+---------------------------------------------------------------+
| Lacunarity (Lac2) | Lacunarity at multi-scale (average of several window sizes)    |
+-------------------+---------------------------------------------------------------+
| Lacunarity (Lac3) | DBC Lacunarity (deep learning-based lacunarity)               |
+-------------------+---------------------------------------------------------------+
| EHD               | Edge Histogram Descriptor (distribution of edge directions)    |
+-------------------+---------------------------------------------------------------+

For each feature above, the following statistics are computed per band:
- Mean
- Standard deviation
- Max
- Min
- Median
- 25th percentile (q25)
- 75th percentile (q75)
- Fraction of NaN values

Morphology Features Supported
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
+-----------------------+-----------------------------------------------+
| Feature               | Description                                   |
+=======================+===============================================+
| Area                  | Total area of the plant region (pixels)       |
+-----------------------+-----------------------------------------------+
| Perimeter             | Perimeter of the plant region                 |
+-----------------------+-----------------------------------------------+
| Width                 | Width of the bounding box                     |
+-----------------------+-----------------------------------------------+
| Height                | Height of the bounding box                    |
+-----------------------+-----------------------------------------------+
| Hull Area             | Area of the convex hull                       |
+-----------------------+-----------------------------------------------+
| Solidity              | Solidity of the plant region                  |
+-----------------------+-----------------------------------------------+
| Extent                | Ratio of region area to bounding box area     |
+-----------------------+-----------------------------------------------+
| Aspect Ratio          | Ratio of major to minor axis                  |
+-----------------------+-----------------------------------------------+
| Eccentricity          | Eccentricity of the plant shape               |
+-----------------------+-----------------------------------------------+
| Major Axis Length     | Length of the major axis                      |
+-----------------------+-----------------------------------------------+
| Minor Axis Length     | Length of the minor axis                      |
+-----------------------+-----------------------------------------------+
| Circularity           | 4π × (Area/Perimeter²)                        |
+-----------------------+-----------------------------------------------+
| Center of Mass X      | X coordinate of the center of mass            |
+-----------------------+-----------------------------------------------+
| Center of Mass Y      | Y coordinate of the center of mass            |
+-----------------------+-----------------------------------------------+
| Bounding Box X        | X coordinate of bounding box                  |
+-----------------------+-----------------------------------------------+
| Bounding Box Y        | Y coordinate of bounding box                  |
+-----------------------+-----------------------------------------------+
| Bounding Box Width    | Width of bounding box                         |
+-----------------------+-----------------------------------------------+
| Bounding Box Height   | Height of bounding box                        |
+-----------------------+-----------------------------------------------+

Step-by-Step Usage Guide
------------------------
1. **Access the Application**
   - Open your browser and go to: `http://localhost:8080` (or your server’s address).

2. **Upload Images**
   - Click the "Upload" button and select one or more plant images (TIFF, PNG, JPEG).
   - Images are uploaded to the server for analysis.

3. **Start Analysis**
   - After uploading, click the "Analyze" button to start the analysis pipeline.
   - The system will process your image(s) in the background using Celery workers.
   - You can monitor the progress/status in the dashboard.

4. **View Results**
   - Once analysis is complete, results will appear in the dashboard.
   - For each image, you can view:
     - Original image
     - Segmented image (plant region)
     - Overlay image (segmentation mask on original)
     - Feature tables (vegetation indices, texture, morphology)

5. **Download Results**
   - Download processed images and result files (JSON, PNG, CSV) for further analysis or record-keeping.

Example Workflow
----------------
1. Go to the application in your browser.
2. Click "Upload" and select a plant image (e.g., `plant7_frame8.tif`).
3. Click "Analyze" to start processing.
4. Wait for the analysis to complete (progress/status will be shown).
5. View the results in the dashboard and download any files you need.

Advanced Usage & API Access
---------------------------
- For automation or integration, you can interact with the backend API directly.
- API documentation is available at `http://localhost:8001/docs` (Swagger UI).
- Example API endpoints:
  - `POST /api/analyze-plant/{plant_id}`: Start analysis for a plant image
  - `GET /api/task-status/{task_id}`: Check the status of an analysis task
  - `GET /api/plant-results/{plant_id}`: Retrieve analysis results for a plant
- Use tools like curl, Postman, or Python scripts to automate analysis and result retrieval.

FAQ
---
**Q: What image formats are supported?**
A: TIFF, PNG, and JPEG.

**Q: Where are my results stored?**
A: Results are available for download in the dashboard and are also stored in AWS S3 (if configured).

**Q: What if my analysis fails or is slow?**
A: Check that all backend services (API, Celery worker, database, Redis) are running. See the developer guide for troubleshooting.

**Q: Can I analyze multiple images at once?**
A: Yes, you can upload and analyze multiple images in a batch.

**Q: How do I interpret the feature tables?**
A: Each table lists the computed values for vegetation indices, texture, and morphology features. See the table descriptions above for details.

**Q: Can I automate analysis with scripts?**
A: Yes, use the API endpoints described above for automation.

Troubleshooting & Help
----------------------
- If you encounter errors, check your internet connection and ensure all backend services are running.
- For persistent issues, consult the Developer Guide or contact your system administrator.
- For more details on the analysis pipeline and features, see the Developer Guide and API documentation.

.. toctree::
   :maxdepth: 1
   :caption: Detailed User Topics

   vegetation_indices
   morphology_features
   texture_features
