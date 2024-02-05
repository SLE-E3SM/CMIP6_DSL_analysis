
scenario=ssp585
index=r1i1p1f1


CMIP_BASE=/global/cfs/projectdirs/m3522/cmip6/CMIP6/ScenarioMIP
DEST=/pscratch/sd/h/hoffman2/DSL/zos_all/$scenario
DEST=/pscratch/sd/h/hoffman2/DSL/zos_r1i1p1f1/$scenario

mkdir -p $DEST
find $CMIP_BASE -wholename "*${scenario}/${index}/*/gn/*/zos_*nc" -exec cp "{}" $DEST  \;
#find $CMIP_BASE -wholename "*${scenario}/*/zos_*nc" -exec ls -althr "{}"  \;
#
#
#2-1/ssp585/r1i1p1f2/Omon/zos/gn/v20190328/zos_Omon_CNRM-ESM
