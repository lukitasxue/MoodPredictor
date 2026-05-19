# Mood Predictor

Unified repository for the Mood Predictor frontend and backend.

## Project Structure

- `frontend/` - Vue 3 + Vite app
- `backend/` - FastAPI prediction API and mood model

## Run Locally

Install the frontend and root development dependencies:

```bash
npm install
npm --prefix frontend install
```

Install the backend dependencies:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
```

Start both apps from the repository root:

```bash
npm run dev
```

Then open:

- Frontend: http://127.0.0.1:5173
- Backend docs: http://127.0.0.1:8000/docs

By default, the frontend calls `http://localhost:8000`. To use a deployed backend, set `VITE_API_BASE_URL` before starting the frontend.
