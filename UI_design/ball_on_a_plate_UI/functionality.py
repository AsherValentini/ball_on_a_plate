
import os

from PyQt5 import QtWidgets, QtCore, QtGui 
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, pyqtSlot, QMutex, QTimer
from PyQt5.QtWidgets import QProgressBar, QMessageBox

from layout import Layout

class Functionality(QtWidgets.QMainWindow):
    def __init__(self): 
        super(Functionality, self).__init__()

        self.layout = Layout()
        self.layout.setupUI(self)






