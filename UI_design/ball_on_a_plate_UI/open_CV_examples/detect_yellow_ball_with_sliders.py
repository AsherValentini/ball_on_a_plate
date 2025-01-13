import sys
import cv2
import imutils
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QThread

class MyThread(QThread):
    frame_signal = pyqtSignal(QImage)

    def __init__(self):
        super(MyThread, self).__init__()
        self.lower_yellow = np.array([5, 70, 70], np.uint8)
        self.upper_yellow = np.array([45, 255, 255], np.uint8)

    def run(self):
        self.cap = cv2.VideoCapture(1)  # Adjust camera index appropriately
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                processed_frame = self.detect_yellow_ball(frame)
                frame = self.cvimage_to_label(processed_frame)
                self.frame_signal.emit(frame)
            else:
                print("Failed to grab frame")

    def detect_yellow_ball(self, image):
        # Use the current slider values for HSV thresholding
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_yellow, self.upper_yellow)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > 500:
                x, y, w, h = cv2.boundingRect(largest_contour)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return image

    def cvimage_to_label(self, image):
        image = imutils.resize(image, width=640)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        return image

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.show()
    
    def init_ui(self):
        self.setFixedSize(800, 700)
        self.setWindowTitle("Camera Feedback")

        widget = QtWidgets.QWidget(self)
        layout = QtWidgets.QVBoxLayout()
        widget.setLayout(layout)

        self.label = QtWidgets.QLabel()
        layout.addWidget(self.label)

        self.open_btn = QtWidgets.QPushButton("Open The Camera", clicked=self.open_camera)
        layout.addWidget(self.open_btn)

        # Adding sliders
        self.add_slider(layout, 'Lower Hue', 180, 5, self.update_hsv_threshold)
        self.add_slider(layout, 'Upper Hue', 180, 45, self.update_hsv_threshold)
        self.add_slider(layout, 'Lower Saturation', 255, 70, self.update_hsv_threshold)
        self.add_slider(layout, 'Upper Saturation', 255, 255, self.update_hsv_threshold)
        self.add_slider(layout, 'Lower Value', 255, 70, self.update_hsv_threshold)
        self.add_slider(layout, 'Upper Value', 255, 255, self.update_hsv_threshold)

        self.setCentralWidget(widget)
        self.camera_thread = MyThread()
        self.camera_thread.frame_signal.connect(self.setImage)

    def add_slider(self, layout, label_text, max_value, initial_value, callback):
        label = QtWidgets.QLabel(f'{label_text}: {initial_value}')
        slider = QtWidgets.QSlider(Qt.Horizontal)  # Correct usage of Qt.Horizontal
        slider.setMaximum(max_value)
        slider.setValue(initial_value)
        slider.valueChanged.connect(lambda value, lbl=label, lt=label_text: (lbl.setText(f'{lt}: {value}'), callback()))
        layout.addWidget(label)
        layout.addWidget(slider)
        setattr(self, f'slider_{label_text.replace(" ", "_").lower()}', slider)


    def update_hsv_threshold(self):
        lh = self.slider_lower_hue.value()
        ls = self.slider_lower_saturation.value()
        lv = self.slider_lower_value.value()
        uh = self.slider_upper_hue.value()
        us = self.slider_upper_saturation.value()
        uv = self.slider_upper_value.value()

        
        self.camera_thread.lower_yellow = np.array([lh, ls, lv], np.uint8)
        self.camera_thread.upper_yellow = np.array([uh, us, uv], np.uint8)

    def open_camera(self):
        self.camera_thread.start()
        print("Camera thread is running:", self.camera_thread.isRunning())

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainApp()
    sys.exit(app.exec_())
