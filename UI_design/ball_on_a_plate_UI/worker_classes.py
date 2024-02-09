import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QByteArray, QTimer, Qt
from rpc import rpc_usb_vcp_master

class ImageTransferApp(QMainWindow):
    def __init__(self, port='COM12'):
        super().__init__()
        # Initialize RPC over USB VCP
        self.rpc_interface = rpc_usb_vcp_master(port=port)
        self.initUI()
        # Start the image streaming process
        QTimer.singleShot(1000, self.startImageStream)  # Start after a short delay

    def initUI(self):
        self.setWindowTitle("OpenMV Camera Stream")
        self.imageLabel = QLabel("Waiting for image...")
        self.imageLabel.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(self.imageLabel)
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
        self.resize(640, 480)
        self.show()

    def startImageStream(self):
        # RPC call to start JPEG image streaming
        self.rpc_interface.call("jpeg_image_stream", "sensor.RGB565,sensor.QQVGA")
        # Setup timer to periodically check and update the image
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateImage)
        self.timer.start(100)  # Check for new images every 100 ms

    def updateImage(self):
        # Check for incoming JPEG data
        if self.rpc_interface.serial.in_waiting > 0:
            data = self.rpc_interface.serial.read_all()
            if data:
                pixmap = QPixmap()
                pixmap.loadFromData(QByteArray(data), "JPEG")
                self.imageLabel.setPixmap(pixmap.scaled(self.imageLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageTransferApp()
    sys.exit(app.exec_())
