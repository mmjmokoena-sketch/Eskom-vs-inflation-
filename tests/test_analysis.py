import pandas as pd
import pytest

from src.analysis import build_table, cagr, compound_index, summarise
from src.load import align, check_complete


def test_compound_index_baby_steps():
    # 10% then 20% is 32% in total, not 30%
    assert compound_index([10, 20]) == pytest.approx([110.0, 132.0])


def test_practice_question():
    assert compound_index([5, 8])[-1] == pytest.approx(113.4)


def test_cagr_baby_steps():
    assert cagr(100, 132, 2) == pytest.approx(14.89, abs=0.01)
    assert cagr(100, 121, 2) == pytest.approx(10.0, abs=1e-9)


def test_alignment_rules():
    tariff = pd.DataFrame({"fy_start_year": [2020, 2021], "increase_pct": [5.0, 6.0]})
    cpi = pd.DataFrame({"year": [2020, 2021, 2022], "cpi_avg_pct": [3.0, 4.0, 5.0]})
    start = align(tariff, cpi, "fy_start_year")
    end = align(tariff, cpi, "fy_end_year")
    assert list(start["cpi_avg_pct"]) == [3.0, 4.0]
    assert list(end["cpi_avg_pct"]) == [4.0, 5.0]


def test_missing_numbers_are_reported():
    df = pd.DataFrame({"fy_start_year": [2020, 2021], "increase_pct": [5.0, None],
                       "cpi_avg_pct": [3.0, 4.0]})
    with pytest.raises(ValueError, match="2021"):
        check_complete(df, 2020, 2021)


def test_summary_counts_years_above_cpi():
    df = pd.DataFrame({"fy_start_year": [2020, 2021], "increase_pct": [10.0, 3.0],
                       "cpi_avg_pct": [5.0, 4.0]})
    table = build_table(df)
    assert int(summarise(table)["years_tariff_above_cpi"].iloc[0]) == 1
