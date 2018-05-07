import numpy
import sys

# Jonathan Barenboim, October 2016
# This function reads the data for a single field at a single timestep
# INPUT:
#	name_var: The prefix of the .data and .meta files. Example 'T' or 'Rho'
#	iteration: the iteration to get the data from. Optional. If iteration is not
#		given, it's assumed that name_var is the full file name (without
#		the .data or .meta suffix)
# Returns a numPy array with the data

def rdmds (name_var, iteration=None):
	fields = readmeta (name_var, iteration)
	data = readdata (name_var, iteration, fields)
	return data

# This function reads a meta file and returns information about the associated data file
# INPUT:
#	name_var: the prefix of the meta file. Example 'T' or 'Rho'
#	iteration: the iteration to get the data from. If iteration is None, 
#		it's assumed that name_var is the full file name (without .meta suffix)
# Returns a dictionary with the following keys:
#	ndims: number of dimensions
#	data_type: type and precision of the data. Ex 'f32'
#	xdim, ydim, zdim: the number of points along each coordinate axis
def readmeta (name_var, iteration):
	fields = {}

	if iteration is None:
		filename = name_var + ".meta"
	else:
		# file names are 10 digits
		filename = "{0}.{1:010}.meta".format(name_var, iteration)
	
	# read in the meta file as text
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


# This function reads a data file based on information from the associated meta file
# Note: MITgcm data is always written in big endian byteorder and Fortran memory order
# INPUT:
#	name_var: the prefix of the data file. Example 'T' or 'Rho'
#	iteration: the iteration to get the data from. If iteration is None, it's
#		assumed that name_var is the full file name (without .data suffix)
#	fields: a dictionary containing the following fields from the associated meta file:
#		ndims: number of dimensions
#		data_type: type and precision of the data. Ex 'f32'
#		xdim, ydim, zdim: the number of points along each coordinate axis
# returns a numPy array with the data
def readdata(name_var, iteration, fields):

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







