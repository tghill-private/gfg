"""
    initconditions.py

    Create files specifying the initial conditions for MIZ simulations

    This sets the initial conditions for
     *  c - sea ice concentration
     *  h - sea ice thickness
     *  s - salinity
"""

import argparse
import os

import numpy as np

_xlim = (0., 150.e3)
_ylim = (-25.e3, 25.e3)
_zlim = (-100, 0)

Lf = 5.e3   # width of transition (5 km)
c0 = 0.50   # initial high concentration (50 %)
h0 = 2      # initial thickness at thick end (2 m)

# Mixed layer depths
Hm = 25     # freshwater mixed layer depth (25 m)
Hd = 35     # Salty deep mixed layer depth (35 m)

def write(ndarray):
    """saves an ndarray as tuples (x1, x2, ...)"""
    data = np.zeros((np.prod(ndarray.shape), ndarray.ndim))
    for ax in range(ndim):
        axis = (ndim-1) - ax


def set_ic(size, basename):
    """set_c sets the initial ice concentration in the domain"""
    nx, ny, nz = size
    z = _zlim[-1]
    k = nz - 1

    C = np.zeros(size)
    H = np.zeros(size)
    S = np.zeros(size)
    for i,x in enumerate(np.linspace(_xlim[0], _xlim[1], nx)):
        for j,y in enumerate(np.linspace(_ylim[0], _ylim[1], ny)):
            c = c0 * (0.5 + 0.5 * np.tanh(y / Lf))
            C[i, j, k] = c

            h = h0 * (0.5 + 0.5 * np.tanh(y / Lf))
            H[i, j, k] = h

    base, ext = os.path.split(basename)

    c_fname = base + "_c" + ext
    h_fname = base + "_h" + ext
    s_fname = base + "s" + ext

    write(c_fname, c)
    write(h_fname, h)
    write(s_fname, s)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("nx", help = "Number of x grid-points", type = int)
    parser.add_argument("ny", help = "Number of y grid-points", type = int)
    parser.add_argument("nz", help = "Number of z grid-points", type = int)
    parser.add_argument("filename", help = "Base filename to save data")
    args = parser.parse_args()

    size = (args.nx, args.ny, args.nz)
    set_ic(size, args.filename)

if __name__ == "__main__":
    main()
