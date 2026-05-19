# Mood Predictor

Mood Predictor is a full-stack app that helps people explore why their mood might feel off. The frontend lets users log daily lifestyle habits, while the backend predicts a mood score using a custom multivariable linear regression model built with NumPy.

The goal is not to diagnose anyone. It is a learning-focused project that turns simple daily inputs into a prediction, then visualizes trends so users can reflect on patterns over time.

## What It Does

- Predicts a mood score from 1 to 10
- Tracks mood history in the browser
- Shows mood trends over time
- Compares logged habits against recommended targets
- Estimates which habits have the strongest positive or negative relationship with mood
- Includes a test-log generator so the charts can be explored quickly

## Inputs

The current model uses:

- Sleep hours
- Stress level
- Nutrition quality
- Social minutes
- Water intake, transformed into a hydration-effect feature

## Model Insight

The model learns one weight per input. A positive weight raises the predicted mood score; a negative weight lowers it.

Current trained weights:

| Feature | Weight | Meaning |
| --- | ---: | --- |
| Hydration effect | +0.41 | Best near the hydration sweet spot, around 2L |
| Sleep hours | +0.38 | More sleep tends to improve the prediction |
| Nutrition quality | +0.22 | Better nutrition tends to lift mood |
| Social minutes | +0.01 | Small effect in this dataset |
| Stress level | -0.26 | Higher stress pulls mood down |

Earlier analysis also showed why diagnostics matter: when a group is underrepresented in the training data, such as very low sleep, predictions can become less reliable for that group. The charts are meant to make those patterns visible instead of hiding the model behind a single number.

## Tech Stack

- Frontend: Vue 3, Vite, Chart.js
- Backend: FastAPI, NumPy, pandas
- Model: custom multivariable linear regression

## Project Structure

- `frontend/` - Vue app
- `backend/` - FastAPI API and model code

## Run Locally

Install JavaScript dependencies:

```bash
npm install
npm --prefix frontend install
```

Install Python dependencies:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
```

Start the frontend and backend together:

```bash
npm run dev
```

Open:

- Frontend: http://127.0.0.1:5173
- Backend docs: http://127.0.0.1:8000/docs

By default, the frontend calls `http://localhost:8000`. To use a deployed backend, set `VITE_API_BASE_URL` before starting the frontend.
