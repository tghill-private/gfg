"""

    module ice_plt_ani.py

    Plot sea ice fraction with overlaid wind direction field from MITgcm
    model runs.

    This module makes animations from converted netCDF4 files, which should have
    been converted from the binary .data files from datnetcdf.py

"""

import imageio

filenames = ['image_%s.png' % str(x).zfill(1) for x in 12*list(range(5)]

print(filenames)

def main():
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    imageio.mimsave('/path/to/movie.gif', images)

if __name__ == "__main__":
    pass
