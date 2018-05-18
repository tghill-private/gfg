##Set parameters##
#grid dimensions
nx = 20
ny = 16
nz = 23
#grid resolutions
dx = "2"
dy = "3"
dz = "5"
#time information
start_time = 3600
end_time = 36000
sec_per_iter = 3600
sec_per_file = 3600
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
