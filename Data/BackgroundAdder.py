import cv2
import numpy as np
import os
import random
import pandas as pd

# Paths
input_folder = r"D:\SE\Data\screenshots\augmented_dataset"  # Folder with 40k transparent images
output_folder = r"D:\SE\Data\screenshots\augmented_data"
input_labels = os.path.join(input_folder, "labels.txt")
output_labels = os.path.join(output_folder, "labels.txt")

# Background BGR colors to use (OpenCV format)
background_colors = [
    (75, 92, 0),      # WhatsApp Green - #005C4B
    (66, 57, 50),     # Dark Gray - #323942
    (84, 98, 19),     # Teal Green - #136254
    (75, 77, 37),     # Dull Green - #254D4B
    (0, 0, 0),        # Black - #000000
    (255, 255, 255)   # White - #FFFFFF
]

# Make output directory
os.makedirs(output_folder, exist_ok=True)

# Load labels
df = pd.read_csv(input_labels, header=None, names=["filename", "emoji", "unicode"])

# List to hold updated labels
new_labels = []

print("Applying random backgrounds to dataset...")

for i, row in df.iterrows():
    filename = row["filename"]
    emoji = row["emoji"]
    unicode_ = row["unicode"]

    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, filename)

    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)  # Load with alpha

    if img is None or img.shape[2] != 4:
        print(f"Skipping invalid or non-transparent image: {filename}")
        continue

    # Random background
    bg_color = random.choice(background_colors)

    # Create solid background image (same size)
    bg = np.full(img.shape, (*bg_color, 255), dtype=np.uint8)

    # Extract alpha mask & blend
    alpha = img[:, :, 3:] / 255.0
    blended_rgb = alpha * img[:, :, :3] + (1 - alpha) * np.array(bg_color)
    blended_rgb = blended_rgb.astype(np.uint8)

    # Save RGB (no alpha channel)
    cv2.imwrite(output_path, blended_rgb)

    new_labels.append([filename, emoji, unicode_])

# Save updated labels
pd.DataFrame(new_labels).to_csv(output_labels, index=False, header=False)

print(f"\n✅ Background mixing complete. Saved to: {output_folder}")
