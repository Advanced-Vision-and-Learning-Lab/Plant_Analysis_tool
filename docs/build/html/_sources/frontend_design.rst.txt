Frontend Design
===============

The frontend of the Plant Analysis Tool is built using **Vue.js**, a modern JavaScript framework for building dynamic, interactive single-page applications (SPAs).

Key Features
------------
- User-friendly interface for uploading plant images, starting analysis, and viewing results
- Responsive design for desktop and mobile
- Tabbed result viewer for images, vegetation indices, texture, and morphology features
- Integration with the backend API for triggering analysis and retrieving results
- Downloadable results (images, JSON, CSV)

Structure
---------
- The main app is in `frontend/src/App.vue`.
- Views and components are organized in `frontend/src/views/` and `frontend/src/components/`.
- API calls are managed in `frontend/src/api.js`.
- Routing is handled by Vue Router (`frontend/src/router/index.js`).
- State management is handled locally in components (no global store required for current features).

Development
-----------
- Use `npm run serve` for hot-reload development.
- The frontend communicates with the backend API at `http://localhost:8001` (configurable in `.env`).
- All analysis and result retrieval is done via REST API calls.

Why Vue.js?
-----------
Vue.js was selected for its balance of simplicity, flexibility, and power. It enables rapid development of interactive UIs and integrates seamlessly with the Python backend.
