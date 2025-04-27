from fastapi import FastAPI, File, UploadFile, HTTPException
import uvicorn
from PIL import Image
import numpy as np
import pandas as pd
import io
import os
from pathlib import Path
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from fastapi.middleware.cors import CORSMiddleware
import pickle

# Initialize the FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Can restrict for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set base directory and label path
BASE_DIR = Path(__file__).resolve().parent
LABELS_PATH = (BASE_DIR / ".." / "data" / "emojis_unicode.txt").resolve()

# Load the trained model
model = load_model(os.path.join(BASE_DIR, "my_model.h5"))

# Load label encoder from file
with open(os.path.join(BASE_DIR, '..', 'Data', 'label_encoder.pkl'), 'rb') as f:
    le = pickle.load(f)

# Preprocess image
def preprocess_image(image: Image.Image):
    image = image.resize((64, 64))
    img_array = img_to_array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# Predict unicode
def predict_unicode(image: Image.Image) -> str:
    processed_image = preprocess_image(image)
    prediction = model.predict(processed_image)
    predicted_class = np.argmax(prediction, axis=-1)[0]
    predicted_unicode = le[predicted_class] # Using LabelEncoder here
    return predicted_unicode

# API Endpoint
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        image = Image.open(io.BytesIO(await file.read())).convert("RGB")
        unicode_char = predict_unicode(image)
        return {"unicode": unicode_char}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")

# Basic health check endpoint (good for monitoring)
@app.get("/health/")
def health():
    return {"status": "Model is running"}

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
