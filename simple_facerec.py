import pyttsx3
import cv2
import os
import face_recognition

class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.engine = pyttsx3.init()
        self.last_spoken_name = None

    def load_encoding_images(self, images_path):
        images_list = os.listdir(images_path)

        for img_name in images_list:
            img_path = os.path.join(images_path, img_name)
            img = cv2.imread(img_path)

            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            basename = os.path.basename(img_path)
            (filename, ext) = os.path.splitext(basename)

            face_encodings = face_recognition.face_encodings(rgb_img)
            if face_encodings:
                self.known_face_encodings.append(face_encodings[0])
                self.known_face_names.append(filename)
                print(f"[INFO] Loaded {filename}")

    def detect_known_faces(self, frame):
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        face_names = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = face_distances.argmin() if face_distances.size > 0 else None

            if best_match_index is not None and matches[best_match_index]:
                name = self.known_face_names[best_match_index]

            face_names.append(name)

            # Voice output
            if name != "Unknown" and name != self.last_spoken_name:
                self.speak(f"Hello, {name}")
                self.last_spoken_name = name

        return face_locations, face_names

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()