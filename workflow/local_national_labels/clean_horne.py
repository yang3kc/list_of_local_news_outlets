"""Clean and process Horne dataset of local news domains.

This script processes the raw Horne dataset which contains local news domains.
It extracts domain names from the sourcedomain_id field, removes duplicates,
and labels all domains as local news sources.

Args:
    input_file (str): Path to input CSV file containing raw Horne data
    output_file (str): Path to output CSV file to save cleaned data

The output CSV will contain the following columns:
    - domain: The extracted domain name
    - classification: Always "local" for this dataset
    - dataset: Source dataset identifier ("horne")
"""

import sys
import pandas as pd

input_file = sys.argv[1]
output_file = sys.argv[-1]

horne_raw_df = pd.read_csv(input_file)

horne_domains = []
for index, row in horne_raw_df.iterrows():
    domain = row["sourcedomain_id"].split("-")[1]
    # Remove the ones without a dot
    if "." in domain:
        horne_domains.append(domain)

horne_df = pd.DataFrame(horne_domains, columns=["domain"])
horne_df.dropna(inplace=True)
horne_df.drop_duplicates(inplace=True)

# All domains in this dataset are local
horne_df["classification"] = "local"
horne_df["dataset"] = "horne"

horne_df.to_csv(output_file, index=False)
