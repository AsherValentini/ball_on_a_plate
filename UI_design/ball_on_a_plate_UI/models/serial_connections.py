import serial
import serial.tools.list_ports

class SerialDeviceBySerialNumber():
    def __init__(self, serial_numbers):
        self.serial_numbers = serial_numbers
   
    def find_serial_port(self):
        """
        Find a serial port by checking each connected device's serial number against a list of known serial numbers.
        """
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.serial_number in self.serial_numbers:
                print(f"Found device at {port.device} with serial number {port.serial_number}")
                return port.device, port.serial_number  # Return both device and serial number
        print("Device with specified serial numbers not found.")
        return None, None
    
    def establish_connection(self, baud_rate=115200, timeout=1):
        """
        Establishes a serial connection using the serial number to find the port.
        """
        port, found_serial_number = self.find_serial_port()  # Get both port and serial number
        if port:
            self.serial_device = serial.Serial(port, baud_rate, timeout=timeout)
            print(f"Connection established to device with serial number {found_serial_number} at port {port}")
            return self.serial_device
        else:
            print("Failed to establish connection.")
            return None
        
    def close_connection(self):
        if self.serial_device and self.serial_device.is_open:
            self.serial_device.close()