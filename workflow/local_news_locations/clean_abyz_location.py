"""
Extract state location information from ABYZ News Links dataset.

This script reads the raw ABYZ dataset containing domain and state abbreviation information,
cleans and processes it by:
1. Converting state abbreviations to uppercase
2. Filtering out national outlets (marked as 'NA')
3. Dropping duplicate domains
4. Validating state abbreviations against a reference list
5. Saving the cleaned domain-state mapping for local news outlets

Arguments:
    input_file: Path to raw ABYZ dataset CSV
    us_states_abbr_file: Path to CSV containing valid US state abbreviations
    output_file: Path to save cleaned domain-state mapping CSV

Output format:
    CSV with columns: domain, state
"""

import sys
import pandas as pd

input_file = sys.argv[1]
us_states_abbr_file = sys.argv[2]
output_file = sys.argv[-1]

abyz_raw_df = pd.read_csv(input_file, usecols=["domain", "state_abbr"])
abyz_raw_df["state_abbr"] = abyz_raw_df["state_abbr"].str.upper()

us_states_abbr_df = pd.read_csv(us_states_abbr_file, usecols=["abbr"])

# only keep the local ones
# NA stands for national
abyz_local_df = abyz_raw_df[abyz_raw_df["state_abbr"] != "NA"].copy()

# remove duplicate domains
abyz_local_df.drop_duplicates(subset="domain", inplace=True)

# validate state abbreviations
abyz_local_df = abyz_local_df.merge(
    us_states_abbr_df, left_on="state_abbr", right_on="abbr"
)

# rename columns
abyz_local_df.rename(columns={"abbr": "state"}, inplace=True)

abyz_local_df["dataset"] = "abyz"

# output
abyz_local_df[["domain", "state", "dataset"]].to_csv(output_file, index=False)
