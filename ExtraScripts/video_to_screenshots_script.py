import cv2
import os

# Ask user for the video file path
video_path = "C:/users/lms/desktop/codespace/uni/se_project/vid.mp4"

# Ask user for the output directory
output_dir = "C:/users/lms/desktop/codespace/uni/se_project/script_ss"
os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist

# Ask for the starting label number
start_number = 2732

# Open video file
cap = cv2.VideoCapture(video_path)

# Check if the video was successfully opened
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Get frame rate of video
fps = cap.get(cv2.CAP_PROP_FPS)
frame_interval = int(fps * 4)  # Capture every 4 seconds

frame_count = 0  # Track total frames
saved_count = start_number  # Start labeling from the given number

while True:
    ret, frame = cap.read()
    
    if not ret:
        break  # Break when video ends

    if frame_count % frame_interval == 0:
        # Save frame as PNG
        filename = os.path.join(output_dir, f"frame_{saved_count}.png")
        cv2.imwrite(filename, frame)
        print(f"Saved: {filename}")
        saved_count += 1  # Increment label number

    frame_count += 1

cap.release()
cv2.destroyAllWindows()

print("Frame extraction complete!")
