"""
    vis.py

    Python script for visualizing MIT gcm model output.

    Currently set to create pseudo-color plot of surface temperature for
    a single netCDF4 input file


    Takes the input .nc file as its only command line argument
"""


import argparse

import netCDF4
import numpy as np
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

    Tslice = np.ma.masked_less_equal(Tslice, 11.001)
    pcolor = ax.imshow(Tslice, vmin = 11, vmax = 13.5,
                interpolation = 'bilinear', origin = 'lower', cmap = 'Blues',
                extent = (X[0]/1000., X[-1]/1000., Y[0]/1000., Y[-1]/1000.))

    ax.set_xlabel('x [km]')
    ax.set_ylabel('y [km]')


    fig.colorbar(pcolor)

    fig.savefig('MITgcmpyvis.png',dpi = 500)


def main():
    """Setup command line interface, open file, and call plot functions"""
    parser = argparse.ArgumentParser()
    parser.add_argument("file",help = "netCDF4 file to visualize")
    args = parser.parse_args()

    print("Visualizing file %s" % args.file)

    # open data in read mode
    data = netCDF4.Dataset(args.file, 'r')

    surf_2d_slice(data)

if __name__== "__main__":
    main()
