from pathlib import Path
import pandas as pd

# --------------------------------------------------
# File paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "clinvar_download_20260920.tsv"

# --------------------------------------------------
# Read source TSV
# --------------------------------------------------

df = pd.read_csv(
    DATA_FILE,
    sep="\t",
    keep_default_na=False,
    usecols=range(24)
)

# --------------------------------------------------
# 1. Gene table
# --------------------------------------------------

gene_rows = []
gene_symbol_to_id = {}

for gene_value in df["Gene(s)"]:
    if not gene_value:
        continue

    # A row can contain multiple genes separated by "|"
    genes = gene_value.split("|")

    for gene_symbol in genes:
        gene_symbol = gene_symbol.strip()

        if not gene_symbol:
            continue

        if gene_symbol not in gene_symbol_to_id:
            gene_id = len(gene_symbol_to_id) + 1
            gene_symbol_to_id[gene_symbol] = gene_id

            gene_rows.append({
                "gene_id": gene_id,
                "gene_symbol": gene_symbol,
            })


gene_df = pd.DataFrame(
    gene_rows,
    columns=["gene_id", "gene_symbol"],
)


# --------------------------------------------------
# 2. Variant table
# --------------------------------------------------

variant_rows = []

for _, row in df.iterrows():

    canonical_spdi = row["Canonical SPDI"]

    spdi_parts = canonical_spdi.split(":")

    if len(spdi_parts) >= 4:
        position = spdi_parts[1]
        ref = spdi_parts[2]
        alt = spdi_parts[3]
    else:
        position = ""
        ref = ""
        alt = ""

    variant_rows.append({
        "variant_id": row["VariationID"],
        "chromosome": row["GRCh38Chromosome"],
        "genomic_position": position,
        "reference": ref,
        "alternate": alt,
        "canonical_spdi": canonical_spdi,
        "variant_type": row["Variant type"],
    })


variant_df = pd.DataFrame(
    variant_rows,
    columns=[
        "variant_id",
        "chromosome",
        "genomic_position",
        "reference",
        "alternate",
        "canonical_spdi",
        "variant_type",
    ]
)
variant_df["genomic_position"] = variant_df["genomic_position"].apply(
    lambda x: int(x) if pd.notna(x) and str(x).strip() != "" else None
)


# --------------------------------------------------
# 3. Variant-gene bridge table
# --------------------------------------------------

variant_gene_rows = []

for _, row in df.iterrows():

    variant_id = row["VariationID"]
    gene_value = row["Gene(s)"]

    if not gene_value:
        continue

    genes = gene_value.split("|")

    for gene_symbol in genes:
        gene_symbol = gene_symbol.strip()

        if not gene_symbol:
            continue

        gene_id = gene_symbol_to_id[gene_symbol]

        variant_gene_rows.append({
            "variant_id": variant_id,
            "gene_id": gene_id,
        })


variant_gene_df = pd.DataFrame(
    variant_gene_rows,
    columns=["variant_id", "gene_id"],
)

# --------------------------------------------------
# 4. Source table
# --------------------------------------------------

source_df = pd.DataFrame([
    {
        "source_id": 1,
        "source_name": "clinvar",
        "access_date": "20/9/2026",
    }
]).astype({
    "access_date": "datetime64[ns]"
})


# --------------------------------------------------
# 5. Annotation table
# --------------------------------------------------

classification_rows = []

for classification_id, (_, row) in enumerate(df.iterrows(), start=1):

    classification_rows.append({
        "classification_id": classification_id,
        "classification_value": row["Germline classification"],
        "eval_date": row["Germline date last evaluated"],
        "review_status": row["Germline review status"],
        "variant_id": row["VariationID"],
        "source_id": 1,
    })


classification_df = pd.DataFrame(
    classification_rows,
    columns=[
        "classification_id",
        "classification_value",
        "eval_date",
        "review_status",
        "variant_id",
        "source_id",
    ],
).astype({
    "eval_date" : "datetime64[ns]"
})


# --------------------------------------------------
# Integrity checks
# --------------------------------------------------

# # 1. Count genes in row 1 of the source data
# gene_count = len([
#     gene
#     for gene in df.iloc[0, 1].split("|")
#     if gene.strip()
# ])

# # Count variant_gene rows for the corresponding variant
# first_variant_id = df.iloc[0]["VariationID"]

# variant_gene_count = (
#     variant_gene_df["variant_id"] == first_variant_id
# ).sum()

# print("\n=== INTEGRITY CHECKS ===")

# print(
#     f"Row 1 gene count: {gene_count}"
# )

# print(
#     f"variant_gene rows for variant {first_variant_id}: "
#     f"{variant_gene_count}"
# )

# print(
#     "Gene count matches variant_gene count:",
#     gene_count == variant_gene_count
# )
# print ("If False, data integrity may be compromised")... assert?

# # 2. Check all ID columns
# id_columns = {
#     "gene": ["gene_id"],
#     "variant": ["variant_id"],
#     "variant_gene": ["variant_id", "gene_id"],
#     "source": ["source_id"],
#     "classification": ["classification_id", "variant_id", "source_id"],
# }

# print("\n=== ID CHECKS ===")

# for table_name, columns in id_columns.items():

#     table = {
#         "gene": gene_df,
#         "variant": variant_df,
#         "variant_gene": variant_gene_df,
#         "source": source_df,
#         "classification": classification_df,
#     }[table_name]

#     for column in columns:

#         # Check for null/empty values
#         null_count = table[column].isna().sum()
#         empty_count = (table[column].astype(str).str.strip() == "").sum()

#         print(
#             f"{table_name}.{column}: "
#             f"null={null_count}, "
#             f"empty={empty_count} "
#         )


from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg://username:password@localhost:5432/ITGA3_var"
)

with engine.connect() as connection:
    results = connection.exec_driver_sql("SELECT 1")
    print(results.scalar())

#sned to db
with engine.begin() as connection:

    source_df.to_sql(
        "source",
        connection,
        if_exists="append",
        index=False,
    )

    gene_df.to_sql(
        "gene",
        connection,
        if_exists="append",
        index=False,
    )

    variant_df.to_sql(
        "variant",
        connection,
        if_exists="append",
        index=False,
    )

    variant_gene_df.to_sql(
        "variant_gene",
        connection,
        if_exists="append",
        index=False,
    )

    classification_df.to_sql(
        "classification",
        connection,
        if_exists="append",
        index=False,
    )
