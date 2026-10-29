"""Generate notebooks/01_explore.ipynb (run once: python make_notebook.py)."""
import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = [
    ("md", "# 01 Explore: Eskom tariffs versus inflation\n\nRun each cell, then answer the "
           "questions in the markdown cells in your own words."),
    ("code", '''import os
import sys
from pathlib import Path

ROOT = Path.cwd().resolve().parents[0]       # repo root, one level above notebooks/
sys.path.insert(0, str(ROOT))

import matplotlib.pyplot as plt
import pandas as pd

from src import analysis
from src.load import align, check_complete, load_inputs, load_settings

settings = load_settings()
MODE = os.environ.get("DATA_MODE")           # None = real data; "synthetic" = fake demo
tariff, cpi = load_inputs(settings, MODE)
merged = align(tariff, cpi, settings["cpi_alignment"])
data = check_complete(merged, settings["base_financial_year"],
                      settings["last_financial_year"])
table = analysis.build_table(data)
table.round(2)'''),
    ("md", "**Question 1.** In how many years was the tariff increase above CPI? "
           "Is that what you expected?"),
    ("code", '''summary = analysis.summarise(table)
summary.round(2).T'''),
    ("md", "**Question 2.** Compare the compound annual growth of the tariff and CPI. "
           "Why is compound growth better than averaging the yearly percentages?"),
    ("code", '''table.plot(x="fy_label", y=["increase_pct", "cpi_avg_pct"], kind="bar", figsize=(9, 4))
plt.ylabel("% per year")
plt.show()'''),
    ("md", "**Question 3.** Which years have the biggest gap between tariff and CPI? "
           "What was happening in those years?"),
    ("code", '''table.sort_values("gap_pp", ascending=False)[["fy_label", "gap_pp"]].head(5)'''),
    ("md", "**Question 4.** The real tariff index divides the tariff index by the CPI index. "
           "What does a value above 100 mean?"),
    ("code", '''plt.plot(table["fy_label"], table["real_tariff_index"], marker="o")
plt.xticks(rotation=60)
plt.ylabel("Real tariff index")
plt.show()'''),
]
nb.cells = [nbf.v4.new_markdown_cell(t) if k == "md" else nbf.v4.new_code_cell(t) for k, t in cells]
nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
nbf.write(nb, "notebooks/01_explore.ipynb")
print("notebook written")
