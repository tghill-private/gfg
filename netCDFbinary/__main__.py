"""

    main script to enable use use netCDFbinary package as a script.

    Usage:

        python -m netCDFbinary.py

"""

import argparse

from . import datnetcdf

parser = argparse.ArgumentParser()
parser.add_argument('fields', help = 'fields to convert', nargs = '*')
parser.add_argument('--iter', help = 'None or list of iterations',
                        nargs = '*')
parser.add_argument('-o', '--overwrite', help = 'Overwrite previous files',
                        action = 'store_true')
args = parser.parse_args()

indices = args.iter if args.iter else None

datnetcdf.convert(args.fields, indices = indices, verbose = True,
                        overwrite = args.overwrite)
