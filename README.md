# Automated Plant Phenotyping Analysis

![Project Status](https://img.shields.io/badge/status-active-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Vue.js](https://img.shields.io/badge/frontend-Vue.js-4FC08D)
![Airflow](https://img.shields.io/badge/workflow-Apache%20Airflow-007A88)

Automated Plant Phenotyping Analysis is a pipeline for plant image analysis, leveraging advanced workflows, image segmentation, and statistical insights to simplify phenotyping tasks.

## Table of Contents

- [Developer Guide](#developerguide)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#Prerequisites)
- [Contributing](#contributing)


---

## Developer Guide

Please refer to the [developer guide](https://automatedplantphenotypinganalysisdocs.readthedocs.io/en/latest/developer_guide.html) for detailed info about the project.

## Features

- **Workflow Automation**: Powered by Apache Airflow for seamless DAG-based task scheduling.
- **Image Processing**: Color image generation, stitching, segmentation, and feature extraction.
- **Statistical Analysis**: Insightful calculations for phenotyping metrics.
- **Frontend GUI**: Intuitive interface for monitoring and interacting with the pipeline.
- **Scalable Architecture**: Modular design for ease of maintenance and scaling.

---

## Tech Stack

- **Backend**: Python (FastAPI, SQLAlchemy)
- **Frontend**: Vue.js (CLI 4+)
- **Workflow Manager**: Apache Airflow
- **Database**: PostgreSQL


## Prerequisites

- [Node.js 22.12+](https://nodejs.org/) (for frontend)
- [Python 3.10+](https://www.python.org/) (for backend)
- Docker and Docker Compose

### Contributing

Refer to the [Developer Guide](https://automatedplantphenotypinganalysisdocs.readthedocs.io/en/latest/collaboration_guidelines.html) for detailed collaboration guidelines.
