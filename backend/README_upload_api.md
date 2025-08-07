# Upload API Documentation

This document describes the upload API endpoints for the Plant Analysis Tool.

## Overview

The upload API provides endpoints for uploading raw plant image files and result files from plant analysis. It automatically extracts species information from filenames and creates/updates database entries for plants and their associated data.

## API Endpoints

### 1. Upload Raw Files

**Endpoint:** `POST /api/upload/raw-files`

**Description:** Upload raw plant image files and create database entries for plants.

**Expected File Structure:**
```
Sorghum_dataset/{date}/{plant_id}/{plant_id}_frame#.tiff
```

**Example:**
```
Sorghum_dataset/2024-12-04/plant7/plant7_frame8.tiff
Sorghum_dataset/2024-12-04/plant7/plant7_frame9.tiff
Sorghum_dataset/2024-12-04/plant8/plant8_frame10.tiff
```

**Parameters:**
- `files` (required): List of files to upload
- `species` (optional): Species name. If not provided, extracted from filename

**Request Example:**
```bash
curl -X POST "http://localhost:8000/api/upload/raw-files" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@Sorghum_dataset/2024-12-04/plant7/plant7_frame8.tiff" \
  -F "files=@Sorghum_dataset/2024-12-04/plant7/plant7_frame9.tiff" \
  -F "species=Sorghum"
```

**Response Example:**
```json
{
  "message": "Raw files upload processed successfully",
  "species": "Sorghum",
  "plants_processed": 2,
  "total_files": 2,
  "plant_ids": ["plant7", "plant8"]
}
```

### 2. Upload Result Files

**Endpoint:** `POST /api/upload/result-files`

**Description:** Upload result files from plant analysis and save data to database.

**Expected File Structure:**
```
Sorghum_results/{plant_id}/{date}/{plant_id}_frame#_result.json
```

**Example:**
```
Sorghum_results/plant7/2024-12-04/plant7_frame8_result.json
Sorghum_results/plant7/2024-12-04/plant7_frame9_result.json
```

**Parameters:**
- `files` (required): List of result files to upload
- `species` (optional): Species name. If not provided, extracted from filename

**Request Example:**
```bash
curl -X POST "http://localhost:8000/api/upload/result-files" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@Sorghum_results/plant7/2024-12-04/plant7_frame8_result.json" \
  -F "species=Sorghum"
```

**Response Example:**
```json
{
  "message": "Result files upload processed successfully",
  "species": "Sorghum",
  "plants_processed": 1,
  "total_files": 1,
  "plant_ids": ["plant7"]
}
```

### 3. Get Upload Status

**Endpoint:** `GET /api/upload/status`

**Description:** Get upload status and statistics.

**Response Example:**
```json
{
  "total_plants": 15,
  "total_species": 3,
  "species_breakdown": {
    "Sorghum": 8,
    "Corn": 4,
    "Wheat": 3
  }
}
```

### 4. Get Plants by Species

**Endpoint:** `GET /api/plants/{species}`

**Description:** Get all plants for a specific species.

**Response Example:**
```json
{
  "species": "Sorghum",
  "plants": [
    {
      "id": "plant7",
      "name": null,
      "dates_captured": ["2024-12-04", "2024-12-05"]
    },
    {
      "id": "plant8",
      "name": null,
      "dates_captured": ["2024-12-04"]
    }
  ]
}
```

## Database Operations

### Plant Table Operations

The upload API automatically manages the `plants` table:

1. **Creating New Plants:** When a new plant ID is encountered, a new entry is created with:
   - `id`: Plant identifier (e.g., "plant7")
   - `species`: Plant species (e.g., "Sorghum")
   - `dates_captured`: List of dates when the plant was captured

2. **Updating Existing Plants:** When an existing plant ID is encountered with a new date:
   - The new date is added to the `dates_captured` list
   - No duplicate dates are created

### File Processing Logic

#### Raw Files Processing:
1. Parse file path to extract date, plant_id, and filename
2. Create or update plant entry in database
3. Track processed plants and files
4. Return summary of processing results

#### Result Files Processing:
1. Parse file path to extract plant_id, date, and filename
2. Create or update plant entry in database
3. Track processed plants and files
4. Return summary of processing results

## Error Handling

The API includes comprehensive error handling:

- **Invalid File Paths:** Files with incorrect path structure are logged and skipped
- **Invalid Date Formats:** Files with invalid date formats are logged and skipped
- **Database Errors:** Integrity errors and other database issues are caught and reported
- **Missing Files:** Requests without files return appropriate error messages

## Logging

The API includes detailed logging for:
- File processing operations
- Database operations
- Error conditions
- Success confirmations

Logs are written to stdout with INFO level by default.

## Testing

Use the provided test script to verify API functionality:

```bash
cd backend
python test_upload_api.py
```

The test script includes tests for:
- Upload status endpoint
- Get plants by species endpoint
- Raw files upload endpoint
- Result files upload endpoint

## Dependencies

The upload API requires:
- FastAPI
- SQLAlchemy
- boto3 (for S3 operations)
- Python 3.7+

## Configuration

The API uses the following configuration:
- **S3 Bucket:** `plant-analysis-data`
- **S3 Region:** `us-east-2`
- **Database:** MySQL (configured in `database.py`)

## Future Enhancements

Potential future enhancements include:
1. **S3 Upload Integration:** Direct upload to S3 bucket
2. **File Validation:** Validate file formats and content
3. **Batch Processing:** Process large batches of files efficiently
4. **Progress Tracking:** Track upload progress for large files
5. **Authentication:** Add authentication and authorization
6. **File Compression:** Support for compressed file uploads 