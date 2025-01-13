import cv2

# Open the camera
cap = cv2.VideoCapture(1)  # Adjust camera index

if cap.isOpened():
    # List of some common properties you might want to check
    properties = [
        "POS_MSEC", "POS_FRAMES", "POS_AVI_RATIO", "FRAME_WIDTH", "FRAME_HEIGHT",
        "FPS", "FOURCC", "FRAME_COUNT", "FORMAT", "MODE", "BRIGHTNESS",
        "CONTRAST", "SATURATION", "HUE", "GAIN", "EXPOSURE", "CONVERT_RGB",
        "WHITE_BALANCE_BLUE_U", "RECTIFICATION", "MONOCHROME", "SHARPNESS",
        "AUTO_EXPOSURE", "GAMMA", "TEMPERATURE", "TRIGGER", "TRIGGER_DELAY",
        "WHITE_BALANCE_RED_V", "ZOOM", "FOCUS", "GUID", "ISO_SPEED",
        "BACKLIGHT", "PAN", "TILT", "ROLL", "IRIS", "SETTINGS"
    ]

    # Check which properties are supported
    for prop in properties:
        prop_id = getattr(cv2, f'CAP_PROP_{prop}', None)
        if prop_id is not None:
            value = cap.get(prop_id)
            if value != -1:
                print(f"{prop}: {value}")
            else:
                print(f"{prop} is not supported")
else:
    print("Failed to open camera")

cap.release()  # Don't forget to release the camera
