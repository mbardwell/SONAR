clc; clear
NoSets = 25;

for i = 1:NoSets
    x = num2str(i);
    if i < 10
        x = strcat('0',x);
    end
    filename = strcat('Jan05_test4_', x, 'f.csv');
    
    if exist(filename, 'file') == 0
      % File does not exist
      % Skip to bottom of loop and continue with the loop
      continue;
    end
    load(filename); % Read in datas
end

clear NoSets; clear x; clear filename; clear i;
save('OutputFilename.mat'); %Change output filename as necessary