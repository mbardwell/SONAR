#https://github.com/surendharreddy/Arduino-Python-live-data-plot/blob/master/TMP36.py
import serial  # import serial library
import numpy as np  # import numpy
import matplotlib.pyplot as plt  # import matplotlib library
from drawnow import *

temperatureF = []
arduinoData = serial.Serial('COM6', 115200, timeout=1)  # Creating our serial object named arduinoData
plt.ion()  # Tell matplotlib you want interactive mode to plot live data
cnt = 0


def makeFig():  # Create a function that makes our desired plot
    plt.ylim(80, 90)  # Set y min and max values
    plt.title('My Live Streaming Sensor Data')  # Plot the title
    plt.grid(True)  # Turn the grid on
    plt.ylabel('Temp F')  # Set ylabels
    plt.plot(temperatureF, 'ro-', label='Degrees F')  # plot the temperature
    plt.legend(loc='upper left')  # plot the legend


while True:  # While loop that loops forever
    while (arduinoData.inWaiting() == 0):  # Wait here until there is data
        pass  # do nothing
    arduinoString = arduinoData.readline()  # read the line of text from the serial port
    dataArray = arduinoString.split(',')  # Split it into an array called dataArray
    print
    arduinoString
    temperatureF.append(dataArray[2])  # Build our temperatureF array by appending temp readings
    drawnow(makeFig)  # Call drawnow to update our live graph
    plt.pause(.000001)  # Pause Briefly. Important to keep drawnow from crashing
    cnt = cnt + 1
    if (cnt > 50):  # If you have 50 or more points, delete the first one from the array
        temperatureF.pop(0)  # This allows us to just see the last 50 data points