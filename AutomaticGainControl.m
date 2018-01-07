%Issues
%Identify ping start: done
%Identify ping stop: Cant just do start+2500, needs to be programmed
%Adjust gain to attain best signal
clc; clear

load('data.mat');
data = Jan05_test1_6f;
windowsize = 256;
stddev = zeros(length(data),1);

for i=1:windowsize:length(data)-windowsize
    window = data(i:windowsize+i,1);
    stddev(i) = std(window);
end
subplot(2,1,1); plot(data(:,1)); title('adc data')
subplot(2,1,2); plot(stddev); title('standard deviation of 256 sample blocks')

sigma = stddev(stddev > 0);
%Determine standard deviation noise floor for proper thresholding
threshold = 4*mean(sigma(1:1000));

pingindex = find(stddev > threshold);
pingwindows(1) = pingindex(1); j = 2;
for i=2:length(pingindex)
   if(pingindex(i)-pingindex(i-1) > 5000)
      pingwindows(j) = pingindex(i-1); j = j + 1; %end index of ping
      pingwindows(j) = pingindex(i); j = j + 1; %start index of ping
   end
end
pingwindows(j) = pingindex(length(pingindex));

subplot(2,1,1); vline(pingwindows);
subplot(2,1,2); hline(threshold);