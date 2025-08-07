// src/api.js
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

export async function analyzePlant(species, plantId, date) {
  const url = `${API_BASE}/analyze-plant/${species}/${plantId}?date=${date}`;
  const res = await axios.post(url);
  return res.data;
}

export async function getPlantResults(species, plantId, date) {
  const url = `${API_BASE}/plant-results/${species}/${plantId}?date=${date}`;
  const res = await axios.get(url);
  return res.data;
}

// Timeline API functions
export async function getPlantTimeline(species, plantId) {
  const url = `${API_BASE}/plant-timeline/${species}/${plantId}`;
  const res = await axios.get(url);
  return res.data;
}

export async function getVegetationTimeline(species, plantId, indexType) {
  const url = `${API_BASE}/plant-timeline/${species}/${plantId}/vegetation/${indexType}`;
  const res = await axios.get(url);
  return res.data;
}

export async function getTextureTimeline(species, plantId, bandName, textureType) {
  const url = `${API_BASE}/plant-timeline/${species}/${plantId}/texture/${bandName}/${textureType}`;
  const res = await axios.get(url);
  return res.data;
}

export async function getDatabaseData(species, plantId, date) {
  const url = `${API_BASE}/plant-database-data/${species}/${plantId}?date=${date}`;
  const res = await axios.get(url);
  return res.data;
}

/**
 * Upload files to the backend (raw or result).
 * @param {FileList|Array<File>} files - The files to upload.
 * @param {string} endpoint - 'raw-files' or 'result-files'
 * @returns {Promise<Object>} - The response from the backend.
 */
export async function uploadFiles(files, endpoint = "raw-files") {
  const url = `${API_BASE}/upload/${endpoint}`;
  const formData = new FormData();

  // Append each file to the form data
  for (let i = 0; i < files.length; i++) {
    formData.append("files", files[i], files[i].webkitRelativePath || files[i].name);
  }

  try {
    const response = await fetch(url, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Upload failed");
    }

    return await response.json();
  } catch (err) {
    // You can handle error display here or in your Vue component
    throw err;
  }
}

export async function getUploadStatus() {
  const url = `${API_BASE}/upload/status`;
  const response = await fetch(url);
  if (!response.ok) throw new Error("Failed to fetch upload status");
  return await response.json();
}
