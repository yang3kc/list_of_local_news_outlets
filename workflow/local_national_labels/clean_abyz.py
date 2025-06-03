import sys
import pandas as pd

input_file = sys.argv[1]
output_file = sys.argv[-1]

abyz_raw_df = pd.read_csv(input_file)

abyz_raw_df.dropna(inplace=True)

# na stands for national
abyz_raw_df["classification"] = abyz_raw_df.state_abbr.apply(
    lambda abbr: "national" if abbr == "na" else "local"
)

abyz_df = abyz_raw_df[["domain", "classification"]].copy()
abyz_df.drop_duplicates(inplace=True)

# 18 domains are labeled as both national and local by abyz news
# The national label takes precedence here
domain_value_counts = abyz_df.domain.value_counts()
domain_with_multiple_labels = list(domain_value_counts[domain_value_counts > 1].index)

for domain in domain_with_multiple_labels:
    # Remove the local label
    abyz_df = abyz_df.query(
        f"not (domain == '{domain}' and classification == 'local')"
    ).copy()

abyz_df["dataset"] = "abyz"

abyz_df.to_csv(output_file, index=False)
