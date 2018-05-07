%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% function timeStr = convertSeconds(seconds, show_days)                   %
%                                                                         %
% Input:                                                                  %
%   seconds: Time in seconds                                              %
%   showDays:  optional logical value; whether or not to include days     %
%              in the format of the time stamp. Default true.             %
%              If false, time stamp may show more than 24 hours. For      %
%              example, 5 days will be '120:00:00'                        %
%                                                                         %
% Output:                                                                %
%   timeStr: time string with format 'days hh:mm:ss' or 'hh:mm:ss'        %
%                                                                         %    
% Written by Wentao Liu, Feb 28, 2009, U of Waterloo                      %
% Refactored by Jonathan Barenboim, September 2016                        %
%                                                                         %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function timeStr = convertSeconds(seconds, showDays)
secondsInDay = 60*60*24;
if ~exist('showDays', 'var')
    showDays = true;
end

if (showDays) 
    days = floor (seconds / secondsInDay);
    seconds = seconds - days * secondsInDay;
end

hours = floor (seconds / 3600);
seconds = seconds - hours * 3600;

minutes = floor (seconds / 60);
seconds = seconds - minutes * 60;

if (showDays)
    format = '%02dD %02d:%02d:%02d';
    timeStr = sprintf(format, days, hours, minutes, seconds);
else
    format = '%02d:%02d:%02d';
    timeStr = sprintf(format, hours, minutes, seconds);
end