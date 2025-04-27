import os
from PIL import Image

# Your specified folders
input_folder = r"D:\SE\Data\screenshots\screenshots10"
output_folder = r"D:\SE\Data\croppedscreenshots\screenshots10cropped"

# Crop area: (left, top, right, bottom)
crop_box = (1242, 567, 1242 + 64, 567 + 64)

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Process each image
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        with Image.open(input_path) as img:
            cropped = img.crop(crop_box)
            cropped.save(output_path)
            print(f'Cropped and saved: {output_path}')
