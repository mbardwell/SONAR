#http://playground.arduino.cc/interfacing/python
import matplotlib.pyplot as plt
import numpy as np

sample = 250000; Fs = 250000; samplingTime = sample*1000/Fs
xcorr=[None]
i=0
while i < 10:
    weightA = [0.1,1,0.1]; freqA = [5,30,100]*1000; thetaA = 0; thetaB = np.pi*i/180
    x = np.arange(sample)/Fs

    reference = weightA[0]*np.sin(2*np.pi*freqA[0]*x+thetaA)+weightA[1]*np.sin(2*np.pi*freqA[1]*x+thetaA)+weightA[2]*np.sin(2*np.pi*freqA[2]*x+thetaA)
    signalA = weightA[0]*np.sin(2*np.pi*freqA[0]*x+thetaB)+weightA[1]*np.sin(2*np.pi*freqA[1]*x+thetaB)+weightA[2]*np.sin(2*np.pi*freqA[2]*x+thetaB)

    reference = reference/max(reference)
    signalA = signalA/max(signalA)

    xcorr.append(np.correlate(reference, signalA)); print(xcorr)
    i=i+1

plt.figure(1)
plt.subplot(211)
plt.plot(x,reference, 'k', x, signalA, 'b')
plt.xlabel('time(ms)')
plt.ylabel('voltage(V)')

plt.subplot(212)
plt.plot(np.arange(i+1),xcorr,'k')
plt.xlabel('i')
plt.ylabel('correlation value')
plt.show()