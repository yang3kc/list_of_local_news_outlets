"""
This script extracts state location information from Fisher et al.'s dataset of news outlets.

The script:
1. Reads the raw Fisher dataset containing domain, classification and state information
2. Drops duplicate domains
3. Handles special cases:
   - Removes subdomain entries for 4 regional domains
   - Resolves CNN's dual classification
   - Reclassifies regional outlets as local
4. Filters to only keep local news outlets
5. Validates state abbreviations against a reference list to make sure they are valid
6. Outputs a cleaned CSV mapping domains to their states


Input:
    - raw csv file containing domain, classification and state information
    - csv file containing US state abbreviations
Output: csv file containing domain and state for local news outlets
"""

import sys
import pandas as pd

input_file = sys.argv[1]
us_states_abbr_file = sys.argv[2]
output_file = sys.argv[-1]

fisher_df = pd.read_csv(input_file, usecols=["domain", "classification", "state"])
us_states_abbr_df = pd.read_csv(us_states_abbr_file, usecols=["abbr"])

fisher_df.drop_duplicates(inplace=True, subset="domain")

# Fisher et al. include classifications for the top domains as well as the subdomains.
# For the following four domains, their top domains are classified as regional, their subdomains are classified as local.
# Since we only consider top domains, we remove the rows for the subdomains.
regional_domains = ["desmoinesregister.com", "pantagraph.com", "chron.com", "mlive.com"]
for domain in regional_domains:
    fisher_df = fisher_df[
        ~((fisher_df.domain == domain) & (fisher_df.classification == "local"))
    ]

# cnn.com is classified as both national and internationl, we only keep the national label here.
fisher_df = fisher_df[
    ~((fisher_df.domain == "cnn.com") & (fisher_df.classification == "international"))
]

fisher_df["domain"] = fisher_df.domain.str.lower()
# Remove the ones without a dot
fisher_df = fisher_df[fisher_df["domain"].str.contains("\\.")]

# Fisher et al. didn't provide a clear criteria to distinguish between local and regional domains.
# Moreover, they often treat them as the same category in the analysis.
# Therefore, we reclassify regional as local to simplify the analysis.
fisher_df.loc[fisher_df.classification == "regional", "classification"] = "local"

# We only keep the local domains
fisher_local_df = fisher_df[fisher_df.classification == "local"]

fisher_local_df = fisher_local_df.merge(
    us_states_abbr_df, left_on="state", right_on="abbr"
)

fisher_local_df["dataset"] = "fisher"

fisher_local_df[["domain", "state", "dataset"]].to_csv(output_file, index=False)
