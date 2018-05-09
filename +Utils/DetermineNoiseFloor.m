% Determine noise floor

function [nf, nfdev] = DetermineNoiseFloor(ADC)
    nf = mean(ADC(:));
    nfdev = 5*std(ADC(:)); % Over 99.99% within range
%     subplot(2,1,2); plot(ADC(:)); Utils.hline(nfdev+nf); Utils.hline(nf-(nfdev)); % For debug
end