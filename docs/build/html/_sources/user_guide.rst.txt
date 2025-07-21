User Guide
==========

Welcome to the Automated Plant Phenotyping Analysis application! This guide will help you understand the features and services offered by the app, as well as how to use it effectively.

Overview
--------
The application provides a modern, web-based pipeline for automated plant phenotyping. It allows users to upload plant images, run advanced analysis (segmentation, feature extraction), and view/download results—all through a user-friendly interface.

Key Features
------------
- Upload plant images for analysis
- Automated image segmentation and feature extraction (vegetation indices, texture, morphology)
- Downloadable results (images, JSON)
- Modern, responsive web interface

Getting Started
---------------
1. **Access the Application**
   - Open your browser and go to: `http://localhost:8080` (or your server’s address)

2. **Upload Images**
   - Use the upload form to select and submit plant images for analysis.
   - Supported formats: TIFF, PNG, JPEG.

3. **Start Analysis**
   - After uploading, click the "Analyze" button to start the analysis pipeline.
   - The system will process your image in the background (using Celery workers).

4. **View Results**
   - Once analysis is complete, results will appear in the dashboard.
   - You can view original, segmented, and overlay images, as well as feature tables.

5. **Download Results**
   - Download processed images and result files (JSON, PNG) for further analysis.

Troubleshooting
---------------
- If you encounter errors, check your internet connection and ensure all backend services are running.
- For persistent issues, contact your system administrator or refer to the developer guide.
