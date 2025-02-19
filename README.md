# Bioinformatics Pipeline - Muthina

This tool processes mutation and methylation data (from Illumina platforms) using Python scripts and `bedtools`. It works with mutation data, methylation data (beta values), and methylation loci metadata downloaded from xenabrowser. It merges the data by genomic location based on a provided (optional) window and extracts unique genes within it. That is, it identifies genes within the regions of mutation and methylation sites.

## Installation

### Clone the Repository
```bash
git clone https://github.com/chisomgold/pipeline.git
cd pipeline
```

### Install Python Dependencies
Make sure you have Python installed (version 3.x), and then install the required packages:
```bash
pip install -r requirements.txt
```

### Install Bedtools
If `bedtools` is not installed on your system, you can install it with:
- On Ubuntu/Debian:
  ```bash
  sudo apt-get install bedtools
  ```

- On macOS:
  ```bash
  brew install bedtools
  ```
- On Linux/HPC with Conda environment
  ```bash
  conda install -c bioconda bedtools
  ```

### Input data
Somatic mutation zip file (.gz), DNA Methylation450k data (.gz), and DNA methylation ID mapping file of the same cancer type, all downloaded from the TCGA datasets on [xenabrowser](https://xenabrowser.net/datapages/).  The mutation file should be the public version option, not the gene-level non-silent mutation or other alternatives.

### Known Issues
The data formats expected for this pipeline are not standard (like vcf, for instance). This means that in the event of an update to the data format or structure on xenabrowser, including column header names, the pipeline might not work as expected. 

### Run the Pipeline
```bash
bash scripts/muthina.sh <mutation.zip> <methylation.zip> <methylation.txt> [optional: window size]
```
**Note** that the default window size is 1000bp on both sides of any given location.

### Example
Download mutation data (example)
```bash
wget https://gdc-hub.s3.us-east-1.amazonaws.com/download/TCGA-LAML.somaticmutation_wxs.tsv.gz
```
Download methylation data (example)
```bash
wget https://gdc-hub.s3.us-east-1.amazonaws.com/download/TCGA-LAML.methylation450.tsv.gz
```
Download methylation id data
```bash
wget https://gdc-hub.s3.us-east-1.amazonaws.com/download/HM450.hg38.manifest.gencode.v36.probeMap
```
Then run...
```bash
bash scripts/muthina.sh TCGA-LAML.somaticmutation_wxs.tsv.gz TCGA-LAML.methylation450.tsv.gz HM450.hg38.manifest.gencode.v36.probeMap 500
```
You should get a list of 10 genes intersected in that region. You will also find 2 files: `unique_gene.txt` with a list of all the genes present in affected regions and `merged_output.tsv` with more info on chromosome locations and mutation and methylation values.
