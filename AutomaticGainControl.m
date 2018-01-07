%Issues
%Identify ping start: done
%Identify ping stop: Cant just do start+2500, needs to be programmed
%Adjust gain to attain best signal
clc; clear

load('data.mat');
data = Jan05_test1_4f;
window_size = 256;

stddev = zeros(10000,1);

for i=11:length(data)-256
    window = data(i:256+i,1);
    stddev(i) = std(window);
end
subplot(2,1,1); plot(data(:,1))
subplot(2,1,2); plot(stddev);

threshold = max(stddev) - 10*mean(stddev);
pingindexes = find(stddev > threshold);
pingindex = [pingindexes(1), pingindexes(2500)]; k = 3;

for j=2501:length(pingindexes)
   if(pingindexes(j)-pingindexes(j-1) > 10000)
       pingindex(k) = pingindexes(j);
       k = k + 1;
       pingindex(k) = pingindexes(j+2500);
       k = k + 1;
   end
end

vline(pingindex);