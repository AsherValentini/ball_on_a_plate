
#==============================================================================================================
#=======imports================================================================================================
#==============================================================================================================
import os
import serial
import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui 
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, pyqtSlot, QMutex, QTimer
from PyQt5.QtGui import QImage, QPixmap #imports for displaying jpeg streams 
from layout import Layout
from models.worker_classes import OpenMVImageStreamThread, OpenCVImageStreamThread , MotorDriverWorker
from models.serial_connections import SerialDeviceBySerialNumber
import constants.device_IDs
from controllers.controller_motors import MotorController
from models.PID import VectorPIDController
#==============================================================================================================
#=======globals================================================================================================
#==============================================================================================================
GRID = [[0, 1, 2],[3, 4, 5],[6, 7, 8]]
KP = 44
KI = 0
KD = 0
#==============================================================================================================
#=======functionality class====================================================================================
#==============================================================================================================
class Functionality(QtWidgets.QMainWindow):
    signal_start_pid = pyqtSignal()
    sginal_stop_pid = pyqtSignal()
    def __init__(self): 
        super(Functionality, self).__init__()
        #=======================================================================================================
        #=======set up UI elements==============================================================================
        #=======================================================================================================
        #region: 
        self.ui = Layout()      # create in instance of the apps layout 
        self.ui.setupUI(self)   # show that instance 
        #endregion 
        #=======================================================================================================
        #=======initialize models=================================================
        #=======================================================================================================
        #region: 
        #self.openMV_image_stream_thread = ImageStreamThread(port="COM12")                   #create openMV serial object-create openMV thread 
        #self.openMV_image_stream_thread.image_received.connect(self.update_openMV_image)    #connect the emitted signal from openMV thread to update_openMV_image method to update the gui thread with the new image recieved over the comport 
        #self.openMV_image_stream_thread.start()                                             #start the thread which starts the run method in the worker class
        #endregion 
        self.flag_serial_connections = [False]
        self.serial_devices = [None]
        self.motor_driver_serial_device = SerialDeviceBySerialNumber(constants.device_IDs.MOTOR_DRIVER_SERIAL_NUMBERS)

        self.serial_devices[0] = self.motor_driver_serial_device.establish_connection()

        if self.serial_devices[0] is not None and self.serial_devices[0].isOpen(): 
            self.flag_serial_connections[0] = True

        if self.flag_serial_connections[0]: 
            self.motor_driver_thread = QThread()
            self.motor_driver_worker = MotorDriverWorker(self.motor_driver_serial_device)
            self.motor_driver_worker.moveToThread(self.motor_driver_thread)
            #self.motor_driver_thread.started.connect(self.motor_driver_worker.run)
            self.motor_driver_thread.start()

        self.openCV_image_stream_thread = OpenCVImageStreamThread()
        self.openCV_image_stream_thread.start()
        self.openCV_image_stream_thread.frame_signal.connect(self.update_openCV_image)
        self.ui.signal_update_yellow_range.connect(self.openCV_image_stream_thread.update_yellow_range)

        self.pid_model = VectorPIDController(KP, KI, KD)
        self.openCV_image_stream_thread.position_signal.connect(self.pid_model.update) # connect the error value from the image streamer to the pid algo from the pid model
        
        if self.flag_serial_connections[0]: 
            self.pid_model.output_signal.connect(self.motor_driver_worker.write_serial_message)
        #=======================================================================================================
        #=======initialize the starting states for each flag in the program=====================================
        #=======================================================================================================
        #region: 
        self.flag_button_0 = False # make sure that the buttons in the program start as unclicked 
        self.flag_button_1 = False # make sure that the buttons in the program start as unclicked 
        self.flag_button_2 = False # make sure that the buttons in the program start as unclicked 
        self.flag_button_3 = False # make sure that the buttons in the program start as unclicked 
        self.flag_button_4 = False # make sure that the buttons in the program start as unclicked 
        self.flag_button_5 = False # make sure that the buttons in the program start as unclicked 
        self.flag_button_6 = False # make sure that the buttons in the program start as unclicked 
        self.flag_button_7 = False # make sure that the buttons in the program start as unclicked 
        self.flag_button_8 = False # make sure that the buttons in the program start as unclicked 
        #endregion
        #=======================================================================================================
        #=======automatic positioning frame=====================================================================
        #=======================================================================================================
        #region: 
        self.ui.buttons[0].clicked.connect(lambda: self.toggle_button(self.ui.buttons[0]))
        self.ui.buttons[1].clicked.connect(lambda: self.toggle_button(self.ui.buttons[1]))
        self.ui.buttons[2].clicked.connect(lambda: self.toggle_button(self.ui.buttons[2]))
        self.ui.buttons[3].clicked.connect(lambda: self.toggle_button(self.ui.buttons[3]))
        self.ui.buttons[4].clicked.connect(lambda: self.toggle_button(self.ui.buttons[4])) # center button 
        self.ui.buttons[5].clicked.connect(lambda: self.toggle_button(self.ui.buttons[5]))
        self.ui.buttons[6].clicked.connect(lambda: self.toggle_button(self.ui.buttons[6]))
        self.ui.buttons[7].clicked.connect(lambda: self.toggle_button(self.ui.buttons[7]))
        self.ui.buttons[8].clicked.connect(lambda: self.toggle_button(self.ui.buttons[8]))
        #endregion
        #=======================================================================================================
        #=======motor controller================================================================================
        #=======================================================================================================
        #region: 
        if self.flag_serial_connections[0]:
            self.motor_controller = MotorController(self.ui, self.motor_driver_worker)
            self.ui.joystick.signal_joystick_direction.connect(self.motor_controller.handle_joy_stick_movement_event)

        #endregion

    def toggle_button(self, button):
        if(button == self.ui.buttons[0]):
            if(self.flag_button_0 == False):
                self.ui.set_button_style(button)
                self.flag_button_0 = True
                print(GRID[0][0])
            else: 
                self.ui.reset_button_style(button)
                self.flag_button_0 = False
        elif(button == self.ui.buttons[1]):
            if(self.flag_button_1 == False):
                self.ui.set_button_style(button)
                self.flag_button_1 = True
                print(GRID[0][1])
            else: 
                self.ui.reset_button_style(button)
                self.flag_button_1 = False
        elif(button == self.ui.buttons[2]):
            if(self.flag_button_2 == False):
                self.ui.set_button_style(button)
                self.flag_button_2 = True
                print(GRID[0][2])
            else: 
                self.ui.reset_button_style(button)
                self.flag_button_2 = False
        elif(button == self.ui.buttons[3]):
            if(self.flag_button_3 == False):
                self.ui.set_button_style(button)
                self.flag_button_3 = True
                print(GRID[1][0])
            else: 
                self.ui.reset_button_style(button)
                self.flag_button_3 = False
        elif(button == self.ui.buttons[4]):
            if(self.flag_button_4 == False):
                self.ui.set_button_style(button)
                self.flag_button_4 = True
                self.pid_model.start_PID_timer()
                print(GRID[1][1])
            else: 
                self.ui.reset_button_style(button)
                self.flag_button_4 = False  
                self.pid_model.stop_PID_timer()
        elif(button == self.ui.buttons[5]):
            if(self.flag_button_5 == False):
                self.ui.set_button_style(button)
                self.flag_button_5 = True
                print(GRID[1][2])
            else: 
                self.ui.reset_button_style(button)
                self.flag_button_5 = False   
        elif(button == self.ui.buttons[6]):
            if(self.flag_button_6 == False):
                self.ui.set_button_style(button)
                self.flag_button_6 = True
                print(GRID[2][0])
            else: 
                self.ui.reset_button_style(button)
                self.flag_button_6 = False   
        elif(button == self.ui.buttons[7]):
            if(self.flag_button_7 == False):
                self.ui.set_button_style(button)
                self.flag_button_7 = True
                print(GRID[2][1])
            else: 
                self.ui.reset_button_style(button)
                self.flag_button_7 = False           
        elif(button == self.ui.buttons[8]):
            if(self.flag_button_8 == False):
                self.ui.set_button_style(button)
                self.flag_button_8 = True
                print(GRID[2][2])
            else: 
                self.ui.reset_button_style(button)
                self.flag_button_8 = False       
    
    @pyqtSlot(QImage)
    def update_openCV_image(self, image):
        self.ui.openCV_image_label.setPixmap(QPixmap.fromImage(image))

    def closeEvent(self, event): 
 
        if hasattr(self, 'motor_driver_thread') and self.motor_driver_thread.isRunning():
            self.motor_driver_worker.stop()
            self.motor_driver_thread.quit()
            self.motor_driver_thread.wait()

        # Iterate over each serial device stored in device_serials
        for serial_device in self.serial_devices:
            # Check if the serial_device is an instance of serial.Serial and it's open
            if isinstance(serial_device, serial.Serial) and serial_device.is_open:
                serial_device.close()  # Use the close method directly from pyserial
            # Handling other threads similarly...
            print('application stopped successfully')
            #event.accept()  # Accept the close event to close the application

    #not in use atm (potentially needed if openMV camera is connected) 
    def update_openMV_image(self, image): 
        pixmap = QPixmap.fromImage(image)
        self.ui.openMV_image_label.setPixmap(pixmap)