import cv2
import numpy as np
import os
import time
from datetime import datetime
from PIL import Image
import sounddevice as sd

# Define folder paths for saving alert images and video recordings
alert_folder_path = r""
alert_log_file = r"D:\phi-2-chatbot\alerts_log.txt"

# Ensure folder paths exist
os.makedirs(alert_folder_path, exist_ok=True)

# Save alert image to the specified folder with timestamp
def save_alert_image(frame, alert_type):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = os.path.join(alert_folder_path, f"{alert_type}_{timestamp}.jpg")
    cv2.imwrite(image_path, frame)
    return image_path

# Save alert message to a log file
def log_alert(message):
    with open(alert_log_file, 'a') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

# Audio detection function using sounddevice
def detect_sound(threshold=0.01, duration=0.5, fs=44100):
    """Detects sound based on threshold."""
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    energy = np.sum(np.abs(audio_data) ** 2)
    return energy > threshold

# Function to detect faces and track presence
def detect_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))
    return faces

# Function to monitor the environment and log alerts
def run_monitoring():
    cap = cv2.VideoCapture(0)
    last_capture_time = time.time()
    face_alert_count = 0
    sound_alert_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to access webcam.")
            break

        current_time = time.time()

        # Detect faces in the frame
        faces = detect_faces(frame)
        if len(faces) == 0:
            face_alert_count += 1
            alert_message = "No face detected in the current frame."
            print(alert_message)
            save_alert_image(frame, "no_face")
            log_alert(alert_message)
        else:
            face_alert_count = 0  # Reset count if face detected
            print("Face detected.")

        # Detect loud noise in the environment
        if detect_sound():
            sound_alert_count += 1
            alert_message = "Loud noise detected in the environment."
            print(alert_message)
            save_alert_image(frame, "noise_detected")
            log_alert(alert_message)
        else:
            sound_alert_count = 0  # Reset count if no noise detected

        # End monitoring if alert count exceeds 3 for any alert type
        if face_alert_count >= 3 or sound_alert_count >= 3:
            print("Monitoring ended due to excessive alerts.")
            break

        # Show the video feed (optional)
        cv2.imshow("Camera Feed", frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("Starting monitoring...")
    run_monitoring()
