import sys

defaults = {    'vmin' : None,
                'vmax' : None,
                'file_type' : 'png',
                'iter_start' : None,
                'iter_end' : None,
                'x_axis_start' : None,
                'x_axis_end' : None,
                'y_axis_start' : None,
                'y_axis_end' : None,
                'stitch_gif' : True,
                'image_folder_name' : 'PNG_IMAGES',
                'gif_folder_name' : 'GIF_MOVIES',
                'min_points' : 100,
                'bathy_file_name' : 'bathymetry.bin' }

types = {       'vmin' : 'number, None',
                'vmax' : 'number, None',
                'file_type' : 'string',
                'iter_start' : 'number, None',
                'iter_end' : 'number, None',
                'x_axis_start' : 'number, None',
                'x_axis_end' : 'number, None',
                'y_axis_start' : 'number, None',
                'y_axis_end' : 'number, None',
                'stitch_gif' : 'boolean',
                'image_folder_name' : 'string',
                'gif_folder_name' : 'string',
                'min_points' : 'number',
                'bathy_file_name' : 'string' }

requireds = ['cut_var', 'cut_val' ,'data_var', 'movie_name']
params = list(defaults.keys())
params.extend(requireds)

# This function checks that the required arguments were given and are valid
def check_requireds(gif_args):

    # Exit if cut_val is not initialized or is not a number
    try:
        if type(gif_args['cut_val']) not in [int, float]:
            print ("Error: cut_val must be a number. Make sure it is not surrounded in quotes")
            sys.exit(1)
    except KeyError:
        print ("Error: cut_val is a required parameter but was not initialized")
        sys.exit(1)

    # Exit if cut_var is not initialized or is not an allowed option
    try:
        if gif_args['cut_var'] not in ['x', 'y', 'z']:
            print ("Error: cut_var must be one of 'x', 'y', 'z'")
            sys.exit(1)
    except KeyError:
        print ("Error: cut_var is a required parameter but was not initialized")
        sys.exit(1)

    # Exit if movie_name is not initialized or is not a string
    try:
        if type(gif_args['movie_name']) is not str:
            print ("Error: movie_name must be a string")
            sys.exit(1)
        if gif_args['movie_name'] == '':
            print ("Error: movie_name is a required parameter but was not initialized")
            sys.exit(1)
    except KeyError:
        print ("Error: movie_name is a required parameter but was not initialized")
        sys.exit(1)

    # Exit if data_var is not initialized or is not a string
    try:
        if type(gif_args['data_var']) is not str:
            print ("Error: data_var must be a string")
            sys.exit(1)
        if gif_args['data_var'] == '':
            print ("Error: data_var is a required parameter but was not initialized")
            sys.exit(1)
    except KeyError:
            print ("Error: data_var is a required parameter but was not initialized")
            sys.exit(1)

# This functions sets default values of optional arguments and returns the new dictionary
def set_default(gif_args):


    for k in defaults.keys():
        try:
            gif_args[k]
        except KeyError:
            gif_args[k] = defaults[k]

    return gif_args

# This function checks the type of the optional arguments and exits if they are invalid
def check_types (gif_args):


    for k in types.keys():
        if types[k] == 'number':
            if type(gif_args[k]) not in [int, float]:
                print ("Error: {0} must be a number. Make sure it is not surrounded in quotes".format(k))
                sys.exit(1)
        elif types[k] == 'number, None':
            if type(gif_args[k]) not in [int, float, type(None)]:
                print ("Error: {0} must be a number. Make sure it is not surrounded in quotes".format(k))
                sys.exit(1)
        elif types[k] == 'string':
            if type(gif_args[k]) is not str:
                print ("Error: {0} must a string".format(k))
                sys.exit(1)
        elif types[k] == 'boolean':
            if type(gif_args[k]) not in [int, bool]:
                print ("Error: {0} must be a boolean. Remember that True and False must be capitalized".format(k))
                sys.exit(1)

# This function prints out the parameters being used to generate the gif
def print_params(gif_args):
    print ("\nGenerating the gif with arguments: ")
    for k in params:
        print ("{0:<23}{1}".format(k + ":", gif_args[k]))

# This function prints a warning if an unknown argument was set
def check_extraneous(gif_args):
    for k in gif_args.keys():
        if k not in params:
            print ("Warning! unknown key found in arguments:   {0}".format(k))

# This function tests that the optional arguments are valid
def check_optionals(gif_args):

    # Exit if file type is not valid
    a = ['emf', 'eps', 'pdf', 'png', 'ps', 'raw', 'rgba', 'svg', 'svgz']
    if gif_args['file_type'] not in a:
        print ("Error: invalid file type for images. Valid options are: {0}".format(a))
        sys.exit(1)
