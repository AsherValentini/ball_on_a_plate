
#==============================================================================================================
#=======imports================================================================================================
#==============================================================================================================
import os
from PyQt5 import QtWidgets, QtCore, QtGui 
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, pyqtSlot, QMutex, QTimer
from PyQt5.QtWidgets import QProgressBar, QMessageBox
from layout import Layout
#==============================================================================================================
#=======globals================================================================================================
#==============================================================================================================
GRID = [[0, 1, 2],[3, 4, 5],[6, 7, 8]]
#==============================================================================================================
#=======functionality class====================================================================================
#==============================================================================================================
class Functionality(QtWidgets.QMainWindow):
    def __init__(self): 
        super(Functionality, self).__init__()
        #=======================================================================================================
        #=======set up UI elements==============================================================================
        #=======================================================================================================
        #region: 
        self.layout = Layout()      # create in instance of the apps layout 
        self.layout.setupUI(self)   # show that instance 
        #endregion 
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
        self.layout.buttons[0].clicked.connect(lambda: self.toggle_button(self.layout.buttons[0]))
        self.layout.buttons[1].clicked.connect(lambda: self.toggle_button(self.layout.buttons[1]))
        self.layout.buttons[2].clicked.connect(lambda: self.toggle_button(self.layout.buttons[2]))
        self.layout.buttons[3].clicked.connect(lambda: self.toggle_button(self.layout.buttons[3]))
        self.layout.buttons[4].clicked.connect(lambda: self.toggle_button(self.layout.buttons[4]))
        self.layout.buttons[5].clicked.connect(lambda: self.toggle_button(self.layout.buttons[5]))
        self.layout.buttons[6].clicked.connect(lambda: self.toggle_button(self.layout.buttons[6]))
        self.layout.buttons[7].clicked.connect(lambda: self.toggle_button(self.layout.buttons[7]))
        self.layout.buttons[8].clicked.connect(lambda: self.toggle_button(self.layout.buttons[8]))
        #endregion

    def toggle_button(self, button):
        if(button == self.layout.buttons[0]):
            if(self.flag_button_0 == False):
                self.layout.set_button_style(button)
                self.flag_button_0 = True
                print(GRID[0][0])
            else: 
                self.layout.reset_button_style(button)
                self.flag_button_0 = False
        elif(button == self.layout.buttons[1]):
            if(self.flag_button_1 == False):
                self.layout.set_button_style(button)
                self.flag_button_1 = True
                print(GRID[0][1])
            else: 
                self.layout.reset_button_style(button)
                self.flag_button_1 = False
        elif(button == self.layout.buttons[2]):
            if(self.flag_button_2 == False):
                self.layout.set_button_style(button)
                self.flag_button_2 = True
                print(GRID[0][2])
            else: 
                self.layout.reset_button_style(button)
                self.flag_button_2 = False
        elif(button == self.layout.buttons[3]):
            if(self.flag_button_3 == False):
                self.layout.set_button_style(button)
                self.flag_button_3 = True
                print(GRID[1][0])
            else: 
                self.layout.reset_button_style(button)
                self.flag_button_3 = False
        elif(button == self.layout.buttons[4]):
            if(self.flag_button_4 == False):
                self.layout.set_button_style(button)
                self.flag_button_4 = True
                print(GRID[1][1])
            else: 
                self.layout.reset_button_style(button)
                self.flag_button_4 = False    
        elif(button == self.layout.buttons[5]):
            if(self.flag_button_5 == False):
                self.layout.set_button_style(button)
                self.flag_button_5 = True
                print(GRID[1][2])
            else: 
                self.layout.reset_button_style(button)
                self.flag_button_5 = False   
        elif(button == self.layout.buttons[6]):
            if(self.flag_button_6 == False):
                self.layout.set_button_style(button)
                self.flag_button_6 = True
                print(GRID[2][0])
            else: 
                self.layout.reset_button_style(button)
                self.flag_button_6 = False   
        elif(button == self.layout.buttons[7]):
            if(self.flag_button_7 == False):
                self.layout.set_button_style(button)
                self.flag_button_7 = True
                print(GRID[2][1])
            else: 
                self.layout.reset_button_style(button)
                self.flag_button_7 = False           
        elif(button == self.layout.buttons[8]):
            if(self.flag_button_8 == False):
                self.layout.set_button_style(button)
                self.flag_button_8 = True
                print(GRID[2][2])
            else: 
                self.layout.reset_button_style(button)
                self.flag_button_8 = False       
