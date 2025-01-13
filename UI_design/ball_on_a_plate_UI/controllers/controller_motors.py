from PyQt5.QtCore import QObject, pyqtSlot
import math

class MotorController(QObject): 
    def __init__(self, view, model): 
        super().__init__()
        self.ui = view
        self.motor_driver_worker = model
        self.x = 0
        self.y = 0
        self.threshold = 0.1  # Define a threshold for significant changes

    @pyqtSlot(float, float)
    def handle_joy_stick_movement_event(self, angle, r): 
        # Calculate potential new x, y values based on the angle and radius
        new_x, new_y = self.calculate_xy_from_angle_radius(angle, r)

        # Check if the change in x or y is greater than the threshold
        if abs(new_x - self.x) > self.threshold or abs(new_y - self.y) > self.threshold:
            # Update x and y if the change is significant
            self.x = new_x
            self.y = new_y
            message = f"m<{self.x}><{self.y}>\n"
            print(message)
            self.motor_driver_worker.write_serial_message(message)
        else:
            pass

    def calculate_xy_from_angle_radius(self, angle, r):
        rad_angle = math.radians(angle)
        if angle >= 0 and angle < 90:
            # First quadrant
            x = r * math.cos(rad_angle)
            y = r * math.sin(rad_angle)
        elif angle >= 90 and angle < 180:
            # Second quadrant
            rad_angle -= math.radians(90)
            x = -r * math.sin(rad_angle)
            y = r * math.cos(rad_angle)
        elif angle >= 180 and angle < 270:
            # Third quadrant
            rad_angle -= math.radians(180)
            x = -r * math.cos(rad_angle)
            y = -r * math.sin(rad_angle)
        else:
            # Fourth quadrant
            rad_angle -= math.radians(270)
            x = r * math.sin(rad_angle)
            y = -r * math.cos(rad_angle)
        return x, y
