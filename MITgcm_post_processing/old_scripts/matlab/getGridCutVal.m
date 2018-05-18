function gridCutVal = getGridCutVal (cutVal, resolution, n)
    % Jonathan Barenboim, October 2016
    % This function takes a cutVal in meters and returns the grid index to cut at
    % cutVal: the position in meters to take the slice at
    % resolution: a string than can either be a single number, representing a constant
    % 	resolution, or a list like '6*2, 6*1' representing variable resolution
    % n: the total number of points in the axis being cut
    
    gridCutVal = 0;
    
    % if resolution is a list
    if strfind (resolution, '*')
            % Split the string into a list of pairs 'a*b'
            resolutions = strsplit (resolution, ', ');
            for each = resolutions
                   % Split string into a pair [a,b] where a is the number
                   % of grids the resolution applies to and b is the size
                   % of the grid
                   tmp = strsplit (char(each), '*');
                   a = str2num(char(tmp(1)));
                   b = str2num(char(tmp(2)));
                   
                   if cutVal > a * b 
                       cutVal = cutVal - a * b;
                       gridCutVal = gridCutVal + a;
                   else
                       gridCutVal = floor(gridCutVal + cutVal / b) + 1;
                       break
                   end

            end
    % if resolution is a single number        
    else
        resolution = str2num (resolution);
		gridCutVal = floor (cutVal / resolution + 1);
    end
	gridCutVal = min (gridCutVal, n);
                   
                   
