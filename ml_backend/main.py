from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI()

# Load already trained model and vectorizer
model = joblib.load("se_detector_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

class Message(BaseModel):
    text: str

@app.post("/predict")
def predict(msg: Message):
    X_vect = vectorizer.transform([msg.text])
    pred = model.predict(X_vect)[0]
    return {"prediction": pred}
