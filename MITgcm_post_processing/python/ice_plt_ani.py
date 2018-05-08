"""

    module ice_plt_ani.py

    Plot sea ice fraction with overlaid wind direction field from MITgcm
    model runs.

    This module makes animations from converted netCDF4 files, which should have
    been converted from the binary .data files from datnetcdf.py

"""

"""
import imageio

filenames = ['image%s.png' % str(12*x).zfill(10) for x in list(range(11))]

def main():
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    imageio.mimsave('GIF_MOVIE/movie.gif', images)

if __name__ == "__main__":
    main()
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import gridspec

writer = animation.ImageMagickFileWriter(fps = 5)

y, x = np.meshgrid(np.linspace(-10, 10,100), np.linspace(-10, 10,100))
z = np.sin(x)*np.sin(x)+np.sin(y)*np.sin(y)
###########

fig = plt.figure(facecolor='white')
gs = gridspec.GridSpec(1, 1)
ax1 = plt.subplot(gs[0,0])

pcolor = ax1.pcolormesh(x, y, z,)
ax1.set_xlim(-10,10)
ax1.set_ylim(0,1)
ax1.set_xlabel('time')
ax1.set_ylabel('amplitude')
ax1.set_title('Oscillationsssss')
time_text = ax1.text(0.02, 0.95, '', transform=ax1.transAxes)

def init():
    pcolor.set_array([])
    return pcolor

def animate(iter):
    z = np.sin(x-iter/(2*np.pi))*np.sin(x-iter/(2*np.pi))+np.sin(y)*np.sin(y)
    # see https://stackoverflow.com/questions/18797175/animation-with-pcolormesh-routine-in-matplotlib-how-do-i-initialize-the-data
    z = z[:-1, :-1]
    pcolor.set_array(z.ravel())
    return pcolor

gs.tight_layout(fig)

anim = animation.FuncAnimation(fig,animate,frames=100,interval=50,blit=False,repeat=False)

anim.save('image.gif', writer=writer)
