"""

    module ice_plt.py

    Plot sea ice fraction with overlaid wind direction field from MITgcm
    model runs.

    This module makes plots from converted netCDF4 files, which should have
    been converted from the binary .data files from datnetcdf.py

"""

import argparse
import glob
import os

import netCDF4 as nc
import numpy as np
from matplotlib import pyplot as plt

def show_ice(dataset, pngname, cmap = 'Blues'):
    """Make a png figure of ice fraction and velocity field for one timestep.

    Shows a colour plot of variable 'ice_fract', with the ice velocity
    field (taken from 'UICE' and 'VICE') overlaid as a direction field.

    Required Arguments:
     *  dataset:    the netcdf4 Dataset object to plot from
     *  pngname:    filepath to save the png image as.

    Optional Arguments:
     *  cmap:       string specifying the colormap to use (default 'Blues')
    """
    print("Processing file %s" % dataset.filepath())

    X, Y = np.meshgrid(dataset['x'], dataset['y'])

    icefract = np.array(dataset['ice_fract']).reshape(X.shape)
    uice = np.array(dataset['UICE']).reshape(X.shape)
    vice = np.array(dataset['VICE']).reshape(X.shape)

    vmin = 0.2
    vmax = 1

    fig, ax = plt.subplots()
    pcolor = ax.pcolormesh(X, Y, icefract, cmap = cmap, vmin = vmin, vmax = vmax)

    cbar = fig.colorbar(pcolor)
    cbar.set_label('Ice fraction')

    ax.set_xlabel('X [m]')
    ax.set_ylabel('Y [m]')
    ax.set_title('Variable ice_fract from %s' % dataset.filepath())

    iceufield = ax.quiver(X[::2, ::2], Y[::2, ::2], uice[::2, ::2], vice[::2, ::2], angles = 'uv')
    fig.savefig(pngname, dpi = 500)

def show_ice_velo_field(dataset):
    """Make a png figure of ice velocity field for one timestep.

    Shows the ice velocity field as a direction field over a plain
    background (no ice fraction).

    Required Arguments:
     *  datatset:   the netcdf$ Dataset object to plot from
    """
    print("Processing file %s" % dataset.filepath())
    X, Y = np.meshgrid(dataset['x'], dataset['y'])

    uice = np.array(dataset['UICE']).reshape(X.shape)
    vice = np.array(dataset['VICE']).reshape(Y.shape)

    fig, ax = plt.subplots()

    quiverplot = ax.quiver(X, Y, uice, vice, angles = 'uv')

    fig.savefig('quiver_%s.png' % dataset.filepath())


def main():
    """Command line interface to make png figures.

    python ice_plt.py file

    Arguments:
     *  ncfile:   Filepath to the netcdf4 data
     *  pngfile:  Filepath to save the pngs as. Will append the iteration
                    number before the file extension.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('ncfile', help = 'input .nc file to visualize or pattern'
                                       ' to match file names to')
    parser.add_argument('pngfile', help = 'output filepath to save png'
                                         ' image as')
    args = parser.parse_args()
    paths = glob.glob(args.ncfile)
    for file in paths:
        iter = os.path.splitext(file)[0][-10:]
        print(file)
        print(iter)
        data = nc.Dataset(file)
        newpngname = os.path.splitext(args.pngfile)[0] + iter + '.png'
        print(newpngname)
        show_ice(data, newpngname)

if __name__ == '__main__':
    main()
