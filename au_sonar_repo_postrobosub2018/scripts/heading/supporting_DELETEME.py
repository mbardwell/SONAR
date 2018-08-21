import matplotlib.pyplot as plt
import numpy as np

def check(xpoints, ypoints):
    L = np.sqrt(np.square(ypoints[1]-ypoints[0]) + np.square(xpoints[0]))
    if L != 15:
        print('bad L', L)
        
def distanceto(i, px, py, h1x, h1y, h2x, h2y):
    plt.plot(px, py, 'o')
    d1 = np.sqrt(np.square(h1x-px) + np.square(h1y-py))/1000 # in m
    d2 = np.sqrt(np.square(h2x-px) + np.square(h2y-py))/1000 # in m
#    print(d2 - d1)
    phaseshift(i, 27000, d2 - d1)

def phaseshift(i, fc, d):
    vwater = 1484
    timediff = d/vwater
    if timediff < 0 or timediff == 0:
        phase = -60 - (360*fc*timediff * 90/120)
    else:
        phase = -60 - (360*fc*timediff * 90/120)
    print(i, phase)

x = np.linspace(0,1,100) # cm's
a = 15; R = a/np.sqrt(3); r = R / 2
xpoints = [-7.5, 0, 7.5] # hydrophones
ypoints = [-r, R, -r]
check(xpoints, ypoints)

xsin = np.linspace(xpoints[0], 8, 20)
ysin = np.tan(np.deg2rad(30))*xsin
xsinleft = np.linspace(xpoints[2], -8, 20)
ysinleft = np.tan(np.deg2rad(30))*xsin
xdownsin = np.zeros(20)
ydownsin = np.linspace(9, -7, 20)


for i in np.arange(0, 45):
    px = np.linspace(0, -10, 18)
    py = -np.tan(np.deg2rad(i))*px
    distanceto(i-90, px[-1:], py[-1:], xpoints[0], ypoints[0], xpoints[1], ypoints[1])
plt.plot(xpoints, ypoints, 'o', xsin, ysin, xdownsin, ydownsin, xsinleft, ysinleft)
