from pyb import I2C

i2c = I2C(4) #or use 2 if wired up to sda and scl 2 on the openMV board 
i2c = I2C(4, I2C.MASTER)
i2c.init(I2C.MASTER, baudrate = 100000) #lower baudrate for longer cables 

print("Scanning I2C bus...")
devices = i2c.scan()

if devices: 
    for device in devices: 
        print("Found i2C device at address:", hex(device))
else: 
    print("No i2C devices found.")