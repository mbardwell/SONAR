clc; clear
NoSets = 25;

for i = 1:NoSets
    x = num2str(i);
    filename = strcat('Jan05_test1_', x, 'f.csv');
    load(filename); % Read in data
end

clear NoSets; clear x; clear filename; clear i;
save('OutFilenametobeChanged.mat'); %Change output filename as necessary