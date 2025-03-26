from fastapi import FastAPI, File, UploadFile, Depends
import uvicorn
from PIL import Image
import io
import importlib

app = FastAPI()

# Function to dynamically load the chosen ML model
def load_model(model_name: str):
    model_module = importlib.import_module(f"models.{model_name}")
    return model_module.load_model()

# Specify the model name here (can be changed as needed)
MODEL_NAME = "pytorch_model"  # Example: "tensorflow_model", "sklearn_model"
model = load_model(MODEL_NAME)

def preprocess_image(image: Image.Image, model_name: str):
    preprocess_module = importlib.import_module(f"models.{model_name}")
    return preprocess_module.preprocess(image)

def predict_unicode(image: Image.Image) -> str:
    processed_image = preprocess_image(image, MODEL_NAME)
    
    with model.no_grad() if hasattr(model, 'no_grad') else nullcontext():
        output = model(processed_image)
        predicted_unicode = output.argmax(dim=1).item() if hasattr(output, 'argmax') else output
    
    unicode_char = chr(predicted_unicode)  # Convert to Unicode character
    return unicode_char

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read()))
    unicode_char = predict_unicode(image)
    return {"unicode": unicode_char}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
