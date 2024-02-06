from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout 

class Layout(object): 

    def setupUI(self, MainWindow): 

        #region : main window
        MainWindow.resize(1280, 1920)                           # size the main window to the size of the tablet screen (will not be doing media queries in this UI design)
        MainWindow.setStyleSheet("background-color: #121212;")  # set the color of the UIs background deep charcoal  
        #endregion

        #region : central widget
        self.central_widget = QtWidgets.QWidget()          # create the central widget upon which to build the page on
        MainWindow.setCentralWidget(self.central_widget)   # assign the central widget as the main windows central widget so that it takes up all the space on the page
        self.main_h_layout = QHBoxLayout()                 # create the main horizontal layout upon which to add a side bar layout | main content regions to 
        self.central_widget.setLayout(self.main_h_layout)  # attach the main horizontal layout to the central widget
        #endregion

        #region : side bar
        self.frame_side_bar = QtWidgets.QFrame()                            # create side bar frame 
        self.frame_side_bar.setContentsMargins(0, 0, 0, 0)                  # effect tbd 
        self.frame_side_bar.setFixedWidth(int(MainWindow.height() * 0.07))  # limit the width of the side bar as a ratio to the mainwindow size 
        self.frame_side_bar.setStyleSheet("background-color: #222222;")     # set the color of the side bar frame as light charcoal

        self.side_bar_layout = QVBoxLayout()                # create side bar layout
        self.side_bar_layout.addStretch(1)                  # add a stretch to the frame so that it extends to the bottom of the screen 
        self.frame_side_bar.setLayout(self.side_bar_layout) # attach side bar layout to the side bar frame
        self.main_h_layout.addWidget(self.frame_side_bar)   # attach the side bar to the central widgets main horizontal layout
        self.main_h_layout.addStretch(1)                    # add a stretch to the main horizontal layout to push the side bar to the left most side of the page
        #endregion


