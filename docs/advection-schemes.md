# MITgcm Advection Schemes
MITgcm has different options for numerical schemes to advect state variables, referred to as advection schemes. These become important when looking at ice, and comparing the SEAICE package to the THSICE package. The documentation for each has recommendations for which advection schemes to use.

The advection schemes are listed in the first section, and recommendations for the SEAICE and THSICE are listed after.

Advection schemes are selected by a token in one of the data files. The token is an integer, for example in

    thSIceAdvScheme = 77
The token is 77.
## List of advection schemes
These schemes are not listed anywhere in the documentation as far as I can tell, but they are listed in the header file `MITgcm/pkg/generic_advdiff/GAD.h`.

Token | Advection Scheme
----- | -----------------------
  1   | 1st-order upwind
  2   | 2nd-order centered difference
  3   | 3rd-order upwind
  4   | 3th-order centered difference
  7   | 7th-order one step method with monotonicity preserving limiter
  20  | 2nd-order direct space and time (Lax-Wendroff)
  30  | 3rd-order direct space and time
  33  | 3rd-order flux-limited direct space and time
  40  | Piecewise parabolic method with "null" limiter
  41  | Piecewise parabolic method with "mono" limiter
  42  | Piecewise parabolic method with "weno" limiter
  50  | Piecewise quartic method with "null" limiter
  51  | Piecewise quartic method with "mono" limiter
  52  | Piecewise quartic method with "weno" limiter
  77  | Non-linear flux limiter
  80  | 2nd-order moment advection scheme (Prather, 1986)
  81  | 2nd-order moment advection scheme, Prather Limiter

## SEAICEadvScheme
The SEAICE package advection scheme is controlled by the option

    SEAICEadvScheme = token

in the `PARM01` namelist of `data.seaice`.

The SEAICE package [documentation](http://mitgcm.org/public/r2_manual/latest/online_documents/node254.html) recommends,

> From the various advection scheme that are available in the MITgcm, we recommend flux-limited schemes [multidimensional 2nd and 3rd-order advection scheme with flux limiter [Hundsdorfer and Trompert, 1994; Roe, 1985] to preserve sharp gradients and edges that are typical of sea ice distributions and to rule out unphysical over- and undershoots (negative thickness or concentration). These schemes conserve volume and horizontal area and are unconditionally stable, so that we can set D_X = 0

For example, `SEAICEadvScheme = 33` would be a good choice according to this recommendation. This scheme is used by some of the `/verification` examples.

Advection scheme 7 is **not recommended** for the SEAICE package. With `SEAICEadvScheme = 7` the ice can form in grids which do not advect with the velocity field.

An example with advection scheme 7:

![Advection Scheme 7](https://github.com/timghill/gfg/blob/master/data/ice_gridding.png)

Compare to advection scheme 33:

![Advection Scheme 7](https://github.com/timghill/gfg/blob/master/data/ice_smooth.png)

## thSIceAdvScheme
The THSICE package advection scheme is constrolled by the option

    thSIceAdvScheme = token

in the `PARM01` namelist of `data.ice`.

The documentation for SEAICE recommends when using THSICE,
> To avoid unphysical (negative) values for ice thickness and concentration, a positive 2nd-order advection scheme with a SuperBee flux limiter [Roe, 1985] should be used to advect all sea-ice-related quantities of the Winton [2000] thermodynamic model (runtime flag thSIceAdvScheme=77 and thSIce_diffK= D_X =0 in data.ice, defaults are 0). [...]

Therefore, the following should always be in the `data.ice` file

    &THSICE_PARM01
    thSIceAdvScheme = 77,
    thSIce_diffK    = 0,
    ...
