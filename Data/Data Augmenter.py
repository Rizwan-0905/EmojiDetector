import os
import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array, array_to_img

# Paths
input_dir = r"D:\SE\Data\screenshots\OG"
input_labels_file = os.path.join(input_dir, "labels.txt")
output_dir = r"D:\SE\Data\screenshots\augmented_data/"
output_labels_file = os.path.join(output_dir, "labels.txt")

# Create output directory if not exists
os.makedirs(output_dir, exist_ok=True)

# Load original labels
df = pd.read_csv(input_labels_file, header=None, names=["filename", "emoji", "unicode"], sep=",\s*", engine='python')

# Setup augmentation generator with extra randomness
datagen = ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    brightness_range=[0.8, 1.2],
    shear_range=10,
    fill_mode='nearest'
)

# List to store new labels
new_labels = []

# How many augmented images per original?
augment_count = 20  # Increase from 5 to 20

print("Starting augmentation...")

for i, row in df.iterrows():
    filepath = os.path.join(input_dir, row["filename"])
    
    try:
        image = load_img(filepath, target_size=(64, 64))
        x = img_to_array(image)
        x = np.expand_dims(x, axis=0)

        # Save original
        original_name = f"{os.path.splitext(row['filename'])[0]}_orig.png"
        array_to_img(x[0]).save(os.path.join(output_dir, original_name))
        new_labels.append([original_name, row["emoji"], row["unicode"]])

        # Generate augmentations with a new seed for each augmentation to add randomness
        for j in range(augment_count):
            gen = datagen.flow(x, batch_size=1, seed=np.random.randint(10000))  # New random seed for each image
            augmented = next(gen)[0]
            aug_filename = f"{os.path.splitext(row['filename'])[0]}_aug{j+1}.png"
            array_to_img(augmented).save(os.path.join(output_dir, aug_filename))
            new_labels.append([aug_filename, row["emoji"], row["unicode"]])
    
    except Exception as e:
        print(f"Failed to process {row['filename']}: {e}")

# Save new labels
labels_df = pd.DataFrame(new_labels, columns=["filename", "emoji", "unicode"])
labels_df.to_csv(output_labels_file, index=False, header=False)

print(f"\n✅ Augmentation complete. Total images: {len(new_labels)}")
print(f"Labels saved to: {output_labels_file}")
