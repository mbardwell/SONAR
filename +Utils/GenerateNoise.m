%Based on experimental data, noise does not increase with gain
function [noise] = GenerateNoise(time)
    bias = 512;
    Fs = 500000;
    t = 0:1/Fs:time; %Ping lasts for 4ms
    noise = wgn(1,length(t),1)*0.02*1024+bias; % Noise w/ correction factor    
end