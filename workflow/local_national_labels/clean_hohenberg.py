"""
Clean and standardize the Hohenberg dataset of US news domains.

This script processes the raw Hohenberg dataset which contains domain names and their
classification as local or national news outlets. It performs the following steps:
1. Reads the raw CSV file
2. Renames the 'type' column to 'classification'
3. Filters out rows with missing classifications
4. Keeps only the domain and classification columns
5. Adds a 'dataset' column to track the data source
6. Converts all domain names to lowercase
7. Removes duplicate domain entries
8. Saves the cleaned data to a new CSV file

Args:
    input_file (str): Path to the raw Hohenberg CSV file
    output_file (str): Path where the cleaned CSV file will be saved

The input CSV should contain at least the following columns:
- domain: The news outlet's domain name
- type: The classification as local or national news
"""

import sys
import pandas as pd

input_file = sys.argv[1]
output_file = sys.argv[-1]

hohenberg_raw_df = pd.read_csv(input_file)

hohenberg_raw_df.rename(columns={"type": "classification"}, inplace=True)

hohenberg_df = hohenberg_raw_df[hohenberg_raw_df["classification"].notna()][
    ["domain", "classification"]
]

hohenberg_df["domain"] = hohenberg_df.domain.str.lower()
hohenberg_df.drop_duplicates(inplace=True)

hohenberg_df["dataset"] = "hohenberg"

hohenberg_df.to_csv(output_file, index=False)
