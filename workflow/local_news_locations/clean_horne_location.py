"""
Extract state location information from Horne et al.'s dataset of local news outlets.

This script reads the raw Horne dataset containing domain and state information,
cleans and processes it by:
1. Extracting domain names from sourcedomain_id field
2. Dropping duplicate domains
3. Validating state names against a reference list to make sure they are valid
4. Converting full state names to standard abbreviations
5. Saving the cleaned domain-state mapping

Arguments:
    input_file: Path to raw Horne dataset CSV
    us_states_abbr_file: Path to CSV containing valid US state names and abbreviations
    output_file: Path to save cleaned domain-state mapping CSV

Output format:
    CSV with columns: domain, state
"""

import sys
import pandas as pd

input_file = sys.argv[1]
us_states_abbr_file = sys.argv[2]
output_file = sys.argv[-1]

raw_horne_df = pd.read_csv(input_file, usecols=["sourcedomain_id", "state"])
print(f"Loaded {len(raw_horne_df)} rows from {input_file}")
us_states_abbr_df = pd.read_csv(us_states_abbr_file)

horne_domains = []
for index, row in raw_horne_df.iterrows():
    domain = row["sourcedomain_id"].split("-")[1]
    state = row["state"]
    # Remove the ones without a dot
    if "." in domain:
        horne_domains.append([domain, state])

horne_df = pd.DataFrame(horne_domains, columns=["domain", "state"])
print(f"Extracted {len(horne_df)} domains from {input_file}")

horne_df.dropna(inplace=True)
horne_df.drop_duplicates(inplace=True)
print(f"After removing duplicates and nulls: {len(horne_df)} domains")

horne_df = horne_df.merge(us_states_abbr_df, on="state")
print(f"After merging with {len(us_states_abbr_df)} states: {len(horne_df)} domains")

horne_df.rename(columns={"state": "state_full_name", "abbr": "state"}, inplace=True)

horne_df["dataset"] = "horne"

horne_df[["domain", "state", "dataset"]].to_csv(output_file, index=False)
