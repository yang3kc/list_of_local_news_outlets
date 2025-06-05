"""
Assign states to domains based on consistent state mappings.

This script takes a CSV file containing domain and state information and creates a final
mapping of domains to states, keeping only domains that have a consistent state assignment
across all datasets.

Parameters:
    location_path (str): Path to input CSV containing domain and state data
    output_path (str): Path where final domain-state mapping will be saved

The script performs the following steps:
1. Loads the CSV containing domain and state information
2. Gets unique domain-state pairs
3. Counts number of unique states per domain
4. Keeps only domains that map to exactly one state
5. Saves final domain-state mapping to output CSV

Example input CSV format:
    domain,state,dataset
    example.com,CA,dataset1
    example2.com,NY,dataset2
    example3.com,CA,dataset1
    example3.com,NY,dataset2

Example output CSV format:
    domain,state
    example.com,CA
    example2.com,NY

Example usage:
    python assign_state.py input.csv output.csv
"""

import pandas as pd
import sys

location_path = sys.argv[1]
output_path = sys.argv[-1]

location_all_df = pd.read_csv(location_path)
print(f"Loaded {len(location_all_df)} rows from {location_path}")

domain_state_unique_pairs = location_all_df[["domain", "state"]].drop_duplicates()
print(f"After dropping duplicates, {len(domain_state_unique_pairs)} rows remain")

domain_num_unique_states = domain_state_unique_pairs.domain.value_counts()

domain_with_consistent_state_set = set(
    domain_num_unique_states[domain_num_unique_states == 1].index
)
domain_with_consistent_state_df = domain_state_unique_pairs[
    domain_state_unique_pairs.domain.isin(domain_with_consistent_state_set)
]
print(
    f"After dropping domains with inconsistent state assignments, {len(domain_with_consistent_state_df)} rows remain"
)


domain_with_consistent_state_df.to_csv(output_path, index=False)
