import pandas as pd
import pytest

from src import govhk, hkma
from src.periods import parse_period


# ---------------------------------------------------------------- periods

@pytest.mark.parametrize("value,expected", [
    ("2026-09", "2026-09-30"), ("202609", "2026-09-30"), (202609, "2026-09-30"),
    ("Sep 2026", "2026-09-30"), ("September 2026", "2026-09-30"),
    ("Jul - Sep 2026", "2026-09-30"), ("Jul-Sep 2026", "2026-09-30"),
    ("2026 Q2", "2026-06-30"), ("Q2 2026", "2026-06-30"), ("2Q2026", "2026-06-30"),
    ("2nd Quarter 2026", "2026-06-30"),
])
def test_parse_period(value, expected):
    assert parse_period(value)[0] == pd.Timestamp(expected)


def test_parse_period_uses_carried_year():
    assert parse_period("Jul - Sep", 2026)[0] == pd.Timestamp("2026-09-30")
    assert parse_period("Total")[0] is None


# ---------------------------------------------------------------- HKMA

class FakeResp:
    def __init__(self, payload=None, content=b""):
        self._payload, self.content = payload, content

    def raise_for_status(self):
        pass

    def json(self):
        return self._payload


def test_hkma_paging_and_frame(monkeypatch):
    months = pd.period_range("2024-01", "2026-10", freq="M")[::-1]
    records = [{"end_of_month": str(p), "loans_total": 100 + i, "classif_loans": 2.0 if p.month % 3 == 0 else None}
               for i, p in enumerate(months)]
    records.insert(5, {"end_of_month": "2025-00", "loans_total": 999, "classif_loans": None})  # annual row
    calls = []

    def fake_get(url, params=None, **kw):
        calls.append(params)
        off, size = params["offset"], params["pagesize"]
        return FakeResp({"header": {"success": True}, "result": {"records": records[off:off + size]}})

    monkeypatch.setattr(hkma, "PAGE", 10)
    monkeypatch.setattr(hkma.requests, "get", fake_get)
    df = hkma.to_frame(hkma.get_records("x"))
    assert len(calls) == 4 and len(df) == len(months)
    assert df.index[-1] == pd.Timestamp("2026-10-31")
    assert 999 not in df["loans_total"].values
    assert hkma.field(df, "classif_loans", "c").index[-1] == pd.Timestamp("2026-09-30")


def test_hkma_daily_to_month_end():
    recs = [{"end_of_date": d.strftime("%Y-%m-%d"), "closing_balance": 50000 + i}
            for i, d in enumerate(pd.bdate_range("2026-09-01", "2026-10-31"))][::-1]
    df = hkma.to_frame(recs)
    s = hkma.month_end_last(hkma.field(df, "closing_balance", "x"), "agg")
    assert list(s.index) == [pd.Timestamp("2026-09-30"), pd.Timestamp("2026-10-31")]


def test_hkma_yoy_growth():
    idx = pd.date_range("2025-01-31", periods=13, freq="ME")
    g = hkma.yoy_growth(pd.Series([100.0] * 12 + [105.0], index=idx), "g")
    assert g.iloc[-1] == pytest.approx(5.0)


# ---------------------------------------------------------------- DATA.GOV.HK tables

def test_pick_prefers_csv_and_excludes():
    res = [{"name": "Table 210-06101 [Traditional Chinese]", "format": "CSV", "url": "a"},
           {"name": "Table 210-06101 [English]", "format": "XLSX", "url": "b"},
           {"name": "Table 210-06101 [English]", "format": "CSV", "url": "c"}]
    assert govhk.pick(res, r"\[English\]")[0]["url"] == "c"


def test_csd_unemployment_year_column_and_moving_periods():
    rows = [["Table 210-06101 : Statistics on labour force, employment, unemployment and underemployment"], [],
            ["Year", "Period", "Labour force ('000)", "Unemployment rate (%)",
             "Unemployment rate (seasonally adjusted) (%)", "Underemployment rate (%)"]]
    for y in (2025, 2026):
        for i, p in enumerate(["Nov - Jan", "Dec - Feb", "Jan - Mar", "Feb - Apr", "Mar - May", "Apr - Jun",
                               "May - Jul", "Jun - Aug", "Jul - Sep"]):
            rows.append([y if i == 0 else None, p, 3800, 3.5, 3.4 + (0.5 if y == 2026 else 0) + i * 0.01, 1.2])
    f = govhk.series_from_rows(rows, govhk.CSD_SPECS[0].label_patterns[0], valid=(0.5, 15))
    assert f.series.index[-1] == pd.Timestamp("2026-09-30")
    assert f.series.iloc[-1] == pytest.approx(3.98)
    assert "seasonally adjusted" in f.how


