# Notes on using the MITgcm with ice
These notes are intended to help setup the MITgcm model in configurations with ice. This mainly focuses on how to use the EXF, SEAICE, and THSICE packages.

## Overview
Some useful packages for running the MITgcm with ice are
  * [EXF](http://mitgcm.org/sealion/online_documents/node260.html): External forcing from meteorological data
  * [SEAICE](http://mitgcm.org/sealion/online_documents/node215.html): Ice dynamics and single-layer thermodynamics
  * [THSICE](http://mitgcm.org/sealion/online_documents/node214.html): Improved ice thermodynamics
  * [Diagnostics](http://mitgcm.org/public/r2_manual/latest/online_documents/node269.html): Controlling output data fields

The most general model setup would require all three of these packages to be compiled and used at runtime, along with the `cal` package which EXF requires.

## External Forcing
This package allows you to force the model with air temperature, wind, humidity, radiation etc. To effect the water temperature, the model needs at least air temperature, humidity, downward shortwave and longwave radiation, and winds. There is more detail in the [documentation](http://mitgcm.org/sealion/online_documents/node261.html), but at least a few of the possible fields must be specified, with values in the particular ranges. The model works when the following fields are specified

Field name  |   Description       | Typical range
----------- | ------------------- | ----------------
uwind       | Surface (10-m) zonal winds in m/s | -10 < uwind < 10
vwind       | Surface (10-m) meridional winds in m/s |  -10 < vwind < 10
atemp       | Surface (2-m) air temperature in deg K |  200 < atemp < 300
aqh         | Surface (2-m) air humidity in kg/kg    |  0 < aqh < 0.02
swdown      | Downward shortwave radiation in W/m^2  |  0 < swdown < 450
lwdown      | Downward longwave radiation in W/m^2   |  50 < lwdown < 450

Initial state files should be put into `data.exf` in the namelist `&EXF_NML_02` with the name "[fieldname]file". For example, include the line

    uwindfile = 'initial_x_wind.bin'
to include the initial x-direction winds.

## THSICE
The Thermodynamic Seaice package includes improved thermodynamics compared to the SEAICE package. Including just the THSICE package lets ice form, but the ice is not dynamic.

The [THSICE documentation](http://mitgcm.org/sealion/online_documents/node214.html) has some information, but is outdated and incomplete.

To make the THSICE model work, the EXF package must be included, and enough fields must be specified to cool the water. Compile the model including the THSICE package, and add `useTHSICE = .TRUE.` to `data.pkg`. Parameters to control THSICE are in the file `data.ice`. One of the more important parameters is `hIceMin`. In the documentation it is often still referred to as `himin`, but in the model it has been renamed to `hIceMin`. From the documentation,

>If the current ice height is less than [hIceMin] then the ice layer is set to zero and the ocean model upper layer temperature is allowed to drop lower than its freezing temperature; and atmospheric fluxes are allowed to effect the grid cell. If the ice height is greater than [hIceMin] we proceed with the ice model calculation.

Therefore, for reasonably small time steps the default value 0.01 might not be small enough, and a smaller value should be specified. The `data.ice` file below worked to form ice on a small rectangular lake with very cold air temperature (240 K).


### Initial configuration
Initial ice area, thickness, and snow thickness should be specified in the `THSICE_PARM01` namelist with the lines
  * `thSIceFract_InitFile = ...` to set initial ice area fraction
  * `thSIceThick_InitFile = ...` to set initial ice thickness
  * `thSiceSnowH_InitFile = ...` to set initial snow height

### data file
The line `tracForcingAB=1` must be included in the data file in `PARM03`. For example, see the following data file

    ## data

    # Continuous equation parameters
     &PARM01
     tRef=,
     sRef=20*0.,
     tempAdvScheme=33,
     no_slip_sides=.FALSE.,
     no_slip_bottom=.TRUE.,
     f0=1.E-4,
     beta=0.E-11,
     tAlpha=2.E-4,
     sBeta =0.,
     gravity=9.81,
     rhonil=1000.,
     rigidLid=.FALSE.,
     implicitFreeSurface=.TRUE.,
     nonHydrostatic=.FALSE.,
     eosType='LINEAR',
     hFacMin=0.5,
     bottomDragLinear=0.E-4,
     bottomDragQuadratic=0.003,
     staggerTimeStep=.TRUE.,
     implicitDiffusion=.TRUE.,
     implicitViscosity=.TRUE.,
     usesinglecpuio=.TRUE.,
     exactConserv=.TRUE.,
     readBinaryPrec=64,
     viscAhGridMax=1.,
     viscC2Smag=2.2,
     viscAh=0.1,
     viscAz=1.E-6,
     diffKzT=3.E-5,
     diffKzS=3.E-5
     &
    # Elliptic solver parameters
     &PARM02
     cg2dMaxIters=600,
     cg2dTargetResidual=1.E-8,
     cg3dMaxIters=300,
     cg3dTargetResidual=1.E-8,
     &
    # Time stepping parameters
     &PARM03
     startTime=0.,
     endTime=1209600.0,
     deltaT=30.0,
     abEps=0.1,
     dumpFreq=0.0,
     monitorFreq=0.0,
     tracForcingOutAB=1,  # <----- necessary for THSICE
     &
    # Gridding parameters
     &PARM04
     usingCartesianGrid=.TRUE.,
     usingSphericalPolarGrid=.FALSE.,
     delX=60*100.00,
     delY=60*100.0,
     delZ=20*0.5

     &
     &PARM05
     bathyFile='bathymetry.bin',
     hydrogThetaFile='initial_temp.bin',
     &

### data.ice
Parameters related to the THSICE package are specified in `data.ice`. For example,

    ## data.ice

    &THSICE_CONST
    Tf0kel  = 273.15,
    iceMaskMin = 0.05,
    hiMax      = 10.,
    hsMax      = 10.,
    hIceMin    = 0.0,   # <---- To ensure ice grows
    &

    &THSICE_PARM01
    StartIceModel=1,
    # thSIceFract_InitFile = 'initial_area.bin',
    # thSIceThick_InitFile = 'initial_heff.bin',
    # thSIceSnowH_InitFile = 'initial_snow.bin',
    &

### data.diagnostics
See the section on diagnostics. For this run, the diagnostics file might look like


    ## data.diagnostics

    # Diagnostic Package Choices
    #-----------------
    # for each output-stream:
    #  filename(n) : prefix of the output file name (only 8.c long) for outp.stream n
    #  frequency(n):< 0 : write snap-shot output every |frequency| seconds
    #               > 0 : write time-average output every frequency seconds
    #  timePhase(n)     : write at time = timePhase + multiple of |frequency|
    #  averagingFreq(n) : frequency (in s) for periodic averaging interval
    #  averagingPhase(n): phase     (in s) for periodic averaging interval
    #  repeatCycle(n)   : number of averaging intervals in 1 cycle
    #  levels(:,n) : list of levels to write to file (Notes: declared as REAL)
    #                 when this entry is missing, select all common levels of this list
    #  fields(:,n) : list of diagnostics fields (8.c) (see "available_diagnostics.log"
    #                 file for the list of all available diag. in this particular config)
    #-----------------
     &DIAGNOSTICS_LIST
    # diag_mnc     = .FALSE.,
    # dumpAtLast   = .TRUE.,
    #==============================
      frequency(1) = -21600.0,
      timePhase(1) = 0,
      fields(1, 1) = 'THETA',
      filename(1) = 'T',
    #-----------------
      frequency(2) = -21600.0,
      timePhase(2) = 0,
      fields(1, 2) = 'UVEL',
      filename(2) = 'U',
    #-----------------
      frequency(3) = -21600.0,
      timePhase(3) = 0,
      fields(1, 3) = 'VVEL',
      filename(3) = 'V',
    #-----------------
      frequency(4) = -21600.0,
      timePhase(4) = 0,
      fields(1, 4) = 'momVort3',
      filename(4) = 'momVort3',
    #-----------------
      frequency(5) = -21600.0,
      timePhase(5) = 0,
      fields(1, 5) = 'RHOAnoma',
      filename(5) = 'Rho',
    #-----------------
      frequency(6) = -21600.0,
      timePhase(6) = 0,
      fields(1, 6) = 'SI_Fract',
      filename(6) = 'SI_Fract',
    #----------------
      frequency(7) = -21600.0,
      timePhase(7) = 0,
      fields(1, 7) = 'SIflx2oc',
      filename(7) = 'SIflx2oc',
    #-----------------
      frequency(8) = -21600.0,
      timePhase(8) = 0,
      fields(1, 8) = 'SI_Thick',
      filename(8) = 'SI_Thick'
    #-----------------


## SEAICE
The SEAICE package includes ice dynamics as well as a simple thermodynamic model. With the above setup with THSICE, ice will form but will not move. ** I have not yet gotten the ice to drift with the THSICE package though.

The SEAICE package uses `SEAICE_area_reg` and `SEAICE_hice_reg` similarly to `hIceMin` from THSICE. The default values might be too large for runs with a small timestep.

Initial configuration is specified in files `SEAICE_initial_HEFF`, `SEAICE_initialAREA`, etc.

The SEAICE package parameters are specified in `data.seaice`. The defualt parameters should work, so this file will be pretty minimal. The below file worked for me

    ## data.seaice

    # SEAICE parameters
    &SEAICE_PARM01
    SEAICEuseDYNAMICS   = .TRUE.,
    MIN_LWDOWN          = 5.0E1,
    SEAICE_area_reg     = 1.0E-5,
    SEAICE_hice_reg     = 1.0E-5,
    HeffFile            = 'initial_heff.bin',
    AreaFile            = 'initial_area.bin',
    HsnowFile           = 'initial_snow.bin',
    SEAICEadvArea        = .TRUE.,
    SEAICEadvSnow        = .TRUE.,
    SEAICEadvHeff        = .TRUE.,
    SEAICEscaleSurfStress=.TRUE.,
    SEAICEadvScheme      = 7,
    &
