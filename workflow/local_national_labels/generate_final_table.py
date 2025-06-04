import sys
import pandas as pd

input_file = sys.argv[1]
output_file = sys.argv[2]

raw_df = pd.read_csv(input_file)
print(f"Before filtering: {len(raw_df)} domains")

classification_count = raw_df.groupby("domain").classification.nunique()
domains_with_unique_classifications = set(
    classification_count[classification_count == 1].index
)

df = raw_df[raw_df.domain.isin(domains_with_unique_classifications)][
    ["domain", "classification"]
].copy()
print(f"After filtering: {len(df)} domains")

df.drop_duplicates(inplace=True)
print(f"After removing duplicates: {len(df)} domains")

df.to_csv(output_file, index=False)
