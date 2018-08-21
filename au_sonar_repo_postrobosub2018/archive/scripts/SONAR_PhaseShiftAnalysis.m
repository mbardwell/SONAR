%%%%%%%%SONAR Data Analysis%%%%%%%%
%https://www.mathworks.com/help/signal/ref/designfilt.html
%https://www.mathworks.com/help/signal/ref/xcorr.html
clear; clc; %clf;                       %Clear workspace
titlestring = '-3.048m_7.62m_parallel_1.csv';
data = xlsread(titlestring);            %Read data
% data(:,1) = data(:,1)+abs(data(1,1));
side = 1;                               %1 = +x axis, -1 = -x axis
dist_hydrophones = 0.014;               %HP's are max 22mm apart. 14mm mean 

%%%%%%%%Normalize data%%%%%%%%
normdata(:,1) = data(:,1);
for j=2:min(size(data))
normdata(:,j) = data(:,j)/max(data(:,j));
end

Fs = 500000;                            %Sampling frequency in Hz -- this must be what you sampled at
T = 1/Fs;                               %Sampling period
L = length(data);                       %Number of samples
t = (0:L-1)*T;                          %Time vector in s

%%%%%%%%Digital bandpass filter%%%%%%%%
bpFilt = designfilt('bandpassfir','FilterOrder',20, ...
        'CutoffFrequency1',20000,'CutoffFrequency2',50000, ...
        'SampleRate',Fs);
fvtool(bpFilt)
data(:,2) = filter(bpFilt,data(:,2));
data(:,3) = filter(bpFilt,data(:,3));

%%%%%%%%Cross correlation%%%%%%%%
[r,lag] = xcorr(data(:,3),data(:,2));
[~,I] = max(abs(r));
lagDiff = lag(I);
timeDiff = lagDiff/Fs; 
disp(timeDiff)

if lag ~= 0
    subplot(3,1,3)
    plot(lag,r)
    a3 = gca;
    a3.XTick = sort([-3000:1000:3000 lagDiff]);
end

%%%%%%%%Plot normalized time domain signal%%%%%%%%
subplot(3,1,1)
plot(1000000*t(1:length(data)),normdata(:,2),'-',1000000*t(1:length(data)),normdata(:,3),'--')
title(titlestring)
xlabel('t (microseconds)')
ylabel('S(t)')
axis([0 1000000*t(length(data)) -1.1 1.1])
legend('Hydrophone 1','Reference')

%%%%%%%%Compute FFT of signal%%%%%%%%
for i=1:((min(size(data)))-1)                   %Iterate over no. voltage samples
    Y(:,i) = fft(data(:,i+1));                  %FFT function
    P2(:,i) = abs(Y(:,i)/L);
    P1(:,i) = P2(1:L/2+1,i);
    P1(2:end-1,i) = 2*P1(2:end-1,i);
    dbmV(:,i) = 20*log10(P1(:,i)/0.001);
    
    f = Fs*(0:(L/2))/L;
    fc(:,i) = f(P1(:,i)==max(P1(:,i)));         %Identify centre frequency
end

if fc(:,1) ~= fc(:,2)
    disp('ERROR: centre frequencies do not match - please check your data');
else
    Tc = 1/fc(:,1);                             %Calculate period (the time it takes to complete a cycle) of fc
    WL = 1484/fc(:,1);                          %The distance sound travels during one period is the wavelength
end

%%%%%%%%Plot FFT%%%%%%%%
subplot(3,1,2)
plot(f,dbmV)
title('Single-Sided Amplitude Spectrum of S(t)')
xlabel('f (Hz)')
ylabel('dbmV')                                  %Ratio of signal to 1mV
axis([0 50000 -50 20])
legend('show')

%%%%%%%%Peak hunting%%%%%%%%
numberofpeaks = L*T/Tc;

for n=2:min(size(normdata))
    m=1; klast=1;                           %Initialize klast
    for k=floor(length(t)/numberofpeaks):floor(length(t)/numberofpeaks):length(t)
        peakvalue(m,n-1) = max(normdata(klast:k,n));                                %Find peak values
        peakindex(m,n-1) = find(normdata(klast:k,n)==peakvalue(m,n-1),1)+(klast-1); %Find peak index values
        klast = k+5; m=m+1;
    end
end
peakindex(:,3) = normdata([peakindex(:,1)],1);
peakindex(:,4) = normdata([peakindex(:,2)],1);

%%%%%%%%Finding time difference%%%%%%%%
timediff(:,1) = side*(normdata([peakindex(:,1)],1)-normdata([peakindex(:,2)],1));