import sys
import vtk
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout 
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from custom_3D_object_tracker import CustomTrackballObjectRotation

from joy_stick import Joystick

WINDOW_L = 1280 
WINDOW_H = 1920 

THREE_D_OBJECT_FRAME_H = 900
THREE_D_OBJECT_FRAME_L = 650

CONTROLLER_FRAME_H = 450
CONTROLLER_FRAME_L = 600

CAMERA_FRAME_H = 800
CAMERA_FRAME_L = 1240

class Layout(object): 

    def setupUI(self, MainWindow): 
        #region : main window
        MainWindow.resize(WINDOW_L, WINDOW_H)                   # size the main window to the size of the tablet screen (will not be doing media queries in this UI design)
        MainWindow.setStyleSheet("background-color: #121212;")  # set the color of the UIs background deep charcoal  
        #endregion

        #region : central widget
        self.central_widget = QtWidgets.QWidget()          # create the central widget upon which to build the page on
        MainWindow.setCentralWidget(self.central_widget)   # assign the central widget as the main windows central widget so that it takes up all the space on the page
        self.main_v_layout = QVBoxLayout()                 # create the main vertical layout 
        self.central_widget.setLayout(self.main_v_layout)  # attach the main vertical layout
        #endregion
        
        #region: top and bottom layouts
        self.top_region_h_layout = QHBoxLayout()                    # create the top region horizonral layout upon which to stack the the 3D image layout next to the controllers vertical layout 
        self.bottom_region_h_layout =QHBoxLayout()                  # create the bottom region layout upon which to stack the camera frame
        self.main_v_layout.addLayout(self.top_region_h_layout)      # stack the top region layout at the top of the main vertical layout
        self.main_v_layout.addLayout(self.bottom_region_h_layout)   # stack the bottom region layout at the bottom of the main vertical layout
        #endregion

        #region : 3D object 
        self.frame_3D_object = QtWidgets.QFrame()    # create the frame that will hold the 3D Object 
        self.style_widget(self.frame_3D_object, border_radius=1, background_color="#121212", border="1px solid #121212", padding=5, margin=2) # style the 3D image frame
        self.frame_3D_object.setFixedSize(THREE_D_OBJECT_FRAME_L, THREE_D_OBJECT_FRAME_H)  # fix the size of the 3D image frame

        self.frame_3D_layout = QVBoxLayout(self.frame_3D_object)           # create a layout to stack the 3D object on
        self.vtk_widget = QVTKRenderWindowInteractor(self.frame_3D_object) # create the 3D object
        self.frame_3D_layout.addWidget(self.vtk_widget)                    # stack the 3D object to the 3D object layout      

        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.renderer.SetBackground(0.0706, 0.0706, 0.0706)  # Set to the same color as the MainWindow background

        self.interactor = self.vtk_widget.GetRenderWindow().GetInteractor()

        interactor_style = CustomTrackballObjectRotation()
        self.vtk_widget.GetRenderWindow().GetInteractor().SetInteractorStyle(interactor_style)

        
        obj_file_location = r"C:\Users\localuser\OBJ_in_PYQT5\render\ball_on_a_plate_render.obj"
        mtl_file_location = r"C:\Users\localuser\OBJ_in_PYQT5\render\ball_on_a_plate_render.mtl"

        texture_path = r"C:\Users\localuser\OBJ_in_PYQT5\render"
        self.load_obj_with_materials(obj_file_location, mtl_file_location, texture_path)

        self.top_region_h_layout.addWidget(self.frame_3D_object) # stack the 3D image frame on the left most side of the top region horizontal layout
        #endregion

        #region : controllers 
        self.controllers_v_layout = QVBoxLayout()                       # create the controllers vertical layout upon which to stack the joystick frame and the automatic positioning frame
        self.top_region_h_layout.addLayout(self.controllers_v_layout)   # stack the controllers vertical layout on the right most side of the top region horizontal layout
        #region : automatic posititioning frame
        self.frame_automatic_positioning_frame = QtWidgets.QFrame() # create the automatic positioning frame 
        self.style_widget(self.frame_automatic_positioning_frame, border_radius=15, background_color="#222222", border="1px solid #222222", padding=5, margin=2) # style the automatic positioning frame
        self.frame_automatic_positioning_frame.setFixedSize(CONTROLLER_FRAME_L, CONTROLLER_FRAME_H) # fix the size of the automatic positioning frame
        self.controllers_v_layout.addWidget(self.frame_automatic_positioning_frame) # stack the automatic positioning frame to on the top most position of the controllers vertical layout
        #endregion
        #region : joy stick 
        self.frame_joy_stick = QtWidgets.QFrame()    # create joystick frame
        self.style_widget(self.frame_joy_stick, border_radius=15, background_color="#222222", border="1px solid #222222", padding=5, margin=2) # style the joystick frame
        self.frame_joy_stick.setFixedSize(CONTROLLER_FRAME_L, CONTROLLER_FRAME_H)  # fix the size of the joystick frame

        self.joy_stick_layout = QVBoxLayout()                 # create joystick layout
        self.joystick = Joystick(self.central_widget)         # create the joystick widget
        self.joy_stick_layout.addWidget(self.joystick)        # add the joystick widget to the joystick layout
        self.frame_joy_stick.setLayout(self.joy_stick_layout) # attach joystick layout to the joystick frame
        
        self.controllers_v_layout.addWidget(self.frame_joy_stick)   # stack the joystick frame at bottom most position of the controllers vertical layout
        #endregion 
        #endregion 

        #region : camera frame 
        self.frame_camera = QtWidgets.QFrame()
        self.style_widget(self.frame_camera, border_radius=8, background_color="#222222", border="1px solid #222222", padding=5, margin=2) # style the 3D image frame
        self.frame_camera.setFixedSize(CAMERA_FRAME_L, CAMERA_FRAME_H)  # fix the size of the 3D image frame

        self.bottom_region_h_layout.addWidget(self.frame_camera)
        #endregion 
    


    def style_widget(self, widget, border_radius=20, background_color="#222222", border="2px solid #555555", padding=10, margin=5):
        """
        Apply CSS styles to a given widget to set rounded corners and other visual properties.

        :param widget: The widget to which the styles will be applied.
        :param border_radius: The radius of the widget's corners.
        :param background_color: The background color of the widget.
        :param border: The border style.
        :param padding: Inner padding of the widget.
        :param margin: Margin outside the widget.
        """
        style_sheet = f"""
        background-color: {background_color};
        border-radius: {border_radius}px;
        border: {border};
        padding: {padding}px;
        margin: {margin}px;
        """
        widget.setStyleSheet(style_sheet)

    def load_obj_with_materials(self, obj_path, mtl_path, texture_path):
        # OBJ Importer
        importer = vtk.vtkOBJImporter()
        importer.SetFileName(obj_path)
        importer.SetFileNameMTL(mtl_path)
        importer.SetTexturePath(texture_path)
        importer.SetRenderWindow(self.vtk_widget.GetRenderWindow())
        importer.Update()

        # Initialize the interactor
        self.interactor.Initialize()
