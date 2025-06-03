"""
Clean and standardize the Fisher dataset of US news domains.

This script processes the raw Fisher dataset which contains domain names and their
classification as local, regional, national, or international news outlets. It performs
the following steps:
1. Reads the raw CSV file
2. Keeps only the domain and classification columns
3. Removes duplicate entries
4. Handles special cases:
   - Removes subdomain classifications for certain regional domains
   - Resolves CNN's dual classification by keeping only 'national'
   - Reclassifies 'regional' outlets as 'local' for analysis simplicity
5. Adds a 'dataset' column to track the data source
6. Saves the cleaned data to a new CSV file

Args:
    input_file (str): Path to the raw Fisher CSV file
    output_file (str): Path where the cleaned CSV file will be saved

The input CSV should contain at least the following columns:
- domain: The news outlet's domain name
- classification: The classification as local, regional, national, or international news
"""

import sys
import pandas as pd

input_file = sys.argv[1]
output_file = sys.argv[-1]

fisher_raw_df = pd.read_csv(input_file)

fisher_df = fisher_raw_df[["domain", "classification"]].copy()
fisher_df.drop_duplicates(inplace=True)

# Fisher et al. include classifications for the top domains as well as the subdomains.
# For the following four domains, their top domains are classified as regional, their subdomains are classified as local.
# Since we only consider top domains, we remove the rows for the subdomains.
regional_domains = ["desmoinesregister.com", "pantagraph.com", "chron.com", "mlive.com"]
for domain in regional_domains:
    fisher_df = fisher_df[
        ~((fisher_df.domain == domain) & (fisher_df.classification == "local"))
    ]

# cnn.com is classified as both national and internationl, we only keep the national label here.
fisher_df = fisher_df[
    ~((fisher_df.domain == "cnn.com") & (fisher_df.classification == "international"))
]

fisher_df["domain"] = fisher_df.domain.str.lower()
# Remove the ones without a dot
fisher_df = fisher_df[fisher_df["domain"].str.contains("\\.")]

# Fisher et al. didn't provide a clear criteria to distinguish between local and regional domains.
# Moreover, they often treat them as the same category in the analysis.
# Therefore, we reclassify regional as local to simplify the analysis.
fisher_df.loc[fisher_df.classification == "regional", "classification"] = "local"

fisher_df["dataset"] = "fisher"

fisher_df.to_csv(output_file, index=False)
