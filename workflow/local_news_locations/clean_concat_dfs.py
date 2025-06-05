"""
Clean and process location data for local news domains.

This script takes a CSV file containing domain names and state information, along with
a file containing local/national classifications. It cleans the domain names and keeps
only local news domains with their state assignments.

Parameters:
    input_file (str): Path to input CSV containing domain and state data
    local_national_labels_file (str): Path to CSV with local/national classifications
    output_file (str): Path where cleaned CSV will be saved

The script performs the following steps:
1. Loads and cleans domain names by normalizing to lowercase
2. Extracts clean domain names using extract_domain()
3. Removes entries with paths using extract_path()
4. Removes entries with invalid domains
5. Removes duplicate entries
6. Merges with local/national classifications
7. Keeps only local domains and their state assignments
8. Saves cleaned data to output CSV

Example input CSV format:
    domain,state,dataset
    example.com,CA,dataset1
    sub.example.com/path,NY,dataset2

Example local/national labels CSV format:
    domain,classification,dataset
    example.com,local,dataset1
    other.com,national,dataset2

Example output CSV format:
    domain,state,dataset
    example.com,CA,dataset1

Example usage:
    python clean_concat_dfs.py input.csv labels.csv output.csv
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
import pandas as pd
from url_utils import extract_domain, extract_path


input_file = sys.argv[1]
local_national_labels_file = sys.argv[2]
output_file = sys.argv[-1]

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

# Remove national domains and only keep the local domains
local_national_labels_df = pd.read_csv(local_national_labels_file)
merged_df = df.merge(local_national_labels_df, on="domain")
print(f"After merging: {len(merged_df)} domains")

output_df = merged_df.query("classification == 'local'")
print(f"After filtering out national domains: {len(output_df)} domains")

cols_to_keep = ["domain", "state", "dataset"]
output_df[cols_to_keep].to_csv(output_file, index=False)
