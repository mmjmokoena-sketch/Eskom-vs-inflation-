"""Load, align and check the two small input tables."""
from pathlib import Path

import pandas as pd
import yaml

from .synthetic import make_demo

ROOT = Path(__file__).resolve().parents[1]


def load_settings():
    with open(ROOT / "config" / "settings.yaml", "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_inputs(settings, mode=None):
    """Return (tariff, cpi) tables. Mode 'synthetic' gives fake demo data."""
    mode = mode or settings["data_mode"]
    if mode == "synthetic":
        print("WARNING: SYNTHETIC demo data in use. Never publish results built from it.")
        return make_demo()
    tariff = pd.read_csv(ROOT / settings["paths"]["tariff"])
    cpi = pd.read_csv(ROOT / settings["paths"]["cpi"])
    return tariff, cpi


def align(tariff, cpi, rule):
    """Attach the right year of CPI to each financial year."""
    if rule not in ("fy_start_year", "fy_end_year"):
        raise ValueError("cpi_alignment must be fy_start_year or fy_end_year")
    df = tariff.copy()
    offset = 0 if rule == "fy_start_year" else 1
    df["cpi_year"] = df["fy_start_year"] + offset
    cpi = cpi[["year", "cpi_avg_pct"]]
    df = df.merge(cpi, left_on="cpi_year", right_on="year", how="left")
    return df.drop(columns="year")


def check_complete(df, first, last):
    """Stop with a clear message if any year in the range is missing a number."""
    df = df[(df["fy_start_year"] >= first) & (df["fy_start_year"] <= last)]
    expected = set(range(first, last + 1))
    have_tariff = set(df.loc[df["increase_pct"].notna(), "fy_start_year"])
    have_cpi = set(df.loc[df["cpi_avg_pct"].notna(), "fy_start_year"])
    no_tariff = sorted(expected - have_tariff)
    no_cpi = sorted(expected - have_cpi)
    if no_tariff or no_cpi:
        raise ValueError(
            f"Still to fill in. Tariff increases missing for FY starting: {no_tariff}. "
            f"CPI missing for the matching years: {no_cpi}. "
            "Add the numbers and sources in data/processed/."
        )
    return df.sort_values("fy_start_year").reset_index(drop=True)
