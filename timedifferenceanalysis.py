import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.signal import butter, lfilter

filename = r"C:\Users\Michael\Downloads\July4_phasetest_45.csv"

def extractfile():
    global hydrophonech1, hydrophonech2, hydrophonech3
    hydrophonech1 = []; hydrophonech2 = []; hydrophonech3 = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['CH1'] == 'Volt':
                continue
            hydrophonech1 = np.append(hydrophonech1, float(row['CH3']))
            hydrophonech2 = np.append(hydrophonech2, float(row['CH1']))
            hydrophonech3 = np.append(hydrophonech3, float(row['CH2']))
        hydrophonech1 = dcbiasremoval(hydrophonech1)
        hydrophonech2 = dcbiasremoval(hydrophonech2)
        hydrophonech3 = dcbiasremoval(hydrophonech3)
    file.close() 

def correlate():
    global t
    plt.plot(t,hydrophonech1,t,hydrophonech2,t,hydrophonech3)
    ##Range selection
    cutrange = pingfinder(hydrophonech1)
    cut(cutrange)
    plt.axvline(x=cutrange[0]*T)
    plt.axvline(x=cutrange[-1:]*T)
    plt.show()
    
    plt.plot(tcut,h1cut,tcut,h2cut,tcut,h3cut)
    plt.axvline(x=tcut[int(len(tcut)*0.4)])
    plt.axvline(x=tcut[int(len(tcut)*0.5)])
    plt.show()
    
    blowup(tcut,h1cut,h2cut,h3cut)
    
    corrL = np.correlate(h1cut,h2cut,"full")
    corrR = np.correlate(h3cut,h2cut,"full")
    maxcorrL, maxcorrR = corrplotting(corrL, corrR)
    corrcheck(tcut,h1cut,h2cut,h3cut,maxcorrL,maxcorrR)
    timedifferenceL = (maxcorrL-h1cut.size)*(T/interp_factor)
    timedifferenceR = (maxcorrR-h1cut.size)*(T/interp_factor)
    if timedifferenceL == 0:
        timedifferenceL = 1e-9
    if timedifferenceR == 0:
        timedifferenceR = 1e-9
    print('Time difference AB: ', timedifferenceL, 's')
    print('Time difference CB: ', timedifferenceR, 's')
    print('Phase shift AB: ', phaseshift(timedifferenceL), 'deg')
    print('Phase shift CB: ', phaseshift(timedifferenceR), 'deg')
    
def cut(signalrange):
    global tcut, h1cut, h2cut, h3cut
    tcut = t[signalrange]; tcut = tcut/np.max(t)
    h1cut = hydrophonech1[signalrange]; h1cut = h1cut/np.max(h1cut)
    h2cut = hydrophonech2[signalrange]; h2cut = h2cut/np.max(h2cut)
    h3cut = hydrophonech3[signalrange]; h3cut = h3cut/np.max(h3cut)
    tcut, h1cut, h2cut, h3cut = interpolate(interp_factor, tcut, h1cut, h2cut, h3cut)
    hamm = np.hamming(tcut.size)
    h1cut = h1cut*hamm; h2cut = h2cut*hamm; h3cut = h3cut*hamm
    
def interpolate(mult_factor, tcut, h1cut, h2cut, h3cut):
    global Fs, interp_factor
    fa = interp1d(tcut, h1cut, kind='cubic')
    fb = interp1d(tcut, h2cut, kind='cubic')
    fc = interp1d(tcut, h3cut, kind='cubic')
    t_interp = np.linspace(tcut[0],tcut[-1:],num=mult_factor*len(tcut),endpoint=True)
    h1cut_interp = fa(t_interp)
    h2cut_interp = fb(t_interp)
    h3cut_interp = fc(t_interp)
    h1cut_interp = butter_bandpass_filter(h1cut_interp, Fs*interp_factor, order=1)
    h2cut_interp = butter_bandpass_filter(h2cut_interp, Fs*interp_factor, order=1)
    h3cut_interp = butter_bandpass_filter(h3cut_interp, Fs*interp_factor, order=1)
    return t_interp, h1cut_interp, h2cut_interp, h3cut_interp

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, fs, lowcut=20000, highcut=50000, order=5):
#    fs = Fs*interp_factor
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y
    
def pathlengthdiff(timediff):
    vsoundwater = 1484 # m/s
    return vsoundwater*timediff

def phaseshift(timediff):
    global f_centre
    shift = 360*timediff*f_centre
#    if (shift > 90) :
#        shift = -(180 - shift)
    return shift

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

def blowup(t,signalh1,signalh2,signalh3,minrange=0.4,maxrange=0.5,xline1=None,xline2=None):
    tnew = np.arange(int(len(tcut)*minrange), int(len(tcut)*maxrange))
    plt.plot(t[tnew], signalh1[tnew], t[tnew], signalh2[tnew], t[tnew], signalh3[tnew])
    if xline1 or xline2 != None:
        centre = t[tnew[int(len(tnew)/2)]]
        plt.axvline(x=centre)
        plt.axvline(x=centre+xline1*T)
        plt.axvline(x=centre+xline2*T)
    plt.show()
    
def corrplotting(corrL, corrR):
    maxcorrL = np.argmax(np.abs(corrL))
    maxcorrR = np.argmax(np.abs(corrR))
    trangeL = np.arange(int(0.99*maxcorrL),int(1.01*maxcorrL))
    trangeR = np.arange(int(0.99*maxcorrR),int(1.01*maxcorrR))
    plt.plot(trangeL, corrL[trangeL], trangeR, corrR[trangeR])
    plt.axvline(x=maxcorrL)
    plt.axvline(x=maxcorrR)
    plt.show()
    return maxcorrL, maxcorrR

def corrcheck(tcut,h1cut,h2cut,h3cut,maxcorrL,maxcorrR):
    indexshiftL = (maxcorrL - h1cut.size)/interp_factor
    indexshiftR = (maxcorrL - h1cut.size)/interp_factor
    blowup(tcut,h1cut,h2cut,h3cut,0.499,0.501,indexshiftL,indexshiftR)
    
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
    L = int(hydrophonech1.size);
    
    ##Time signal synthesis
    t = np.linspace(0,L*T,num=L,endpoint=True)
    interp_factor = 50 # this number will multiple the signal density
    
    correlate()
    return 0

if __name__ == "__main__":
    main()