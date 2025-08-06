import cv2
from simple_facerec import SimpleFacerec
import pyttsx3
from frame_design import draw_faces_on_frame, apply_frame_design 

# Initialize face recognition
sfr = SimpleFacerec()
sfr.load_encoding_images("C:/Users/abhi6/OneDrive/Documents/Face_Recog/images/")

# Initialize speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Optional female voice

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

previous_names = set()

while True:
    ret, frame = cap.read()

    if not ret or frame is None:
        print("Failed to grab frame")
        break

    face_locations, face_names = sfr.detect_known_faces(frame)

    current_names = set(face_names)

    # Speak only for new faces not seen in last frame
    new_faces = current_names - previous_names
    for name in new_faces:
        if name != "Unknown":
            engine.say(f"Hello {name}")
            engine.runAndWait()

    previous_names = current_names

    # Apply UI design
    frame = apply_frame_design(frame)

    # Draw face bounding boxes and names
    frame = draw_faces_on_frame(frame, face_locations, face_names)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == ord('q') or key == ord('Q'):
        break

cap.release()
cv2.destroyAllWindows()
