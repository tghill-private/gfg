"""

    Create a gif animation and still frame images of slices of a 3D data set.

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
                        or without the .gif. e

        cut_var     :   Axis to take a constant slice of. One of 'x', 'y'
                        or 'z'.

        cut_val     :   Value to take a slice at. Must be a level in the
                        model data.
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
                                                extension

        bathy_file_name     :   bathymetry.bin: Name of bathymetry file. If None
                                                do not apply land mask

        namespec            :   output_{iter}.nc    :   Specifies a file name
                                                        pattern for the .nc
                                                        files

        fps                 :   2           :   Frames per second in the
                                                output .gif animation

        cmap                :   'Spectral_r':   Colour map for animation

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
        --------------------|---------------|--------------------"""

import glob
import os

import numpy as np

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib import animation

import netCDF4

defaults = {    'vmin' : None,
                'vmax' : None,
                'image_folder_name' : 'PNG_IMAGES',
                'gif_folder_name' : 'GIF_MOVIES',
                'min_points' : 100,
                'bathy_file_name' : 'bathymetry.bin',
                'namespec' : 'output_{iter}.nc',
                'image_name' : 'still_.png',
                'fps' : 2,
                'cmap' : 'Blues',
                'dpi' : 200,
                'plot_type' : None,
                'interp_type' : None,
                'aspect' : 'auto'
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

def makeanimate(args):
    """Make gif animation and still frames.

    Args is a dictionary containing all arguments specified above. Saves the
    movies and images according to arguments in args.

    TODO: support bathymetry files and proper time labelling.
    """
    # pre-process iters list to make sure they are 10-digit strings.
    iters = args['iters']
    # if iters is None, find all matching files.
    if iters:
        iters = [str(i).zfill(10) for i in iters]
    else:
        pattern = args['namespec'].replace('{iter}', '*')
        files = glob.glob(pattern)
        iters = sorted([os.path.splitext(f)[0][-10:] for f in files], key = int)

    # deal with directories for .gif and .png; make them if they don't exist
    if not os.path.exists(args['gif_folder_name']):
        os.mkdir(args['gif_folder_name'])
    gifname = os.path.join(args['gif_folder_name'], args['movie_name'])

    if not os.path.exists(args['image_folder_name']):
        os.mkdir(args['image_folder_name'])
    imgname = os.path.join(args['image_folder_name'], args['image_name'])

    # get the grids from the first nc file
    ncdata = _getdataset(iters[0], args['namespec'])
    X = np.array(ncdata['x'])
    Y = np.array(ncdata['y'])
    Z = np.array(ncdata['z'])

    cutindex = int(np.where(np.array(ncdata[args['cut_var']]) == args['cut_val'])[0])
    if args['cut_var'] == 'x':
        plotXgrid, plotYgrid = np.meshgrid(Y, Z)
        xlabel = 'y'
        ylabel = 'z'
        cutaxis = 2
    elif args['cut_var'] == 'y':
        plotXgrid, plotYgrid = np.meshgrid(X, Z)
        cutaxis = 1
        xlabel = 'y'
        ylabel = 'z'
    elif args['cut_var'] == 'z':
        plotXgrid, plotYgrid = np.meshgrid(X, Y)
        cutaxis = 0
        xlabel = 'x'
        ylabel = 'y'


    # if args['bathy_file_name']:
    #     # Create a mask of land values
    #     land_area = utils.getland(gif_args['cut_var'], grid_cut_val, nx, ny, nz, dz, gif_args['bathy_file_name'])
    #     # Take the land area slice associated with the plotting range
    #     land_area = utils.zoommask(land_area, xis, xie, yis, yie, zoom)
    #     # Transpose land_area so it's orientation matches data
    #     land_area = numpy.transpose(land_area)
    # else:
    #     land_area = None
    land_area = None

    if args['aspect'] == 'auto':
        fig = plt.figure(figsize = (8, 6))
    else:
        C = 6*8
        x = float(np.sqrt(C*args['aspect']))
        y = float(x/args['aspect'])
        fig = plt.figure(figsize=(x, y))

    ax = plt.subplot(111)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    stillname = _getstillname(iters[0], imgname)
    initdata = _getdataset(iters[0], args['namespec'])
    print(initdata.filepath())
    initvar = np.array(initdata[args['var']])
    print(initvar.shape)
    plotdata_var = np.take(initvar, cutindex, axis = cutaxis)
    print(plotdata_var.shape)
    # see https://stackoverflow.com/questions/18797175/animation-with-pcolormesh-routine-in-matplotlib-how-do-i-initialize-the-data
    plotdata_var = plotdata_var[:-1, :-1]


    if args['plot_type'] == None:
        pcolor = ax.pcolormesh(plotXgrid, plotYgrid, plotdata_var,
                                cmap = args['cmap'], vmin = args['vmin'],
                                vmax = args['vmax'])
    elif args['plot_type'] == 'gs':
        pcolor = ax.pcolormesh(plotXgrid[:-1, :-1], plotYgrid[:-1, :-1], plotdata_var,
                                cmap = args['cmap'], vmin = args['vmin'],
                                vmax = args['vmax'], shading = 'gouraud')
        print('interpolating')

    elif args['plot_type'] == 'interp':
        pcolor = ax.imshow(plotdata_var, interpolation = args['interp_type'],
                        extent = [plotXgrid[0,0], plotXgrid[-1, -1],
                                    plotYgrid[0, 0], plotYgrid[-1, -1]],
                        cmap = args['cmap'], vmin = args['vmin'],
                        vmax = args['vmax'], origin = 'lower',
                        aspect = 'auto')

    if args['cut_var'] != 'z':
        ax.invert_yaxis()
    plt.tight_layout()
    def animate(iter):
        stillname = _getstillname(iter, imgname)
        iterdata = _getdataset(iter, args['namespec'])
        print(iterdata.filepath())
        itervar = np.array(iterdata[args['var']])
        plotdata_var = np.take(itervar, cutindex, axis = cutaxis)
        plotdata_var = plotdata_var[:-1, :-1]

        plotdata = plotdata_var if args['plot_type'] == 'interp' \
                        else plotdata_var.ravel()
        # plt.tight_layout()
        pcolor.set_array(plotdata)

        # TODO fix this
        time = iter
        title = '{var} at {cut_var}={cut_val} at t=%s' % time
        title = title.format(var=args['var'], cut_var=args['cut_var'], cut_val=args['cut_val'])
        ax.set_title(title)

        _adjustsubplots(fig)
        fig.savefig(stillname, dpi = args['dpi'])

        iterdata.close()

        return pcolor
    fig.colorbar(pcolor)

    anim = animation.FuncAnimation(fig, animate, frames = iters,
                        blit = False, repeat = False)

    gifwriter = animation.ImageMagickFileWriter(fps = args['fps'])
    anim.save(gifname, writer = gifwriter)

    print('Saved animation as %s' % gifname)

if __name__ == '__main__':
    args = {'var':'T', 'iters':[20520, 20640, 20760, 20880],
            'movie_name':'2dslice_gs_autoaspect.gif',
            'cut_var':'z',
            'cut_val':0,
            'cmap':'Spectral_r',
            'vmin':11, 'vmax':13.5,
            'image_name':'still_gs_autoaspect.png',
            'plot_type':'gs'}
    gifargs = defaults.copy()
    gifargs.update(args)
    makeanimate(gifargs)
