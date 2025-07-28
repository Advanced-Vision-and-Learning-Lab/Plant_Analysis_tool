// src/api.js
import axios from 'axios';

const API_BASE = 'http://localhost:8001/api';

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
