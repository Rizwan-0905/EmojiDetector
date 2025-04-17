from fastapi import FastAPI, File, UploadFile
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

# Load label CSV and initialize label encoder
df = pd.read_csv(LABELS_PATH, header=None, names=["filename", "emoji", "unicode"], sep=",\s*", engine='python')
le = LabelEncoder()
df['encoded_unicode'] = le.fit_transform(df['unicode'])

# Load the trained model
model = load_model("model.h5")

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
    predicted_unicode = le.inverse_transform([predicted_class])[0]
    return predicted_unicode

# API Endpoint
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):  # This is the fix
    image = Image.open(io.BytesIO(await file.read())).convert("RGB")
    unicode_char = predict_unicode(image)
    return {"unicode": unicode_char}

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
