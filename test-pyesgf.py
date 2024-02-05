from pyesgf.search import SearchConnection
#conn = SearchConnection('https://esgf-data.dkrz.de/esg-search', distrib=True)
conn = SearchConnection('https://esgf-node.llnl.gov/esg-search', distrib=True)
facets='project,experiment_id,variable,ensemble,realm,source_id,grid_label,frequency'
ctx = conn.new_context(facets=facets,
    project='CMIP6',
    source_id='UKESM1-0-LL',
    experiment_id='ssp585',
    variable='zos',
    frequency='mon',
    grid_label='gn,gr',
    replica=False,
    latest=True
    )
print('Hits: {}, Realms: {}, Ensembles: {}'.format(
    ctx.hit_count,
    ctx.facet_counts['realm'],
    ctx.facet_counts['ensemble']))
print(ctx.hit_count)


ds = ctx.search(facets=facets)
print(f'ds={len(ds)}')
for d in ds:
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
