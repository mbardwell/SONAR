import csv
import numpy as np
import matplotlib.pyplot as plt

filename = r"C:\Users\Michael\Documents\SONAR\Data\forphaseshiftanalysis_sampletime2us.csv"

a = []; b = []

with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            a = np.append(a, float(row['CH1']))
            b = np.append(b, float(row['CH2']))
        #Normalize
        a = a / max(a)
file.close()

#FFT analysis
Fs = 500000; timestep = 1/Fs
sp = np.fft.fft(a)
freq = np.fft.rfftfreq(len(sp), timestep)
plt.plot(freq, np.abs(sp[0:len(freq)]))
plt.show()