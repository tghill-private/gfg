import argparse

import netCDF4
import numpy as np
from matplotlib import pyplot as plt

class MITgcmNC:
	def __init__(self, nc4file):
		self.nc4 = netCDF4.Dataset(nc4file, 'r')

	def surf_2d_slice(self):
		X = np.array(self.nc4['x'])
		Y = np.array(self.nc4['y'])
		Z = np.array(self.nc4['z'])

		Xgrid, Ygrid = np.meshgrid(X,Y)
		zlevel = Z[-1]

		Tslice = np.array(self.nc4['T'][:, :, -1])

		fig, ax = plt.subplots()

		ax.pcolormesh(Xgrid, Ygrid, Tslice)

		fig.colorbar()

		fig.savefig('MITgcmpyvis.png',dpi = 500)
		

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("file",help = "netCDF4 file to visualize")
	args = parser.parse_args()

	print("Visualizing file %s" % args.file)

	data = MITgcmNC(args.file)

	data.surf_2d_slice()

if __name__== "__main__":
	main()
