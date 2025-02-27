import sys, rpc, serial
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSignal, QThread, QObject, pyqtSlot, QMutex
import io

import sys
import cv2
import imutils
import numpy as np


class OpenMVImageStreamThread(QThread):
    image_received = pyqtSignal(QImage)

    def __init__(self, port):
        super().__init__()
        self.rpc_interface = rpc.rpc_usb_vcp_master(port)
        self.is_running = True

    def run(self):
        # Call the method on OpenMV cam to start streaming images. Adjust as needed.
        while self.is_running:
            sys.stdout.flush()
            self.rpc_interface.call("jpeg_image_stream", "sensor.RGB565,sensor.QVGA")

            def callback(data):
                if not self.is_running:
                    return
                # Convert bytes to QImage and emit signal
                try:
                    image = QImage.fromData(data)
                    self.image_received.emit(image)
                except Exception as e:
                    print(f"Failed to convert image data: {e}")

            # Start listening for images
            self.rpc_interface.stream_reader(callback, queue_depth=8)

    def stop(self):
        self.is_running = False
        self.rpc_interface.close()  # Ensure the serial connection is properly closed
        self.terminate()

class MotorDriverWorker(QObject):
    def __init__(self, esp32_RTOS_serial):
        super(MotorDriverWorker, self).__init__()
        self.esp32_RTOS_serial = esp32_RTOS_serial
        self._lock = QMutex()
        self._is_running = False
        self.interval = 250

    @pyqtSlot()
    def run(self):
        self._is_running = True
        while self._is_running:
            QThread.msleep(self.interval)
            self._lock.lock()
            line = self.read_serial_line()
            self._lock.unlock()
            if line:
                print(line)

    def read_serial_line(self):
        try:
            # Check if there is any data waiting
            if self.esp32_RTOS_serial.serial_device.in_waiting:
                # Read the line from the serial device
                line = self.esp32_RTOS_serial.serial_device.readline().decode('utf-8').strip()
                return line
        except Exception as e:
            print(f"Error in read_serial_line for peristaltic driver board: {e}")


    @pyqtSlot(str)
    def write_serial_message(self, message):
        self._lock.lock()
        try:
            if self.esp32_RTOS_serial.serial_device and self.esp32_RTOS_serial.serial_device.is_open:
                # Flush the output buffer to ensure only the latest command is sent
                self.esp32_RTOS_serial.serial_device.reset_output_buffer()
                self.esp32_RTOS_serial.serial_device.write(message.encode())
                print(f"Message '{message}' sent to the motor driver.")
        except Exception as e:
            print(f"Failed to send message Error: {e}")
        finally:
            self._lock.unlock()

    @pyqtSlot()
    def stop(self):
        self._lock.lock()
        self._is_running = False
        self._lock.unlock()

class OpenCVImageStreamThread(QThread):
    frame_signal = pyqtSignal(QImage)
    position_signal = pyqtSignal(float, float)  # Signal to emit ball's position relative to center
    interval = 100

    def __init__(self):
        super(OpenCVImageStreamThread, self).__init__()
        self.lower_yellow = np.array([5, 70, 70], np.uint8)
        self.upper_yellow = np.array([45, 255, 255], np.uint8)

    def run(self):
        self.cap = cv2.VideoCapture(0)  # Adjust camera index appropriately
        while self.cap.isOpened():
            #QThread.msleep(self.interval)
            ret, frame = self.cap.read()
            if ret:
                processed_frame, error_x, error_y = self.detect_yellow_ball(frame)
                frame = self.cvimage_to_label(processed_frame)
                self.frame_signal.emit(frame)
                
                # Emit the ball's position if detected, otherwise emit zero position
                self.position_signal.emit(error_x if error_x is not None else 0, error_y if error_y is not None else 0)
            else:
                print("Failed to grab frame")

    def detect_yellow_ball(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_yellow, self.upper_yellow)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        frame_center_x = image.shape[1] // 2
        frame_center_y = image.shape[0] // 2

        error_x = None
        error_y = None

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > 500:
                x, y, w, h = cv2.boundingRect(largest_contour)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                ball_center_x = x + w // 2
                ball_center_y = y + h // 2
                
                error_x = ball_center_x - frame_center_x
                error_y = ball_center_y - frame_center_y
                #print(f"{error_x}-{error_y}")

        else:
            # Set errors to zero if no contours are found
            error_x, error_y = 0, 0

        return image, error_x, error_y

    def cvimage_to_label(self, image):
        image = imutils.resize(image, width=640)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        return image

    def update_yellow_range(self, lower_yellow, upper_yellow):
        self.lower_yellow = np.array(lower_yellow, np.uint8)
        self.upper_yellow = np.array(upper_yellow, np.uint8)
