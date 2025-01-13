from PyQt5.QtCore import QObject, pyqtSignal, QTimer, pyqtSlot
import time

class VectorPIDController(QObject):
    output_signal = pyqtSignal(str)

    def __init__(self, kp, ki, kd, output_limits=(-960, 960)):
        super(VectorPIDController, self).__init__()
        self.kp = kp
        self.ki = ki
        self.kd = kd
  
        self.output_limits = output_limits
        
        self.integral_x = 0
        self.integral_y = 0
        self.last_error_x = None
        self.last_error_y = None
        self.last_time = None

        # Timer to control how often PID controller outputs are emitted
        self.emit_timer = QTimer(self)
        self.emit_timer.timeout.connect(self.emit_control_signals)
        
        self.control_x = 0
        self.control_y = 0

    @pyqtSlot(float, float)
    def update(self, measurement_x, measurement_y):
        current_time = time.time()
        if self.last_time is None:
            self.last_time = current_time
            return  # Skip the first update to stabilize dt calculation

        dt = current_time - self.last_time
        if dt <= 0:  # Guard against zero division error
            return  # Skip this update cycle or manage as needed

        error_x = measurement_x
        error_y = measurement_y
        
        self.integral_x += error_x * dt
        self.integral_y += error_y * dt
        
        derivative_x = (error_x - self.last_error_x) / dt if self.last_error_x is not None else 0
        derivative_y = (error_y - self.last_error_y) / dt if self.last_error_y is not None else 0
        
        self.integral_x = max(min(self.integral_x, self.output_limits[1]), self.output_limits[0])
        self.integral_y = max(min(self.integral_y, self.output_limits[1]), self.output_limits[0])
        
        self.control_x = (self.kp * error_x) + (self.ki * self.integral_x) + (self.kd * derivative_x)
        self.control_y = (self.kp * error_y) + (self.ki * self.integral_y) + (self.kd * derivative_y)
        
        self.last_error_x = error_x
        self.last_error_y = error_y
        self.last_time = current_time

    def emit_control_signals(self):
        # Clipping output to output limits before emission
        clipped_output_x = max(min(self.control_x, self.output_limits[1]), self.output_limits[0])
        clipped_output_y = max(min(self.control_y, self.output_limits[1]), self.output_limits[0])
        message = f"j<{-1*clipped_output_x}><{-1*clipped_output_y}>\n"
        self.output_signal.emit(message)
        #print(message)

    def start_PID_timer(self): 
        self.emit_timer.start(200)  
        print("started")

    def stop_PID_timer(self): 
        self.emit_timer.stop()  
        print("stopped")
