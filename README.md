# Bioinformatics Pipeline - Mutathem

This tool processes mutation and methylation data using Python scripts and `bedtools`. It works with mutation and methylation zip files as well as methylation loci metadata downloaded from xenabrowser. It merges both data by genomic location based on the provided (optional) window and extracts unique genes.

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
Somatic mutation zip file (.gz), DNA Methylation450k data (.gz), and DNA methylation ID mapping file of the same cancer, all downloaded from the TCGA datasets on xenabrowser.  The mutation file should be the public version option, not the gene-level non-silent mutation or other alternatives.

### Run the Pipeline
```bash
bash scripts/mutathem.sh <mutation.zip> <methylation.zip> <methylation.txt> [optional: window size]
```

### Example
```bash
bash scripts/mutathem.sh data/mutation.zip data/methylation.zip data/methylation.txt 500
```
