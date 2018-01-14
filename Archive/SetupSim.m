% Plot Transdec pool
function [] = SetupSim()
    r = 20;
    graphic = 10; % in m
    t = linspace(0,2*pi);
    plot(r*cos(graphic*t),r*sin(graphic*t));
    grid on; grid minor
    hold on
end