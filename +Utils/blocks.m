function [chopped_pinger] = blocks(pinger)
    blocks = 256;
    chopped_pinger = zeros(ceil(length(pinger)/256),blocks);
    chopped_pinger(1,:) = pinger(1:256);
    for i=1:ceil(length(pinger)/256)-2
       chopped_pinger(i,:) = pinger(i*blocks+1:(i+1)*blocks);
    end
end