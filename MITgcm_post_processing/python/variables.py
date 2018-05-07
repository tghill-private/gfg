##Set parameters##
#grid dimensions
nx = 360
ny = 210
nz = 40
#grid resolutions
dx = "50"
dy = "50"
dz = "0.5"
#time information
start_time = 0
end_time = 21600
sec_per_iter = 10
sec_per_file = 600
#plot type
#options :  None = pcolormesh no shading,
#        'gs' = pcolormesh w shading,
#        'interp' = imshow interpolation
#        'contour' = contourf with automatic shading levels chosen
plot_type = 'contour'
    #if type is interp set interpolation type, see python imshow docs for options
interp_type = 'bilinear'
    #if type is contour, set max number of contour levels
contour_max = 50
