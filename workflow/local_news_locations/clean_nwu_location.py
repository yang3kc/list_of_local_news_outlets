"""
Extract state location information from NWU dataset.

This script reads the raw NWU dataset containing domain and state abbreviation information,
cleans and processes it by:
1. Converting state abbreviations to uppercase
2. Validating state abbreviations against a reference list
3. Saving the cleaned domain-state mapping

Arguments:
    input_file: Path to raw NWU dataset CSV
    us_states_abbr_file: Path to CSV containing valid US state abbreviations
    output_file: Path to save cleaned domain-state mapping CSV

Output format:
    CSV with columns: domain, state, dataset
"""

import sys
import pandas as pd

input_file = sys.argv[1]
us_states_abbr_file = sys.argv[2]
output_file = sys.argv[-1]

nwu_raw_df = pd.read_csv(input_file, usecols=["domain", "state_abbr"])
nwu_raw_df["state_abbr"] = nwu_raw_df["state_abbr"].str.upper()

us_states_abbr_df = pd.read_csv(us_states_abbr_file, usecols=["abbr"])

nwu_df = nwu_raw_df.merge(us_states_abbr_df, left_on="state_abbr", right_on="abbr")

nwu_df.rename(columns={"abbr": "state"}, inplace=True)

nwu_df["dataset"] = "nwu"

nwu_df[["domain", "state", "dataset"]].to_csv(output_file, index=False)
