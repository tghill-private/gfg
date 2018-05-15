"""

    Convert MITgcm binary model output to netCDF4 format.

    This script is originally from the fluids wiki
    https://wiki.math.uwaterloo.ca/fluidswiki/index.php?title=NetCDF_Converter

    I have modified it to work with 2D variables (ex. ice_fract), which is
    the conditional statement at line 107.

    See docstring for function convert for how to use as a module function,
    or documentation in the README for how to use the package

"""

import glob, sys, os

import MITgcmutils as mgu
import numpy as np
from netCDF4 import Dataset

_3d_ref_vars = ['T', 'Rho', 'U', 'V', 'W']

def convert(fields, indices = None, verbose = True, overwrite = False):
    """converts binary MITgcm .data files to netCDF4 .nc files.

    Required Arguments:
     *  fields:     List of strings specifying the variables to include
                    in the produced netCDF files. These are the prefixes
                    to the .data files, eg. 'T', 'Rho'.

    Optional Arguments:
     *  indices:    List of length 10 strings specifying the iterations
                    to convert, or None to convert all indices in the
                    directory (default None)
     *  verbose:    Boolean. If True, status is printed to the screen. If
                    False, no output is printed.
    """
    if fields == []:
        return
    if indices:
        indices = [str(i).zfill(10) for i in indices]
    if indices == None:
        names = glob.glob(fields[0] + '.*.data')
        indices = [nm[len(fields[0])+1:-5] for nm in names]
    if verbose:
        print("Preparing to convert {0:d} outputs to netcdf.".format(len(indices)))

    # Manually extract the grids
    for var in _3d_ref_vars:
        if var in fields:
            ref_var = var
    refdatafile = glob.glob('%s*.data'%ref_var)[0]
    refdatafile = os.path.splitext(refdatafile)[0]
    print("Using reference data %s" % refdatafile)
    refdata = mgu.rdmds(refdatafile)

    Nx = refdata.shape[2]
    Ny = refdata.shape[1]
    Nz = refdata.shape[0]

    if verbose:
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

    if verbose:
        print("{0:d} of {1:d} points ({2:.3g}%) are purely topographic".format(cntP, Nx*Ny, 100.*cntP/(Nx*Ny)))
        print("{0:d} of {1:d} points ({2:.3g}%) have no topography".format(cntN, Nx*Ny, 100.*cntN/(Nx*Ny)))

    # Step 2: Create netcdf
    output_files = []
    for index in indices:
        if verbose:
            print("Processing index {0}".format(index))

        # Create file
        outfile = 'output_{0}.nc'.format(index)
        if os.path.exists(outfile):
            if overwrite:
                print("Overwriting file %s" % outfile)
            else:
                print('Skipping file %s' % outfile)
                continue
        output_files.append(outfile)
        fp = Dataset(outfile, 'w', format='NETCDF4')

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
    return output_files
