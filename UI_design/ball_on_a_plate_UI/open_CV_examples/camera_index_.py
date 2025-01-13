import cv2
import time

# Improved method to test camera indices
def test_camera_index(index):
    cap = cv2.VideoCapture(index)
    time.sleep(2)  # Give some time for the camera to initialize
    if not cap.isOpened():
        print(f"No camera found at index {index}")
        return False
    ret, frame = cap.read()
    cap.release()
    if ret:
        print(f"Camera found at index {index}")
        return True
    else:
        print(f"Failed to grab frame from camera at index {index}")
        return False

# Check multiple indices
for index in range(10):
    test_camera_index(index)
