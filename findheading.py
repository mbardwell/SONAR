import csv
import numpy as np
import matplotlib.pyplot as plt
from signalanalysis import PhaseShiftAnalysis, TimeDifferenceAnalysis, SignalConditioning

def main():
    filename = r"C:\Users\Michael\Downloads\July4_phasetest_45.csv"
    signalA, signalB, signalC = extractfile(filename)
    
    tda = TimeDifferenceAnalysis()
    psa = PhaseShiftAnalysis()
    sig = SignalConditioning(500000/4, signalA, signalB, signalC)
    sig.removebias()
    sig.cutoutping()
    sig.normalise()
#    sig.hamming()
    sig.butter_bandpass_filter(order=3)
    
    desired_L = 5000
    while (sig.L != desired_L):
        sig.interpolate(desired_L/sig.L)
    print('L', sig.L, 'Fs', sig.Fs)
    psa.fftanalysis(sig.signalA, sig.Fs)
#    plt.plot(sig.signalA[0:100] ,'o')

## Use mock data ##
def sinewave(t, phase):
    f_centre = 27000
    wave = t
    wave = 0.01*np.sin(2*np.pi*t[0:int(len(t)*0.6)]*10)
    wave = np.append(wave,np.sin(2*np.pi*t[0:int(len(t)*0.4)]*f_centre + phase))
    wave = np.append(wave,0.01*np.sin(2*np.pi*t[0:int(len(t)*0.6)]*10))
    return wave

## Use real data ##
def extractfile(filename):
    hydrophonech1 = []; hydrophonech2 = []; hydrophonech3 = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['CH1'] == 'Volt':
                continue
            hydrophonech1 = np.append(hydrophonech1, float(row['CH3']))
            hydrophonech2 = np.append(hydrophonech2, float(row['CH1']))
            hydrophonech3 = np.append(hydrophonech3, float(row['CH2']))
#        tp = np.linspace(0,1000/500000,num=1000,endpoint=True)
#        hydrophonech1 = sinewave(tp, 0)
#        hydrophonech2 = sinewave(tp, 30)
#        hydrophonech3 = sinewave(tp, 45)
    file.close()
    return hydrophonech1, hydrophonech2, hydrophonech3
    
if __name__ == "__main__":
    main()
    
#### Plotting functions ####
#    def plotinputs(cutrange):
#        plt.plot(t,hydrophonech1,t,hydrophonech2,t,hydrophonech3)
#        plt.axvline(x=cutrange[0]*T)
#        plt.axvline(x=cutrange[-1:]*T)
#        plt.show()
    
#    def corrplotting(corrL, corrR):
#        maxcorrL = np.argmax(np.abs(corrL))
#        maxcorrR = np.argmax(np.abs(corrR))
#        trangeL = np.arange(int(0.8*maxcorrL),int(1.2*maxcorrL))
#        trangeR = np.arange(int(0.8*maxcorrR),int(1.2*maxcorrR))
#        plt.plot(trangeL, corrL[trangeL], trangeR, corrR[trangeR])
#        plt.axvline(x=maxcorrL)
#        plt.axvline(x=maxcorrR)
#        plt.show()
#        return maxcorrL, maxcorrR
    
#    def blowup(t,signalh1,signalh2,signalh3,minrange=0.4,maxrange=0.5,xline1=None,xline2=None):
#        tnew = np.arange(int(len(tping)*minrange), int(len(tping)*maxrange))
#        plt.plot(t[tnew], signalh1[tnew], t[tnew], signalh2[tnew], t[tnew], signalh3[tnew])
#        if xline1 or xline2 != None:
#            centre = t[tnew[int(len(tnew)/2)]]
#            plt.axvline(x=centre)
#            plt.axvline(x=centre+xline1*T)
#            plt.axvline(x=centre+xline2*T)
#        plt.show()


#TO DO
#1. Import data
#2. Remove DC bias
#3. Cutout ping
#4. Interpolate
#5. Bandpass filter
#6. Multiply by Hamming factor (?)
#
#Apply perfect sine waves and check FFT amplitude/phase information	