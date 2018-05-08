"""

    data processing for the offline seaice verification example

    This should act as a prototype for some actual analysis

"""

import argparse
import glob

import netCDF4 as nc
import numpy as np
from matplotlib import pyplot as plt

def show_ice(dataset):
    print("Processing file %s" % dataset.filepath())

    X, Y = np.meshgrid(dataset['x'], dataset['y'])

    icefract = np.array(dataset['ice_fract']).reshape(X.shape)
    uice = np.array(dataset['UICE']).reshape(X.shape)
    vice = np.array(dataset['VICE']).reshape(X.shape)

    vmin = 0.2
    vmax = 1

    fig, ax = plt.subplots()
    pcolor = ax.pcolormesh(X, Y, icefract, cmap = 'Blues', vmin = vmin, vmax = vmax)

    cbar = fig.colorbar(pcolor)
    cbar.set_label('Ice fraction')

    ax.set_xlabel('X [m]')
    ax.set_ylabel('Y [m]')
    ax.set_title('Variable ice_fract from %s' % dataset.filepath())

    iceufield = ax.quiver(X[::2, ::2], Y[::2, ::2], uice[::2, ::2], vice[::2, ::2], angles = 'uv')
    fig.savefig('img_%s.png' % dataset.filepath(), dpi = 500)

def show_icevelo(dataset):
    print("Processing file %s" % dataset.filepath())
    X, Y = np.meshgrid(dataset['x'], dataset['y'])

    uice = np.array(dataset['UICE']).reshape(X.shape)
    vice = np.array(dataset['VICE']).reshape(Y.shape)

    fig, ax = plt.subplots()

    quiverplot = ax.quiver(X, Y, uice, vice, angles = 'uv')

    fig.savefig('quiver_%s.png' % dataset.filepath())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help = 'input .nc file to visualize')
    args = parser.parse_args()
    paths = glob.glob(args.file)
    for file in paths:
        data = nc.Dataset(file)
        show_ice(data)

if __name__ == '__main__':
    main()
