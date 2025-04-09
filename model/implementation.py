import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load labels from TXT
txt_path = "C:/Users/lms/Desktop/Codespace/uni/EmojiDetector/model/labels.txt"  # TXT should have lines in format: filename, emoji, unicode
data_dir = "C:/Users/lms/Desktop/Codespace/uni/EmojiDetector/data/Emojis_data_M"
image_size = (128, 128)

def load_labels(txt_path):
    labels = []
    with open(txt_path, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) == 3:
                labels.append(parts)
    return labels

def load_images_and_labels(data_dir, labels):
    images = []
    label_list = []
    
    for filename, _, unicode_val in labels:
        img_path = os.path.join(data_dir, filename)
        if os.path.exists(img_path):
            img = load_img(img_path, target_size=image_size)
            img = img_to_array(img) / 255.0  # Normalize
            images.append(img)
            label_list.append(unicode_val)  # Use Unicode as label
    
    return np.array(images), np.array(label_list)

# Load dataset
labels = load_labels(txt_path)
X, y = load_images_and_labels(data_dir, labels)

# Encode labels (convert unicode to numerical labels)
unique_labels = list(set(y))
label_map = {label: idx for idx, label in enumerate(unique_labels)}
y = np.array([label_map[label] for label in y])

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build CNN model
model = keras.Sequential([
    layers.Conv2D(32, (3,3), activation='relu', input_shape=(128, 128, 3)),
    layers.MaxPooling2D(2,2),
    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),
    layers.Conv2D(128, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(len(unique_labels), activation='softmax')
])

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
epochs = 3
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=epochs, batch_size=32)

# Evaluate accuracy
train_loss, train_acc = model.evaluate(X_train, y_train, verbose=0)
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print(f"Train Accuracy: {train_acc:.4f}, Test Accuracy: {test_acc:.4f}")

# Save model
model.save("object_recognition_model.h5")

# Function to predict a new image
def predict_image(image_path, model, label_map):
    img = load_img(image_path, target_size=image_size)
    img = img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    
    prediction = model.predict(img)
    predicted_label = list(label_map.keys())[np.argmax(prediction)]
    return predicted_label

# Example usage
result = predict_image("test_image.jpg", model, label_map)
print("Predicted Unicode:", result)
