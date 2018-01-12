#http://playground.arduino.cc/interfacing/python
import matplotlib.pyplot as plt
import numpy as np

string = 'C:/Users/Mikey/PycharmProjects/SONAR/Transdec_Data/SubRightFacing/test0.dat'

data = np.fromfile(string, dtype=np.int16).reshape(-1, 2) # Colorado samples are 360000 long

for j in range(0,2):
    for i in range(0,100):
        data[i,j] = 0
        i += 1
    j += 1

# np.savetxt("test0.csv", data, delimiter=",")

# Plotting code

plt.figure(1)
plt.subplot(211)
plt.title('Hydrophone Data 1')  # Plot the title
plt.grid(True)  # Turn the grid on
plt.ylabel('Hydrophone Signal')  # Set ylabels
plt.plot(data[:,0], label='w')  # plot the temperature
plt.legend(loc='upper left')  # plot the legend

plt.subplot(212)
plt.title('Hydrophone Data 2')  # Plot the title
plt.grid(True)  # Turn the grid on
plt.ylabel('Hydrophone Signal')  # Set ylabels
plt.plot(data[:,1], label='w')  # plot the temperature
plt.legend(loc='upper left')  # plot the legend
plt.show()