# ui_utils.py

import cv2

def draw_fancy_border(frame, color=(0, 255, 255), thickness=4, margin=10):
    """
    Draws a simple fancy border around the camera frame.
    
    Parameters:
        frame (numpy.ndarray): The frame to draw on.
        color (tuple): BGR color of the border.
        thickness (int): Thickness of the border lines.
        margin (int): Margin from the edges.
    
    Returns:
        frame (numpy.ndarray): The frame with border.
    """
    height, width, _ = frame.shape

    # Outer border
    cv2.rectangle(frame, (margin, margin), (width - margin, height - margin), color, thickness)

    # You can add corner accents or inner layers if you like

    return frame
