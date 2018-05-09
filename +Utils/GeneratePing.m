% Generates 4ms worth of ping signal at specified freq and distance
% Biased to 512 with saturated max at 1024
function [ping] = GeneratePing(frequency, distance, gain)
    PingerPower = 2; %Pinger power in watts
    vhigh = 1024; vlow = 0; bias = 512;
    Power = PingerPower*vhigh/distance^2; % Drops as a function of 1/r^2
    Fs = 500000; % Sampling frequency
    t = 0:1/Fs:0.004; %Ping lasts for 4ms
    ping = Power * gain * sin(2*pi*frequency*t) + bias;
    for i=1:length(ping)
        if (ping(i) > vhigh)
            ping(i) = vhigh;
        elseif (ping(i) < vlow)
            ping(i) = vlow;
        end
    end
end