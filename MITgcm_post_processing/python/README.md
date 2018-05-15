# README for python post-processing routines.

## Usage
Specify parameters for the plots in `generateGifs.py`. Use the 2D or 3D function according to whether your dataset is 2D or 3D.

## Plotting Parameters

### 3D Datasets
Create a gif animation and still frame images of slices of a 3D data set.

Uses netCDF4 files converted from MITgcm binary output (.data) files.
Automatically creates a .gif animation and saves each frame as a still
image.

Parameters:

Required:

Name        |   Description
----        |   ------------------
var         |   Variable prefix to plot. This is the prefix of the MITgcm binary output files. eg 'T', 'Rho'.
movie_name  |   Filename to save the gif animation. This works with or without the .gif. extension
cut_var     |   Axis to take a constant slice of. One of 'x', 'y' or 'z'.
cut_val     |   Value to take a slice at. Must be a level in the model data.
start_time  |   Time (sec) for the start of the run (or specific set of iterations)
sec_per_iter|   Seconds per model iteration.

Optional:

Name                |   Default     |   Description
--------------------|---------------|--------------------
iters               |   None        |   If None, use all iterations for matching file names. Otherwise,  can be a list of iteration numbers. Iterations are auto zero padded to 10 digits
vmin                |   None (auto) |   Colour scale min
vmax                |   None (auto) |   Colour scale max
image_folder_name   |   PNG_IMAGES  |   Directory to save image files in
gif_folder_name     |   GIF_IMAGES  |   Directory to save animation in
image_name          |   still_.png  |   Name to save images as.The model iteration number is put before the file extension
bathy_file_name     |   bathymetry.bin| Name of bathymetry file. If None do not apply land mask
namespec            |   output_{iter}.nc    |   Specifies a file name pattern for the .nc files
fps                 |   2           |   Frames per second in the output .gif animation
cmap                |   'Spectral_r|   Colour map for animation
dpi                 |   200         |   Resolution for still frames
plot_type           |   'gs'        |   One of None, 'gs', 'contour' or 'interp'. None: pcolormesh with no shading/interpolation. gs: pcolormesh with gouraud shading. interp: imshow with interpolation.
interp_type         |   'bilinear'  |   Interpolation type. See [pyplotimshow documentation](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.imshow.html)
aspect              |   'auto'      |   One of 'auto' or number. Auto uses a 4:3 aspect ratio; Passing a number forces that aspect ratio

### 2D Datasets


2d data descriptions
-----------------------------
Create a gif animation and still frame images of a 2D data set.

Uses netCDF4 files converted from MITgcm binary output (.data) files.
Automatically creates a .gif animation and saves each frame as a still
image.

Parameters:

Required:

    Name        |   Description
    ------------|-------------------
    var         :   Variable prefix to plot. This is the prefix of the
                    MITgcm binary output files. eg 'T', 'Rho'.

    movie_name  :   Filename to save the gif animation. This works with
                    or without the .gif. extension

    start_time  :   Time (sec) for the start of the run (or specific
                    set of iterations)

    sec_per_iter:   Seconds per model iteration.
    ------------|-------------------

Optional:

    Name                |   Default     |   Description
    --------------------|---------------|--------------------
    iters               :   None        :   If None, use all iterations for
                                            matching file names. Otherwise,
                                            can be a list of iteration
                                            numbers. Iterations are
                                            auto zero padded to 10 digits

    vmin                :   None (auto) :   Colour scale min

    vmax                :   None (auto) :   Colour scale max

    image_folder_name   :   PNG_IMAGES  :   Directory to save image files in

    gif_folder_name     :   GIF_IMAGES  :   Directory to save animation in

    image_name          :   still_.png  :   Name to save images as. The
                                            model iteration number is
                                            put before the file
                                            extension. The extension given
                                            here specifies what file format
                                            to save the image as

    namespec            :   output_{iter}.nc    :   Specifies a file name
                                                    pattern for the .nc
                                                    files

    fps                 :   2           :   Frames per second in the
                                            output .gif animation

    cmap                :   'Blues'     :   Colour map for animation

    dpi                 :   200         :   Resolution for still frames

    plot_type           :   'gs'        :   One of None, 'gs', 'contour'
                                            or 'interp'.
                                            None: pcolormesh with no
                                                    shading/interpolation
                                            gs: pcolormesh with
                                            gouraud shading
                                            interp: imshow with
                                            interpolation

    interp_type         :   'bilinear'  :   Interpolation type. See pyplot
                                            imshow documentation
    https://matplotlib.org/api/_as_gen/matplotlib.pyplot.imshow.html

    aspect              :   'auto'      :   One of 'auto' or number.
                                            Auto uses a 4:3 aspect
                                            ratio; Passing a number
                                            forces that aspect ratio

    ice_velocity_field  :   True        :   Overlay a direction field of
                                            the ice velocity (from UICE
                                            and VICE)

    stride              :   3           :   stride length for picking
                                            data to splot for ice velocity
                                            field. ie, if stride = 3,
                                            only shows every an arrow for
                                            every 3rd data point

    scale               :   20          :   Scale for ice velocity field
                                            arrow size. A larger scale
                                            means smaller arrows; smaller
                                            scale means larger arrows.

    --------------------|---------------|--------------------
