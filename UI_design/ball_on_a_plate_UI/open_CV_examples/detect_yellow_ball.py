import cv2
import imutils
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread
import sys

class MyThread(QThread):
    frame_signal = pyqtSignal(QImage)

    def run(self):
        self.cap = cv2.VideoCapture(1) #we use the second idex since we are using an external camera 
        while self.cap.isOpened():
            ret, frame = self.cap.read() 
            if ret: #check ret so that we do not emit 
                processed_frame = self.detect_yellow_ball(frame)
                frame = self.cvimage_to_label(processed_frame)
                self.frame_signal.emit(frame) #to be connected to the set image in the gui 
            else:
                print("Failed to grab frame")

    def detect_yellow_ball(self, image):
        # Convert to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) #we do this to more easily detect the ball color 
        # Define the range of yellow color in HSV
        lower_yellow = np.array([5, 70, 70], np.uint8) #using lower saturaton values (70) to adjust for reflective areas on the ball 
        upper_yellow = np.array([45, 255, 255], np.uint8)
        # Threshold the HSV image to get only yellow colors
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            # Find the largest contour based on area
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > 500:  # Check for a minimum area threshold
                x, y, w, h = cv2.boundingRect(largest_contour)
                # Draw a rectangle around the ball
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return image


    def cvimage_to_label(self, image):
        image = imutils.resize(image, width=640)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(image,
                       image.shape[1],
                       image.shape[0],
                       QImage.Format_RGB888)
        return image

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.show()
    
    def init_ui(self):
        self.setFixedSize(640,640)
        self.setWindowTitle("Camera FeedBack")

        widget = QtWidgets.QWidget(self)

        layout = QtWidgets.QVBoxLayout()
        widget.setLayout(layout)

        self.label = QtWidgets.QLabel()
        layout.addWidget(self.label)

        self.open_btn = QtWidgets.QPushButton("Open The Camera", clicked=self.open_camera)
        layout.addWidget(self.open_btn)

        self.camera_thread = MyThread()
        self.camera_thread.frame_signal.connect(self.setImage)

        self.setCentralWidget(widget)
    
    def open_camera(self):        
        self.camera_thread.start()
        print(self.camera_thread.isRunning())

    @pyqtSlot(QImage)
    def setImage(self,image):
        self.label.setPixmap(QPixmap.fromImage(image))



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_window = MainApp()
    sys.exit(app.exec())
