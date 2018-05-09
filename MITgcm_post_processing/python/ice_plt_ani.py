"""

    module ice_plt_ani.py

    Plot sea ice fraction with overlaid wind direction field from MITgcm
    model runs.

    This module makes animations from converted netCDF4 files, which should have
    been converted from the binary .data files from datnetcdf.py

"""

"""
import imageio

filenames = ['image%s.png' % str(12*x).zfill(10) for x in list(range(11))]

def main():
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    imageio.mimsave('GIF_MOVIE/movie.gif', images)

if __name__ == "__main__":
    main()
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import gridspec

import netCDF4

def _getdataset(iter, namespec):
    """Helper function to return the netCDF4 Dataset object corresponding
    to iteration iter, with name format namespec
    """
    ncfilename = namespec.format(iter)
    ncdata = netCDF4.Dataset(ncfile, 'r')
    return ncdata

def animate(iters, gifname, namespec = 'output_{iter}.nc', vmin = 0.2, vmax = 1):
    #pre-process iters list to make sure they are 10-digit strings
    iters = [str(i).zfill(1) for i in iters]

    # get the grids from the first nc file
    ncdata = _getdataset(iters[0], namespec)
    X, Y = np.meshgrid(np.array(ncdata['x']), np.array(ncdata['y']))

    icefract = np.array(ncdata['ice_fract']).reshape(X.shape)
    uice = np.array(ncdata['UICE']).reshape(X.shape)
    vice = np.array(ncdata['VICE']).reshape(X.shape)
    ncdata.close()

    fig = plt.figure()
    gs = gridspec.GridSpec(1, 1)
    ax = plt.subplot(gs[0, 0])

    pcolor = ax.pcolormesh(X, Y, icefract, cmap = cmap, vmin = vmin, vmax = vmax)
    quiverplot = ax.quiver(X[::2, ::2], Y[::2, ::2],
                            uice[::2, ::2], vice[::2, ::2], angles = 'uv')
    ###########

    ax.set_xlabel('X [m]')
    ax.set_ylabel('Y [m]')
    ax.set_title('Variable ice_fract from %s' % ncdata.filepath())

    def init():
        """Initialize an empty plot
        """
        pcolor.set_array([])
        quiverplot.set_UVC([], [])
        return pcolor

    def animate(iter):
        iterdata = _getdataset(iter, namespec)
        iter_icefract = np.array(iterdata['ice_frac']).reshape(X.shape)
        iter_uice = np.array(iterdata['UICE']).reshape(X.shape)
        iter_vice = np.array(iterdata['VICE']).reshape(X.shape)
        iterdata.close()

        # see https://stackoverflow.com/questions/18797175/animation-with-pcolormesh-routine-in-matplotlib-how-do-i-initialize-the-data
        iter_icefract = iter_icefract[:-1, :-1]

        pcolor.set_array(iter_icefract.ravel())
        quiverplot.set_UVC( iter_uice[::2, ::2], iter_vice[::2, ::2])
        return (pcolor, quiverplot)

    gs.tight_layout(fig)

    anim = animation.FuncAnimation(fig,animate,frames=iters,interval=50,blit=False,repeat=False)

    # Then save the gif using ImageMagick writer
    writer = animation.ImageMagickFileWriter(fps = 5)
    anim.save(gifname, writer=writer)
