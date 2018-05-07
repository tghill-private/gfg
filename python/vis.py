"""
    vis.py

    Python script for visualizing MIT gcm model output.

    Currently set to create pseudo-color plot of surface temperature for
    a single netCDF4 input file


    Takes the input .nc file as its only command line argument
"""


import argparse
import os

import netCDF4
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

def surf_2d_slice(data):
    """Plots a pseudo-color plot of surface temperature for the given data.

    Input:
        *   data: a netCDF4 Dataset

    Output:
        *   Saves png pseudocolor plot of surface temperature as MITgcmpyvis.png
    """
    X = np.array(data['x'])
    Y = np.array(data['y'])
    Z = np.array(data['z'])

    Xgrid, Ygrid = np.meshgrid(X,Y)
    zlevel = Z[0]

    Tslice = np.array(data['T'][0,:, :])

    fig, ax = plt.subplots()

    # Tslice = np.ma.masked_less_equal(Tslice, 11.001)

    pcolor = ax.pcolormesh(Xgrid, Ygrid, Tslice, vmin = 11, vmax = 13.5, cmap = 'Blues')

    ax.set_xlabel('x [km]')
    ax.set_ylabel('y [km]')

    ax.set_title("T:%s at z = %s" % (os.path.split(data.filepath())[1], zlevel))


    fig.colorbar(pcolor)

    fig.savefig('MITgcmpyvis.png',dpi = 500)

def xz_slice(data, index):
    """Plot a pseudo-color plot of temperature in the xz-plane.

    Input:
        *   data: a netCDF4 Dataset
        *   index: which y index to slice at

    Output:
        *   Saves png pseudo-color plot of temperature as MITgcmxz.png
    """
    X = np.array(data['x'])
    Y = np.array(data['y'])
    Z = np.array(data['z'])

    Tslice = np.array(data['T'][:, index, :])
    print(Tslice.shape)

    Xgrid, Zgrid = np.meshgrid(X, Z)
    ylevel = Y[index]
    fig, ax = plt.subplots()
    # Tslice = np.ma.masked_less_equal(Tslice, 11.001)
    pcolor = ax.pcolormesh(Xgrid, Zgrid, Tslice, vmin = 11, vmax = 13.5, cmap = 'Blues')

    ax.set_xlabel('x [km]')
    ax.set_ylabel('z [m]')
    ax.set_title("T:%s at y = %s" % (os.path.split(data.filepath())[1], ylevel))


    fig.colorbar(pcolor)

    fig.savefig('MITgcmxz.png',dpi = 500)

def yz_slice(data, index):
    """Plot a pseudo-color plot of temperature in the xz-plane.

    Input:
        *   data: a netCDF4 Dataset
        *   index: which y index to slice at

    Output:
        *   Saves png pseudo-color plot of temperature as MITgcmxz.png
    """
    X = np.array(data['x'])
    Y = np.array(data['y'])
    Z = np.array(data['z'])
    print(Z)

    Tslice = np.array(data['T'][:, :, index])
    print(Tslice.shape)

    Ygrid, Zgrid = np.meshgrid(Y, Z)
    xlevel = X[index]
    fig, ax = plt.subplots()
    # Tslice = np.ma.masked_less_equal(Tslice, 11.001)
    pcolor = ax.pcolormesh(Ygrid, Zgrid, Tslice, vmin = 11, vmax = 13.5, cmap = 'Blues')

    ax.invert_yaxis()
    ax.set_xlabel('y [km]')
    ax.set_ylabel('z [m]')
    ax.set_title("T:%s at x = %s" % (os.path.split(data.filepath())[1], xlevel))


    fig.colorbar(pcolor)

    fig.savefig('MITgcmyz.png',dpi = 500)

def main():
    """Setup command line interface, open file, and call plot functions"""
    parser = argparse.ArgumentParser()
    parser.add_argument("file",help = "netCDF4 file to visualize")
    args = parser.parse_args()

    print("Visualizing file %s" % args.file)

    # open data in read mode
    data = netCDF4.Dataset(args.file, 'r')
    # surf_2d_slice(data)
    yz_slice(data, 50)

if __name__== "__main__":
    main()
