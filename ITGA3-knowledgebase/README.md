## Project description

Using the public ClinVar data, build a relational database of the ITGA3 gene that stores its variant and classification details.
Query the database to find how many variants were classified as pathogenic or likely pathogenic. 
  * Used ITGA3 as an extension from a previous rare disease hackathon project focus
  * Created database with PostgreSQL
  * Built the ingestion script with Python to load data into the database (ETL)

### Data source 
[Clinvar](https://www.ncbi.nlm.nih.gov/clinvar/search/?gene=ITGA3&assembly=GRCh38), accessed on 20/9/2026 and available in the `data` folder as a tsv

### Entity-relationship diagram
[img](ITGA3-knowledgebase/schema-query/erd.png)

### Unsurprising finding from queries
VUS is the most common variant classification in ITGA3, accounting for 266 of 644 variants.

