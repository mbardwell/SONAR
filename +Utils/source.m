function [audible] = source(Simlength, audible, shift, distance, gain)
    for i=1:Simlength % Simlength is in s. At 1 ping/s we get i=1:NoPings
        audible = [audible, Utils.GenerateNoise(1), Utils.GeneratePing(27000,distance,gain)];
    end
    if shift
        Fs = 500000;
        audible = audible(shift*500000:end); 
    end
end