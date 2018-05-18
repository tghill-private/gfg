%Manager for the MITgcm grid functions

function [x y z] = MITgcmGetGrid(type)
% MITGCMGETGRID Gets the grid coordinates of MITgcm binary output
%   Requires the files 
%   XC.*.data (meta)  XG.*.data (meta)     --to read x-coordinate        
%   YC.*.data (meta)  YG.*.data (meta)     --to read y-coordinate
%   RC.data (meta)    RF.data (meta)       --to read z-coordinate
%
%   'C' as input will parse the *C.*.data files to give a tuple of arrays
%   containing the grid centers [ xc yc zc ]
%
%   'G' as input will parse the *G.*.data files to give a tuple of arrays
%   containing the grid corners [ xg yg zg ]
%
%   See also MITGCMGENMOVIE_MAIN

    switch type
        case 'C'
            [ x y z] = getCenterCoords();
        case 'G'
            [x y z] = getCornerCoords(); 
        otherwise
            error('Incorrect usage, please prompt using C for center coordinates, G for grid corner coordinates');
    end
end

function [xc yc zc] = getCenterCoords()
% GETCENTERCOORDS local function that gets the grid center coordinates.
%
% See also MITGCMGETGRID.


%Load the x coordinate of the cell CENTER. xc_MX is a 2D matrix. Define a
%column vector xc to store the values. size(xc)=(nx_c,1).
xc_MX=rdmds('XC');
xc=zeros(length(xc_MX),1);xc(:,1)=xc_MX(:,1);

%Load the y coordinate of the cell CENTER. yc_MX is a 2D matrix. Define a
%column vector yc to store the values. size(yc)=(ny_c,1).
yc_MX=rdmds('YC');
size(yc_MX);
size_yc = size(yc_MX);
num_yc = size_yc(2);
yc=zeros(num_yc,1);yc(:,1)=yc_MX(1,:);

%Load the z coordinate of the cell CENTER. zc_MX is a 3D matrix with
%size (1,1,nz_c). Define a colume vector zc to store the values.
%size(zc)=(nz_c,1).
zc_MX=rdmds('RC');
zc=zeros(length(zc_MX),1);zc(:,1)=zc_MX(1,1,:);

clear xc_MX yc_MX zc_MX 
end

function [xg yg zg] = getCornerCoords()
% GETCORNERCOORDS local function that gets the grid corner coordinates.
%
% See also MITGCMGETGRID.


%Load the x coordinate of the cell CORNER. xg_MX is a 2D matrix. Define a
%column vector xg to store the values. size(xg)=(nx_g,1) and nx_g = nx_c.
xg_MX=rdmds('XG')
xg=zeros(length(xg_MX),1);xg(:,1)=xg_MX(:,1);

%Load the y coordinate of the cell CORNER. yg_MG is a 2D matrix. Define a
%column vector yg to store the values. size(yg)=(ny_g,1) and ny_g = ny_c.
yg_MX=rdmds('YG')
size(yg_MX);
size_yg = size(yg_MX);
num_yg = size_yg(2);
yg=zeros(num_yg,1);yg(:,1)=yg_MX(1,:);

%Load the z coordinate of the cell CORNER. zg_MX is a 3D matrix with
%size (1,1,nz_g). Define a colume vector zg to store the values.
%size(zg)=(nz_g,1). Be aware of nz_g = nz_c + 1.
zg_MX=rdmds('RF');
zg=zeros(length(zg_MX),1);zg(:,1)=zg_MX(1,1,:);

clear xg_MX yg_MX zg_MX
end
