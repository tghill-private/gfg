"""

    script generateGifs.py

    This script generates multiple animated gif cross-sections of data
    from the MITgcm model.

    There are now two functions to create gif animations (and corresponding
    still frames):

     *  3dplot: create a 2D animation of a slice of 3D data (eg. Temperature,
                velocity field, density, ...)

     *  2dplot: create a 2D animation of 2D data (eg. Ice fraction)

     =====================================================================

    plot3d:

    For each animation set parameters

    'cut_var':      Which coordinate cross section (one of 'x', 'y', 'z')
    'cut_val':      Value at which to cross section (in meters)
    'data_var':     Variable prefix in the .data and .meta files
    'movie_name':   Filename of the generated movie (with or without extension)

    Call the plot(gif_args) function with a dictionary containing these args.

    Specify any parameters common to all the animations in the global_gif_args
    dictionary.

    Optional parameters:

    # vmin and vmax: Desired min and max for the colourbar scale. If not given, scale will likely be inconsistent. Not required for temperature
    # file_type: The file type to save the images in. By default, saves as a png. Options are 'emf', 'eps', 'pdf', 'png', 'ps', 'raw', 'rgba', 'svg', and 'svgz'
    # stitch_gif: Boolean controlling whether or not to stitch the images into a gif. By defualt, True
    # iter_start, iter_end: the range of iterations to plot, inclusive. By default, the entire runtime is plotted
    # x_axis_start, x_axis_end: the range of the x-axis coordinate to plot, in meters and inclusive. By default, entire range is plotted
    # y_axis_start, y_axis_end: the range of the y-axis coordinate to plot, in meters and inclusive. By default, entire range is plotted
    # image_folder_name: name of the folder to save images in. By defualt, "PNG_IMAGES"
    # gif_folder_name: name of the folder to save gifs in. By default, "GIF_MOVIES"
    # bathy_file_name: name of the bathymetry file used as input. By default, "bathymetry.bin"

    =====================================================================

    plot2d:

    For each animation set parameters

    'data_var':     Variable prefix in the .data and .meta files
    'movie_name':   Filename of the generated movie (with or without extension)

"""

import twodimensionalgif
import threedimensionalgif

def plot3d(gif_args):
    """Creates an animated gif with the specified parameters.
    See parameter descriptions in the header of this file.
    """
    d = global_gif_args.copy()
    d.update(gif_args)
    twodimensionalgif.twodimensionalgif(d)


def plot2d(gif_args):
    """
    """
    args = global_gif_args.copy()
    args.update(gif_args)
    twodimensionalgif.twodimensionalgif(args)

global_gif_args = {

}

#####
args = {
    'var':          'ice_fract',
    'iters':        None,
    'movie_name':   'ice_frac_velocity_field_True.gif',
    'image_name':   'still_.png',
    'ice_velocity_field':   True,
    'dpi':          200
}


plot2d(args)

"""
gif_args = {
    'cut_var' : 'z',
    'cut_val' : 0,
    'data_var' : 'T',
    'movie_name' : 'T_0_xy_interp',
    'bathy_file_name':None,
    'iter_start':1,
    'iter_end':10
}
plot3d(gif_args)


gif_args = {
    'cut_var' : 'x',
    'cut_val' : 1,
    'data_var' : 'T',
    'movie_name' : 'T_1_zy_interp',
    'bathy_file_name':None,
    'iter_start':1,
    'iter_end':10
}
plot3d(gif_args)

gif_args = {
    'cut_var' : 'y',
    'cut_val' : 10,
    'data_var' : 'T',
    'movie_name' : 'T_10_zx_interp',
    'bathy_file_name':None,
    'iter_start':1,
    'iter_end':10
}
plot3d(gif_args)
"""
print ("\nFinished animating all the gifs")
