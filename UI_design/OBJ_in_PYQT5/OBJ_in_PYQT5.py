import sys
import vtk
import os
import tempfile
import resources_rc
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget
from PyQt5.QtCore import QFile, QIODevice
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # VTK widget
        self.vtk_widget = QVTKRenderWindowInteractor(self.central_widget)
        self.layout.addWidget(self.vtk_widget)
        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)

        # Interactor
        self.interactor = self.vtk_widget.GetRenderWindow().GetInteractor()

        # Extract and load OBJ with materials from resources
        self.load_obj_with_materials_from_resources()

    def extract_resource(self, resource_path, output_path):
        file = QFile(resource_path)
        if file.open(QIODevice.ReadOnly):
            with open(output_path, 'wb') as out_file:
                out_file.write(file.readAll().data())  # Ensure conversion to Python bytes
            file.close()
            return True
        return False

    def load_obj_with_materials_from_resources(self):
        temp_dir = tempfile.mkdtemp()
        obj_resource_path = ":/render/ball_on_a_plate_render.obj"
        mtl_resource_path = ":/render/ball_on_a_plate_render.mtl"
        
        obj_temp_path = os.path.join(temp_dir, "ball_on_a_plate_render.obj")
        mtl_temp_path = os.path.join(temp_dir, "ball_on_a_plate_render.mtl")

        # Extract OBJ and MTL files to the temporary directory
        if self.extract_resource(obj_resource_path, obj_temp_path) and \
           self.extract_resource(mtl_resource_path, mtl_temp_path):
            texture_path = temp_dir  # Assuming textures are alongside OBJ/MTL if any
            self.load_obj_with_materials(obj_temp_path, mtl_temp_path, texture_path)
        else:
            print("Failed to extract resources")

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
