%This program reads the gauge data to visualize the BCs
%Jonathan Varkovitzky
%May 12, 2011

close all
clear all
clc

bc = textread('fdbk3abc.txt');

t = bc(:,1)-258;
posit = bc(:,2);

plot(t,posit,'b')
title('Data From fdbk3abc.txt')
xlabel('time (s)')
ylabel('Amplitude (m)')
saveas(figure(1),'bcPlot.jpg')