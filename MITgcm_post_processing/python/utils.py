# Jonathan Barenboim, October 2016
# This file contains some useful helper functions used by other python scripts

from math import floor
from readmds import rdmds
import numpy
import scipy.io
import sys


# This function gets the gird coordinates of MITgcm binary output
# Requires the files:
#   XC.*.data (meta)  XG.*.data (meta)     --to read x-coordinate
#   YC.*.data (meta)  YG.*.data (meta)     --to read y-coordinate
#   RC.data (meta)    RF.data (meta)       --to read z-coordinate
# INPUT:
#   gridtype: the type of coordinates to retrieve. Must be one of
#       'C': returns the grid centres. This is the default option
#       'G'; returns the grid corners
# Returns a tuple of arrays containing the grid coordinates
def MITgcm_getgrid (gridtype='C'):
    assert gridtype in ['C', 'G'], """unrecognized grid type. Use 'C' for center coordinates or 'G' for grid corner coordinates"""

    if gridtype == 'C':
        xc = rdmds ('XC')
        yc = rdmds ('YC')
        zc = rdmds ('RC')
        xc = xc[:,0]
        yc = yc[0]
        zc = zc[0,0]
        return xc, yc, zc
    else:
        xg = rdmds ('XG')
        yg = rdmds ('YG')
        zg = rdmds ('RF')
        xg = xg[:,0]
        yg = yg[0]
        zg = zg[0,0]
        return xg, yg, zg

# This function converts a time in seconds to a human friendly time stamp
# INPUT:
#    seconds: Time in seconds
#    show_days: whether or not to include days in the format of the time stamp.
#        If false, time stamp may show more than 24 hours. For example, 5 days
#        will be '120:00:00'. True by default

def convertseconds (seconds, show_days=True):
    if show_days:
        days = seconds // (60 * 60 * 24)
        seconds -= days * (60 * 60 * 24)

    hours = seconds // 3600
    seconds -= hours * 3600

    minutes = seconds // 60
    seconds -= minutes * 60

    if show_days:
        return "{0:02}D {1:02}:{2:02}:{3:02}".format(days, hours, minutes, seconds)
    return "{0:02}:{1:02}:{2:02}".format(hours,minutes,seconds)


# This function takes a cut_val in meters and returns the grid index to cut at
# INPUT:
#    cut_val: the position in meters to take the slice at
#    resolution: a string that can be either a single number for a constant
#        resoution, or a list like '6*1, 6*2' for variable resolution
#     n: the total number of points along the axis being cut

def getgridcutval (cut_val, resolution, n):
    # Return None if cut_val is None
    # Required behaviour if x_axis_start, etc is None
    if cut_val == None:
        return None

    grid_cut_val = 0

    # Test that cut_val is inside the grid, and exit if not
    total_length = 0
    if resolution.find("*") != -1:
        res_temp = resolution.split(",")
        for res in res_temp:
            a, b = [ float(x) for x in res.split("*") ]
            total_length += a * b
    else:
        total_length = float(resolution) * n

    if cut_val > total_length:
        print ("Error: cut_val is outside the grid. Failed to find grid_cut_val for: ")
        print ("\tcut_val = {0}, resolution = {1}, n = {2}".format(cut_val, resolution, n))
        sys.exit(1)

    # if resolution is a list
    if resolution.find("*") != -1:
        # split the string into a list of strings "a*b"
        resolution = resolution.split(",")

        for res in resolution:
        # Split the string into a pair (a,b) where a is the number of grid squares
        # the resolution applies to and b is the size of the grid
            a, b = [ float(x) for x in res.split("*") ]
            if cut_val > a * b:
                cut_val -= a * b
                grid_cut_val += a
            else:
                grid_cut_val = floor(grid_cut_val + cut_val / b)
                break

            if grid_cut_val > n - 1:
                return n - 1

    # if resolution is a single number
    else:
        resolution = float(resolution)
        grid_cut_val = floor (cut_val / resolution)

    return min (grid_cut_val, n-1)

