import cv2
import time

from datetime import datetime


def draw_faces_on_frame(frame, face_locations, face_names):
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Use green for known, red for unknown
        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)

        # Glow/shadow effect
        cv2.rectangle(frame, (left - 2, top - 2), (right + 2, bottom + 2), (0, 0, 0), 6)

        # Main face rectangle
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

        # Transparent label background
        label_height = 20
        overlay = frame.copy()
        cv2.rectangle(overlay, (left, bottom), (right, bottom + label_height), color, -1)
        cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)

        # Label text
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, name, (left + 6, bottom + 15), font, 0.5, (255, 255, 255), 1)

    return frame



def apply_frame_design(frame, fps=None):
    height, width, _ = frame.shape
    border_thickness = 6
    top_bar_height = 50
    bottom_bar_height = 35

    # === 1. Border ===
    cv2.rectangle(frame, (0, 0), (width - 1, height - 1), (255, 255, 255), border_thickness)

    # === 2. Top Bar ===
    cv2.rectangle(frame, (0, 0), (width, top_bar_height), (25, 25, 112), -1)  # Midnight blue
    cv2.putText(frame, "Real-Time Face Recognition", (10, 35),
                cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)

    # Timestamp (top-right corner)
    current_time = datetime.now().strftime('%H:%M:%S')
    cv2.putText(frame, current_time, (width - 120, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

    # Live status indicator (moved below time)
    cv2.circle(frame, (width - 30, 55), 8, (0, 0, 255), -1)
    cv2.putText(frame, "Live", (width - 100, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

    # === 3. Bottom Bar ===
    cv2.rectangle(frame, (0, height - bottom_bar_height), (width, height), (25, 25, 112), -1)
    cv2.putText(frame, "Press 'Q' to Quit", (10, height - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    cv2.putText(frame, "By Abhinav's Vision System", (width - 270, height - 10),
                cv2.FONT_HERSHEY_PLAIN, 1.2, (180, 180, 255), 1)

    # === 4. FPS Display (if available) ===
    if fps is not None:
        fps_text = f"FPS: {fps:.2f}"
        cv2.putText(frame, fps_text, (width // 2 - 40, height - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 255, 50), 2)

    return frame