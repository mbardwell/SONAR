import csv
import numpy as np
import matplotlib.pyplot as plt

filename = r"C:\Users\Michael\Downloads\June21_phasetest_-45.csv"

def example():
    ##FFT constants
    Fs = 500000; T = 1/Fs; L = 1100 # L same as in oscdata
    
    ##Signal synthesis
    t = np.arange(0,L)*T
    a = 0.5*np.sin(2*np.pi*27000*t + np.pi/3) # used in examples
    plt.plot(t[0:int(L/5)],a[0:int(L/5)]); plt.show()
    
    ##FFT analysis
    sp = np.fft.fft(a) # compute the fast fourier transform of the signal
    P2 = np.abs(sp/L) # compute two sided spectrum
    P1 = P2[1:int((L/2)+1)] # select the single sided spectrum ignoring DC
    P1[2:-1] = 2*P1[2:-1]; # I don't understand this step
    freq = np.fft.fftfreq(L, d=T)
    ang = np.angle(sp)
    plt.plot(freq[0:int(L/2)], P1); plt.show()
    plt.plot(freq, ang, 'o'); plt.show()
    returnangles(27000, Fs, L, ang)    
    return 0

def oscdata():
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
    Fs = 500000; T = 1/Fs; L = int(hydrophonea.size)
    
    ##Time signal synthesis
    t = np.arange(0,L)*T; print(t[1])
    plt.plot(t,hydrophonea,t,hydrophoneb)
    
    ##Range selection
    start = 0.004; end = start + 0.001
    xcoords = [start, end]
    signalrange = np.arange(int(start*Fs),int(end*Fs))
    cut(signalrange, t, hydrophonea, hydrophoneb)
    for xc in xcoords:
        plt.axvline(x=xc)
    plt.show()
    plt.plot(tcut,acut,tcut,bcut)
    plt.show()
    anglea = fftanalysis(acut, Fs)
    angleb = fftanalysis(bcut, Fs)
    print("Phase shift: ", (anglea - angleb)*180/np.pi)
    plt.show()
    return 0

def pilist():
    print('pi/2: ', np.pi/2, "\n", 'pi/3: ', np.pi/3, '\n', 'pi/4: ', np.pi/4)
    
def returnangles(fc, Fs, L, angles):
    index = round(fc/(Fs/L))
    print(angles[index-1], angles[index], angles[index+1]); pilist()
    
def cut(signalrange, t, hydrophonea, hydrophoneb):
    global tcut, acut, bcut
    tcut = t[signalrange]
    acut = hydrophonea[signalrange]
    bcut = hydrophoneb[signalrange]
    
def fftanalysis(hydrophone, Fs):
    T = 1/Fs; L = hydrophone.size
    ##FFT analysis
    sp = np.fft.fft(hydrophone) # compute the fast fourier transform of the signal
    P2 = np.abs(sp/L) # compute two sided spectrum
    P1 = P2[1:int((L/2)+1)] # select the single sided spectrum ignoring DC
    P1[2:-1] = 2*P1[2:-1]; # I don't understand this step
    freq = np.fft.fftfreq(L, d=T)
    ang = np.angle(sp)
    plt.figure(1)
    plt.plot(freq[0:int(L/2)], P1)
    plt.xlim([20000, 30000])
    plt.figure(2)
    plt.plot(freq[0:int(L/2)], ang[0:int(L/2)])
    plt.xlim([20000, 30000])
    returnangles(1000, Fs, L, ang)
    return ang[P1.argmax()]

def main():
    oscdata()
#    example()
    return 0;

if __name__ == "__main__":
    main()