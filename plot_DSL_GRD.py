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


ds_dsl = xr.open_dataset('grdice1.nc')
if len(ds_dsl.grdice.dims) == 3:
    DSL = ds_dsl.grdice.values[0,:,:]
elif len(ds_dsl.grdice.dims) == 2:
    DSL = ds_dsl.grdice.values[:,:]
else:
    sys.exit('Unexpected dimensions found for DSL')

ds_tgrid0 = xr.open_dataset('OUTPUT_SLM/tgrid0.nc')
ds_tgrid1 = xr.open_dataset('OUTPUT_SLM/tgrid1.nc')

GRD = ds_tgrid0.tgrid.values - ds_tgrid1.tgrid.values
lat = ds_tgrid0.lat
lon = ds_tgrid0.lon

ds_G1 = xr.open_dataset('OUTPUT_SLM/G1.nc')
G = ds_G1.G.values

ds_R1 = xr.open_dataset('OUTPUT_SLM/R1.nc')
R = ds_R1.R.values

fig = plt.figure(figsize=(8, 7))
nlevs = 10
cmap='RdBu'

ax = fig.add_subplot(2, 1, 1, projection=ccrs.Robinson())
ax.set_global()
rng_DSL = np.absolute(DSL).max()
rng_DSL = 0.5
cflevs = np.linspace(-rng_DSL, rng_DSL, num=nlevs*2+1, endpoint=True)
cbarticks = np.linspace(-rng_DSL, rng_DSL, num=nlevs+1, endpoint=True)
#print(cbarticks)
cf1 = ax.contourf(lon, lat, DSL, cflevs,
                  transform=ccrs.PlateCarree(),
                  #vmin=-rng_DSL, vmax=rng_DSL,
                  cmap=cmap, extend='both')
ax.coastlines()
plt.colorbar(cf1, ax=ax, label='DSL (m)', ticks=cbarticks)

ax = fig.add_subplot(2, 1, 2, projection=ccrs.Robinson())
ax.set_global()
rng_GRD = np.absolute(GRD).max()
rng_GRD = 0.05
cflevs = np.linspace(-rng_GRD, rng_GRD, num=nlevs*2+1, endpoint=True)
cbarticks = np.linspace(-rng_GRD, rng_GRD, num=nlevs+1, endpoint=True)
cf2 = ax.contourf(lon, lat, GRD, cflevs,
                  transform=ccrs.PlateCarree(),
                  #vmin=-rng_GRD, vmax=rng_GRD,
                  cmap=cmap, extend='both')
ax.coastlines()
plt.colorbar(cf2, ax=ax, label='GRD (m)', ticks=cbarticks)

plt.suptitle(f'{model}, {experiment}')

plt.draw()
plt.savefig(f'DSL_GRD_{model}.png')

# ratio figure

ratio = GRD / DSL
ratio[np.logical_not(np.isfinite(ratio))] = 0.0
ratio[ratio>1] = 0.0
ratio[ratio<-1] = 0.0

fig = plt.figure(2, figsize=(8, 7))
ax = fig.add_subplot(2, 1, 1, projection=ccrs.Robinson())
ax.set_global()
rng = 0.3; nlevs = 6
cflevs = np.linspace(-rng, rng, num=nlevs*2+1, endpoint=True)
cbarticks = np.linspace(-rng, rng, num=nlevs+1, endpoint=True)
cf3 = ax.contourf(lon, lat, ratio, cflevs,
                  transform=ccrs.PlateCarree(),
                  #vmin=-rng_DSL, vmax=rng_DSL,
                  cmap=cmap, extend='both')
ax.coastlines()
plt.colorbar(cf3, ax=ax, label='GRD/DSL', ticks=cbarticks)

plt.draw()
plt.savefig(f'ratio_GRD_to_DSL_{model}.png')

ind = np.where(ratio != 0.0)[0]
mn = ratio[ind].mean()
print(f'mean GRD/DSL = {mn}')


# G & R

fig = plt.figure(3, figsize=(8, 7))

ax = fig.add_subplot(2, 1, 1, projection=ccrs.Robinson())
ax.set_global()
rng = 0.025; nlevs = 10
cflevs = np.linspace(-rng, rng, num=nlevs*2+1, endpoint=True)
cbarticks = np.linspace(-rng, rng, num=nlevs+1, endpoint=True)
cf = ax.contourf(lon, lat, G, cflevs,
                 transform=ccrs.PlateCarree(),
                 #vmin=-rng_DSL, vmax=rng_DSL,
                 cmap=cmap, extend='both')
ax.coastlines()
plt.colorbar(cf, ax=ax, label='G (m)', ticks=cbarticks)

ax = fig.add_subplot(2, 1, 2, projection=ccrs.Robinson())
ax.set_global()
rng = 0.025; nlevs = 10
cflevs = np.linspace(-rng, rng, num=nlevs*2+1, endpoint=True)
cbarticks = np.linspace(-rng, rng, num=nlevs+1, endpoint=True)
cf = ax.contourf(lon, lat, R, cflevs,
                 transform=ccrs.PlateCarree(),
                 #vmin=-rng_DSL, vmax=rng_DSL,
                 cmap=cmap, extend='both')
ax.coastlines()
plt.colorbar(cf, ax=ax, label='R (m)', ticks=cbarticks)

plt.draw()
plt.savefig(f'G_and_R_{model}.png')


plt.show()
