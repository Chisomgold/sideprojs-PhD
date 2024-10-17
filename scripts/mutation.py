#!/usr/bin/env python

import sys
import gzip
import pandas as pd

# Get the mutation zip file from command-line argument
mutation_zip = sys.argv[1]

# Extract and process the mutation file (assuming it's a CSV inside the zip)
with gzip.open(mutation_zip, 'rt') as z:
    df = pd.read_csv(z, sep='\t', header=0)

# Create a new column for concatenated chr:start-end
df['Location'] = df['chrom'].astype(str) + ':' + df['start'].astype(str) + '-' + df['end'].astype(str)

#filter out the columns of interest
#df_filter = df.iloc[:, [0, df.columns.get_loc('Location')]]

#transform df to make unique samples column headers
new_df = pd.crosstab(index=df['Location'], columns=df.iloc[:, 0])

#calculating mean mutations
new_df['mean_mut'] = new_df.select_dtypes(include='number').mean(axis=1)
mut_data = new_df[['mean_mut']]

mut_data = mut_data.reset_index()
mut_data = mut_data.rename_axis(None, axis=1)

mut_data = mut_data[mut_data['mean_mut'] > mut_data['mean_mut'].min()] #selecting entries with more than 1 mutation in a location

#new table with chr range and mean mutation
mut_data[['chr', 'pos']] = mut_data['Location'].str.split(':', expand=True)
mut_data = mut_data[mut_data['pos'].str.contains('-', na=False)]
mut_data[['start', 'end']] = mut_data['pos'].str.split('-', n=1, expand=True)
mut_data = mut_data.drop(columns=['pos', 'Location'])
#reorder cols to fit bed format
mut_data = mut_data[['chr', 'start', 'end', 'mean_mut']]
mut_data = mut_data.dropna()
mut_data = mut_data.astype({'start' : 'int64', 'end':'int64'})
#merge with original data to get gene names
merged = pd.merge(mut_data, df, left_on = ['chr', 'start', 'end'], right_on = ["chrom", "start", "end"], how='inner')

# Output the processed data without a header
merged.to_csv(sys.stdout, sep='\t', index=False, header=False)
