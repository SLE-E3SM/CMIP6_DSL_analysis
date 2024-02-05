#!/usr/bin/env python

from pyesgf.search import SearchConnection
import pprint, sys, os
import urllib

download_root = '/pscratch/sd/h/hoffman2/DSL/pyesgf_test'
experiment = 'ssp585'

#conn = SearchConnection('https://esgf-data.dkrz.de/esg-search', distrib=True)
conn = SearchConnection('https://esgf-node.llnl.gov/esg-search', distrib=True)
facets='project,experiment_id,variable,ensemble,realm,source_id,grid_label,frequency,variant_label'
ctx = conn.new_context(facets=facets,
    project='CMIP6',
#    source_id='UKESM1-0-LL',
    experiment_id=experiment,
    variable='zos',
    frequency='mon',
#    grid_label='gn,gr',
    replica=False,
    latest=True
    )
print(f"Hits: {ctx.hit_count}, source_id: {len(ctx.facet_counts['source_id'])}")

pprint.pprint(ctx.facet_counts['source_id'])

for src in ctx.facet_counts['source_id']:
    #print(ctx.facet_constraints)
    ctx_src = ctx.constrain(source_id=src)
    #print(ctx_src.facet_constraints)
    ctx_gn = ctx_src.constrain(grid_label='gn')
    #print(ctx_gn.facet_constraints)
    ctx_gr = ctx_src.constrain(grid_label='gr')
    #print(ctx_gr.facet_constraints)
    print(f'{src}: gn={ctx_gn.hit_count} gr={ctx_gr.hit_count}')

    ctx_use = None
    if ctx_gn.hit_count > 0:
        # use native grid
        print(f'Using native grid for {src}')
        ctx_use = ctx_gn
    elif ctx_gr.hit_count > 0:
        # if no native grid data exist, use regridded instead
        print(f'Using regridded grid for {src}')
        ctx_use = ctx_gr
    if ctx_use is not None:
        # turn list of variants into a sorted list so we can get the run closest to r1i1p1f1
        # NOTE: because variant numbers are not 0-padded, this will return r10 instead of r1 if there are that many - to be fixed later
        variant_list = sorted(list(ctx_use.facet_counts['variant_label']))
        print(f"Variants available={variant_list}")
        variant1 = variant_list[0]
        print(f"   using first variant={variant1}")
        ctx_use = ctx_use.constrain(variant_label=variant1)

        ds = ctx_use.search()
        for d in ds:
            files = d.file_context().search(facets=facets)
            print(f'   num files: {len(files)} in dataset_id={d.dataset_id}')
            for f in files:
                print(f.download_url)
                filename = os.path.basename(f.download_url)
                download_path = os.path.join(download_root, experiment, src)
                os.makedirs(download_path, exist_ok=True)
                fpath = os.path.join(download_path, filename)
                try:
                    urllib.request.urlretrieve(f.download_url, fpath)
                except:
                    print(f'   Download failed for {f.download_url}. Skipping the rest of this model')
                    break

sys.exit()


ds = ctx.search(facets=facets)
print(f'ds={len(ds)}')
for d in ds:
    # contents of d: ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__str__', '__subclasshook__', '__weakref__', 'aggregation_context', 'context', 'dataset_id', 'download_url', 'file_context', 'globus_url', 'gridftp_url', 'index_node', 'json', 'las_url', 'number_of_files', 'opendap_url', 'urls']
    print(f'dataset_id={d.dataset_id}')
    files = d.file_context().search(facets=facets)
    print(len(files))
    for f in files:
        print(f.download_url)


#ctx = ctx.constrain(ensemble='r1i1p1f1')
#print(ctx.hit_count)

#result = ctx.search()[0]
#agg_ctx = result.aggregation_context()
#agg = agg_ctx.search()[0]
#print(agg.opendap_url)

#result = ctx.search()[0]
#print(result.dataset_id)
#files = result.file_context().search()
#print(len(files))
#for file in files:
##    print(file.opendap_url)
