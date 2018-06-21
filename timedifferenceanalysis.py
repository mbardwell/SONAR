import csv
import numpy as np
import matplotlib.pyplot as plt

#filename = r"C:\Users\Michael\Documents\SONAR\Data\forphaseshiftanalysis_sampletime2us.csv"
filename = r"C:\Users\Michael\Downloads\June21_phasetest_0.csv"


hydrophonea = []; hydrophoneb = []
with open(filename, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row['CH1'] == 'Volt':
            continue
        hydrophonea = np.append(hydrophonea, float(row['CH1']))
        hydrophoneb = np.append(hydrophoneb, float(row['CH2']))
file.close()

##FFT constants
Fs = 500000; T = 1/Fs; L = int(hydrophonea.size)

##Time signal synthesis
t = np.arange(0,L)*T

##Range selection
start = 0.005; end = start + 0.00005
xcoords = [start, end]
signalrange = np.arange(int(start*Fs),int(end*Fs))

##Cut signals
tcut = t[signalrange]
acut = hydrophonea[signalrange]
bcut = hydrophoneb[signalrange]

plt.plot(t,hydrophonea,t,hydrophoneb)
for xc in xcoords:
    plt.axvline(x=xc)
plt.show()

plt.plot(tcut,acut,tcut,bcut)
plt.axvline(0.005024)
plt.axvline(0.005026)
plt.show()