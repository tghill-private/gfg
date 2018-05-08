"""

    readmds.py (version 2)

    Module for reading MITgcm binary output into python data structures.

    The main function is rdmds, which reads binary MITgcm output into a
    numpy array for python analysis.

    Original version from Jonathan Barenboim, 2016.

    Tim Hill, 2018

"""

## for testing purposes
import argparse

import os
import ast

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
    fields = _readmeta (name_var, iteration)
    data = _readdata (name_var, iteration, fields)
    return data

def _readmeta(name_var, iteration):
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
    # Remove the file extension so this works with or without extension given
    name_var = os.path.splitext(name_var)[0]

    if iteration is None:
        filename = name_var + ".meta"
    else:
        # file names are 10 digits
        filename = "{0}.{1:010}.meta".format(name_var, iteration)

    # read in the meta file as text
    with open(filename, 'r') as metafile:
        metadata = metafile.read()

    # pre-process data
    metadata = metadata.replace('\n', '')
    metadata = metadata.replace('{', '[')
    metadata = metadata.replace('}', ']')

    # fields are delimited by semicolons
    metafields = metadata.split(';')

    # remove any empty strings in the list of data fields
    if '' in metafields:
        metafields.remove('')

    rawmeta = {}
    # get the data into a dictionary
    for variable in metafields:
        key, val = variable.split('=')
        key = key.strip()
        val = val.strip()
        val = ast.literal_eval(val)
        rawmeta[key] = val

    # post-process the dictionary
    fields = {}
    fields['ndims'] = rawmeta['nDims'][0]
    fields['data_type'] = rawmeta['dataprec'][0].replace('float' ,'f')
    fields['xdim'] = rawmeta['dimList'][0]
    fields['ydim'] = rawmeta['dimList'][3]
    if fields['ndims'] > 2:
        fields['zdim'] = rawmeta['dimList'][6]
    return fields

def _readdata(name_var, iteration, fields):
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
    vals = readmeta(args.filename, None)

    valsold = readmetaold(args.filename, None)

    print(vals)
    print(valsold)

if __name__ == "__main__":
    _test()
