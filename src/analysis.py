"""Compare Eskom's annual tariff increases with inflation."""
import pandas as pd


def compound_index(rates_pct, start=100.0):
    """Index level after each year's increase, starting from `start` just before year 1."""
    level = start
    out = []
    for rate in rates_pct:
        level = level * (1 + rate / 100)
        out.append(level)
    return out


def cagr(start_level, end_level, years):
    """Compound annual growth rate, as a percentage."""
    return ((end_level / start_level) ** (1 / years) - 1) * 100


def build_table(df):
    """One row per financial year with gaps and index levels."""
    out = df[["fy_start_year", "increase_pct", "cpi_avg_pct"]].copy()
    start = out["fy_start_year"]
    out["fy_label"] = start.astype(str) + "/" + (start + 1).astype(str).str[-2:]
    out["gap_pp"] = out["increase_pct"] - out["cpi_avg_pct"]
    out["tariff_above_cpi"] = out["gap_pp"] > 0
    out["tariff_index"] = compound_index(out["increase_pct"])
    out["cpi_index"] = compound_index(out["cpi_avg_pct"])
    out["real_tariff_index"] = out["tariff_index"] / out["cpi_index"] * 100
    return out


def summarise(table):
    n = len(table)
    tariff_end = table["tariff_index"].iloc[-1]
    cpi_end = table["cpi_index"].iloc[-1]
    return pd.DataFrame([{
        "years": n,
        "years_tariff_above_cpi": int(table["tariff_above_cpi"].sum()),
        "tariff_total_growth_pct": tariff_end - 100,
        "cpi_total_growth_pct": cpi_end - 100,
        "tariff_cagr_pct": cagr(100, tariff_end, n),
        "cpi_cagr_pct": cagr(100, cpi_end, n),
        "real_tariff_index_end": table["real_tariff_index"].iloc[-1],
    }])
