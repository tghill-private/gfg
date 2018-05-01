%% setting and accuracy
ieee='b';accuracy='real*8';    % store big-endian double precision
%% Grid parameters
nx = 200;
ny = 1;
nz = 40;
%% Grid Resolution 
dx = 25;
dy = 100;
% Split the domain 
T = ones(nx,ny,nz)*4.0;
T2 = ones(nx/4,ny,nz)*14;
T(1:nx/4, :,:)=T2;
       T(1,1,:)
       fprintf('min of T = %f\n',min(min(min(T))) )
       fprintf('max of T = %f\n',max(max(max(T))) )
fid=fopen('initial_temp.bin','w',ieee); fwrite(fid,T,accuracy); fclose(fid);
