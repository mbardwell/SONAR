import csv
import numpy as np
import matplotlib.pyplot as plt

filename = r"C:\Users\Michael\Documents\SONAR\Data\forphaseshiftanalysis_sampletime2us.csv"


def example():
    ##FFT constants
    Fs = 500000; T = 1/Fs; L = 1100 # L same as in oscdata
    
    ##Signal synthesis
    t = np.arange(0,L)*T
    a = 0.5*np.sin(2*np.pi*27000*t + np.pi) # used in examples
    plt.plot(t,a); plt.show()
    
    ##FFT analysis
    sp = np.fft.fft(a) # compute the fast fourier transform of the signal
    P2 = np.abs(sp/L) # compute two sided spectrum
    P1 = P2[1:int((L/2)+1)] # select the single sided spectrum ignoring DC
    P1[2:-1] = 2*P1[2:-1]; # I don't understand this step
    freq = np.fft.fftfreq(L, d=T)
    ang = np.angle(P1)
    plt.plot(freq[0:int(L/2)], P1); plt.show()
    plt.plot(freq[0:ang.size], ang); plt.show()
    return 0

def oscdata():
    a = []; b = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            a = np.append(a, float(row['CH1']))
            b = np.append(b, float(row['CH2']))
    file.close()
    
    ##FFT constants
    Fs = 500000; T = 1/Fs; L = int(a.size)
    
    ##Time signal synthesis
    t = np.arange(0,L)*T # put t in radians
    plt.plot(t,a); plt.show()
    
    ##FFT analysis
    sp = np.fft.fft(a) # compute the fast fourier transform of the signal
    P2 = np.abs(sp/L) # compute two sided spectrum
    P1 = P2[1:int((L/2)+1)] # select the single sided spectrum ignoring DC
    P1[2:-1] = 2*P1[2:-1]; # I don't understand this step
    freq = np.fft.fftfreq(L, d=T)
    plt.plot(freq[0:int(L/2)], P1); plt.show()
    return 0

def main():
    oscdata()
#    example()
    return 0;

if __name__ == "__main__":
    main()