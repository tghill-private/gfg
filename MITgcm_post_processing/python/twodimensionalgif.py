"""

    module twodimensionalgif.py

    Plot sea ice fraction with overlaid wind direction field from MITgcm
    model runs.

    This module makes animations from converted netCDF4 files, which should have
    been converted from the binary .data files from datnetcdf.py

"""

import os

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import gridspec

import netCDF4

defaults = {    'vmin':                 0.2,
                'vmax':                 1.0,
                'ice_velocity_field':   True,
                'image_folder_name':    'PNG_IMAGES',
                'gif_folder_name':      'GIF_MOVIE',
                'cmap':                 'Blues',
                'dpi':                  200,
                'stride':               3,
                'scale':                20,
                'namespec':             'output_{iter}.nc',
                'image_name':           'still_.png'
            }


def twodimensionalgif(gif_args):
    var = gif_args['var']
    iters = gif_args['iters']
    gifname = gif_args['movie_name']
    kwargs = {}
    for key, val in defaults:
        if key in gif_args:
            kwargs[key] = gif_args[key]
        else:
            kwargs[key] = defaults[key]
    animate(var, iters, gifname, pngname, kwargs)

def _getdataset(iter, namespec):
    """Helper function to return the netCDF4 Dataset object corresponding
    to iteration iter, with name format namespec
    """
    ncfilename = namespec.format(iter=iter)
    ncdata = netCDF4.Dataset(ncfilename, 'r')
    return ncdata

def _getstillname(iter, pngname):
    """Helper function to name the individual png frames with the iteration
    """
    stillname, stillext = os.path.splitext(pngname)
    return ''.join([stillname, iter, stillext])

def _adjustsubplots(fig):
    fig.subplots_adjust(bottom = 0.15, top = 0.9, left = 0.15, right = 0.975)

def animate(var, iters, gifname, kwargs):
    """Create .gif animation of sea ice fraction from MITgcm .nc files.

    Required Arguments:
     *  iters:  list of iterations to plot. These should match the file names
                of the output_00{iter}.nc files. The iteration numbers are
                automatically zero padded to 10 digits. Can be list of
                ints or list of strings.
     *  pngname:    File name to save the individual .png frames as.
                    The iteration number will be added between the given
                    name and the extension
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
     *  dpi = 400:   DPI of the png frames
    """
    #pre-process iters list to make sure they are 10-digit strings
    iters = [str(i).zfill(10) for i in iters]

    # deal with directories for .gif and .png; make them if they don't exist
    if not os.path.exists(kwargs['gif_folder_name']):
        os.mkdir(kwargs['gif_folder_name'])
    gifname = os.path.join(kwargs['gif_folder_name'], gifname)

    if not os.path.exists(kwargs['image_folder_name']):
        os.mkdir(kwargs['image_folder_name'])

    imgname = os.path.join(kwargs['image_folder_name'], kwargs['image_name'])

    # get the grids from the first nc file
    ncdata = _getdataset(iters[0], kwargs['namespec'])
    X, Y = np.meshgrid(np.array(ncdata['x']), np.array(ncdata['y']))
    X /= 1000
    Y /= 1000

    data = np.array(ncdata[var]).reshape(X.shape)
    filename = ncdata.filepath()

    fig = plt.figure()
    gs = gridspec.GridSpec(1, 1)
    ax = plt.subplot(gs[0, 0])

    pcolor = ax.pcolormesh(X, Y, var, cmap = kwargs['cmap'],
                        vmin = kwargs['vmin'], vmax = kwargs['vmax'])

    if kwargs['ice_velocity_field']:
        uice = np.array(ncdata['UICE']).reshape(X.shape)
        vice = np.array(ncdata['VICE']).reshape(X.shape)
        st = kwargs['stride']
        quiverplot = ax.quiver(X[::st, ::st], Y[::st, ::st],
                                uice[::st, ::st], vice[::st, ::st],
                                pivot ='mid', scale = kwargs['scale'])

    stillname = _getstillname(iters[0], imgname)
    _adjustsubplots(fig)
    fig.savefig(stillname, dpi = dpi)
    ax.set_xlabel('X [km]')
    ax.set_ylabel('Y [km]')
    ax.set_title('Variable %s from %s' % (var, filename))
    ncdata.close()

    def animate(iter):
        stillname = _getstillname(iter, pngname)
        iterdata = _getdataset(iter, namespec)
        iter_C = np.array(iterdata[var]).reshape(X.shape)
        file = iterdata.filepath()
        ax.set_title('Variable %s from %s' % (var, filename))
        # see https://stackoverflow.com/questions/18797175/animation-with-pcolormesh-routine-in-matplotlib-how-do-i-initialize-the-data
        iter_C = iter_C[:-1, :-1]
        pcolor.set_array(iter_C.ravel())

        if ice_velocity_field:
            iter_uice = np.array(iterdata['UICE']).reshape(X.shape)
            iter_vice = np.array(iterdata['VICE']).reshape(X.shape)
            U = iter_uice[::stride, ::stride]
            V = iter_vice[::stride, ::stride]
            quiverplot.set_UVC(U, V)
            iterdata.close()
            _adjustsubplots(fig)
            fig.savefig(stillname, dpi = dpi)
            return (pcolor, quiverplot)

        iterdata.close()
        _adjustsubplots(fig)
        fig.savefig(stillname, dpi = dpi)
        return pcolor


    anim = animation.FuncAnimation(fig,animate,frames=iters,interval=10000,blit=False,repeat=False)

    cbar = fig.colorbar(pcolor)
    # Then save the gif using ImageMagick writer
    writer = animation.ImageMagickFileWriter(fps = 2.5)
    anim.save(gifname, writer=writer)

if __name__ == "__main__":
    animate([12, 24, 36, 48, 72, 96, 120], 'ice_frac_ice_velocity_field_True.gif',
                'still_.png', dict(ice_velocity_field = True, dpi = 200))
