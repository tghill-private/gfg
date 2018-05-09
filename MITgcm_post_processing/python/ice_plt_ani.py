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
    ncfilename = namespec.format(iter=iter)
    ncdata = netCDF4.Dataset(ncfilename, 'r')
    return ncdata

def animate(iters, gifname, namespec = 'output_{iter}.nc', vmin = 0.2, vmax = 1, cmap = 'Blues'):
    #pre-process iters list to make sure they are 10-digit strings
    iters = [str(i).zfill(10) for i in iters]
    print(iters)

    # get the grids from the first nc file
    ncdata = _getdataset(iters[0], namespec)
    X, Y = np.meshgrid(np.array(ncdata['x']), np.array(ncdata['y']))

    icefract = np.array(ncdata['ice_fract']).reshape(X.shape)
    uice = np.array(ncdata['UICE']).reshape(X.shape)
    vice = np.array(ncdata['VICE']).reshape(X.shape)
    filename = ncdata.filepath()
    ncdata.close()

    fig = plt.figure()
    gs = gridspec.GridSpec(1, 1)
    ax = plt.subplot(gs[0, 0])

    step = 3
    pcolor = ax.pcolormesh(X, Y, icefract, cmap = cmap, vmin = vmin, vmax = vmax)
    quiverplot = ax.quiver(X[::step, ::step], Y[::step, ::step],
                            uice[::step, ::step], vice[::step, ::step],
                            pivot ='mid', scale = 20)
    ###########

    ax.set_xlabel('X [m]')
    ax.set_ylabel('Y [m]')
    ax.set_title('Variable ice_fract from %s' % filename)

    # def init():
    #     """Initialize an empty plot
    #     """
    #     pcolor.set_array([])
    #     quiverplot.set_UVC([], [])
    #     return pcolor, quiverplot

    def animate(iter):
        iterdata = _getdataset(iter, namespec)
        iter_icefract = np.array(iterdata['ice_fract']).reshape(X.shape)
        iter_uice = np.array(iterdata['UICE']).reshape(X.shape)
        iter_vice = np.array(iterdata['VICE']).reshape(X.shape)
        iterdata.close()

        # see https://stackoverflow.com/questions/18797175/animation-with-pcolormesh-routine-in-matplotlib-how-do-i-initialize-the-data
        iter_icefract = iter_icefract[:-1, :-1]

        pcolor.set_array(iter_icefract.ravel())
        U = iter_uice
        V = iter_vice
        U = U[::step, ::step]
        V = V[::step, ::step]
        quiverplot.set_UVC(U, V)
        # quiverplot.set_UVC( iter_uice[::2, ::2].ravel(), iter_vice[::2, ::2].ravel())
        return (pcolor, quiverplot)

    gs.tight_layout(fig)

    anim = animation.FuncAnimation(fig,animate,frames=iters,interval=10000,blit=False,repeat=False)

    # Then save the gif using ImageMagick writer
    writer = animation.ImageMagickFileWriter(fps = 2.5)
    anim.save(gifname, writer=writer)

if __name__ == "__main__":
    animate([0, 12, 24, 36, 48], 'myani.gif')
