#===================================================================================
#============custom class for moving the 3D object around its own axis==============
#===================================================================================

import vtk

class CustomTrackballObjectRotation(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self):
        super().__init__()
        self.AddObserver("LeftButtonPressEvent", self.LeftButtonPressEvent)
        self.AddObserver("LeftButtonReleaseEvent", self.LeftButtonReleaseEvent)
        self.AddObserver("MouseMoveEvent", self.MouseMoveEvent)
        self.is_rotating = False

    def LeftButtonPressEvent(self, obj, event):
        self.is_rotating = True
        self.OnLeftButtonDown()
    
    def LeftButtonReleaseEvent(self, obj, event):
        self.is_rotating = False
        self.OnLeftButtonUp()
    
    def MouseMoveEvent(self, obj, event):
        if self.is_rotating:
            # Calculate the rotation
            self.Rotate()
        self.OnMouseMove()

    def Rotate(self):
        rwi = self.GetInteractor()

        dx = rwi.GetEventPosition()[0] - rwi.GetLastEventPosition()[0]
        dy = rwi.GetEventPosition()[1] - rwi.GetLastEventPosition()[1]

        size = rwi.GetSize()
        
        delta_elevation = -20.0 / size[1]
        delta_azimuth = -20.0 / size[0]

        rxf = dx * delta_azimuth * self.GetMotionFactor()
        ryf = dy * delta_elevation * self.GetMotionFactor()

        camera = self.GetCurrentRenderer().GetActiveCamera()
        camera.Azimuth(rxf)
        camera.Elevation(ryf)
        camera.OrthogonalizeViewUp()

        if self.GetAutoAdjustCameraClippingRange():
            self.GetCurrentRenderer().ResetCameraClippingRange()

        rwi.Render()
