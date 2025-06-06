# List of Local News Outlets

This repository consolidates several open datasets to create a unified list of news domains in the United States. The workflow cleans each source and produces a table indicating whether a domain is local or national. Another workflow associates local outlets with the U.S. state they primarily serve.

## Repository layout

- `data/raw_data/` – unmodified datasets gathered from public sources.
- `data/output/` – generated CSV files, including `local_national_labels.csv` and `local_news_locations.csv`.
- `workflow/` – Snakemake workflow and helper scripts.

## Getting started

1. Install Python 3.12 or later.
2. Install the dependencies with [uv](https://github.com/astral-sh/uv):
   ```bash
   uv sync
   ```
3. Run the workflow to build the local/national labels:
   ```bash
   snakemake -s workflow/local_national_labels/Snakefile
   ```
   The resulting file will be written to `data/output/local_national_labels.csv`.

4. Run the workflow to build the state mapping for local outlets:
   ```bash
   snakemake -s workflow/local_news_locations/Snakefile
   ```
   The resulting file will be written to `data/output/local_news_locations.csv`.

## Data sources

The raw datasets originate from multiple projects such as Hohenberg, Fisher, Yin, Horne, ABYZ and others.
See [data/raw_data/README.md](data/raw_data/README.md) for the full list of sources.
