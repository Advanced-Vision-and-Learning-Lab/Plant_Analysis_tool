Collaboration Guidelines
==================================

1. Follow Git best practices:
   - Use feature branches for development.
   - Open pull requests for code reviews.
2. Write clean, modular, and well-documented code.
3. Use the `tests` folder to write unit and integration tests.

6S Collaboration Checklist
--------------------------

- **Site**
    - Ensure the code is in the correct place architecturally. Verify that new code fits within the intended module or class structure.
    - Keep dependencies explicit and use service objects, form objects, or helpers where appropriate.
    - Ensure proper integration with tools like Docker or CI pipelines.

- **Solid**
    - Follow SOLID principles:
        - **Single Responsibility:** Each class or function should do one thing well.
        - **Open/Closed Principle:** Classes should be open for extension but closed for modification.
        - **Liskov Substitution Principle:** Subtypes should be substitutable for their base types.
        - **Interface Segregation:** Prefer small, specific interfaces over general ones.
        - **Dependency Inversion:** Rely on abstractions, not concrete implementations.

- **SOFA**
    - Ensure methods are:
        - **Short:** Each method should focus on one task.
        - **One thing:** Maintain single-level abstraction within a function.
        - **Few arguments:** Minimize the number of arguments passed to functions.
        - **Abstraction:** Keep the level of abstraction consistent within a class or module.

- **Smells**
    - Avoid code smells such as:
        - **Deeply nested conditionals:** Refactor to improve readability.
        - **Redundant code:** Use DRY principles to eliminate repetition.
        - **Ambiguous naming:** Use descriptive, meaningful names for variables and methods.
        - **High complexity:** Simplify by breaking functions into smaller components.

- **Style**
    - Follow established coding standards for indentation, spacing, and naming conventions.
    - Use linters and formatters to enforce consistent style throughout the codebase.

- **Sign-off**
    - Perform thorough code reviews before merging into the main branch.
    - Test all changes using automated and manual tests.
    - Obtain team approval with comments like "LGTM" (Looks Good To Me) or equivalent.

Usage and Supported Features
===========================

+----------------------+-------------------------------------------------------------+
| Feature              | Description                                                 |
+======================+=============================================================+
| Image Segmentation   | Supports RGB and multispectral plant image segmentation     |
+----------------------+-------------------------------------------------------------+
| Vegetation Indices   | Computes NDVI, EVI, and other indices from spectral data    |
+----------------------+-------------------------------------------------------------+
| Texture Analysis     | Extracts LBP, HOG, Lacunarity, and EHD texture features     |
+----------------------+-------------------------------------------------------------+
| Morphology Analysis  | Calculates area, perimeter, and shape descriptors           |
+----------------------+-------------------------------------------------------------+
| S3 Integration       | Loads/saves data and results directly from/to AWS S3        |
+----------------------+-------------------------------------------------------------+
| API Access           | Trigger analysis and retrieve results via REST API          |
+----------------------+-------------------------------------------------------------+

For more details, see the :doc:`api_design` and :doc:`database_design` sections.

Technical Details
=================

+---------------------+-------------------------------------------------------------+
| Component           | Technology/Library                                          |
+=====================+=============================================================+
| Segmentation Model  | briaai/RMBG-2.0 (HuggingFace Transformers)                  |
+---------------------+-------------------------------------------------------------+
| Image Processing    | OpenCV, PIL, NumPy                                          |
+---------------------+-------------------------------------------------------------+
| Feature Extraction  | Custom Python modules (features.py, morphology.py, etc.)    |
+---------------------+-------------------------------------------------------------+
| Orchestration       | Celery, FastAPI                                             |
+---------------------+-------------------------------------------------------------+
| Storage             | AWS S3                                                      |
+---------------------+-------------------------------------------------------------+