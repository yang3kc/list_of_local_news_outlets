"""
Extract state location information from Yin et al.'s dataset of local news outlets.

This script reads the raw Yin dataset containing domain and state information,
cleans and processes it by:
1. Removing rows with missing domains
2. Dropping duplicate domains
3. Validating state abbreviations against a reference list to make sure they are valid
4. Saving the cleaned domain-state mapping

Arguments:
    input_file: Path to raw Yin dataset CSV
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

yin_raw_df = pd.read_csv(input_file, usecols=["domain", "state"])
us_states_abbr_df = pd.read_csv(us_states_abbr_file, usecols=["abbr"])

yin_df = yin_raw_df[yin_raw_df.domain.notna()][["domain", "state"]].copy()
yin_df.drop_duplicates(inplace=True, subset="domain")

yin_df = yin_df.merge(us_states_abbr_df, left_on="state", right_on="abbr")

yin_df["dataset"] = "yin"

yin_df[["domain", "state", "dataset"]].to_csv(output_file, index=False)
