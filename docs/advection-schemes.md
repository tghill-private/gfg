# MITgcm Advection Schemes
MITgcm has different options for numerical schemes to advect state variables, referred to as advection schemes. These become important when looking at ice, and comparing the SEAICE package to the THSICE package. The documentation for each has recommendations for which advection schemes to use.

The advection schemes are listed in the first section, and recommendations for the SEAICE and THSICE are listed after.

Advection schemes are selected by a token in one of the data files. The token is an integer, for example in

    thSIceAdvScheme = 77
The token is 77.
## List of advection schemes
These schemes are listed in the documentation in sections [2.17](https://mitgcm.readthedocs.io/en/latest/algorithm/algorithm.html#linear-advection-schemes) and [2.18](https://mitgcm.readthedocs.io/en/latest/algorithm/algorithm.html#non-linear-advection-schemes), and are compared in section [2.19](https://mitgcm.readthedocs.io/en/latest/algorithm/algorithm.html#comparison-of-advection-schemes). They are also listed in the header file `MITgcm/pkg/generic_advdiff/GAD.h`.

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

![Advection Scheme 7 [Link to image](https://github.com/timghill/gfg/blob/master/data/ice_gridding.png)](https://github.com/timghill/gfg/blob/master/data/ice_gridding.png)

Compare to advection scheme 33:

![Advection Scheme 7 [Link to image]((https://github.com/timghill/gfg/blob/master/data/ice_smooth.png))](https://github.com/timghill/gfg/blob/master/data/ice_smooth.png)

The default advection scheme is 2, a 2nd-order centered difference method. This method seems to create a lot more ice than expected, and a lot more ice than the other methods. With constant air and water temperatures of 2 degrees C, the default scheme covers the entire lake in ice, schemes 33 and 77 both advect the ice with the wind for some time, and slowly the ice melts. Therefore, scheme 33 and 77 are recommended.

## thSIceAdvScheme
The THSICE package advection scheme is controlled by the option

    thSIceAdvScheme = token

in the `PARM01` namelist of `data.ice`.

The documentation for SEAICE recommends when using THSICE,
> To avoid unphysical (negative) values for ice thickness and concentration, a positive 2nd-order advection scheme with a SuperBee flux limiter [Roe, 1985] should be used to advect all sea-ice-related quantities of the Winton [2000] thermodynamic model (runtime flag thSIceAdvScheme=77 and thSIce_diffK= D_X =0 in data.ice, defaults are 0). [...]

Therefore, the following should always be in the `data.ice` file

    &THSICE_PARM01
    thSIceAdvScheme = 77,
    thSIce_diffK    = 0,
    ...

However, when testing this scheme, the model reverts to NaN in the STDOUT.xxxx files after the first few time-steps. At this time, I can't recommend using the THSICE package along with ice dynamics. The good advection schemes for the SEAICE package seem to do an adequate job.
