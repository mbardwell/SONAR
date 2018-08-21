function [data] = load_Jan05(testNo, url)
% LOAD_JAN05 takes testNo and url of dataset and returns data
%   data is an array of structs
%   structs have fields data(Nx2), distance, pinger_power and gain
%   note this script does not load control data from test 4

if testNo == 5
    F = dir([url 'Jan05_test5.csv']);
else
    if testNo > 0 && testNo < 5
        F = dir([url 'Jan05_test' num2str(testNo) '_*f.csv']);
    else
        disp('Incorrect test number specified')
        return
    end
end

if length(F) <= 0
    disp(['No data found. Please check that data exists at url: ' url]);
    return
end

data_structure.data = [];
data_structure.distance = 0;
data_structure.pinger_power = 0;
data_structure.gain = 0;

% pinger power for various tests
pinger_power = [1/8 1/2 2 2 2];
% gains for various tests
gain = [65.6 27.8 21 0 25];
% test 5 distance in feet
test5_distance = 6;
% gains for test4
test4_gains = [19.4 32.0 44.6 86.6 0 97.1 0 103.5 0 106.8 0 106.8 0 106.8 0 107.7 0 107.7 0 107.7 0 0 0 0 107.7];

data = repmat(data_structure, 1, length(F));
for f_index = 1:length(F)
    if F(f_index).name == "Jan05_test4_control_robotoff.csv"
        continue
    end
    disp(['Processing: ' F(f_index).name]);
    file_url = strcat(url, F(f_index).name);
    if testNo < 5
        distance = str2num(F(f_index).name(13:end-5));
    else
        distance = test5_distance;
    end
    data(f_index).distance = distance;
    data(f_index).pinger_power = pinger_power(testNo);
    if testNo == 4
        data(f_index).gain = test4_gains(distance);
    end
    data(f_index).data = load(file_url);
end

end

