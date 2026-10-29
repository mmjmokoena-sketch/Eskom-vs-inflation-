"""Build the comparison table, summary and charts."""
import argparse

from . import analysis, charts
from .load import ROOT, align, check_complete, load_inputs, load_settings


def main(mode=None):
    settings = load_settings()
    mode = mode or settings["data_mode"]
    tariff, cpi = load_inputs(settings, mode)
    merged = align(tariff, cpi, settings["cpi_alignment"])
    try:
        data = check_complete(merged, settings["base_financial_year"],
                              settings["last_financial_year"])
    except ValueError as problem:
        print(f"STOP: {problem}")
        raise SystemExit(1)

    table = analysis.build_table(data)
    summary = analysis.summarise(table)

    out = ROOT / "outputs" / ("synthetic" if mode == "synthetic" else "")
    (out / "tables").mkdir(parents=True, exist_ok=True)
    (out / "figures").mkdir(parents=True, exist_ok=True)
    table.to_csv(out / "tables" / "comparison.csv", index=False)
    summary.to_csv(out / "tables" / "summary.csv", index=False)
    charts.annual_bars(table, out / "figures" / "annual_bars.png")
    charts.index_lines(table, out / "figures" / "index_lines.png")
    print(summary.round(2).T)
    print(f"Done ({mode}). Outputs in {out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["raw", "synthetic"], default=None)
    main(parser.parse_args().mode)
