# frame_design.py
import cv2
from datetime import datetime

def draw_faces_on_frame(frame, face_locations, face_names, last_seen_times):
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if name != "Unknown":
            color = (0, 255, 0)  # Green for known
        else:
            color = (0, 0, 255)  # Red for unknown

        # Face rectangle
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

        # Name background
        cv2.rectangle(frame, (left, bottom), (right, bottom + 40), color, cv2.FILLED)

        # Text for known faces
        if name != "Unknown":
            label = f"{name}"
            time_label = f"Last seen: {last_seen_times.get(name, 'Now')}"
            cv2.putText(frame, label, (left + 6, bottom + 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            cv2.putText(frame, time_label, (left + 6, bottom + 33),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
        else:
            # Unknown face warning
            cv2.putText(frame, "⚠ Stranger Detected", (left + 6, bottom + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    return frame


def apply_frame_design(frame, fps=None):
    height, width, _ = frame.shape
    border_thickness = 6
    top_bar_height = 50
    bottom_bar_height = 35

    # Border
    cv2.rectangle(frame, (0, 0), (width - 1, height - 1),
                  (255, 255, 255), border_thickness)

    # Top bar
    cv2.rectangle(frame, (0, 0), (width, top_bar_height), (25, 25, 112), -1)
    cv2.putText(frame, "Real-Time Face Recognition", (10, 35),
                cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)

    # Time
    current_time = datetime.now().strftime('%H:%M:%S')
    cv2.putText(frame, current_time, (width - 120, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

    # Bottom bar
    cv2.rectangle(frame, (0, height - bottom_bar_height), (width, height),
                  (25, 25, 112), -1)
    cv2.putText(frame, "Press 'Q' to Quit", (10, height - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    cv2.putText(frame, "By Abhinav's Vision System", (width - 270, height - 10),
                cv2.FONT_HERSHEY_PLAIN, 1.2, (180, 180, 255), 1)

    # FPS
    if fps is not None:
        fps_text = f"FPS: {fps:.2f}"
        cv2.putText(frame, fps_text, (width // 2 - 40, height - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 255, 50), 2)

    return frame
