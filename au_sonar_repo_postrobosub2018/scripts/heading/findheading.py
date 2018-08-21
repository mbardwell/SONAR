from signalanalysis import PhaseShiftAnalysis, SignalConditioning, Misc
psamisc = Misc()
import os, numpy as np, matplotlib.pyplot as plt

class FindHeading(object):
    def __init__(self, Fs, hydrophoneA, refY, hydrophoneB, refX, Fc = '27000'):
        self.psa = PhaseShiftAnalysis()
        self.sig = SignalConditioning(Fs, hydrophoneA, refY, hydrophoneB, refX)
        self.complete_flag = False
        self.frequencyok_flag = False
        
    def heading(self, suppress_output = False):
        self.sig.removebias()
        self.sig.normalise()
#        self.sig.cutsignal()
#        self.sig.hamming()
#        self.sig.butter_bandpass_filter(order=5)
#        
#        desired_L = 2000 # for interpolation
#        while (self.sig.L != desired_L):
#            self.sig.interpolate(desired_L/self.sig.L)
#        psamisc.plotsignals(self.sig.signalY, self.sig.refY, self.sig.signalX, self.sig.refX, 'o')
        
        self.frequencyok_flag = self.psa.phasecleanup(self.sig.Fs, self.sig.signalY, self.sig.refY, self.sig.signalX, self.sig.refX)
        if not self.psa.phasedifference(suppress_output):
            return False
        else:
            self.complete_flag = True
#            psamisc.plotfft(self.psa.freq, self.psa.P1, self.psa.ang, self.psa.L)
            return self.psa.heading()
        
class AverageHeading(object):
    def __init__(self, indir, Fs = 1e6):
        self.pings = []
        for root, dirs, filenames in os.walk(indir):
            for f in filenames:
                if self.windowed(indir+f) == True:
                    continue
                hydrophoneA, refY, hydrophoneB, refX = psamisc.extractfile(indir+f)
                fh = FindHeading(Fs, hydrophoneA, refY, hydrophoneB, refX)
                calculated_heading = fh.heading(suppress_output=True)
                
                if calculated_heading is not False:
                    self.pings = np.append(self.pings, calculated_heading)
        print('guess: ', self.guess_heading())
        
    def guess_heading(self):
        minimum_no_signals = 5
        if len(self.pings) < minimum_no_signals:
            print('provide {} more signals'.format(minimum_no_signals-len(self.pings)))
            return False
        else:
            self.std_dev = 100
            while self.std_dev > 15:
                self.outlier_elimination() # run a few times
            return np.mean(self.pings)
        
    def outlier_elimination(self):
        if np.any(self.pings < 0):
            positions = np.argwhere(self.pings < 0)
            self.pings[positions] = self.pings[positions] + 360
        mean = np.mean(self.pings)
        self.std_dev = np.std(self.pings)
        self.pings = np.array([x for x in self.pings if (mean - self.std_dev) < x < (mean + self.std_dev)])
        if np.any(self.pings > 180):
            positions = np.argwhere(self.pings > 180)
            self.pings[positions] = self.pings[positions] - 360
        print(mean, self.std_dev, 'headings:', self.pings)
        
    def windowed(self, filename):
        indir = filename
        Fs = 1e6
        hydrophoneY, refY, hydrophoneX, refX = psamisc.extractfile(indir)
        keys = ['hydrophoneY', 'refY', 'hydrophoneX', 'refX']
        windows = {}
        for key in keys:
            windows[key] = []
        for i in np.arange(5, len(hydrophoneY), 256):
            if len(hydrophoneY) - i < 256:
                continue
            for key in keys:
                if key in windows:
                    if key == keys[0]:
                        windows[key].append(hydrophoneY[i:i+256])
                    if key == keys[1]:
                        windows[key].append(refY[i:i+256])
                    if key == keys[2]:
                        windows[key].append(hydrophoneX[i:i+256])
                    if key == keys[3]:
                        windows[key].append(refY[i:i+256])
    
        shiftYs = []; shiftXs = []
        for i in range(0,len(windows[keys[0]])):
            fh = FindHeading(Fs,windows[keys[0]][i], windows[keys[1]][i], windows[keys[2]][i], windows[keys[3]][i])
            if fh.heading(suppress_output = True) != False:
                shiftYs.append(fh.psa.shiftY)
                shiftXs.append(fh.psa.shiftX)
        if np.all([np.abs(shiftYs - np.mean(shiftYs)) < 50]) and np.all([np.abs(shiftXs - np.mean(shiftXs)) < 50]):
            return False # windows showed reasonable phase shift variation
        return True # windows showed large phase shift variation
    #        psa = PhaseShiftAnalysis()
    #        print('Windowed heading: ', psa.heading(np.mean(shiftXs), np.mean(shiftYs)))
                
    
