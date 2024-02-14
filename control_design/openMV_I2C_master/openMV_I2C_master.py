from pyb import I2C

# Initialize I2C in master mode
i2c = I2C(4)                         # create on bus 2
i2c = I2C(4, I2C.MASTER)             # create and init as a master
i2c.init(I2C.MASTER, baudrate=100000) # init as a master

# ESP32's I2C slave address (change as required)
esp32_addr = 0x42  # Example address

# Example message to send
message = "Hello Esp32\n"  # Example command with parameters

# Convert the message to bytes and send
#i2c.mem_write(message.encode('utf-8'), esp32_addr, 0x00)  # Assuming 0x00 as the starting memory address
# OpenMV script adjustment
i2c.send(message.encode('utf-8'), addr=esp32_addr)