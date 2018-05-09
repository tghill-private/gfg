"""

    module ice_plt_ani.py

    Plot sea ice fraction with overlaid wind direction field from MITgcm
    model runs.

    This module makes animations from converted netCDF4 files, which should have
    been converted from the binary .data files from datnetcdf.py

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

def animate(iters, gifname, namespec = 'output_{iter}.nc',
                vmin = 0.2, vmax = 1, cmap = 'Blues',
                ice_velocity_field = True, stride = 3, scale = 20):
    """Create .gif animation of sea ice fraction from MITgcm .nc files.

    Required Arguments:
     *  iters:  list of iterations to plot. These should match the file names
                of the output_00{iter}.nc files. The iteration numbers are
                automatically zero padded to 10 digits. Can be list of
                ints or list of strings.

     *  gifname:    File name to save the resulting .gif animation as

    Optional Parameters:
     *  namespec = 'output_{iter}.nc': String formatting argument to specify
                                       how the MITgcm filenames are formatted
     *  vmin = 0.2:   Minimum ice_fract value for colour scale
     *  vmax = 1.0:   Maximum ice_fract value for colour scale
     *  cmap = 'Blues':  Colour map for ice_fract
     *  ice_velocity_field = True:  Show a direction field of the ice velocity
                                    field (from UICE and VICE data fields
     *  stride = 3:  Stride length for ice velocity field. Plotting all the
                     datapoints for ice velocity can look too busy.
     *  scale = 20:  Scale for ice velocity field arrow size. A larger
                     scale means smaller arrows; smaller scale means larger
                     arrows.
    """
    #pre-process iters list to make sure they are 10-digit strings
    iters = [str(i).zfill(10) for i in iters]

    # get the grids from the first nc file
    ncdata = _getdataset(iters[0], namespec)
    X, Y = np.meshgrid(np.array(ncdata['x']), np.array(ncdata['y']))

    icefract = np.array(ncdata['ice_fract']).reshape(X.shape)
    filename = ncdata.filepath()

    fig = plt.figure()
    gs = gridspec.GridSpec(1, 1)
    ax = plt.subplot(gs[0, 0])

    pcolor = ax.pcolormesh(X, Y, icefract, cmap = cmap, vmin = vmin, vmax = vmax)

    if ice_velocity_field:
        uice = np.array(ncdata['UICE']).reshape(X.shape)
        vice = np.array(ncdata['VICE']).reshape(X.shape)
        quiverplot = ax.quiver(X[::stride, ::stride], Y[::stride, ::stride],
                                uice[::stride, ::stride], vice[::stride, ::stride],
                                pivot ='mid', scale = scale)

    ax.set_xlabel('X [m]')
    ax.set_ylabel('Y [m]')
    ax.set_title('Variable ice_fract from %s' % filename)
    ncdata.close()

    def animate(iter):
        iterdata = _getdataset(iter, namespec)
        iter_icefract = np.array(iterdata['ice_fract']).reshape(X.shape)
        file = iterdata.filepath()
        ax.set_title('Variable ice_frac from %s' % file)

        # see https://stackoverflow.com/questions/18797175/animation-with-pcolormesh-routine-in-matplotlib-how-do-i-initialize-the-data
        iter_icefract = iter_icefract[:-1, :-1]
        pcolor.set_array(iter_icefract.ravel())

        if ice_velocity_field:
            iter_uice = np.array(iterdata['UICE']).reshape(X.shape)
            iter_vice = np.array(iterdata['VICE']).reshape(X.shape)
            U = iter_uice[::stride, ::stride]
            V = iter_vice[::stride, ::stride]
            quiverplot.set_UVC(U, V)
            iterdata.close()
            return (pcolor, quiverplot)

        iterdata.close()
        return pcolor

    gs.tight_layout(fig)

    anim = animation.FuncAnimation(fig,animate,frames=iters,interval=10000,blit=False,repeat=False)

    cbar = fig.colorbar(pcolor)
    # Then save the gif using ImageMagick writer
    writer = animation.ImageMagickFileWriter(fps = 2.5)
    anim.save(gifname, writer=writer)

if __name__ == "__main__":
    animate([12, 24, 36, 48, 72, 96, 120], 'ice_frac_ice_velocity_field_True.gif',
                ice_velocity_field = True)
