#!/bin/bash

# Check for correct number of arguments
if [ $# -lt 3 ]; then
    echo "Usage: $0 <mutation.zip> <methylation.zip> <methylation.txt> [optional: bedtools window size]"
    exit 1
fi

# Input files
mutation_file=$1
methylation_zip=$2
methylation_txt=$3
window_size=${4:-0}

echo "processing mutation data"
python3 mutation.py "$mutation_file" > processed_mutation.tsv

echo "processing methylation data"
python3 methylation.py "$methylation_zip" "$methylation_txt" > combined_methylation.tsv

#Remove lines with -1 in combined methylation file using grep
# grep -v '\t-1\t' combined_methylation.tsv > filtered_methylation.tsv

#merge files using bedtools
if [ "$window_size" -gt 0 ]; then
    bedtools window -w "$window_size" -a processed_mutation.tsv -b combined_methylation.tsv > merged_output.tsv
else
    bedtools window -a processed_mutation.tsv -b combined_methylation.tsv > merged_output.tsv
fi

cut -f 9 merged_output.tsv | sort | uniq > unique_genes.txt

# Display the unique genes to the user
echo "Some affected genes:"
head unique_genes.txt

# Cleanup: Remove intermediate files
rm processed_mutation.tsv combined_methylation.tsv #filtered_methylation.tsv

echo "Run complete. Output saved as merged_output.tsv, and affected genes saved in unique_genes.txt."



