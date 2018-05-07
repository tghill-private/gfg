function genMovie = MITgcmGenGifMovie(array1, array2, data, label1, label2, mvfile, numFiles, secPerFile, nameVar, nameValue, plotType)
% Author: Emily Tyhurst
% Refactored September 2016 by Jonathan Barenboim

% MITGCMGENGIFMOVIE - Function that generates gif movies given data from
%                     the MITgcm.
%
% input: array1 - the array that will go along the x axis.
%        array2 - the array that will go along the y axis.
%        data   - the data array for the third dimension
%        label1 - the label for the x-axis array
%        label2 - the label for the y-axis array
%        mvfile - the name of the jpg and gif images to be generated
%        numFiles - total number of data files
%        secPerFile - model time in seconds between data dumps
%        nameVar - the label of the data
%        plotType - whether a contour plot (1) or a surface plot (2) is
%                    desired.
%
% See also MITgcmGenMovie_Main
    
    genMovie= 0; 
    
    % option to format time into days. See convertSeconds.m for more info
    showDays = 1;
    
    %sets up the directories for the individual frames
    jpgdir='JPG_IMAGES';
    gifmdir='GIF_MOVIE';
    unix(sprintf('mkdir -p %s',jpgdir));
    unix(sprintf('mkdir -p %s',gifmdir));
    
    minCaxis=min(data(:));
    maxCaxis=max(data(:));
    % handle case of minCaxis = maxCaxis to prevent program end due to error
    if minCaxis == maxCaxis
        minCaxis = minCaxis -1;
        maxCaxis = maxCaxis + 1;
    end
    minCaxis
    maxCaxis
    
    if ~(exist('screenpos','var'))
        screenpos= [ 20 60 900 300];
    end
    
    for nn=1:numFiles
        set(gcf,'position',screenpos);
        if (plotType==1)
            contourf(array1,array2,data(:,:,nn)');
        elseif(plotType==2)
            pcolor(array1,array2,data(:,:,nn)');
            shading interp;
        end
        caxis([minCaxis maxCaxis]);
        colorbar;
        colormap(darkjet);
            
        timeStr=convertSeconds((nn-1) * secPerFile, showDays);
        title([nameVar ' at ' num2str(nameValue) ', at ' timeStr],'FontWeight','bold','FontSize',12);
        xlabel(label1,'FontWeight','bold','FontSize',12)
        ylabel(label2,'FontWeight','bold','FontSize',12)
        drawnow
        
        jpgimg=sprintf('%s/%s.%04d.jpg',jpgdir,mvfile,nn)
        %0.015 is an approximate ratio of pixels and cm, find out the exact one
        set(gcf,'paperposition',[0.25 0.25 0.015*screenpos(3) 0.015*screenpos(4)]);
        print('-djpeg',jpgimg);
    end
    
    %Stitch together movie and optimize the gif file
    fprintf('stitching together the gif...\n');
    unix(sprintf('convert -delay 14 -depth 8 -loop 1 %s/%s.*.jpg %s/%s.gif', jpgdir, mvfile, gifmdir,mvfile));
	unix(sprintf('gifsicle -b -O1 --colors 256 --careful %s/%s.gif', gifmdir, mvfile));
    genMovie=1;
