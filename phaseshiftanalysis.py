import csv
import numpy as np
import matplotlib.pyplot as plt

filename = r"C:\Users\Michael\Documents\SONAR\Data\forphaseshiftanalysis_sampletime2us.csv"


def example():
    ##FFT constants
    Fs = 500000; T = 1/Fs; L = 1100 # L same as in oscdata
    
    ##Signal synthesis
    t = np.arange(0,L)*T
    a = 0.5*np.sin(2*np.pi*27000*t + np.pi/4) # used in examples
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
    a = []; b = []
    with open(filename, 'r') as file:
        dialect = csv.Sniffer().sniff(file.read(1024))
        file.seek(0)
        reader = csv.DictReader(file)
        for row in reader:
            if row['CH1'] == 'Volt':
                continue
            a = np.append(a, float(row['CH1']))
            b = np.append(b, float(row['CH2']))
    file.close()
    
    ##FFT constants
    Fs = 500000; T = 1/Fs; L = int(a.size)
    
    ##Time signal synthesis
    t = np.arange(0,L)*T
    plt.plot(t,a); plt.show()
    
    ##FFT analysis
    sp = np.fft.fft(a) # compute the fast fourier transform of the signal
    P2 = np.abs(sp/L) # compute two sided spectrum
    P1 = P2[1:int((L/2)+1)] # select the single sided spectrum ignoring DC
    P1[2:-1] = 2*P1[2:-1]; # I don't understand this step
    freq = np.fft.fftfreq(L, d=T)
    ang = np.angle(sp)
    plt.plot(freq[0:int(L/2)], P1); plt.show()
    plt.plot(freq, ang, 'o'); plt.show()
    returnangles(1000, Fs, L, ang)    
    return 0

def pilist():
    print('pi/2: ', np.pi/2, "\n", 'pi/3: ', np.pi/3, '\n', 'pi/4: ', np.pi/4)
    
def returnangles(fc, Fs, L, angles):
    index = round(fc/(Fs/L))
    print(angles[index-1], angles[index], angles[index+1]); pilist()

def main():
    oscdata()
#    example()
    return 0;

if __name__ == "__main__":
    main()