import numpy as np
import matplotlib.pyplot as plt

filename = r"C:\Users\Michael\Downloads\June21_phasetest_-45.csv"

class PhaseShiftAnalysis(object):
#    def __init__(self):
        
    def example(self):
        ##FFT constants
        Fs = 500000; T = 1/Fs; L = 50000 # L same as in oscdata
        
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
#    
#    def oscdata():
#        hydrophonea = []; hydrophoneb = []
#        with open(filename, 'r') as file:
#            reader = csv.DictReader(file)
#            for row in reader:
#                if row['CH1'] == 'Volt':
#                    continue
#                hydrophonea = np.append(hydrophonea, float(row['CH1']))
#                hydrophoneb = np.append(hydrophoneb, float(row['CH2']))
#        file.close()
#        
#        ##FFT constants
#        Fs = 500000; T = 1/Fs; L = int(hydrophonea.size)
#        
#        ##Time signal synthesis
#        t = np.arange(0,L)*T; print(t[1])
#        plt.plot(t,hydrophonea,t,hydrophoneb)
#        
#        ##Range selection
#        start = 0.004; end = start + 0.001
#        xcoords = [start, end]
#        signalrange = np.arange(int(start*Fs),int(end*Fs))
#        cut(signalrange, t, hydrophonea, hydrophoneb)
#        for xc in xcoords:
#            plt.axvline(x=xc)
#        plt.show()
#        plt.plot(tcut,acut,tcut,bcut)
#        plt.show()
#        anglea = fftanalysis(acut, Fs)
#        angleb = fftanalysis(bcut, Fs)
#        print("Phase shift: ", (anglea - angleb)*180/np.pi)
#        plt.show()
#        return 0
#    
    def pilist(self):
        print('pi/2: ', np.pi/2, "\n", 'pi/3: ', np.pi/3, '\n', 'pi/4: ', np.pi/4)
#        
    def returnangles(self, angles, freq):
        index = self.binselection(27000, freq)
        print(angles[index[0]])
        #self.pilist()
    
    def binselection(self, fc, freq):
        return np.where(freq == min(freq, key=lambda x:abs(x-fc)))
#        
#    def cut(signalrange, t, hydrophonea, hydrophoneb):
#        global tcut, acut, bcut
#        tcut = t[signalrange]
#        acut = hydrophonea[signalrange]
#        bcut = hydrophoneb[signalrange]
        
    def fftanalysis(self, hydrophone, Fs, fc):
        self.T = 1/Fs
        self.L = hydrophone.size
        ##FFT analysis
        sp = np.fft.fft(hydrophone) # compute the fast fourier transform of the signal
        P2 = np.abs(sp/self.L) # compute two sided spectrum
        P1 = P2[1:int((self.L/2)+1)] # select the single sided spectrum ignoring DC
        P1[2:-1] = 2*P1[2:-1]; # I don't understand this step
        freq = np.fft.fftfreq(self.L, d=self.T)
        ang = np.angle(sp)
        plt.figure(1)
        plt.plot(freq[0:int(self.L/2)], P1)
        plt.xlim([20000, 50000])
        plt.plot()
        plt.figure(2)
        plt.plot(freq[0:int(self.L/2)], ang[0:int(self.L/2)])
        plt.xlim([20000, 50000])
        plt.plot()
        self.returnangles(fc, Fs, self.L, ang)
        return ang[P1.argmax()]
    
def main():
    psa = PhaseShiftAnalysis()
#    oscdata()
    psa.example()
    return 0;

if __name__ == "__main__":
    main()