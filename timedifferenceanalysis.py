import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

filename = r"C:\Users\Michael\Downloads\June27_phasetest_0.csv"

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
t = np.linspace(0,L*T,num=L,endpoint=True)

def correlate():
    plt.plot(t,hydrophonea,t,hydrophoneb)
    ##Range selection
    cutrange = pingfinder(hydrophonea)
    cut(cutrange)
    plt.axvline(x=cutrange[0]*T)
    plt.axvline(x=cutrange[-1:]*T)
    plt.show()
    
    plt.plot(tcut,acut,tcut,bcut)
    plt.show()
    
    blowup(tcut,acut,bcut)
    
    corr = np.correlate(acut,bcut,"full")
    plt.plot(corr); plt.show()
    timedifference = (np.argmax(np.abs(corr))-acut.size)*T
    if timedifference == 0:
        timedifference = 1e-9
    print('Time difference: ', timedifference, 's')
    print('Phase shift: ', phaseshift(timedifference), 'deg')

def visual():
    plt.plot(t,hydrophonea,t,hydrophoneb)
    ##Range selection
    start = 0.007; end = start + 0.00005
    xcoords = [start, end]
    signalrange = np.arange(int(start*Fs),int(end*Fs)) 
    cut(signalrange)
    for xc in xcoords:
        plt.axvline(x=xc)
    plt.show()
    plt.plot(tcut,acut,tcut,bcut)
    offset = 0.000004
    plt.axvline(start + offset)
    timedifference = 0.000006
    plt.axvline(start + offset + timedifference)
    plt.show()
    phshift = phaseshift(timedifference)
    print('Time difference: ', timedifference, 's')
    print('Phase shift: ', phshift, 'deg')
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
    tcut = t[signalrange]; tcut = tcut/np.max(t)
    acut = hydrophonea[signalrange]; acut = acut/np.max(acut)
    bcut = hydrophoneb[signalrange]; bcut = bcut/np.max(bcut)
    tcut, acut, bcut = interpolate(5, tcut, acut, bcut)
    
def interpolate(mult_factor, tcut, acut, bcut):
    fa = interp1d(tcut, acut, kind='cubic')
    fb = interp1d(tcut, bcut, kind='cubic')
    t_interp = np.linspace(tcut[0],tcut[-1:],num=mult_factor*len(tcut),endpoint=True)
    acut_interp = fa(t_interp)
    bcut_interp = fb(t_interp)
    return t_interp, acut_interp, bcut_interp
    
def pathlengthdiff(timediff):
    vsoundwater = 1484 # m/s
    return vsoundwater*timediff

def phaseshift(timediff):
    sign = (360*timediff*fc)/abs(360*timediff*fc)
    return sign*(360*timediff*fc % 90)

def pingfinder(hydrophone):
    mean = np.mean(np.abs(hydrophone))
    pingdex = [x for x in hydrophone if x > mean*2]
    pingmin = np.min(np.where(hydrophone == pingdex[0]))
    pingmax = np.max(np.where(hydrophone == pingdex[-1:]))
    if (pingmax - pingmin)*T > 0.004:
        pingmax = int(pingmin + 0.004*Fs)
#    ping = hydrophone[pingmin:pingmax]
#    plt.plot(np.arange(0,(ping.size-0.5)*T,T),ping); plt.show()
    return np.arange(pingmin, pingmax)

def blowup(t,signala,signalb):
    cut = np.arange(int(len(t)*0.4), int(len(t)*0.5))
    plt.plot(t[cut], signala[cut], t[cut], signalb[cut]); plt.show()
    
def main():
    correlate()
#    visual()
#    example()
#    interpolate(t, hydrophonea)
    return 0;

if __name__ == "__main__":
    main()