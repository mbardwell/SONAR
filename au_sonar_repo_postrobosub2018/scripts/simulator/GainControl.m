classdef GainControl < matlab.System
    % SONAR No Pain All Gain
    %
    % This template includes the minimum set of functions required
    % to define a System object with discrete state.

    % Public, tunable properties
    properties
    threshold_constant = 3;
    end

    properties(DiscreteState)
    mem;
    i;
    threshold;
    blockstd;
    ping;
    avg; 
    pinghgt;
    gain; maxgain;
    count;
    end

    % Pre-computed constants
    properties(Access = private)
    usorted; 
    end

    methods(Access = protected)
        function setupImpl(obj)
            % Perform one-time calculations, such as computing constants
              obj.mem = zeros(200,1);
              obj.i = 0;
              obj.threshold = 0;
              obj.blockstd = 0;
              obj.ping = 0; 
              obj.avg = 0; 
              obj.usorted = zeros(256,1); 
              obj.pinghgt = 0;
              obj.gain = 40; obj.maxgain = 1000;
              obj.count = 0;
        end

        function [thresh,stddev,gain,pinghgt] = stepImpl(obj,u)
            % Implement algorithm. Calculate y as a function of input u and
            % discrete states.
            thresh = obj.threshold;
            obj.i = obj.i + 1; step = obj.i; %obj.usorted = zeros(256,1);
            if step < 200; obj.mem(step) = std(u); end % Sample for mean
            if step == 200; obj.threshold = obj.threshold_constant*mean(obj.mem(:)); end % Calculate std baseline
            
            % Ping detection mode
            if step > 200             
                obj.blockstd = std(u); % Determine std of each block
                if obj.blockstd > obj.threshold % Compare to baseline
                    obj.ping = 1;
                    obj.usorted = sort(u, 'descend'); % Find peak values in block
                    obj.pinghgt = mean(obj.usorted(1:5)); % Take mean of first 5 peak values
                    if obj.pinghgt > 1.9 
                        obj.gain = obj.gain/2;
                    elseif obj.pinghgt < 1.5
                        obj.gain = obj.gain*1.8/obj.pinghgt;
                    end
                    obj.count = 0;
                else
                    obj.ping = 0;
                    obj.pinghgt = 0;
                    obj.count = obj.count + 1;
                    if obj.count > 5000; obj.gain = obj.maxgain; end
                end
            end
            stddev = obj.blockstd;
            pinghgt = obj.pinghgt;
            if obj.gain < 1; obj.gain = 1; end
            if obj.gain > 1000; obj.gain = 1000; end
            gain = round(obj.gain);
        end

        function resetImpl(obj)
            % Initialize / reset discrete-state properties
        end
    end
end