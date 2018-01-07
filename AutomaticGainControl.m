%Issues
%Identify ping start/stop: done
%Adjust gain to attain best signal
clc; clear

load('data.mat');
data = Jan05_test1_2f;
window_size = 256;

plot(data(:,1))
stddev = zeros(10000,1);
threshold = 100; j =1;

for i=11:length(data)-256
    window = data(i:256+i,1);
    stddev(i) = std(window);
end

pingindexes = find(stddev > threshold);
pingindex = pingindexes(1); k = 2;

for j=2:length(pingindexes)
   if(pingindexes(j)-pingindexes(j-1) > 10000)
       pingindex(k) = pingindexes(j);
       k = k + 1;
   end
end
