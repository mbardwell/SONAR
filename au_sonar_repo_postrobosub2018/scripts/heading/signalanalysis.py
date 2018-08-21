import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.signal import butter, lfilter


#### Signals have to be conditioned together for findping() reasons ####
class SignalConditioning(object):
    def __init__(self, Fs, signalY, refY, signalX, refX):
        self.t = np.linspace(0,signalY.size/Fs,signalY.size)
        self.signalY = signalY
        self.refY = refY
        self.signalX = signalX
        self.refX = refX
        self.Fs = Fs
        self.L = self.signalY.size
        self.samplingtime = self.L/self.Fs
        self.sizecheck()
        
    def sizecheck(self):
        if self.signalY.size != self.refY.size:
            print("signal A not the same size as ref A")
            exit(1)
        if self.signalX.size != self.refX.size:
            print("signal B not the same size as ref B")
            exit(1)
        
    def removebias(self):        
        if 1.1 > np.mean(self.signalY) > 0.9:
            self.signalY = self.signalY - np.mean(self.signalY)
        if 1.1 > np.mean(self.refY) > 0.9:
            self.refY = self.refY - np.mean(self.refY)
        if 1.1 > np.mean(self.signalX) > 0.9:
            self.signalX = self.signalX - np.mean(self.signalX)
        if 1.1 > np.mean(self.refX) > 0.9:
            self.refX = self.refX - np.mean(self.refX)
    
    def cutsignal(self):
        # processor collects L ~ 1350. Cut that to 1000 for bin sizing 
        self.signalY = self.signalY[10:1010]
        self.refY = self.refY[10:1010]
        self.signalX = self.signalX[10:1010]
        self.refX = self.refX[10:1010]
        self.L = self.signalY.size
        self.t = np.linspace(0,self.L/self.Fs,self.L)
        self.samplingtime = self.L/self.Fs
    
    def normalise(self):
        self.signalY = self.signalY/np.max(self.signalY)
        self.refY = self.refY/np.max(self.refY)
        self.signalX = self.signalX/np.max(self.signalX)
        self.refX = self.refX/np.max(self.refX)
        
    def hamming(self):
        hamm = np.hamming(self.signalY.size)
        self.signalY = self.signalY*hamm
        self.refY = self.refY*hamm
        self.signalX = self.signalX*hamm
        self.refX = self.refX*hamm
    
    def butter_bandpass(self, lowcut, highcut, order=5):
        nyq = 0.5 * self.Fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def butter_bandpass_filter(self, lowcut=20000, highcut=50000, order=5):
        b, a = self.butter_bandpass(lowcut, highcut, order=order)
        self.signalY = lfilter(b, a, self.signalY)
        self.refY = lfilter(b, a, self.refY)
        self.signalX = lfilter(b, a, self.signalX)
        self.refX = lfilter(b, a, self.refX)
    
    def interpolate(self, mult_factor):
        self.originalsize = self.L
        fa = interp1d(self.t, self.signalY, kind='cubic')
        fb = interp1d(self.t, self.refY, kind='cubic')
        fc = interp1d(self.t, self.signalX, kind='cubic')
        fd = interp1d(self.t, self.refX, kind='cubic')
        self.t = np.linspace(self.t[0],self.t[-1:],num=mult_factor*len(self.t),endpoint=True)
        self.signalY = fa(self.t)
        self.refY = fb(self.t)
        self.signalX = fc(self.t)
        self.refX = fd(self.t)
        self.Fs = self.signalY.size/self.samplingtime
#        print('Fs: ', self.Fs)
        self.L = self.signalY.size

class PhaseShiftAnalysis(object):
    def __init__(self, Fc=27000, Fs=500000):
        self.Fc = Fc
        self.Fs = Fs
        self.phase = []
        self.peakfreq = []
        self.phasecleanup_flag = 0
        
    def phasecleanup(self, Fs, signalY, refY, signalX, refX):
        self.phase = np.append(self.phase, self.fftanalysis(Fs, signalY))
        self.phase = np.append(self.phase, self.fftanalysis(Fs, refY))
        self.phase = np.append(self.phase, self.fftanalysis(Fs, signalX))
        self.phase = np.append(self.phase, self.fftanalysis(Fs, refX))
