import sys, rpc, serial
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSignal, QThread
import io

# Assuming rpc.py is in the same directory and contains the rpc_usb_vcp_master class


class ImageStreamThread(QThread):
    image_received = pyqtSignal(QImage)

    def __init__(self, port):
        super().__init__()
        self.rpc_interface = rpc.rpc_usb_vcp_master(port)
        self.is_running = True

    def run(self):
        # Call the method on OpenMV cam to start streaming images. Adjust as needed.
        while self.is_running:
            sys.stdout.flush()
            self.rpc_interface.call("jpeg_image_stream", "sensor.RGB565,sensor.QQVGA")

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
        self.terminate()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenMV Image Stream")
        self.image_label = QLabel("Waiting for image...")
        self.image_label.setScaledContents(True)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Initialize and start the image stream thread
        self.image_stream_thread = ImageStreamThread(port="COM12")  # Adjust the port accordingly
        self.image_stream_thread.image_received.connect(self.update_image)
        self.image_stream_thread.start()

    def update_image(self, image):
        pixmap = QPixmap.fromImage(image)
        self.image_label.setPixmap(pixmap)

    def closeEvent(self, event):
        self.image_stream_thread.stop()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
