import face_recognition
import cv2
import os
import numpy as np

class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

    def load_encoding_images(self, images_path):
        """
        Load all images from the given folder and encode the faces.
        Folder structure:
        images_path/
            Abhinav.jpg
            ElonMusk.jpg
        """
        print("Loading images...")

        for file_name in os.listdir(images_path):
            if file_name.endswith(('.jpg', '.png', '.jpeg')):
                image_path = os.path.join(images_path, file_name)
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)

                if len(encodings) > 0:
                    encoding = encodings[0]
                    name = os.path.splitext(file_name)[0]
                    self.known_face_encodings.append(encoding)
                    self.known_face_names.append(name)
                    print(f"Encoded {name}")
                else:
                    print(f"No faces found in {file_name}!")

    def detect_known_faces(self, frame):
        """
        Detect and recognize faces in the given frame.
        Returns: face_locations, face_names
        """
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)  # speed up
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]

            face_names.append(name)

        # Rescale face locations back to original frame size
        face_locations = [(top * 4, right * 4, bottom * 4, left * 4) for (top, right, bottom, left) in face_locations]
        return face_locations, face_names