# This function returns a mask of the land values at a certain cross section
# INPUT:
#    cut_var: the coordinate of the cross section
#   grid_cut_val: the index of the cross section
#    nx: number of points in the x direction
#    ny: number of points in the y direction
#   nz: number of points in the z direction
#    dz: vertical resolution
# Returns a 2d array the size of the zoomed data that masks the land values
def getland(cut_var, grid_cut_val, nx, ny, nz, dz, bathy_file_name):
    # Read in bathymetry file
    fid = open(bathy_file_name, 'rb')
    dt = numpy.dtype('>f8')
    bathy = numpy.fromfile(fid, dtype=dt)
    bathy = bathy.reshape( (nx, ny), order='F')

    # Get slice of bathymetry data corresponding to the cross section
    depths = bathy[grid_cut_val, :] if cut_var == 'x' else bathy[:, grid_cut_val] if cut_var =='y' else bathy

    # Create array the size of the data
    shape = (ny, nz) if cut_var == 'x' else (nx, nz) if cut_var == 'y' else (nx, ny)
    A = numpy.zeros(shape)

    # Set true for regions that are land
    if cut_var == 'z':
        for i in range(nx):
            for j in range(ny):
                # for each point, get the lowest index that is water
                depth_index = getgridcutval(-bathy[i,j], dz, nz)
                A[i, j] = grid_cut_val >= depth_index

    elif cut_var == 'x':
        for i in range(ny):
            depth_index = getgridcutval(-depths[i], dz, nz)
            A[i, 0:depth_index] = False
            A[i, depth_index:] = True

    elif cut_var == 'y':
        for i in range(nx):
            depth_index = getgridcutval(-depths[i], dz, nz)
            A[i, 0:depth_index] = False
            A[i, depth_index:] = True

    return A

# This function takes a mask and returns a zoomed mask of the correct plotting range
# INPUT:
#     mask: The mask array
#     xis, xie: the start and end indeces of the x-axis data to be plotted
#    yis, yie: the start and end indeces of the y-axis data to be plotted
#    zoom: a tuple representing the zoom factor in the x and y directions
def zoommask(mask, xis, xie, yis, yie, zoom):

    # Take slice of mask that will be plotted
    mask = mask[xis:xie, yis:yie]

    # Create new array of zoomed size
    A = numpy.ones( (mask.shape[0] * zoom[0], mask.shape[1] * zoom[1]) )

    #     Set points from mask into A
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            A[i * zoom[0], j * zoom[1]] = mask[i, j]
            # Fill in empty spaces in A
            if i != 0 and j != 0:
                corner1 = A[i * zoom[0], j * zoom[1]] # bottom right
                corner2 = A[(i-1) * zoom[0], j * zoom[1]] # top right
                corner3 = A[i * zoom[0], (j-1) * zoom[1]] # bottom left
                corner4 = A[(i-1) * zoom[0], (j-1) * zoom[1]] # top left

                # Spaces between two points are True if both points are True
                #    left side
                A[(i-1) * zoom[0] + 1 : i * zoom[0], (j-1) * zoom[1]] = corner3 and corner4
                #   right side
                A[(i-1) * zoom[0] + 1 : i * zoom[0], j * zoom[1]] = corner1 and corner2
                #    top side
                A[(i-1) * zoom[0], (j-1) * zoom[1] + 1 : j * zoom[1]] = corner4 and corner2
                #    bottom side
                A[i * zoom[0], (j-1) * zoom[1] + 1 : j * zoom[1]] = corner3 and corner1

                # Spaces in the centre are True if 3+ of the nearest corners are also True
                land_corners = corner1 + corner2 + corner3 + corner4
                A[(i-1) * zoom[0] + 1 : i * zoom[0], (j-1) * zoom[1] + 1 : j * zoom[1]] = land_corners >=3

    return A
