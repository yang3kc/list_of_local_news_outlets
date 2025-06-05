"""
Clean and process a CSV file containing domain classifications.

This script takes a CSV file containing domain names and their classifications,
cleans the domain names by extracting the main domain, removing paths, and
removing duplicates.

Parameters:
    input_file (str): Path to input CSV file containing domain classifications
    output_file (str): Path where cleaned CSV will be saved

The script performs the following steps:
1. Loads the CSV and normalizes domain names to lowercase
2. Extracts clean domain names using extract_domain()
3. Removes entries with paths using extract_path()
4. Removes entries with invalid domains
5. Removes entries with gov, mil, edu suffixes
5. Removes duplicate entries
6. Saves cleaned data to output CSV

Example input CSV format:
    domain,classification,dataset
    example.com,local,dataset1
    sub.example.com/path,national,dataset2

Example usage:
    python clean_concat_dfs.py input.csv output.csv
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
import pandas as pd
from url_utils import extract_domain, extract_path, extract_suffix


input_file = sys.argv[1]
output_file = sys.argv[2]

df = pd.read_csv(input_file)
df.rename(columns={"domain": "domain_raw"}, inplace=True)

df["domain_raw"] = df["domain_raw"].str.lower().str.strip()

# Remove the ones with a path and invalid domains
df["domain"] = df.domain_raw.apply(extract_domain)
df["path"] = df.domain_raw.apply(extract_path)
df = df[df.path == ""]
df = df[df.domain != ""]
print(f"After cleaning: {len(df)} domains")

# Only keep the domains with local or national labels
# Ignore other labels: international, technical, etc.
classifications_to_keep = set(["local", "national"])
df = df[df.classification.isin(classifications_to_keep)]
print(f"After filtering: {len(df)} domains")

# Remove domains with suffix in the following list:
# gov, mil, edu
suffixes_to_remove = set(["gov", "mil", "edu"])
df = df[~df.domain.apply(extract_suffix).isin(suffixes_to_remove)]
print(f"After removing suffixes: {len(df)} domains")

# Remove duplicates
df.drop_duplicates(inplace=True)
print(f"After removing duplicates: {len(df)} domains")

cols_to_keep = ["domain", "classification", "dataset"]
df[cols_to_keep].to_csv(output_file, index=False)
