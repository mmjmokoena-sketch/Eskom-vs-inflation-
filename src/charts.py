"""Two simple charts saved as PNG files."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402


def annual_bars(table, path):
    fig, ax = plt.subplots(figsize=(9, 4))
    x = np.arange(len(table))
    ax.bar(x - 0.2, table["increase_pct"], width=0.4, label="Eskom tariff increase")
    ax.bar(x + 0.2, table["cpi_avg_pct"], width=0.4, label="CPI inflation")
    ax.set_xticks(x)
    ax.set_xticklabels(table["fy_label"], rotation=60, ha="right")
    ax.set_ylabel("% per year")
    ax.set_title("Annual tariff increases versus inflation")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def index_lines(table, path):
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(table["fy_label"], table["tariff_index"], marker="o", label="Eskom tariff")
    ax.plot(table["fy_label"], table["cpi_index"], marker="o", label="CPI")
    ax.set_ylabel("Index (100 = start of first year)")
    ax.set_title("Cumulative increase since the start of the period")
    ax.tick_params(axis="x", rotation=60)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
