# Notes on required modules
The Graham modules can produce some unexpected modules with compiling and running the MITgcm model. Most often errors occur when compiling the model. This page contains module lists which have worked for certain compilation scenarios.

## Compiling on a single cpu
This module list is relevant for compiling the MITgcm on a single cpu, using the following commands (depending on your code and optfile directories)

    ../../tools/genmake2 -mods ../code -of ../../tools/build_options/graham_mpi -mpi
    make depend
    make

* StdEnv/2016.4
* nixpkgs/16.09
* imkl/11.3.4.258
* intel/2016.4
* openmpi/2.1.1

## Compiling in parallel
CMake uses the flag `-j` to compile in parallel. That is, to compile with the following commands

    ../../tools/genmake2 -mods ../code -of ../../tools/build_options/graham_mpi -mpi
    make depend
    make

The following modules should be loaded
* StdEnv/2016.4
* nixpkgs/16.09
* imkl/11.3.4.258
* intel/2016.4
* openmpi/2.1.1
* hdf5/1.8.18
* netcdf-mpi/4.1.3
