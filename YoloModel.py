import os
import cv2
from tqdm import tqdm
from ultralytics import YOLO
import pytesseract
from PIL import Image
import json

# Load YOLO model (pretrained)
model = YOLO("yolov8n.pt")

# Set the folder containing images
image_folder = r"H:\SE\EMOJI DETECTOR DATSET\ss\Rabiya"
output_folder = r"H:\SE\EMOJI DETECTOR DATSET\ss\Rabiya\LABELED_DATA"

os.makedirs(output_folder, exist_ok=True)

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

data_annotations = {}

for image_name in tqdm(os.listdir(image_folder), desc="Processing Images"):
    if image_name.endswith((".jpg", ".png", ".jpeg")):
        image_path = os.path.join(image_folder, image_name)
        img = cv2.imread(image_path)

        # Get file size
        file_size = os.path.getsize(image_path)

        results = model(image_path)  # Run YOLO on the image

        regions = []
        for r in results:
            for box in r.boxes.xyxy:
                x1, y1, x2, y2 = map(int, box)
                width, height = x2 - x1, y2 - y1

                region_data = {
                    "shape_attributes": {
                        "name": "rect",
                        "x": x1,
                        "y": y1,
                        "width": width,
                        "height": height
                    },
                    "region_attributes": {
                        "name": "not_defined",
                        "type": "unknown",
                        "image_quality": {
                            "good": True,
                            "frontal": True,
                            "good_illumination": True
                        },
                        "class": "emoji"
                    }
                }
                regions.append(region_data)

                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Extract text using Tesseract
        pil_img = Image.open(image_path)
        extracted_text = pytesseract.image_to_string(pil_img).strip()

        if extracted_text:
            text_region = {
                "shape_attributes": {
                    "name": "rect",
                    "x": 50, "y": 50, "width": 300, "height": 50  # Dummy coordinates
                },
                "region_attributes": {
                    "name": "not_defined",
                    "type": "unknown",
                    "image_quality": {
                        "good": True,
                        "frontal": True,
                        "good_illumination": True
                    },
                    "class": "text",
                    "content": extracted_text
                }
            }
            regions.append(text_region)

        # Store in final JSON format
        image_key = f"{image_name}{file_size}"
        data_annotations[image_key] = {
            "filename": image_name,
            "size": file_size,
            "regions": regions
        }

        output_path = os.path.join(output_folder, image_name)
        cv2.imwrite(output_path, img)

# Save JSON annotation file
with open("emoji_annotations.json", "w") as f:
    json.dump(data_annotations, f, indent=4)

print("Emoji detection and text annotation completed!")
