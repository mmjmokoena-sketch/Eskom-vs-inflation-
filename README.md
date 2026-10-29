# Eskom tariffs versus inflation

A small practice project: compare Eskom's annual tariff increases with consumer price
inflation, from a hand-built, sourced dataset.

## Quick start

```
conda env create -f environment.yml
conda activate eskom-vs-inflation
make demo        # runs on FAKE demo data to check your setup
make test
```

Then fill in `data/processed/tariff_increases.csv` and `cpi_annual.csv` from primary
sources, log each source in `data/raw/SOURCES.md`, and run `make run`.

## Status

In progress.
