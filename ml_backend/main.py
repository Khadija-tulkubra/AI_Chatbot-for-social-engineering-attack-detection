# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib

app = FastAPI()

# CORS
origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained model and vectorizer
model = joblib.load("se_detector_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

class Message(BaseModel):
    text: str

@app.post("/predict")
def predict(msg: Message):
    X_vect = vectorizer.transform([msg.text])
    pred = model.predict(X_vect)[0]
    return {"prediction": pred}