class DistanceToPinger(object):
    ## initialise class during sonar mission with first heading
    def __init__(self, heading):
        self.heading = [np.deg2rad(heading)]
        self.movedistance = 0.5

    def move(self):
        if self.heading > 0:
            turnangle = -90 - self.heading
        if self.heading < 0:
            turnangle = 90 + self.headings
        ##### turn robot 'turnangle'
        ##### move robot self.movedistance

    ## move x-meters according to move function and take heading again
    ## "height" calculated is approx distance to pinger if you follow heading
    def distance_to_pinger(self, movedistance, heading):
        self.heading.append(np.deg2rad(heading))
        if len(self.heading) > 1:
            sin1 = np.abs(np.sin(self.heading[-1]))
            sin2 = np.abs(np.sin(self.heading[-2]))
            height = movedistance/(sin1 + sin2)
            print(height)
        else:
            print('need 2 headings to calculate')
    
# Example: using FindHeading class
def main():
#    scan('C:/Users/Michael/Downloads/-135/')

#    AverageHeading('C:/Users/Michael/Downloads/transdec/')
    
#    filename = 'C:/Users/Michael/Downloads/July30/1533014612_-90.csv'
#    single(filename)
#    windowed(filename)
    d2p = DistanceToPinger(10)
    d2p.distance_to_pinger(0.5, -10)
    d2p.distance_to_pinger(0.5, 10)

def single(filename):
    indir = filename
    Fs = 1e6
    hydrophoneY, refY, hydrophoneX, refX = psamisc.extractfile(indir)
    fh = FindHeading(Fs, hydrophoneY, refY, hydrophoneX, refX)
    print('Single shot heading:', fh.heading(suppress_output = True))
    
def scan(indir):
    thresh = 30
    Fs = 1e6
    counter = 0; skip_counter = 0
    theIndex = {}
    for root, dirs, filenames in os.walk(indir):
        for f in filenames:
            hydrophoneA, refY, hydrophoneB, refX = psamisc.extractfile(indir+f)
            fh = FindHeading(Fs, hydrophoneA, refY, hydrophoneB, refX)
            calculated_heading = int(fh.heading())
            if not calculated_heading:
                skip_counter += 1
                continue
#            elif windowed(indir+f):
#                skip_counter += 1
#                print('windows showed large phase shift variation')
#                continue
            angle = int((f.split("_")[-1]).split(".")[0])
            if angle in theIndex:
                theIndex[angle].append(calculated_heading)
            else:
                theIndex[angle] = [calculated_heading]
            print('expected: ', angle, 'calculated: ', calculated_heading)
            if (-thresh < angle - calculated_heading < thresh):
                counter += 1; print('counter:', counter)
            elif (angle < 0 and calculated_heading > 0) or (angle > 0 and calculated_heading < 0):
                if (-thresh < angle + calculated_heading < thresh):
                    counter += 1; print('counter:', counter)
    print('% within +/- {} degrees'.format(thresh), counter*100/(len(filenames)-skip_counter), '% bad freq', 100*skip_counter/len(filenames))
    
    for key in theIndex:
        subcount = 0
        for i in theIndex[key]:
            if -thresh < i - key < thresh:
                subcount += 1
            elif (i < 0 and key > 0) or (i > 0 and key < 0):
                if -thresh < i + key < thresh:
                    subcount += 1
        print('Accuracy for angle {} is {}'.format(key, round(100*subcount/len(theIndex[key]))))
        
if __name__ == '__main__':
    main()