import serial
import io
import tkinter
import time
import numpy as np
from matplotlib import pyplot as plt

# tkinter will be used for inputting data collection parameters
#top = tkinter.Tk()
# Code to add widgets will go here...
#top.mainloop()

ser = serial.Serial(
    port='COM5',
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1,  # Read timeout in s
    xonxoff=False,  # Enable software flow control
    rtscts=False,  # Enable hardware RTS/CTS flow control
)

# Initialise variables for looping serial data collection
# start = time.time()
sample_size = 100
s = [None] * sample_size
ser.write(bytes([sample_size]))

for i in range(0,sample_size):
    s[i] = int.from_bytes(ser.read(1), byteorder='little')
print(s)

# while time.time()-start < 2: # Run for 2 seconds
#     np.insert(s,i,int.from_bytes(ser.read(1), byteorder='little'),axis=None)  # convert bytes to int. MSB at end of byte array
#     i = i + 1
# print(len(s))
# print(s)
ser.close()

####To solve
# 12 bit ADC value -> 8 bit UART transmission
