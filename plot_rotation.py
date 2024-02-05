#!/usr/bin/env python

import xarray as xr
import matplotlib.pyplot as plt
#import matplotlib.colors as cols
#import matplotlib.ticker as mticker
#import matplotlib.patches as mpatches
import numpy as np
#from mpl_toolkits.axes_grid1 import make_axes_locatable
#from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import cartopy
import cartopy.crs as ccrs
import os, sys

#from cartopy.util import add_cyclic_point
#import netCDF4
#from pyproj import Transformer, transform, CRS
#import matplotlib.tri as tri
#from matplotlib.colors import Normalize, TwoSlopeNorm
#from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

cwd = os.getcwd()
model = cwd.split('/')[-2]
experiment = cwd.split('/')[-3]


ds_tgrid0 = xr.open_dataset('OUTPUT_SLM/tgrid0.nc')
ds_tgrid1 = xr.open_dataset('OUTPUT_SLM/tgrid1.nc')

GRD = ds_tgrid0.tgrid.values - ds_tgrid1.tgrid.values
lat = ds_tgrid0.lat
lon = ds_tgrid0.lon

ds_tgrid0 = xr.open_dataset('../slm_run_no_rotation/OUTPUT_SLM/tgrid0.nc')
ds_tgrid1 = xr.open_dataset('../slm_run_no_rotation/OUTPUT_SLM/tgrid1.nc')
GRD_no_tpw = ds_tgrid0.tgrid.values - ds_tgrid1.tgrid.values

diff = GRD - GRD_no_tpw


fig = plt.figure(3, figsize=(8, 7))
cmap='RdBu'

ax = fig.add_subplot(2, 1, 1, projection=ccrs.Robinson())
ax.set_global()
rng = 0.025; nlevs = 10
cflevs = np.linspace(-rng, rng, num=nlevs*2+1, endpoint=True)
cbarticks = np.linspace(-rng, rng, num=nlevs+1, endpoint=True)
cf = ax.contourf(lon, lat, diff, cflevs,
                 transform=ccrs.PlateCarree(),
                 #vmin=-rng_DSL, vmax=rng_DSL,
                 cmap=cmap, extend='both')
ax.coastlines()
plt.colorbar(cf, ax=ax, label='rotation (m)', ticks=cbarticks)

plt.draw()
plt.savefig(f'rotation_{model}.png')


plt.show()
