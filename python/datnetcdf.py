"""

    Convert MITgcm binary model output to netCDF4 format.

    This script is originally from the fluids wiki
    https://wiki.math.uwaterloo.ca/fluidswiki/index.php?title=NetCDF_Converter

    I have modified it to work with 2D variables (ex. ice_fract), which is
    the conditional statement at line 107.

"""

import MITgcmutils as mgu
import numpy as np
from netCDF4 import Dataset
import glob, sys

# Step 1: Load data

# Extract for a specific list of times
#fields  = ['Rho', 'T']
#indices = ['0000017040']

# Extract for all times
fields  = ['T', 'UICE', 'VICE']
names = glob.glob(fields[0] + '.*.data')
indices = [nm[len(fields[0])+1:-5] for nm in names]

print("Preparing to convert {0:d} outputs to netcdf.".format(len(indices)))

# Manually extract the grids
refdata = mgu.rdmds('T.0000000001')

Nx = refdata.shape[2]
Ny = refdata.shape[1]
Nz = refdata.shape[0]

print("(Nx, Ny, Nz) = ({0:d}, {1:d}, {2:d})".format(Nx, Ny, Nz))

XC = mgu.rdmds('XG')
YC = mgu.rdmds('YG')
RC = mgu.rdmds('RC')

depth = mgu.rdmds('Depth')

myX = np.tile(XC.reshape(1, Ny, Nx), (Nz, 1, 1))
myY = np.tile(YC.reshape(1, Ny, Nx), (Nz, 1, 1))
myZ = np.tile(RC.reshape(Nz, 1, 1), [1, Ny, Nx])

myDepth = np.tile(depth.reshape(1, Ny, Nx), (Nz, 1, 1))

myInds = np.zeros(depth.shape)

# Handle the topography
cntP = 0
cntN = 0
for jj in range(Ny):
    for ii in range(Nx):
        zs = myZ[:,jj,ii]
        myInds[jj,ii] = np.sum(zs >= -depth[jj,ii])

        # Any z points below the topography are mapped to the lowest
        #  above-topography point
        if int(myInds[jj,ii]) < Nz:
            zs[int(myInds[jj,ii]):] = zs[int(myInds[jj,ii])]
        if int(myInds[jj,ii]) == 0:
            cntP += 1
        if int(myInds[jj,ii]) == Nz:
            cntN += 1

        myZ[:,jj,ii] = zs

print("{0:d} of {1:d} points ({2:.3g}%) are purely topographic".format(cntP, Nx*Ny, 100.*cntP/(Nx*Ny)))
print("{0:d} of {1:d} points ({2:.3g}%) have no topography".format(cntN, Nx*Ny, 100.*cntN/(Nx*Ny)))

# Step 2: Create netcdf

for index in indices:
    print("Processing index {0}".format(index))

    # Create file
    fp = Dataset('output_{0}.nc'.format(index), 'w', format='NETCDF4')

    # Create dimension objects
    x_dim = fp.createDimension('x',Nx)
    y_dim = fp.createDimension('y',Ny)
    z_dim = fp.createDimension('z',Nz)
    t_dim = fp.createDimension('time',1)

    # Create and write grids
    x_grid  = fp.createVariable('x',    np.float64, ('x',))
    y_grid  = fp.createVariable('y',    np.float64, ('y',))
    z_grid  = fp.createVariable('z',    np.float64, ('z',))
    zc_grid = fp.createVariable('zc',   np.float64, ('z','y','x'))
    t_grid  = fp.createVariable('time', np.float64, ('time',))

    x_grid[:]      = myX[0,0,:]
    y_grid[:]      = myY[0,:,0]
    z_grid[:]      = np.arange(Nz)
    zc_grid[:,:,:] = myZ
    t_grid[0]      = int(index)

    # Create and write fields
    field_objs = []
    for f in fields:
        data = mgu.rdmds(f + '.' + index)
        if data.ndim == 2:
            f_var = fp.createVariable(f, np.float64, ('y', 'x'))
            f_var[:, :] = data

        else:
            f_var = fp.createVariable(f, np.float64, ('z','y','x'))

            dat_min = 0*np.min(data[myZ >= -myDepth])

            # Screw with the data to make topography work nicely
            for jj in range(Ny):
                for ii in range(Nx):
                    if (int(myInds[jj,ii]) == 0):
                        data[:,jj,ii] = dat_min
                    elif int(myInds[jj,ii]) < Nz:
                        data[int(myInds[jj,ii]):,jj,ii] = data[int(myInds[jj,ii]),jj,ii]

            f_var[:,:,:] = data

    fp.close()
