import cv2
import numpy as np
import os

def remove_background(img, color_list, tolerance=10):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    for exact_bgr in color_list:
        exact = np.array(exact_bgr)
        lower = np.append(np.clip(exact - tolerance, 0, 255), 0)
        upper = np.append(np.clip(exact + tolerance, 0, 255), 255)

        mask = cv2.inRange(img, lower, upper)
        img[mask > 0] = (0, 0, 0, 0)  # Transparent
    return img

def process_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Add all background BGR colors here
    background_colors = [
        (75, 92, 0),    # #005C4B
        (66, 57, 50),   # #323942
        (84, 98, 19),   # #136254
        (75, 77, 37),   # #254D4B
        (0, 0, 0)       # Black background from augmentation
    ]

    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.png'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            img = cv2.imread(input_path)
            if img is None:
                print(f"Skipping unreadable file: {filename}")
                continue

            cleaned = remove_background(img, background_colors)
            cv2.imwrite(output_path, cleaned)
            print(f"Processed: {filename}")

# Set these to your actual folders
input_dir = "D:/SE/Data/screenshots/augmented_data/"     # folder with your original images
output_dir = "D:/SE/Data/screenshots/augmented_dataset/"   # where cleaned images will go
process_folder(input_dir, output_dir)
