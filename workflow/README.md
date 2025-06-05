# Introduction

This directory contains Snakemake workflows and helper utilities.

## Local national labels

The [local_national_labels](./local_national_labels) workflow merges datasets from `data/raw_data` to produce `data/output/local_national_labels.csv`.

## Local news locations

The [local_news_locations](./local_news_locations) workflow builds a mapping between local outlets and the U.S. states they serve. The final table is written to `data/output/local_news_locations.csv`.
