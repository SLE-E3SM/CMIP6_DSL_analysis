
scenario=ssp126
index=r1i1p1f1


CMIP_BASE=/global/cfs/projectdirs/m3522/cmip6/CMIP6/ScenarioMIP
DEST=/pscratch/sd/h/hoffman2/DSL/zos_r1i1p1f1/$scenario

mkdir -p $DEST
mkdir -p $DEST/2015-2025
mkdir -p $DEST/2090-2100
mkdir -p $DEST/diff
mkdir -p $DEST/diff-remapped
mkdir -p $DEST/SLM

#./MPI-M/MPI-ESM1-2-LR/ssp585/r1i1p1f1/Omon/zos/gn/v20190710/zos_Omon_MPI-ESM1-2-LR_ssp585_r1i1p1f1_gn_209501-210012.nc
#
date
i=0
ii=0
for d1 in $CMIP_BASE/*/ ; do
    INST=`basename $d1`
    echo
    echo "***********************"
    echo d1=$d1
    for d2 in $d1/*/; do
       #echo d2=$d2
       MODEL=`basename $d2`
       #echo model=$MODEL
       d3=${d2}/${scenario}/${index}/Omon/zos/gn/
       if [ -d $d3 ]; then
          #echo d3=${d3}
          echo ver list=`ls -1d ${d3}/*`
          LASTVERDIR=`ls -1d --color=never ${d3}/* | sort -V | tail -n 1`
          echo lastver=${LASTVERDIR}

          path2015=`ls -1 --color=never ${LASTVERDIR}/zos*201501-*.nc`
          file2015=`basename $path2015`
          ncra -O -d time,0,120 $path2015 $DEST/2015-2025/${file2015}.2015-2025.nc

          path2100=`ls -1 --color=never ${LASTVERDIR}/zos*-210012.nc`
          file2100=`basename $path2100`
          ncra -O -d time,-120,-1 $path2100 $DEST/2090-2100/${file2100}.2090-2100.nc

          # diff time periods
          ncdiff -O $DEST/2090-2100/${file2100}.2090-2100.nc $DEST/2015-2025/${file2015}.2015-2025.nc $DEST/diff/${file2015}.2100-2015_diff.nc

          # remap to Gaussian grid
          ncremap -d /global/cfs/cdirs/fanssie/users/hoffman2/RSL/DSL_CMIP6/tgrid0.nc $DEST/diff/${file2015}.2100-2015_diff.nc $DEST/diff-remapped/${file2015}.2100-2015_diff_Gauss.nc

          # set up SLM run dir from template
          cp -R /global/cfs/cdirs/fanssie/users/hoffman2/RSL/DSL_CMIP6/SLM_template_dir $DEST/SLM/$MODEL
          # copy in remapped load change with correct name
          cp $DEST/diff-remapped/${file2015}.2100-2015_diff_Gauss.nc grdice1.nc
          # rename variable as needed
          ncrename -v zos,grdice grdice1.nc
          # set fill value to 0
          ncatted -a _FillValue,,o,f,0.0 grdice1.nc
          # remove fill value attribute
          ncatted -a _FillValue,,d,, grdice1.nc

        fi

    done
done
date
