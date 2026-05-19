from fastapi import FastAPI
from pydantic import BaseModel
from model_predictor import predict_mood
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MoodInput(BaseModel):
    sleep_hours: float
    stress_level: float
    nutrition_quality: float
    social_minutes: float
    water_liters: float

# Launch the FastAPI backend 
@app.post("/predict") # endpoint that accepts POST requests for mood related inputs
def predict(data: MoodInput): 
    mood = predict_mood(data.dict()) # calls predict mood function 
    print("Predicted Mood:", mood) 
    return {"predicted_mood_score": mood} # returns as json  

# cd C:\Users\hsueh\Desktop\MoodPredictor\mood-backend
# venv\Scripts\activate

# uvicorn main:app --reload

# cd mood-frontend
# npm run dev