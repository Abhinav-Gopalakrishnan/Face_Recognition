import cv2

def draw_faces_on_frame(frame, face_locations, face_names):
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)

        # Draw the rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

        # Label background
        cv2.rectangle(frame, (left, bottom - 20), (right, bottom), color, cv2.FILLED)

        # Put name text (black color now)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (0, 0, 0), 1)

    return frame


def apply_frame_design(frame):
    height, width, _ = frame.shape

    # Draw a white border around the frame
    border_thickness = 8
    cv2.rectangle(frame, (0, 0), (width, height), (255, 255, 255), border_thickness)

    # Add a top bar with title
    cv2.rectangle(frame, (0, 0), (width, 40), (30, 30, 30), -1)
    cv2.putText(frame, "Real-Time Face Recognition", (10, 28),
                cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)

    return frame
