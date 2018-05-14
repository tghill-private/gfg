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
    threedimensionalgif.makeanimate(args)


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

args2d = {  'var'       :   'ice_fract',
            'movie_name':   '2d_ice_fract_none.gif',
            'start_time':   12,
            'sec_per_iter': 1,
            'vmin'      :   0.0,
            'vmax'      :   1.0,
            'image_folder_name':    'PNG_NEW',
            'gif_folder_name':      'GIF_NEW',
            'image_name':           '2d_T_none.png',
            'plot_type':           None
        }

args3d = {  'var'       :   'T',
            'movie_name':   'slice_z=15_landmask_small.gif',
            'cut_var'   :   'z',
            'cut_val'   :   15,
            'start_time':   0,
            'sec_per_iter': 1,
            'gif_folder_name':      'GIF_NEW',
            'image_folder_name':    'PNG_NEW',
            'image_name':           'slice_z=15_small.png',
            'iters':                (25320, 25440),
            'vmin':                 11,
            'vmax':                 13.5,
            'plot_type': None,
        }

# plot2d(args2d)
plot3d(args3d)

print ("\nFinished animating all the gifs")
