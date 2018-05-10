"""

    script generateGifs.py

    This script generates multiple animated gif cross-sections of data
    from the MITgcm model.

    There are now two functions to create gif animations (and corresponding
    still frames):

    plot3d  :   Create 2D slices of a 3D dataset (eg T, Rho)

    plot2d  :   Plot a 2D dataset (eg seaice_fract)

"""

import twodimensionalgif
import threedimensionalgif

def plot3d(gif_args):
    """Creates an animated gif with the specified parameters.
    See parameter descriptions in either twodimensionalgif.py or
    generateGifs.txt.

    Raises a KeyError if any unrecognized arguments are passed.
    """
    args = global_gif_args.copy()
    args.update(gif_args)
    twodimensionalgif.makeanimate(args)


def plot2d(gif_args):
    """Creates an animated gif with the specified parameters.
    See parameter descriptions in either twodimensionalgif.py or
    generateGifs.txt.

    Raises a KeyError if any unrecognized arguments are passed.
    """
    args = global_gif_args.copy()
    args.update(gif_args)
    twodimensionalgif.makeanimate(args)

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
