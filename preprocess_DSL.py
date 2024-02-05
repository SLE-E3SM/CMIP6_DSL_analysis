#!/usr/bin/env python

import pprint, sys, os, glob, shutil
import xarray as xr
import subprocess

cmip_base = '/pscratch/sd/h/hoffman2/DSL/pyesgf_test/'
experiment = 'ssp126'
output_base = '/pscratch/sd/h/hoffman2/DSL/processed_DSL_nco_idw'

model_paths = sorted(glob.glob(cmip_base + '/' + experiment + '/*/'))
print(model_paths)
for model_path in model_paths:
    print("========================\n")
    print(model_path)
    nc_files = glob.glob(model_path + '/*.nc')


    if len(nc_files) > 0:
        model = model_path.split('/')[-2]
        print(model)
        print(f"Processing {model_path + '/*.nc'}")

        model_out_path = os.path.join(output_base, experiment, model)
        os.makedirs(model_out_path, exist_ok=True)

        try:
            ds = xr.open_mfdataset(model_path + '/zos*.nc', lock=False, use_cftime=True)
        except:
            print('opening dataset failed')
            continue

        ds_first_decade = ds.sel(time=slice('2015', '2024')).mean(dim='time')
        print(f"Writing 'zos_{model}_2015-2024.nc'")
        try:
            ds_first_decade.to_netcdf(os.path.join(model_out_path, f'zos_{model}_2015-2024.nc'))
        except:
            print('writing first decade failed')
            continue

        ds_last_decade = ds.sel(time=slice('2091', '2100')).mean(dim='time')
        print(f"Writing 'zos_{model}_2091-2100.nc'")
        try:
            ds_last_decade.to_netcdf(os.path.join(model_out_path, f'zos_{model}_2091-2100.nc'))
        except:
            print('writing last decade failed')
            continue

        ds_diff = ds_last_decade
        ds_diff.zos.values = ds_last_decade.zos.values - ds_first_decade.zos.values
        ds_diff.fillna(0.0)

        diff_path = os.path.join(model_out_path, f'zos_{model}_diff.nc')
        print(f"Writing diff file")
        try:
            ds_diff.to_netcdf(diff_path)
        except:
            print('writing diff failed')
            continue

        #print('removing fill value')
        #subprocess.run(['ncatted', '-a', '_FillValue,,o,f,0.0', diff_path])
        #subprocess.run(['ncatted', '-a', '_FillValue,,d,,', diff_path])

        print('remapping')
        remapped_path = f"{diff_path.split('.')[:-1][0]}_Gauss.nc"

        cmd = ['ncremap',
               #'-d', '/global/cfs/cdirs/fanssie/users/hoffman2/RSL/DSL_CMIP6/tgrid0.nc',
               '-G', 'latlon=512,1024#lat_typ=gss',
               '-g', os.path.join(model_out_path, 'grid.nc'),
               '-v', 'zos',
               '-a', 'nco_idw',
               '-i', diff_path, 
               '-o', remapped_path]
        print(cmd)
        try:
            subprocess.check_call(cmd)
        except:
            print('ncremap failed')
            continue

        if os.path.exists(remapped_path):
            print('removing fill value')
            subprocess.run(['ncatted', '-a', '_FillValue,,o,f,0.0', remapped_path])
            subprocess.run(['ncatted', '-a', '_FillValue,,d,,', remapped_path])

            # set up SLM run dir from template
            slm_run_path = os.path.join(model_out_path, 'slm_run')
            if os.path.exists(slm_run_path):
                shutil.rmtree(slm_run_path)
            shutil.copytree('/global/cfs/cdirs/fanssie/users/hoffman2/RSL/DSL_CMIP6/SLM_template_dir', slm_run_path)
            # copy in remapped load change with correct name
            shutil.copyfile(remapped_path, os.path.join(slm_run_path, 'grdice1.nc'))
            # rename variable as needed
            subprocess.run(['ncrename', '-v', 'zos,grdice',
                            os.path.join(slm_run_path, 'grdice1.nc')])

            print(f'** SUCCESS: {model}')


