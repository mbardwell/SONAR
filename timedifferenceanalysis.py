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
Fs = 500000; T = 1/Fs; L = int(hydrophonea.size); fc = 27000

##Time signal synthesis
t = np.arange(0,L)*T

def correlate():
    plt.plot(t,hydrophonea,t,hydrophoneb)
    ##Range selection
    start = 0.003; end = start + 0.004
    xcoords = [start, end]
    signalrange = np.arange(int(start*Fs),int(end*Fs)) 
    cut(signalrange)
    for xc in xcoords:
        plt.axvline(x=xc)
    plt.show()
    plt.plot(tcut,acut,tcut,bcut)
    plt.show()
    print(min(np.abs(np.correlate(acut/max(acut),bcut/max(acut),"full"))))
    print(np.correlate(acut/max(acut),bcut/max(acut),"full"))
    
def visual():
    plt.plot(t,hydrophonea,t,hydrophoneb)
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
    timedifference = 0.0000068
    plt.axvline(0.004024 + timedifference)
    plt.show()
    phaseshift = 360*timedifference*fc
    print('Time difference: ', timedifference, 's')
    print('Phase shift: ', phaseshift, 'deg')
    print('Path length difference: ', pathlengthdiff(timedifference), 'mm')
    
def example():
    # Demonstrates relationship between phase shift and time delay
    Fs = 500000; T = 1/Fs; fc = 27000; phaseshift = 75
    t = np.arange(0,0.0001,T)
    wavea = 0.5*np.sin(2*np.pi*fc*t + phaseshift*np.pi/180)
    waveb = 0.5*np.sin(2*np.pi*fc*t)
    print(np.correlate(wavea, waveb))
    plt.plot(t,wavea,t,waveb)
    plt.axvline(0.000026)
    timedifference = phaseshift/(360*fc)
    plt.axvline(0.000026 + timedifference) # td = ps/2pif
    plt.show()
    print('Time difference: ', timedifference, 's')
    print('Phase shift: ', phaseshift, 'deg')
    print('Path length difference: ', pathlengthdiff(timedifference), 'mm')
    
def cut(signalrange):
    global tcut, acut, bcut
    tcut = t[signalrange]
    acut = hydrophonea[signalrange]
    bcut = hydrophoneb[signalrange]
    
def pathlengthdiff(timediff):
    vsoundwater = 1484 # m/s
    return vsoundwater*timediff

def main():
#    correlate()
    visual()
#    example()
    return 0;

if __name__ == "__main__":
    main()