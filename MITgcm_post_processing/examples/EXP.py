"""
    EXP.py

    Sample file showing how to specify GIF animation arguments.

    See full list of possible parameters in the package README file.

    Descriptions:

     *  GLOBAL_GIF_ARGS :   Dictionary specifying any global arguments
                            common to all figures

     *  ARGS3D :            List of dictionaries specifying arguments
                            for each plot of a 3D dataset.

     *  ARGS2D :            List of dictionaries specifying arguments
                            for each plot of a 2D dataset.

"""

# GLOBAL arguments

GLOBAL_GIF_ARGS = { 'image_folder_name':    'PNG',
                    'gif_folder_name'  :    'GIF',
                    'cmap':                 'jet',
                    'plot_type':            'gs',
                    'start_time' :          0,
                    'sec_per_iter' :        10.0
                }

ARGS3D = [
        {   'var':          'T',
            'cut_var' :     'x',
            'cut_val' :     1500,
            'image_name' :  'slice_x_1500.png',
            'movie_name' :  'slice_x_1500.gif'
        },

        {   'var':          'T',
            'cut_var' :     'y',
            'cut_val' :     675,
            'image_name' :  'slice_y_675.png',
            'movie_name' :  'slice_y_675.gif'
        },

        {   'var':          'T',
            'cut_var' :     'z',
            'cut_val' :     0,
            'image_name' :  'slice_z_0.png',
            'movie_name' :  'slice_z_0.gif'
        }
]

ARGS2D = [
        {   'var' :         'ice_fract',
            'movie_name' :  'ice_fract.gif',
            'fps' :         4
        }
]
