"""
Clean and process a CSV file containing domain and state information.

This script takes a CSV file containing domain names and their associated states,
cleans the domain names by extracting the main domain, removing paths, and
removing duplicates.

Parameters:
    input_file (str): Path to input CSV file containing domain and state data
    output_file (str): Path where cleaned CSV will be saved

The script performs the following steps:
1. Loads the CSV and normalizes domain names to lowercase
2. Extracts clean domain names using extract_domain()
3. Removes entries with paths using extract_path()
4. Removes entries with invalid domains
5. Removes duplicate entries
6. Saves cleaned data to output CSV

Example input CSV format:
    domain,state,dataset
    example.com,CA,dataset1
    sub.example.com/path,NY,dataset2

Example usage:
    python clean_concat_dfs.py input.csv output.csv
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
import pandas as pd
from url_utils import extract_domain, extract_path


input_file = sys.argv[1]
output_file = sys.argv[2]

df = pd.read_csv(input_file)
print(f"Before cleaning: {len(df)} domains")

df.rename(columns={"domain": "domain_raw"}, inplace=True)

df["domain_raw"] = df["domain_raw"].str.lower().str.strip()

# Remove the ones with a path and invalid domains
df["domain"] = df.domain_raw.apply(extract_domain)
df["path"] = df.domain_raw.apply(extract_path)
df = df[df.path == ""]
df = df[df.domain != ""]
print(f"After cleaning: {len(df)} domains")

# Remove duplicates
df.drop_duplicates(inplace=True)
print(f"After removing duplicates: {len(df)} domains")

cols_to_keep = ["domain", "state", "dataset"]
df[cols_to_keep].to_csv(output_file, index=False)
