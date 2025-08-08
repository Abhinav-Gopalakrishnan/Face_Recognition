# main.py
import cv2
import pyttsx3
import time
from datetime import datetime
from simple_facerec import SimpleFacerec
from frame_design import draw_faces_on_frame, apply_frame_design

# Initialize face recognition
sfr = SimpleFacerec()
sfr.load_encoding_images("C:/Users/abhi6/OneDrive/Documents/Face_Recog/images/")

# Initialize speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

previous_names = set()
last_seen = {}

prev_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Detect faces
    face_locations, face_names = sfr.detect_known_faces(frame)

    # Update "last seen" timestamps
    for name in face_names:
        last_seen[name] = datetime.now().strftime('%H:%M:%S')

    # Speak only for new faces
    current_names = set(face_names)
    new_faces = current_names - previous_names
    for name in new_faces:
        if name != "Unknown":
            engine.say(f"Hello {name}")
        else:
            engine.say("Warning. Stranger detected.")
        engine.runAndWait()

    previous_names = current_names

    # Calculate FPS
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    # Apply design
    frame = apply_frame_design(frame, fps)

    # Draw faces with last seen
    frame = draw_faces_on_frame(frame, face_locations, face_names, last_seen)

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF in [ord('q'), ord('Q')]:
        break

cap.release()
cv2.destroyAllWindows()
