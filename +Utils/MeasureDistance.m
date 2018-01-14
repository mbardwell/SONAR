function [distance] = MeasureDistance(locations)
    aurix = locations(1,1); auriy = locations(1,2);
    pingerx = locations(2,1); pingery = locations(2,2);
    
    x = (pingerx - aurix)^2;
    y = (pingery - auriy)^2;
    distance = sqrt(x+y);
end