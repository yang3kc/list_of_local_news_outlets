"""
Clean and standardize the Yin dataset of US news domains.

This script processes the raw Yin dataset which contains domain names of local news outlets.
It performs the following steps:
1. Reads the raw CSV file
2. Keeps only the domain column and removes null values
3. Removes duplicate entries
4. Adds a 'classification' column with value 'local' since all domains are local news
5. Adds a 'dataset' column to track the data source
6. Saves the cleaned data to a new CSV file

Args:
    input_file (str): Path to the raw Yin CSV file
    output_file (str): Path where the cleaned CSV file will be saved

The input CSV should contain at least the following column:
- domain: The news outlet's domain name
"""

import sys
import pandas as pd

input_file = sys.argv[1]
output_file = sys.argv[-1]

yin_raw_df = pd.read_csv(input_file)

yin_df = yin_raw_df[yin_raw_df.domain.notna()][["domain"]].copy()
yin_df.drop_duplicates(inplace=True)

# All domains in this dataset are local
yin_df["classification"] = "local"
yin_df["dataset"] = "yin"

yin_df.to_csv(output_file, index=False)
