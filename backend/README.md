# Mood Predictor - Backend API

This is the backend of the [Mood Predictor App](https://github.com/lukitasxue/mood-frontend), built with **FastAPI**.  
It exposes a single `/predict` endpoint that takes daily lifestyle inputs and returns a **mood score** from 1 to 10 using a trained machine learning model.

> This repo pairs with the Vue frontend: [mood-frontend repo](https://github.com/lukitasxue/mood-frontend)

[Give it a try! (Mood predictor App link)](https://moodpredictorapp.netlify.app)
---

## Files & Purpose

| File                | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `main.py`           | Main FastAPI app with `/predict` endpoint                                  |
| `model.py`          | Core model logic (custom-built linear regression using NumPy)              |
| `model_predictor.py`| Wrapper to load model and make predictions                                 |
| `train_model.py`    | Script to train the multivariable regression model on mood data            |
| `mood_data.csv`     | Dataset used to train and test the model                                   |
| `requirements.txt`  | List of dependencies to install for running the backend                    |
| `start.sh`          | Optional shell script to start the app (Linux/macOS)                       |
| `render.yaml`       | Config file for deployment on Render (or other services)                   |

---

## How the Model Works

- Custom multivariable **linear regression model** built from scratch using **NumPy**
- Inputs:  
  - Sleep hours  
  - Stress level  
  - Nutrition quality  
  - Social time  
  - Water intake
- Output: Predicted **Mood Score** (1 to 10)

You can read more about the model in the future [model breakdown blog](#) (coming soon).

---

## Sample API Request

```json
POST /predict
{
  "sleep": 7,
  "stress": 4,
  "nutrition": 6,
  "social": 90,
  "water_liters": 1.5
}

Response
{
  "predicted_mood": 6.3
}
```

---

## Getting Started Locally

### 1. Clone the repository:
```bash
git clone https://github.com/lukitasxue/backend_moodPredPage.git
cd backend_moodPredPage
```

### 2. Set up virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Run the server:
```bash
uvicorn main:app --reload
```

### 5. Test the API:
Navigate to:
```
http://localhost:8000/docs
```
This opens the **Swagger UI** where you can test the `/predict` endpoint.

---

## Deployment
The backend is ready to deploy with any FastAPI-compatible server. For local testing, `uvicorn` works great. You can containerize it for production use (Docker support to be added later).

---

## Model Info
This model was built from scratch using **NumPy** - no scikit-learn involved. It uses multivariable linear regression with 5 lifestyle input variables and outputs a mood score (1–10).

- Trained manually using a basic loss function (MSE)
- The model achieves:
  - **MSE**: `0.612`
  - **RMSE**: `0.783`

---

## Curiosity Corner
During development, I realized I had originally trained the model using 100% of the data. Classic rookie mistake. I went back, added an 80/20 train-test split, and surprisingly, the model performed **better**!

---

## Author
Lucas Hsueh – [@lukitasxue](https://github.com/lukitasxue)