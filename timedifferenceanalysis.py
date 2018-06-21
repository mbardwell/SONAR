import csv
import numpy as np
import matplotlib.pyplot as plt

filename = r"C:\Users\Michael\Downloads\June21_phasetest_45.csv"

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

##Plot full signal
plt.plot(t,hydrophonea,t,hydrophoneb)

def correlate():
    ##Range selection
    start = 0.004; end = start + 0.003
    xcoords = [start, end]
    signalrange = np.arange(int(start*Fs),int(end*Fs)) 
    cut(signalrange)
    for xc in xcoords:
        plt.axvline(x=xc)
    plt.show()
    plt.plot(tcut,acut,tcut,bcut)
    plt.show()
    print(min(np.abs(np.correlate(acut,bcut,"full"))))
    
def visual():
    ##Range selection
    start = 0.004; end = start + 0.00005
    xcoords = [start, end]
    signalrange = np.arange(int(start*Fs),int(end*Fs)) 
    cut(signalrange)
    for xc in xcoords:
        plt.axvline(x=xc)
    plt.show()
    plt.plot(tcut,acut,tcut,bcut)
    plt.axvline(0.004024)
    plt.axvline(0.00403)
    plt.show()
    
def cut(signalrange):
    global tcut, acut, bcut
    tcut = t[signalrange]
    acut = hydrophonea[signalrange]
    bcut = hydrophoneb[signalrange]

def main():
    correlate()
#    visual()
    return 0;

if __name__ == "__main__":
    main()