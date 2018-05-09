function [adc] = ADCread(block, distance)
    adc = block./distance^2;
end