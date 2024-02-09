import serial

port = 'COM12'  # Adjust as necessary
with serial.Serial(port, 115200, timeout=1) as ser:
    while True:
        if ser.in_waiting:
            data = ser.read(ser.in_waiting)
            print("Received data:", data)