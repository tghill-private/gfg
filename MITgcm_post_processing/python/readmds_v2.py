"""

    readmds.py (version 2)

    Module for reading MITgcm binary output into python data structures.

    Original version from Jonathan Barenboim, 2016.

    Tim Hill, 2018

"""

## for testing purposes
import argparse

import os

import numpy
import sys

def rdmds (name_var, iteration=None):
    """rdmds returns data for one field at a single timestep as a numpy array.

    Input:
     *  name_var: The prefix of the .data and .meta files.
     *  iteration: the iteration to get the data from.

    Returns:
     *  numpy array of the data in the corresponding binary output file
     """
    fields = readmeta (name_var, iteration)
    data = readdata (name_var, iteration, fields)
    return data

def readmeta (name_var, iteration):
    """readmeta returns the dimensions and data types for a binary data file.

    Input:
     *  name_var: The prefix of the .data and .meta files.
     *  iteration: the iteration to get the data from. If iteration is None,
            it is assumed name_var is the full name of the data file

    Returns:
     *  dictionary with key-value pairs
            'ndims':        (int)     number of dimensions of the data
            'data_type':    (str)     type of data (ex 'f32')
            'xdim':         (int)     Dimension in x
            'ydim':         (int)     Dimension in y
            'zdim':         (int)     Dimension in z
    """
    fields = {}
    name_var = os.path.splitext(name_var)[0]
    if iteration is None:
        filename = name_var + ".meta"
    else:
        # file names are 10 digits
        filename = "{0}.{1:010}.meta".format(name_var, iteration)

    # read in the meta file as text
    with open(filename, r') as metafile:
        metadata = metafile.read()

    metadata = metadata.replace('\n', '')
    metadata = metadata.replace('{', '[')
    metadata = metadata.replace('}', ']')

    metafields = metadata.split(';')

    print(metafields)

    """
    f = open(filename)
    text = f.read()
    f.close()

    # remove new line characters and replace curly braces with brackets
    text = text.replace("\n", "")
    text = text.replace("{", "[").replace("}", "]")
    text = text.strip()

    # Execute the code to set all variables
    if sys.version_info[0] < 3:
        exec(text)
    else:
        exec(text, globals())

    fields['ndims'] = nDims[0]
    fields['data_type'] = dataprec[0].replace('float' ,'f')
    fields['xdim'] = dimList[0]
    fields['ydim'] = dimList[3]
    if fields['ndims'] > 2:
        fields['zdim'] = dimList[6]
    return fields
    """

# This function reads a data file based on information from the associated meta file
# Note: MITgcm data is always written in big endian byteorder and Fortran memory order
# INPUT:
#    name_var: the prefix of the data file. Example 'T' or 'Rho'
#    iteration: the iteration to get the data from. If iteration is None, it's
#        assumed that name_var is the full file name (without .data suffix)
#    fields: a dictionary containing the following fields from the associated meta file:
#        ndims: number of dimensions
#        data_type: type and precision of the data. Ex 'f32'
#        xdim, ydim, zdim: the number of points along each coordinate axis
# returns a numPy array with the data
def readdata(name_var, iteration, fields):
    """readdata reads a binary data file and returns a numpy array with the data.

    Inputs:
     *  name_var:   the prefix of the data file
     *  iteration:  the iteration to get the data from. If iteration is None,
            it is assumed name_var is the full name of the data file
    * fields:       a dictionary containing the same keys readdata
            outputs.

    Returns:
     *  numpy array with the data from the corresponding binary file
    """
    name_var = os.path.splitext(name_var)[0]
    if iteration is None:
        filename = name_var + ".data"
    else:
        filename = "{0}.{1:010}.data".format(name_var, iteration)

    # read in the data
    fid = open(filename, 'rb')

    #     Convert data type from bits to bytes and prepend big endian flag
    dt = '>' + fields['data_type'][0] + str(int(fields['data_type'][1:]) // 8)
    dt = numpy.dtype(dt)

    # Two dimensional data
    if fields['ndims'] == 2:
        size = fields['xdim'] * fields['ydim']
        data = numpy.fromfile(fid, dtype=dt, count=-size)
        data = data.reshape( (fields['xdim'],fields['ydim']), order='F' )

    # Three dimensional data
    if fields['ndims'] == 3:
        size = fields['xdim'] * fields['ydim'] * fields['zdim']
        data = numpy.fromfile(fid, dtype=dt, count=-size)
        data = data.reshape( (fields['xdim'], fields['ydim'], fields['zdim']), order='F' )

    fid.close()
    return data

def _test():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    vals = readmeta(args.filename)

if __name__ == "__main__":
    _test()
