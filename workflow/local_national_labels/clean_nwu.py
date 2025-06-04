"""Clean and label the NWU dataset.

This script reads a CSV file containing NWU (Northwestern University) domain data,
adds dataset identification and classification labels, and outputs the cleaned data.

Args:
    input_file (str): Path to input CSV file containing NWU domain data
    output_file (str): Path where the cleaned and labeled CSV will be saved

The script adds two columns:
    - dataset: Set to "nwu" to identify the data source
    - classification: Set to "local" since all NWU domains are local
"""

import sys
import pandas as pd

input_file = sys.argv[1]
output_file = sys.argv[2]

df = pd.read_csv(input_file)
print(f"Loaded {len(df)} domains")

df["dataset"] = "nwu"

# All the domains in the nwu dataset are local
df["classification"] = "local"

df.to_csv(output_file, index=False)
