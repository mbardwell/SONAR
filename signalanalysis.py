import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.signal import butter, lfilter


#### Signals have to be conditioned together for findping() reasons ####
class SignalConditioning(object):
    def __init__(self, Fs, signalA, signalB, signalC):
        self.t = np.linspace(0,signalA.size/Fs,signalA.size)
        self.signalA = signalA
        self.signalB = signalB
        self.signalC = signalC
        self.Fs = Fs
        self.L = self.signalA.size
        self.samplingtime = self.L/self.Fs
        self.sizecheck()
        
    def sizecheck(self):
        if self.signalA.size != self.signalB.size:
            print("signal A not the same size as signal B")
            exit(1)
        if self.signalB.size != self.signalC.size:
            print("signal B not the same size as signal C")
            exit(1)
        
    def removebias(self):        
        if 1.1 > np.mean(self.signalA) > 0.9:
            self.signalA = self.signalA - np.mean(self.signalA)
        if 1.1 > np.mean(self.signalB) > 0.9:
            self.signalB = self.signalB - np.mean(self.signalB)
        if 1.1 > np.mean(self.signalC) > 0.9:
            self.signalC = self.signalC - np.mean(self.signalC)
            
    def findping(self):
        mean = np.mean(np.abs(self.signalA))
        pingdex = [x for x in self.signalA if x > 2*mean]
        pingmin = np.min(np.where(self.signalA == pingdex[0]))
        pingmax = pingmin + 250
#        pingmax = np.max(np.where(self.signalA == pingdex[-1:]))
#        if (pingmax - pingmin)/self.Fs > 0.004:
#            pingmax = int(pingmin + 0.004*self.Fs)
        return np.arange(pingmin, pingmax)
    
    def cutoutping(self):
        signalrange = self.findping()
        self.t = self.t[signalrange]
        self.signalA = self.signalA[signalrange]
        self.signalB = self.signalB[signalrange]
        self.signalC = self.signalC[signalrange]
        self.L = self.signalA.size
        self.samplingtime = self.L/self.Fs
    
    def normalise(self):
        self.signalA = self.signalA/np.max(self.signalA)
        self.signalB = self.signalB/np.max(self.signalB)
        self.signalC = self.signalC/np.max(self.signalC)
        
    def hamming(self):
        hamm = np.hamming(self.t.size)
        self.signalA = self.signalA*hamm
        self.signalB = self.signalB*hamm
        self.signalC = self.signalC*hamm
    
    def butter_bandpass(self, lowcut, highcut, order=5):
        nyq = 0.5 * self.Fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def butter_bandpass_filter(self, lowcut=20000, highcut=50000, order=5):
        b, a = self.butter_bandpass(lowcut, highcut, order=order)
        self.signalA = lfilter(b, a, self.signalA)
        self.signalB = lfilter(b, a, self.signalB)
        self.signalC = lfilter(b, a, self.signalC)
    
    def interpolate(self, mult_factor):
        self.originalsize = self.L
        fa = interp1d(self.t, self.signalA, kind='cubic')
        fb = interp1d(self.t, self.signalB, kind='cubic')
        fc = interp1d(self.t, self.signalC, kind='cubic')
        self.t = np.linspace(self.t[0],self.t[-1:],num=mult_factor*len(self.t),endpoint=True)
        self.signalA = fa(self.t)
        self.signalB = fb(self.t)
        self.signalC = fc(self.t)
        self.Fs = self.signalA.size/self.samplingtime
        print('Fs: ', self.Fs)
        self.L = self.signalA.size

class PhaseShiftAnalysis(object):
    def __init__(self, Fc=27000, Fs=500000):
        self.Fc = Fc
        self.Fs = Fs
        self.phase = []
        self.peakfreq = []
        self.phasecleanup_flag = 0
        
    def returnangles(self, angles):
        return angles[self.peakindex]
        
    def pilist(self):
        print('pi/2: ', np.pi/2, "\n", 'pi/3: ', np.pi/3, '\n', 'pi/4: ', np.pi/4)
    
