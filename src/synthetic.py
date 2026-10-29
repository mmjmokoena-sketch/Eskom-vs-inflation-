"""FAKE data for testing the code before your real tables are complete.

Nothing made from this is real. Never publish results built from it.
"""
import numpy as np
import pandas as pd


def make_demo(first=2007, last=2026, seed=1):
    rng = np.random.default_rng(seed)
    years = np.arange(first, last + 1)
    tariff = pd.DataFrame({"fy_start_year": years,
                           "increase_pct": rng.uniform(2, 30, len(years)).round(2),
                           "source": "FAKE", "verified": False, "note": "demo"})
    cpi = pd.DataFrame({"year": years,
                        "cpi_avg_pct": rng.uniform(3, 8, len(years)).round(1),
                        "source": "FAKE", "verified": False, "note": "demo"})
    return tariff, cpi
