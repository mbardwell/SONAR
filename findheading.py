import csv
import numpy as np
from signalanalysis import PhaseShiftAnalysis, SignalConditioning, Misc
psamisc = Misc()

def main():
    filename = r"C:\Users\Michael\Downloads\July4_phasetest_90.csv"
    signalA, signalB, signalC = extractfile(filename)
    psa = PhaseShiftAnalysis()
    sig = SignalConditioning(500000/4, signalA, signalB, signalC)
    sig.removebias()
    sig.cutoutping()
    sig.normalise()
#    sig.hamming() # this seems to cause phase shift trouble
    sig.butter_bandpass_filter(order=3)
    
    desired_L = 5000
    while (sig.L != desired_L):
        sig.interpolate(desired_L/sig.L)
    psamisc.plotsignals(sig.signalA, sig.signalB, sig.signalC)
    psa.phasecleanup(sig.Fs, sig.signalA, sig.signalB, sig.signalC)
    psa.phasedifference()
    psa.heading()
    psamisc.plotfft(psa.freq, psa.P1, psa.ang, psa.L)
    


## Use real data ##
def extractfile(filename):
    hydrophonech1 = []; hydrophonech2 = []; hydrophonech3 = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['CH1'] == 'Volt':
                continue
            hydrophonech1 = np.append(hydrophonech1, float(row['CH1']))
            hydrophonech2 = np.append(hydrophonech2, float(row['CH2']))
            hydrophonech3 = np.append(hydrophonech3, float(row['CH3']))
    file.close()
    
#    tp = np.linspace(0,500/500000,num=500,endpoint=True)
#    hydrophonech1 = psamisc.sinewave(tp, 20)
#    hydrophonech2 = psamisc.sinewave(tp, 190)
#    hydrophonech3 = psamisc.sinewave(tp, 270)
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