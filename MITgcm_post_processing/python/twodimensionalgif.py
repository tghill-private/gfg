"""

    Create a gif animation and still frame images of a 2D data set.

    Uses netCDF4 files converted from MITgcm binary output (.data) files.
    Automatically creates a .gif animation and saves each frame as a still
    image.

    Parameters:

    Required:
        Name        |   Description
        ------------|-------------------
        var         :   Variable prefix to plot. This is the prefix of the
                        MITgcm binary output files. eg 'T', 'Rho'.

        movie_name  :   Filename to save the gif animation. This works with
                        or without the .gif. extension

        start_time  :   Time (sec) for the start of the run (or specific
                        set of iterations)

        sec_per_iter:   Seconds per model iteration.
        ------------|-------------------

    Optional:
        Name                |   Default     |   Description
        --------------------|---------------|--------------------
        vmin                :   None (auto) :   Colour scale min

        vmax                :   None (auto) :   Colour scale max

        image_folder_name   :   PNG_IMAGES  :   Directory to save image files in

        gif_folder_name     :   GIF_IMAGES  :   Directory to save animation in

        image_name          :   still_.png  :   Name to save images as. The
                                                model iteration number is
                                                put before the file
                                                extension. The extension given
                                                here specifies what file format
                                                to save the image as

        namespec            :   output_{iter}.nc    :   Specifies a file name
                                                        pattern for the .nc
                                                        files

        fps                 :   2           :   Frames per second in the
                                                output .gif animation

        cmap                :   'Blues'     :   Colour map for animation

        dpi                 :   200         :   Resolution for still frames

        plot_type           :   'gs'        :   One of None, 'gs', 'contour'
                                                or 'interp'.
                                                None: pcolormesh with no
                                                        shading/interpolation
                                                gs: pcolormesh with
                                                gouraud shading
                                                interp: imshow with
                                                interpolation

        interp_type         :   'bilinear'  :   Interpolation type. See pyplot
                                                imshow documentation
        https://matplotlib.org/api/_as_gen/matplotlib.pyplot.imshow.html

        aspect              :   'auto'      :   One of 'auto' or number.
                                                Auto uses a 4:3 aspect
                                                ratio; Passing a number
                                                forces that aspect ratio

        ice_velocity_field  :   True        :   Overlay a direction field of
                                                the ice velocity (from UICE
                                                and VICE)

        stride              :   3           :   stride length for picking
                                                data to splot for ice velocity
                                                field. ie, if stride = 3,
                                                only shows every an arrow for
                                                every 3rd data point

        scale               :   20          :   Scale for ice velocity field
                                                arrow size. A larger scale
                                                means smaller arrows; smaller
                                                scale means larger arrows.

        --------------------|---------------|--------------------
"""

import os
import glob

import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import gridspec

import netCDF4

defaults = {    'vmin':                 0.2,
                'vmax':                 1.0,
                'image_folder_name':    'PNG_IMAGES',
                'gif_folder_name':      'GIF_MOVIE',
                'image_name':           'still_.png',
                'namespec':             'output_{iter}.nc',
                'fps':                  2,
                'cmap':                 'Blues',
                'dpi':                  200,
                'plot_type':            'gs',
                'interp_type':          'bilinear',
                'aspect':               'auto',
                'ice_velocity_field':   True,
                'stride':               3,
                'scale':                20
            }

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
    """Helper function to set the spacing around the figure to make
    sure no axes or titles are cut off
    """
    fig.subplots_adjust(bottom = 0.15, top = 0.9, left = 0.15, right = 0.975)

