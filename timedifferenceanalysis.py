import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.signal import butter, lfilter

filename = r"C:\Users\Michael\Downloads\June30_phasetest_0.csv"

def extractfile():
    global hydrophonea, hydrophoneb, hydrophonec
    hydrophonea = []; hydrophoneb = []; hydrophonec = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['CH1'] == 'Volt':
                continue
            hydrophonea = np.append(hydrophonea, float(row['CH1']))
            hydrophoneb = np.append(hydrophoneb, float(row['CH2']))
            hydrophonec = np.append(hydrophonec, float(row['CH3']))
        hydrophonea = dcbiasremoval(hydrophonea)
        hydrophoneb = dcbiasremoval(hydrophoneb)
        hydrophonec = dcbiasremoval(hydrophonec)
    file.close() 

def correlate():
    global t
    plt.plot(t,hydrophonea,t,hydrophoneb,t,hydrophonec)
    ##Range selection
    cutrange = pingfinder(hydrophonea)
    cut(cutrange)
    plt.axvline(x=cutrange[0]*T)
    plt.axvline(x=cutrange[-1:]*T)
    plt.show()
    
    plt.plot(tcut,acut,tcut,bcut,tcut,ccut)
    plt.show()
    
    blowup(tcut,acut,bcut,ccut)
    
    corrL = np.correlate(acut,bcut,"full")
    corrR = np.correlate(bcut,ccut,"full")
    plt.plot(corrL); plt.show()
    timedifferenceL = (np.argmax(np.abs(corrL))-acut.size)*(T/interp_factor)
    timedifferenceR = (np.argmax(np.abs(corrR))-acut.size)*(T/interp_factor)
#    print(np.argmax(np.abs(corr))-acut.size) #debug
    if timedifferenceL == 0:
        timedifferenceL = 1e-9
    if timedifferenceR == 0:
        timedifferenceR = 1e-9
    print('Time difference L: ', timedifferenceL, 's')
    print('Time difference R: ', timedifferenceR, 's')
    print('Phase shift L: ', phaseshift(timedifferenceL), 'deg')
    print('Phase shift R: ', phaseshift(timedifferenceR), 'deg')

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
    Fs = 500000; T = 1/Fs; f_centre = 27000; phaseshift = 75
    t = np.arange(0,0.0001,T)
    wavea = 0.5*np.sin(2*np.pi*f_centre*t + phaseshift*np.pi/180)
    waveb = 0.5*np.sin(2*np.pi*f_centre*t)
    print(np.correlate(wavea, waveb))
    plt.plot(t,wavea,t,waveb)
    plt.axvline(0.000026)
    timedifference = phaseshift/(360*f_centre)
    plt.axvline(0.000026 + timedifference) # td = ps/2pif
    plt.show()
    print('Time difference: ', timedifference, 's')
    print('Phase shift: ', phaseshift, 'deg')
    print('Path length difference: ', pathlengthdiff(timedifference), 'mm')
    
def cut(signalrange):
    global tcut, acut, bcut, ccut
    tcut = t[signalrange]; tcut = tcut/np.max(t)
    acut = hydrophonea[signalrange]; acut = acut/np.max(acut)
    bcut = hydrophoneb[signalrange]; bcut = bcut/np.max(bcut)
    ccut = hydrophonec[signalrange]; ccut = ccut/np.max(ccut)
    tcut, acut, bcut, ccut = interpolate(5, tcut, acut, bcut, ccut)
    
def interpolate(mult_factor, tcut, acut, bcut, ccut):
    global Fs, interp_factor
    fa = interp1d(tcut, acut, kind='cubic')
    fb = interp1d(tcut, bcut, kind='cubic')
    fc = interp1d(tcut, ccut, kind='cubic')
    t_interp = np.linspace(tcut[0],tcut[-1:],num=mult_factor*len(tcut),endpoint=True)
    acut_interp = fa(t_interp)
    bcut_interp = fb(t_interp)
    ccut_interp = fc(t_interp)
    acut_interp = butter_bandpass_filter(acut_interp, Fs*interp_factor)
    bcut_interp = butter_bandpass_filter(bcut_interp, Fs*interp_factor)
    ccut_interp = butter_bandpass_filter(ccut_interp, Fs*interp_factor)
    return t_interp, acut_interp, bcut_interp, ccut_interp

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, fs, lowcut=20000, highcut=50000, order=3):
#    fs = Fs*interp_factor
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y
    
def pathlengthdiff(timediff):
    vsoundwater = 1484 # m/s
    return vsoundwater*timediff

def phaseshift(timediff):
    global f_centre
    sign = (360*timediff*f_centre)/abs(360*timediff*f_centre)
    return sign*(360*timediff*f_centre % 90)

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

def blowup(t,signala,signalb,signalc):
    cut = np.arange(int(len(t)*0.4), int(len(t)*0.5))
    plt.plot(t[cut], signala[cut], t[cut], signalb[cut], t[cut], signalc[cut])
    plt.show()
    
def dcbiasremoval(hydrophone):
    if 1.1 > np.mean(hydrophone) > 0.9:
        return hydrophone - np.mean(hydrophone)
    else:
        return None
    
def main():
    global Fs, T, L, f_centre, t, interp_factor
    ##FFT constants
    Fs = 500000; T = 1/Fs; f_centre = 27000
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