#        print('phases', self.phase)
#        print('centre frequencies', self.peakfreq) # debug
        if self.fccheck():
            self.phasecleanup_flag = 1
            return True
        else:
            return False
        
    def phasedifference(self, suppress_output = False):
        if self.phasecleanup_flag == 1:
            self.shiftY = self.phase[1]-self.phase[0]
            if self.shiftY > 180:
                self.shiftY = self.shiftY - 360
            elif self.shiftY < -180:
                self.shiftY = self.shiftY + 360
            self.shiftX = self.phase[3]-self.phase[2]
            if self.shiftX > 180:
                self.shiftX = self.shiftX - 360
            elif self.shiftX < -180:
                self.shiftX = self.shiftX + 360
            if not suppress_output:
                print('shiftY', round(self.shiftY), 'shiftX', round(self.shiftX))
            self.phasecleanup_flag = 0 # reset flag for next run
            return True
        else:
            print('Must run phasecleanup method before phasedifference method')
            return False
        
    def returnangles(self, angles):
        return angles[self.peakindex]
        
    def fftanalysis(self, Fs, hydrophone):
        self.Fs = Fs
        T = 1/self.Fs
        self.L = hydrophone.size
        ##FFT analysis
        sp = np.fft.rfft(hydrophone) # compute the fast fourier transform of the signal
        P2 = np.abs(sp/self.L) # compute two sided spectrum
        self.P1 = P2[1:] # select the single sided spectrum ignoring DC
        self.P1[2:-1] = 2*self.P1[2:-1]; # I don't understand this step
        self.peakindex = np.argmax(self.P1)
        self.freq = np.fft.rfftfreq(self.L, d=T)[1:]
        self.peakfreq = np.append(self.peakfreq, self.freq[self.peakindex])
        self.ang = np.angle(sp, deg=1)[1:]
        return self.returnangles(self.ang)
    
    def heading(self, shiftX = None, shiftY = None):
        if shiftX == None and shiftY == None:
            self.heading = np.rad2deg(np.arctan2(self.shiftX, self.shiftY))
        else:
            self.heading = np.rad2deg(np.arctan2(shiftX, shiftY))
            
        if self.heading < 0:
            self.heading = 180 + self.heading
        elif self.heading > 0:
            self.heading = self.heading-180
        
        
#        if self.shiftY < 0 and self.shiftX < 0: #sections I (0,90)
#            print('section I')
# 
#        if self.shiftY < 0 and self.shiftX > 0: # section II (0,-90)
#            self.heading = self.heading
#            print('section II')
#       
#        if self.shiftY > 0 and self.shiftX > 0: # sections III (-90,-180)
#            self.heading = -90 - self.heading
#            print('section III')
#        
#        if self.shiftY > 0 and self.shiftX < 0: # section IV (90,180)
#            self.heading = 180 + self.heading
#            print('section IV')
            
#        print('Heading:', self.heading)
        return self.heading
            
    def fccheck(self):
        if self.peakfreq[0] != self.peakfreq[1]:
            print('signal 1 and ref centre frequencies not aligned')
            return False
        if self.peakfreq[2] != self.peakfreq[1]:
            print('signal 1 and ref centre frequencies not aligned')
            return False
        return True
    
        
class Misc(object):
    
    def plotsignals(self, signalY, refY, signalX, refX, display, cutstart = 'None'):
        if cutstart == 'None':
#            plt.plot(signalY, 'r'+display)
#            plt.plot(refY, 'r-o')
            plt.plot(signalX, 'g'+display)
            plt.plot(refX, 'g-o')
            plt.show()
        else:
            cutrange = np.arange(cutstart, cutstart+100,1)
#            plt.plot(signalY[cutrange], 'r'+display)
#            plt.plot(refY[cutrange], 'r-o')
            plt.plot(signalX[cutrange], 'g'+display)
            plt.plot(refX[cutrange], 'g-o')
            plt.show()
        
    # fccheck function has already verified that the fc's are the same. fft's should be close    
    def plotfft(self, freq, P1, ang, L): 
        plt.plot(freq, P1/max(P1)) 
#        plt.plot(freq, ang/max(ang))
        plt.title('FFT Results for Data Recording of 27 kHz Signal')
        plt.xlabel('Frequency Bins')
        plt.ylabel('P1 Magnitude')
        plt.show()
#        plt.plot(self.freq, self.ang, 'o'); plt.show()
                
    # Creates mock data
    def sinewave(self, t, phase):
        f_centre = 27000
        wave = t
        wave = 0.01*np.sin(2*np.pi*t[0:int(len(t)*0.6)]*10)
        wave = np.append(wave,np.sin(2*np.pi*t[0:int(len(t)*0.4)]*f_centre + phase*np.pi/180))
        wave = np.append(wave,0.01*np.sin(2*np.pi*t[0:int(len(t)*0.6)]*10))
        return wave
    
    ## Use real data ##
    def extractfile(self, filename):
        hydrophoneA = []; refY = []; hydrophoneB = []; refX = []
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['hydrophoneA'] == 'Volt':
                    continue
                hydrophoneA = np.append(hydrophoneA, float(row['hydrophoneA']))
                refY = np.append(refY, float(row['refA']))
                hydrophoneB = np.append(hydrophoneB, float(row['hydrophoneB']))
                refX = np.append(refX, float(row['refB']))
        file.close()
    #    tp = np.linspace(0,500/500000,num=500,endpoint=True)
    #    hydrophonech1 = psamisc.sinewave(tp, 20)
    #    hydrophonech2 = psamisc.sinewave(tp, 190)
    #    hydrophonech3 = psamisc.sinewave(tp, 270)
        return hydrophoneA, refY, hydrophoneB, refX