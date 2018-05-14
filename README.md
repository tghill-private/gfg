# gfg
Geophysical Fluids Group files


## Installing requirements:
Most required python packages from requirements.txt are straightforward to install. The MITgcmutils package does not have a PyPI distribution, so below are some installation options.

### Install using virtualenv
The easiest way to track dependencies for a project, manage required package versions, and install from source is to use a python virtual environment. This guide is good http://docs.python-guide.org/en/latest/dev/virtualenvs/.

With the virtual environment activated, navigate to the python utilities folder `$MITGCM/utils/python/MITgcmutils`. Run

    python setup.py install
    
and the MITgcmutils python package should install somewhere in the virtualenv path.


### Install without virtualenv
It should also be possible to install MITgcmutils without using a virtualenv by specifying the installation directory and potentially adding this to your python path. Either specify `--prefix=install/path` where `install.path` is somewhere in your python path, or add the line `export PYTHONPATH="${PYTHONPATH}:/install\path` to the `.bashrc` file.
