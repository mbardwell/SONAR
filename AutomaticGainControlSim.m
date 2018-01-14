clc; clear
%% Auri SONAR Controller Setup
maxgain = 250;
gain(1) = maxgain;

%% Place Auri and Pinger
subplot(2,1,1); Utils.ellipse(91, 61, 0, 0, 0, 'r');
locations = [0,0;20,20]; % Auri row 1. Pinger row 2
scatter(locations(:,1), locations(:,2))
distance = Utils.MeasureDistance(locations);

%% Determine noise floor
ADC = [Utils.GenerateNoise(1),Utils.GeneratePing(2700,distance,gain)]; % Read for 1s
nf = mean(ADC);
nfdev = 3*std(ADC); threshold = (4/3)*nfdev;
subplot(2,1,2); plot(ADC); Utils.hline(nfdev+nf); Utils.hline(nf-(nfdev)); % For debug

%% Gain calculation
Util.GainChanger(
