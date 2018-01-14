function [ping] = PingIdentification(threshold, block256)
    clc; clear

%     load('Jan05_test4.mat');
%     data = Jan05_test4_02f;
    windowsize = length(block256); offset = 1;



    %% std dev method
    stddev = zeros(length(data),1);
    
    for i=offset:windowsize:length(data)-(windowsize+offset)
        window = data(i:windowsize+i,1);
        stddev(i) = std(window);
    end
    subplot(2,1,1); plot(data(:,1)); title('adc data')
    subplot(2,1,2); plot(stddev); title('standard deviation of 256 sample blocks')
    
    sigma = stddev(stddev > 0);
    Determine standard deviation noise floor for proper thresholding
    threshold = 4*threshold(sigma(1:1000));
    
    pingindex = find(stddev > threshold);
    if(pingindex)
        pingwindows(1) = pingindex(1); j = 2;
        for i=2:length(pingindex)
           if(pingindex(i)-pingindex(i-1) > 5000)
              pingwindows(j) = pingindex(i-1); j = j + 1; %end index of ping
              pingwindows(j) = pingindex(i); j = j + 1; %start index of ping
           end
        end
        pingwindows(j) = pingindex(length(pingindex));
        subplot(2,1,1); vline(pingwindows);
    end
    
    subplot(2,1,2); hline(threshold);
end

%% Addition Method (Scrapped)
%     windowtot = zeros(length(data),1);
% 
%     for i=offset:windowsize:length(data)-(windowsize+offset)
%         window = data(i:windowsize+i,1);
%         windowtot(i) = sum(window); %data
%     end
%     windowtot(windowtot ~= 0) = windowtot(windowtot ~= 0) - min(windowtot(windowtot ~= 0));
% 
%     subplot(2,1,1); plot(data(:,1)); title('adc data')
%     subplot(2,1,2); plot(windowtot); title(['addition of 256 sample blocks with offset ' num2str(offset)])