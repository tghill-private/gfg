# netCDFbinary
netCDFbinary is a python package for converting MITgcm binary model output `.data` files to NetCDF `.nc` files. The variables to be included in the netcdf files are specified as command line arguments.

The core functionality of this package comes from the [UW fluids group wiki](https://wiki.math.uwaterloo.ca/fluidswiki/index.php?title=NetCDF_Converter). That script was modified to work with 2D variables such as ice fraction (`ice_fract`) and wrapped in a more distributable package with a command line interface.

## Installation
Clone or download and extract the code. Put the code directory on your python path, or add the directory to your python path by adding the following line to your `.bashrc` file

    export PYTHONPATH="${PYTHONPATH}:/path/to/netCDFbinary

### Requirements

#### Running on Graham
I have had an unexpected error where the script exists with a Segmentation Fault. The cause of this error is unknown, but with the modules consistent with the list in `modules.txt` the script runs.

#### Python Packages
netCDFbinary requires the following python packages
  * numpy
  * [netCDF4](http://unidata.github.io/netcdf4-python/)
  * [MITgcmutils](https://github.com/MITgcm/MITgcm), install from the folder `$MITgcm/utils/python/MITgcmutils` and install with `python setup.py install`.
    * If you aren't using [virtualenv](https://virtualenv.pypa.io/en/stable/) for package managment you will likely need to specify `--prefix={where/to/install}`, again adding the path to your python path (or installing into your local python path probably in `~/.local/...`)

## Usage
The package is set up with a `__main__.py` file, to [run the package as a script](https://docs.python.org/2/using/cmdline.html) (`-m` flag). Command line arguments are
  * fields: The MITgcm variables to add to the netCDF file. These are the variable prefixes to the `.meta` and `.data` binary files. For example, `T` and `Rho`.
  * [iters, optional]: If iters is specified, it is a list of iterations to convert. If it is not given, all available iterations will be converted.
  * [-o, --overwrite]: Flag specifying whether to overwrite previously converted files. If given, all old netCDF files will be overwritten with new files. If not given, will skip any existing files.

For example, to convert Temperature `T`, density `Rho`, and U and V velocities `U`, `V` for all available iterations:

    python -m netCDFbinary T Rho U V

For the same fields but only select iterations, for example

    python -m netCDFbinary T Rho U V --iters 0 10 20 30 40 50

  And to overwrite any existing files

    python- m netCDFbinary T Rho U V -o
