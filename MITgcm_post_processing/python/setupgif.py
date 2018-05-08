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

def check_requireds(gif_args):
    """
    check_requireds validates the arguments given to [what function].

    Requires following keys to be of these types/values
    Key:            Type/Value
    'cut_val'       Numeric
    'cut_var'       one of 'x', 'y', 'z'
    'movie_name'    Nonempty string

    Implicitly raises KeyError for missing keys, and explicitly raises
    ValueError if the value is inconsistent with above requirements
    """
    # make sure cut_val is numeric. This line used to be
    """if type(gif_args['cut_val']) not in [int, float]:
        print ("Error: cut_val must be a number. Make sure it is not surrounded in quotes")
        sys.exit(1)"""
    gif_args['cut_val'] = float(gif_args['cut_val'])

    if gif_args['cut_var'] not in ['x', 'y', 'z']:
        raise ValueError('"cut_var" must be one of "x", "y", or "z"')

    gif_args['movie_name'] = str(gif_args['movie_name'])
    if gif_args['movie_name'] == '':
        raise ValueError('"movie_name" must be a non-empty string')

    gif_args['data_var'] = str(gif_args['data_var'])
    if gif_args['data_var'] == '':
        raise ValueError('"data_var" must be a non-empty string')


# This functions sets default values of optional arguments and returns the new dictionary
def set_default(gif_args):
    """set_default sets the default values of optional parameters in dictionary.

    Raises KeyError if a key is specified in gif_args that is
    not in parameter list params
    """
    new_args = defaults.copy()
    for key, val in gif_args.items():
        if key not in params:
            raise KeyError('Unrecognized key "%s"' % key)
        else:
            new_args[key] = val

    return new_args

def check_types (gif_args):
    """check_types verifies the types of all optional arguments.

    Raises Exceptions for any invalid types..
    """
    # for k in types.keys():
    #     if types[k] == 'number':
    #         if type(gif_args[k]) not in [int, float]:
    #             print ("Error: {0} must be a number. Make sure it is not surrounded in quotes".format(k))
    #             sys.exit(1)
    #     elif types[k] == 'number, None':
    #         if type(gif_args[k]) not in [int, float, type(None)]:
    #             print ("Error: {0} must be a number. Make sure it is not surrounded in quotes".format(k))
    #             sys.exit(1)
    #     elif types[k] == 'string':
    #         if type(gif_args[k]) is not str:
    #             print ("Error: {0} must a string".format(k))
    #             sys.exit(1)
    #     elif types[k] == 'boolean':
    #         if type(gif_args[k]) not in [int, bool]:
    #             print ("Error: {0} must be a boolean. Remember that True and False must be capitalized".format(k))
    #             sys.exit(1)
    pass

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
