% Goal: To simulate gain control 
% Assumes we can't change gain during the ping cycle
% Steps: 
% Model pinger as unidirectional power output

clc; clear
simlength = 5; % Length of simulation in seconds
%% Auri SONAR Controller Setup
maxgain = 250;
gain(1:20) = maxgain; counter = 0;
block = 256;
Fs = 500000;
bias = 512;

%% Place Auri and Pinger
subplot(2,1,1); Utils.ellipse(91, 61, 0, 0, 0, 'r');
aurix = 0;
locations = [aurix,0;20,0]; % Auri row 1. Pinger row 2
scatter(locations(:,1), locations(:,2))
distance(1:20) = Utils.MeasureDistance(locations); d = 1;
pingerADCvalue = Utils.source(simlength,[],0,distance(1),gain(1));

pru = Utils.blocks(pingerADCvalue);
[nf, nfdev] = Utils.DetermineNoiseFloor(pru(1:20)); % 

for i=21:length(pru)
   if sum(pru(i,:) > nf + nfdev) > 5 % Ping detected
      counter = 0; % Reset ping detection counter
      if max(pru(i,:)) > 1000
          pru(i+1:end) = pru(i+1:end)/2; gain(i) = gain(i-1)/2;
      else
          aurix = aurix + 1; % Move auri towards pinger
      end
   end
   
   if counter > 1953
      pru(i+1:end) = pru(i+1:end)*2; gain(i) = gain(i-1)*2;
   end
   gain(i) = gain(i-1);
   location = [aurix,0;20,0];
   distance(i) = Utils.MeasureDistance(locations);
end






%% BS
% blockc = 1; pruc = 1; adc = zeros(length(sounds),1); flag = 0; pings = [];
% for i=1:simlength*Fs % 1 iter of i = 1/Fs = 0.000002s
%     adc(i) = sounds(i);
%     if rem(i,block) == 0; pru(:,pruc) = adc(i+1-block:i); pruc = pruc + 1; end
%     if i == 5000; [nf, nfdev] = Utils.DetermineNoiseFloor(adc(1:i)); end% 0.01s of data
%     if i > 5000    
%         if adc(i) > nf+nfdev && not(flag); flag = flag + 1; end
%         if flag > 5 % Make sure we hit a ping and not noise
%             pings = [pings, pru(:,flag)];
%             flag = 0;
%         end
% %         if flag; try ping = pru(:,pruc+1); catch; end; end
%     end
% end
% 
% function [] = gc()
% 
% end