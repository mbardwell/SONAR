import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.signal import butter, lfilter

filename = r"C:\Users\Michael\Downloads\June30_phasetest_45.csv"

def extractfile():
    global hydrophonea, hydrophoneb
    hydrophonea = []; hydrophoneb = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['CH1'] == 'Volt':
                continue
            hydrophonea = np.append(hydrophonea, float(row['CH1']))
            hydrophoneb = np.append(hydrophoneb, float(row['CH2']))
        hydrophonea = dcbiasremoval(hydrophonea)
        hydrophoneb = dcbiasremoval(hydrophoneb)
    file.close() 

def correlate():
    global t
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
    timedifference = (np.argmax(np.abs(corr))-acut.size)*(T/interp_factor)
#    print(np.argmax(np.abs(corr))-acut.size) #debug
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
    acut_interp = butter_bandpass_filter(acut_interp)
    bcut_interp = butter_bandpass_filter(bcut_interp)
    return t_interp, acut_interp, bcut_interp

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut=20000, highcut=50000, fs=Fs*interp_factor, order=3):
    global interp_factor
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y
    
def pathlengthdiff(timediff):
    vsoundwater = 1484 # m/s
    return vsoundwater*timediff

def phaseshift(timediff):
    global fc
    sign = (360*timediff*fc)/abs(360*timediff*fc)
    return sign*(360*timediff*fc % 90)

def pingfinder(hydrophone):
    global Fs, T
    mean = np.mean(np.abs(hydrophone))
    pingdex = [x for x in hydrophone if x > 2*mean]
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
    
def dcbiasremoval(hydrophone):
    if 1.1 > np.mean(hydrophone) > 0.9:
        return hydrophone - np.mean(hydrophone)
    else:
        return None
    
def main():
    global Fs, T, L, fc, t, interp_factor
    ##FFT constants
    Fs = 500000; T = 1/Fs; fc = 27000
    extractfile()
    L = int(hydrophonea.size);
    
    ##Time signal synthesis
    t = np.linspace(0,L*T,num=L,endpoint=True)
    interp_factor = 5 # this number will multiple the signal density
    
    correlate()
#    visual()
#    example()
#    interpolate(t, hydrophonea)
    return 0;

if __name__ == "__main__":
    main()