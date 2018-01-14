function [gainout] = GainChanger (signalin, noisefl, currentgain)
    maxsignal = 1000;
    if(max(signalin) > maxsignal)
        gainout = currentgain/2;
    elseif(max(signalin) <= noisefl)
        gainout = currentgain*2;
    end
end