def makeanimate(kwargs):
    """Create .gif animation of a 2D data field from MITgcm .nc files.

    args is a dictionary containing all arguments specified above.
    """
    args = defaults.copy()
    for key,val = kwargs.items():
        if key in defaults:
            args[key] = val
        else:
            raise KeyError('Unrecognized argument "%s"' % key)
    #pre-process iters list to make sure they are 10-digit strings
    iters = args['iters']
    if iters:
        iters = [str(i).zfill(10) for i in iters]
    else:
        pattern = args['namespec'].replace('{iter}', '*')
        files = glob.glob(pattern)
        iters = sorted([os.path.splitext(f)[0][-10:] for f in files], key = int)

    # deal with directories for .gif and .png; make them if they don't exist
    if not os.path.exists(args['gif_folder_name']):
        os.mkdir(args['gif_folder_name'])
    gifname = os.path.splitext(args['movie_name'])[0] + '.gif'
    gifname = os.path.join(args['gif_folder_name'], gifname)

    if not os.path.exists(args['image_folder_name']):
        os.mkdir(args['image_folder_name'])
    imgname = os.path.join(args['image_folder_name'], args['image_name'])

    # get the grids from the first nc file
    ncdata = _getdataset(iters[0], args['namespec'])
    X, Y = np.meshgrid(np.array(ncdata['x']), np.array(ncdata['y']))
    X /= 1000
    Y /= 1000

    data = np.array(ncdata[args['var']]).reshape(X.shape)
    filename = ncdata.filepath()

    fig = plt.figure()
    gs = gridspec.GridSpec(1, 1)
    ax = plt.subplot(gs[0, 0])

    if args['plot_type'] == None:
        pcolor = ax.pcolormesh(X, Y, data, cmap = args['cmap'],
                            vmin = args['vmin'], vmax = args['vmax'])

    elif args['plot_type'] == 'gs':
        pcolor = ax.pcolormesh(X[:-1, :-1], Y[:-1, :-1], data, cmap = args['cmap'],
                            vmin = args['vmin'], vmax = args['vmax'],
                            shading = 'gouraud')

    elif args['plot_type'] == 'interp':
        pcolor = ax.imshow(data, cmap = args['cmap'], cmin = args['vmin'],
                            vmax = args['vmax'], origin = 'lower',
                            extent = [X[0, 0], X[-1, -1], Y[0, 0], Y[-1, -1]],
                            interpolation = args['interp_type'])

    if args['ice_velocity_field']:
        uice = np.array(ncdata['UICE']).reshape(X.shape)
        vice = np.array(ncdata['VICE']).reshape(X.shape)
        st = args['stride']
        quiverplot = ax.quiver(X[::st, ::st], Y[::st, ::st],
                                uice[::st, ::st], vice[::st, ::st],
                                pivot ='mid', scale = args['scale'])

    cbar = fig.colorbar(pcolor)
    stillname = _getstillname(iters[0], imgname)
    _adjustsubplots(fig)
    fig.savefig(stillname, dpi = args['dpi'])
    ax.set_xlabel('X [km]')
    ax.set_ylabel('Y [km]')
    ax.set_title('Variable %s from %s' % (args['var'], filename))
    ncdata.close()

    def animate(iter):
        stillname = _getstillname(iter, imgname)
        iterdata = _getdataset(iter, args['namespec'])
        iter_C = np.array(iterdata[args['var']]).reshape(X.shape)
        file = iterdata.filepath()
        time = args['start_time'] + (int(iter) - int(iters[0])) * args['sec_per_iter']
        title = '{0} at t = {1} s'.format(args['var'], time)
        ax.set_title(title)
        # see https://stackoverflow.com/questions/18797175/animation-with-pcolormesh-routine-in-matplotlib-how-do-i-initialize-the-data
        iter_C = iter_C[:-1, :-1]
        iterarr = iter_C if args['plot_type'] == interp else iter_C.ravel()
        pcolor.set_array(iterarr)

        if args['ice_velocity_field']:
            iter_uice = np.array(iterdata['UICE']).reshape(X.shape)
            iter_vice = np.array(iterdata['VICE']).reshape(X.shape)
            U = iter_uice[::st, ::st]
            V = iter_vice[::st, ::st]
            quiverplot.set_UVC(U, V)
            iterdata.close()
            _adjustsubplots(fig)
            fig.savefig(stillname, dpi = args['dpi'])
            return (pcolor, quiverplot)

        iterdata.close()
        _adjustsubplots(fig)
        fig.savefig(stillname, dpi = args['dpi'])
        return pcolor


    anim = animation.FuncAnimation(fig, animate, frames=iters,
                                    blit=False,repeat=False)

    # Then save the gif using ImageMagick writer
    gifwriter = animation.ImageMagickFileWriter(fps = args['fps'])
    anim.save(gifname, writer=gifwriter)

if __name__ == "__main__":
    twodimensionalgif(dict( var = 'ice_fract',
                            iters=[12, 24, 36, 48, 72, 96, 120],
                            movie_name='ice_frac_ice_velocity_field_True.gif',
                            image_name='still_.png',
                            ice_velocity_field = True,
                            dpi = 200,
                            start_time = 100,
                            sec_per_iter = 10))