#    def binselection(self, fc):
#        return np.where(self.freq == min(self.freq, key=lambda x:abs(x-fc)))
        
    def fftanalysis(self, Fs, hydrophone):
        self.Fs = Fs
        T = 1/self.Fs
        self.L = hydrophone.size
        ##FFT analysis
        sp = np.fft.rfft(hydrophone) # compute the fast fourier transform of the signal
        P2 = np.abs(sp/self.L) # compute two sided spectrum
        P1 = P2[1:int((self.L/2)+1)] # select the single sided spectrum ignoring DC
        P1[2:-1] = 2*P1[2:-1]; # I don't understand this step
        self.P1 = P1
        self.peakindex = np.argmax(P1)
        self.freq = np.fft.rfftfreq(self.L, d=T)
        self.peakfreq = np.append(self.peakfreq, self.freq[self.peakindex])
        self.ang = np.angle(sp, deg=1)
        return self.returnangles(self.ang)
    
    def phasecleanup(self, Fs, signalA, signalB, signalC):
        self.phase = np.append(self.phase, self.fftanalysis(Fs, signalA))
        self.phase = np.append(self.phase, self.fftanalysis(Fs, signalB))
        self.phase = np.append(self.phase, self.fftanalysis(Fs, signalC))
        print('pre cleanup phase', self.phase)
        
        for phase in self.phase:
            if phase < 0:
                self.phase[np.where(self.phase == phase)] = 360 + phase
        print('post cleanup phase', self.phase)
        self.fccheck()
        print('centre frequencies', self.peakfreq)
        self.phasecleanup_flag = 1
        
    def phasedifference(self):
        if self.phasecleanup_flag == 1:
            self.shiftL = self.phase[1]-self.phase[0]
            self.shiftR = self.phase[1]-self.phase[2]
            print('shiftL', round(self.shiftL), 'shiftR', round(self.shiftR))
            self.phasecleanup_flag = 0 # reset flag for next run
        else:
            print('Must run phasecleanup method before phasedifference method')
    
    def heading(self):
        if self.shiftL > 0 and self.shiftR > 0:
            self.heading = self.shiftL - self.shiftR

        if self.shiftL < 0 and self.shiftR > 0:
            self.heading = -60 - self.shiftR + np.abs(self.shiftL)
        
        if self.shiftL > 0 and self.shiftR < 0:
            self.heading = 60 + self.shiftL - np.abs(self.shiftR)
#        
        if self.shiftL < 0 and self.shiftR < 0:
            self.heading = -(self.shiftL - self.shiftR) # not verified
            
        print('Heading:', self.heading)    
            
    def fccheck(self):
        if self.peakfreq[0] != self.peakfreq[1]:
            print('signal 1 and ref centre frequencies not aligned')
        if self.peakfreq[2] != self.peakfreq[1]:
            print('signal 1 and ref centre frequencies not aligned')
        
        
    def example(self):
        ##FFT constants
        Fs = 500000; T = 1/Fs; L = 1000 # L same as in oscdata
        
        ##Signal synthesis
        t = np.arange(0,L)*T
        a = 0.5*np.cos(2*np.pi*27000*t + np.pi/2) # used in examples
        plt.plot(t[0:int(L/5)],a[0:int(L/5)]); plt.show()
        
        ##FFT analysis
        sp = np.fft.rfft(a) # compute the fast fourier transform of the signal
        P2 = np.abs(sp/L) # compute two sided spectrum
        P1 = P2[1:int((L/2)+1)] # select the single sided spectrum ignoring DC
        P1[2:-1] = 2*P1[2:-1]; # I don't understand this step [2:-1 = 2:end]
        freq = np.fft.rfftfreq(L, d=T)
        ang = np.angle(sp, deg=1)
        plt.plot(freq[0:int(L/2)], P1); plt.show()
        plt.plot(freq, ang, 'o'); plt.show()
        self.returnangles(ang, freq)    
        return 0   

    
class TimeDifferenceAnalysis(object):
    def __init__(self, Fc=27000, Fs=500000):
        self.Fc = Fc
        self.Fs = Fs
    
    def correlate(self, signalA, signalB):        
        corrarray = np.correlate(signalA,signalB,"full")
        correlation = np.argmax(np.abs(corrarray)) - corrarray.size()
        return correlation
        
    def timedifference(self, correlation):
        timediff = correlation/self.Fs #/interp_factor
        return timediff
        
    def pathlengthdiff(self, timediff):
        vsoundwater = 1484 # m/s
        return vsoundwater*timediff
    
#    def phaseshift(self, timediff): ## Functionality overlap with PSA
#        shift = 360*timediff*self.Fc
#        return shift
        
class Misc(object):
    
    def plotsignals(self, signalA, signalB, signalC):
        plt.plot(signalA[0:100] ,'o')
        plt.plot(signalB[0:100] ,'o')
        plt.plot(signalC[0:100] ,'o'); plt.show()
        
    # fccheck function has already verified that the fc's are the same. fft's should be close    
    def plotfft(self, freq, P1, ang, L): 
        plt.plot(freq[0:int(L/2)], P1); plt.show()
#        plt.plot(self.freq, self.ang, 'o'); plt.show()
                
    # Creates mock data
    def sinewave(self, t, phase):
        f_centre = 27000
        wave = t
        wave = 0.01*np.sin(2*np.pi*t[0:int(len(t)*0.6)]*10)
        wave = np.append(wave,np.sin(2*np.pi*t[0:int(len(t)*0.4)]*f_centre + phase*np.pi/180))
        wave = np.append(wave,0.01*np.sin(2*np.pi*t[0:int(len(t)*0.6)]*10))
        return wave
    
### For testing ###
            
#def main():
#    psa = PhaseShiftAnalysis()
##    oscdata()
#    psa.example()
#    return 0;
#
#if __name__ == "__main__":
#    main()