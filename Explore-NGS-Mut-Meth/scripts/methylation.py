#!/usr/bin/env python

import sys
import gzip
import pandas as pd

# Get the methylation files from command-line arguments
methylation_zip = sys.argv[1]
methylation_txt = sys.argv[2]

with gzip.open(methylation_zip, 'rt') as f:
    meth = pd.read_csv(f, sep='\t', header=0)

#open methylation identifier file
meth_id = pd.read_csv(methylation_txt, sep='\t', header=0)

meth_id_filter = meth_id[['#id', 'chrom', 'chromStart', 'chromEnd']]

# merging methylation table with the cg ids table
merged_meth = pd.merge(meth_id_filter, meth, how='inner', left_on=meth_id_filter.columns[0], right_on=meth.columns[0])

merged_meth['median_meth'] = merged_meth.median(axis=1, numeric_only=True)

#extracting meth data with chr regions
meth_data = merged_meth[['chrom', 'chromStart', 'chromEnd', 'median_meth']]
meth_data = meth_data[meth_data['chromStart'].isin([-1]) == False] # removing unknown sites

meth_data.to_csv(sys.stdout, sep='\t', index=False, header=False)