def test_csd_dates_across_layout():
    months = [f"{m} 2026" for m in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"]]
    rows = [["Consumer Price Indices"], ["", *months],
            ["Composite CPI (index)", *[100 + i for i in range(9)]],
            ["Composite CPI (year-on-year % change)", *[1.0 + i / 10 for i in range(9)]]]
    f = govhk.series_from_rows(rows, govhk.CSD_SPECS[1].label_patterns[0], valid=(-10, 20))
    assert f.series.iloc[-1] == pytest.approx(1.8)


def test_csd_long_format():
    rows = [["period", "sv", "svDesc", "figure"]]
    for q, v in [("2025Q2", 3.1), ("2025Q3", 3.8), ("2025Q4", 2.4), ("2026Q1", 3.0), ("2026Q2", 2.9), ("2026Q3", 2.6)]:
        rows.append([q, "GDP_RC", "GDP in real terms, year-on-year % change", v])
        rows.append([q, "GDP_N", "GDP at current market prices", 800000])
    f = govhk.series_from_rows(rows, govhk.CSD_SPECS[2].label_patterns[1], valid=(-15, 20))
    assert f.series.index[-1] == pd.Timestamp("2026-09-30") and f.series.iloc[-1] == pytest.approx(2.6)


def test_rvd_month_year_columns_and_yoy():
    rows = [["Private Domestic - Price Indices by Class (Territory-wide)"], ["(1999 = 100)"],
            ["Year", "Month", "A", "B", "C", "D", "E", "All Classes"]]
    level = 400.0
    for y in (2024, 2025, 2026):
        for m in range(1, 13):
            if y == 2026 and m > 9:
                break
            level *= 0.995
            rows.append([y if m == 1 else None, ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
                                                 "Oct", "Nov", "Dec"][m - 1], 1, 1, 1, 1, 1, round(level, 1)])
    f = govhk.series_from_rows(rows, r"all classes|^\s*overall|all\s*$|territory-wide", valid=(30, 600))
    yoy = govhk.yoy_change(f.series)
    assert f.series.index[-1] == pd.Timestamp("2026-09-30")
    assert yoy.iloc[-1] == pytest.approx((0.995 ** 12 - 1) * 100, abs=0.1)


def test_oro_monthly_file_with_year_in_name(monkeypatch):
    def table(rows_):
        return [["Monthly Statistics on Compulsory Winding-up"],
                ["Month", "No. of petitions presented", "No. of winding-up orders made"]] + rows_

    files = {
        "u25": table([[m, 50 + i, 30] for i, m in enumerate(["January", "February", "March", "April", "May", "June",
                                                              "July", "August", "September", "October", "November",
                                                              "December"])] + [["Total", 700, 400]]),
        "u26": table([[m, 70 + i, 40] for i, m in enumerate(["January", "February", "March", "April", "May", "June",
                                                              "July", "August", "September", "October"])]),
    }
    res = [{"name": "Monthly Statistics on Compulsory Winding-up 2025 (English)", "format": "CSV", "url": "u25"},
           {"name": "Monthly Statistics on Compulsory Winding-up 2026 (English)", "format": "CSV", "url": "u26"},
           {"name": "Monthly Statistics on Compulsory Winding-up 2026 (Traditional Chinese)", "format": "CSV", "url": "x"},
           {"name": "Annual Statistics on Number of Public Searches 2025 (English)", "format": "CSV", "url": "y"}]
    monkeypatch.setattr(govhk, "load_rows", lambda url, fmt: files[url])
    report = []
    s = govhk._oro_series(res, r"compulsory winding", "winding_up_petitions", (0, 1000), report)
    assert s.index[0] == pd.Timestamp("2025-01-31") and s.index[-1] == pd.Timestamp("2026-10-31")
    assert s.loc["2026-10-31"] == 79 and len(s) == 22
    r12 = govhk.rolling_12m(s)
    assert r12.iloc[-1] == sum(50 + i for i in range(10, 12)) + sum(70 + i for i in range(10))


def test_series_from_rows_raises_with_no_match():
    with pytest.raises(LookupError):
        govhk.series_from_rows([["a", "b"], ["Jan 2026", 1]], r"nothing")
