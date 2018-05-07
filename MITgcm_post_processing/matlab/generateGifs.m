% Jonathan Barenboim
% September 2016
% This script reads the movie settings from generateGifs.txt and creates a
% gif for each of the sets of variables in that file

f = fopen('generateGifs.txt');
gifVars = [];
while true
    line = fgetl(f);
	if ~(ischar(line))
		break
	end

    % skip comments
    if line(1) == '#'
        continue
    % An ampersand seperates sets of variables. Initialize the variables and generate the gif

    elseif line(1) == '&'
        eval(gifVars);
        fprintf (['generating gif with cut_var = ' cut_var ', cut_val = ' num2str(cut_val) ', name_var = ' name_var ', movie_name = ' movie_name]);
        TwoDimensionalGif(cut_var, cut_val, name_var, movie_name)
        gifVars = [];
    % append the variable to the string to be executed
    else 
        gifVars = [gifVars line ', '];
    end

end
    
    
