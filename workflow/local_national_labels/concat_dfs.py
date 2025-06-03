"""
This script concatenates all the csv files with the same columns

Inputs: csv files
Output: combined csv file
"""

import sys
import pandas as pd

input_files = sys.argv[1:-1]
output_file = sys.argv[-1]

dfs = []
for input_file in input_files:
    dfs.append(pd.read_csv(input_file))

combined_df = pd.concat(dfs)

combined_df.to_csv(output_file, index=False)
