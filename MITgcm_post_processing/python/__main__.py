"""
    ___main__.py for MITgcmpp package.

    Lets the package be called as

    $ python -m MITgcmpp optfile


    Defines the command line interface.

"""

import importlib
from importlib import util

import argparse
import os

# create parser, and take command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('optfile', help = 'Animation options file')
args = parser.parse_args()
optfile = os.path.abspath(args.optfile)

# Find module name, filepath, and import the module
moddir, modfile = os.path.split(optfile)
modname = os.path.splitext(modfile)[0]
module_spec = importlib.util.spec_from_file_location(modname, args.optfile)
optmodule = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(optmodule)

# Process the module

# Make 3D plots
if hasattr(optmodule, 'ARGS3D'):
    for argspec3d in optmodule.ARGS3D:
        if hasattr(optmodule, 'GLOBAL_GIF_ARGS'):
            args = optmodule.GLOBAL_GIF_ARGS.copy()
        else:
            args = {}
        args.update(argspec3d)
        print(args)
        # threedimensionalgif.makeanimate(args)

# Make 2D plots
if hasattr(optmodule, 'ARGS2D'):
    for argspec2d in optmodule.ARGS3D:
        if hasattr(optmodule, 'GLOBAL_GIF_ARGS'):
            args = optmodule.GLOBAL_GIF_ARGS.copy()
        else:
            args = {}
        args.update(argspec2d)
        print(args)
        # twodimensionalgif.makeanimate(args)
