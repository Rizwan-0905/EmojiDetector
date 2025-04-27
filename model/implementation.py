
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import Sequence, to_categorical
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.callbacks import Callback

# Step 1: Load and preprocess labels
df = pd.read_csv(r"drive/MyDrive/screenshots10cropped/labels.txt", header=None, names=["filename", "emoji", "unicode"], sep=",\s*", engine='python')

# Only one emoji per image, no need to group
le = LabelEncoder()
df['encoded_unicode'] = le.fit_transform(df['unicode'])  # Encoded labels as integers
num_classes = len(le.classes_)  # Should be 1906

# Step 2: Dataset generator
class EmojiDataset(Sequence):
    def __init__(self, df, img_dir, batch_size=32, img_size=(64, 64), shuffle=True):
        self.df = df
        self.img_dir = img_dir
        self.batch_size = batch_size
        self.img_size = img_size
        self.shuffle = shuffle
        self.indexes = np.arange(len(df))
        self.on_epoch_end()

    def __len__(self):
        return int(np.ceil(len(self.df) / self.batch_size))

    def __getitem__(self, index):
        batch_indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]
        batch_data = self.df.iloc[batch_indexes]

        images = []
        labels = []

        for _, row in batch_data.iterrows():
            img_path = os.path.join(self.img_dir, row['filename'])
            image = load_img(img_path, target_size=self.img_size)
            image = img_to_array(image) / 255.0
            images.append(image)
            labels.append(row['encoded_unicode'])

        # Convert to one-hot encoded labels
        return np.array(images), to_categorical(np.array(labels), num_classes=num_classes)

    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(self.indexes)

# Step 3: Define CNN model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    MaxPooling2D(pool_size=(2, 2)),

    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),

    Flatten(),

    Dense(128, activation='relu'),
    Dense(num_classes, activation='softmax')  # Softmax for multi-class classification
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
# Step 4: Train generator
train_generator = EmojiDataset(df, img_dir='/content/drive/MyDrive/screenshots10cropped/', batch_size=1, img_size=(64, 64))

# Step 5: Accuracy tester
def test_model_accuracy(model, df, img_dir):
    correct_predictions = 0
    total_predictions = len(df)

    for index, row in df.iterrows():
        img_path = os.path.join(img_dir, row['filename'])
        img = load_img(img_path, target_size=(64, 64))
        img = img_to_array(img) / 255.0
        img = np.expand_dims(img, axis=0)

        predicted_class = np.argmax(model.predict(img, verbose=0), axis=-1)[0]
        actual_class = row['encoded_unicode']

        if predicted_class == actual_class:
            correct_predictions += 1

    accuracy = correct_predictions / total_predictions * 100
    print(f"Model Accuracy: {accuracy:.2f}%")

# Optional: Predict the emoji from class index
def class_to_unicode(pred_class_idx):
    return le.inverse_transform([pred_class_idx])[0]

# Step 6: Accuracy callback
class AccuracyTestingCallback(Callback):
    def __init__(self, df, img_dir, interval=30):
        super().__init__()
        self.df = df
        self.img_dir = img_dir
        self.interval = interval

    def on_epoch_end(self, epoch, logs=None):
        if (epoch + 1) % self.interval == 0:
            print(f"\nTesting accuracy after epoch {epoch + 1}...")
            test_model_accuracy(self.model, self.df, self.img_dir)

# Step 7: Train the model
accuracy_callback = AccuracyTestingCallback(df, '/content/drive/MyDrive/screenshots10cropped/')
model.fit(train_generator, epochs=30, callbacks=[accuracy_callback])

# Step 8: Test on a single image
test_img_path = "/content/drive/MyDrive/screenshot_1.png"

# Preprocess the image
img = load_img(test_img_path, target_size=(64, 64))
img_array = img_to_array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Predict
prediction = model.predict(img_array)
predicted_class = np.argmax(prediction, axis=-1)[0]
predicted_unicode = class_to_unicode(predicted_class)

print(f"\nPrediction for {os.path.basename(test_img_path)}:")
print(f"Predicted Class Index: {predicted_class}")
print(f"Predicted Unicode: {predicted_unicode}")

model.save("my_model.h5")  # HDF5 format
from google.colab import files
files.download("my_model.h5")