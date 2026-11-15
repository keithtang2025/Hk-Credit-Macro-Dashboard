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


# ---------------------------------------------------------------- fixes after the first live run

def test_mm_yyyy_period():
    assert parse_period("01-1993")[0] == pd.Timestamp("1993-01-31")
    assert parse_period("10-2026")[0] == pd.Timestamp("2026-10-31")


def test_rvd_real_layout_from_first_run():
    rows = [["PRIVATE  DOMESTIC  -  PRICE  INDICES  BY  CLASS"],
            ["Month", "Class A", "Class A - Remarks", "Class B", "Class B - Remarks", "Class C", "Class C - Remarks",
             "Class D", "Class D - Remarks", "Class E", "Class E - Remarks", "Classes A, B & C",
             "Classes A, B & C - Remarks", "Classes D & E", "Classes D & E - Remarks", "All Classes", "All Classes - Remarks"]]
    for i, p in enumerate(pd.period_range("2024-01", "2026-09", freq="M")):
        rows.append([p.strftime("%m-%Y"), 300, None, 290, None, 280, None, 270, None, 260, None, 285, None, 265,
                     None, 300 - i, "(p)" if i > 30 else None])
    f = govhk.series_from_rows(rows, r"all classes|^\s*overall|all\s*$|territory-wide", valid=(30, 600))
    assert f.series.index[-1] == pd.Timestamp("2026-09-30") and f.series.iloc[-1] == 300 - 32
    assert "All Classes" in f.how and "Remarks" not in f.how


def test_hkma_falls_back_when_pagesize_rejected(monkeypatch):
    import requests

    recs = [{"end_of_month": f"2026-{m:02d}", "usd": 7.8} for m in range(10, 0, -1)]

    def fake_get(url, params=None, **kw):
        if "pagesize" in params:
            resp = FakeResp()
            def bad():
                raise requests.HTTPError("405 Client Error: Not Allowed")
            resp.raise_for_status = bad
            return resp
        off = params["offset"]
        return FakeResp({"header": {"success": True}, "result": {"records": recs[off:off + 4]}})

    monkeypatch.setattr(hkma.requests, "get", fake_get)
    assert len(hkma.get_records("x")) == 10


def test_hkma_keeps_rows_when_deep_page_refused(monkeypatch):
    import requests
    monkeypatch.setattr(hkma, "PAGE", 5)

    def fake_get(url, params=None, **kw):
        if params["offset"] >= 10:
            resp = FakeResp()
            def bad():
                raise requests.HTTPError("405")
            resp.raise_for_status = bad
            return resp
        return FakeResp({"header": {"success": True},
                         "result": {"records": [{"end_of_date": f"2026-10-{d:02d}", "closing_balance": 1}
                                                for d in range(params["offset"] + 1, params["offset"] + 6)]}})

    monkeypatch.setattr(hkma.requests, "get", fake_get)
    assert len(hkma.get_records("x")) == 10


def test_web_page_is_not_data(monkeypatch):
    monkeypatch.setattr(govhk, "_get", lambda url, **kw: FakeResp(content=b"<!DOCTYPE html><html lang='en'>"))
    with pytest.raises(govhk.NotData):
        govhk.load_rows("u", "CSV")


def test_csd_json_long_format(monkeypatch):
    import json
    recs = []
    for p in pd.period_range("2025-09", "2026-09", freq="M"):
        recs.append({"period": p.strftime("%Y%m"), "sv": "UR", "svDesc": "Unemployment rate (%)",
                     "sd_value": "SA", "sdDesc": "Seasonally adjusted", "figure": 3.5 + p.month / 100})
        recs.append({"period": p.strftime("%Y%m"), "sv": "UR", "svDesc": "Unemployment rate (%)",
                     "sd_value": "Raw", "sdDesc": "Not seasonally adjusted", "figure": 9.9})
        recs.append({"period": p.strftime("%Y%m"), "sv": "LF", "svDesc": "Labour force ('000)",
                     "sd_value": "Raw", "sdDesc": "", "figure": 3800})
    body = json.dumps({"header": {"title": "Table 210-06101"}, "dataSet": recs}).encode()
    monkeypatch.setattr(govhk, "_get", lambda url, **kw: FakeResp(content=body))
    rows = govhk.load_rows("u", "JSON")
    f = govhk.series_from_rows(rows, govhk.CSD_SPECS[0].label_patterns[0], valid=(0.5, 15))
    assert f.series.index[-1] == pd.Timestamp("2026-09-30") and f.series.iloc[-1] == pytest.approx(3.59)


def test_snapshot_accumulates_history(tmp_path, monkeypatch):
    from src import data as data_mod
    monkeypatch.setattr(data_mod, "SNAPSHOT_DIR", tmp_path)
    old = pd.Series([1.0, 2.0], index=pd.to_datetime(["2025-01-31", "2025-02-28"]))
    new = pd.Series([2.5, 3.0], index=pd.to_datetime(["2025-02-28", "2025-03-31"]))
    data_mod.save_snapshot({"x": old})
    data_mod.save_snapshot({"x": new})
    s = data_mod.load_snapshot("x")
    assert list(s.values) == [1.0, 2.5, 3.0]


# ---------------------------------------------------------------- layouts seen in the second live run

def _csd_rows(records):
    keys = list(records[0].keys())
    return [keys] + [[r.get(k) for k in keys] for r in records]


def test_csd_unemployment_records_with_sex_dimension():
    recs = []
    for p in pd.period_range("2025-01", "2026-09", freq="M"):
        per = p.strftime("%Y%m")
        for sex, desc, adj in ((None, "Total", 0.0), ("F", "Female", -0.3), ("M", "Male", 0.3)):
            recs.append({"SEX": sex, "SEXDesc": desc, "freq": "M3M", "period": per, "sv": "LF",
                         "svDesc": "No. ('000)", "figure": "3800", "sd_value": None})
            recs.append({"SEX": sex, "SEXDesc": desc, "freq": "M3M", "period": per, "sv": "UR",
                         "svDesc": "%", "figure": str(3.9 + adj), "sd_value": None})
            recs.append({"SEX": sex, "SEXDesc": desc, "freq": "M3M", "period": per, "sv": "UR_SA",
                         "svDesc": "%", "figure": str(3.8 + adj), "sd_value": None})
            recs.append({"SEX": sex, "SEXDesc": desc, "freq": "M3M", "period": per, "sv": "UNDR",
                         "svDesc": "%", "figure": "1.4", "sd_value": None})
    s, how, listing = govhk.csd_select(_csd_rows(recs), govhk.CSD_SPECS[0].csd, (0.5, 15))
    assert "sv=UR_SA" in how and s.iloc[-1] == pytest.approx(3.8)
    assert s.index[-1] == pd.Timestamp("2026-09-30") and "UNDR" in listing


def test_csd_gdp_records_pick_real_not_current():
    recs = [{"freq": "Y", "period": "1973", "sv": "CUR", "svDesc": "Year-on-year % change", "figure": "28.3", "sd_value": None}]
    for i, q in enumerate(pd.period_range("2024Q1", "2026Q3", freq="Q")):
        per = q.end_time.strftime("%Y%m")
        recs.append({"freq": "Q", "period": per, "sv": "CUR", "svDesc": "HK$ million", "figure": "800000", "sd_value": None})
        recs.append({"freq": "Q", "period": per, "sv": "CUR", "svDesc": "Year-on-year % change", "figure": "5.5", "sd_value": None})
        recs.append({"freq": "Q", "period": per, "sv": "CHN", "svDesc": "Year-on-year % change", "figure": str(2.0 + i / 10), "sd_value": None})
        recs.append({"freq": "Q", "period": per, "sv": "IPD", "svDesc": "Year-on-year % change", "figure": "1.1", "sd_value": None})
    s, how, _ = govhk.csd_select(_csd_rows(recs), govhk.CSD_SPECS[2].csd, (-15, 20))
    assert "sv=CHN" in how and s.index[-1] == pd.Timestamp("2026-09-30") and s.iloc[-1] == pytest.approx(3.0)


def test_csd_cpi_records_pick_composite():
    recs = []
    for p in pd.period_range("2025-01", "2026-09", freq="M"):
        per = p.strftime("%Y%m")
        for code, desc, yoy in (("CCPI", "Composite CPI", 1.4), ("CPIA", "CPI(A)", 1.9), ("CPIB", "CPI(B)", 1.2)):
            recs.append({"CPI_TYPE": code, "CPI_TYPEDesc": desc, "freq": "M", "period": per, "sv": "IDX",
                         "svDesc": "Index", "figure": "105", "sd_value": None})
            recs.append({"CPI_TYPE": code, "CPI_TYPEDesc": desc, "freq": "M", "period": per, "sv": "YOY",
                         "svDesc": "Year-on-year % change", "figure": str(yoy), "sd_value": None})
    s, how, _ = govhk.csd_select(_csd_rows(recs), govhk.CSD_SPECS[1].csd, (-10, 20))
    assert s.iloc[-1] == pytest.approx(1.4) and len(s) == 21


def test_oro_combined_monthly_file():
    rows = [["Year", "Month", "Bankruptcy Petitions presented", "Receiving/Bankruptcy Orders made",
             "Compulsory Winding-up Petitions presented", "Winding-up Orders made by the Court", "Weekly court hearing"],
            [1996, "-", 780, 543, 742, 557, 48], [1997, "-", 829, 639, 658, 503, 49]]
    for y in (2025, 2026):
        for m in range(1, 13):
            if y == 2026 and m > 10:
                break
            rows.append([y, m, 800 + m, 700, 60 + m, 40, 5])
        rows.append([y, "Annual total", 9999, 8888, 777, 666, 55])
    f_b = govhk.series_from_rows(rows, r"bankruptcy petition", valid=(0, 5000))
    f_w = govhk.series_from_rows(rows, r"winding-?\s?up petition", valid=(0, 1000))
    assert f_b.series.index[-1] == pd.Timestamp("2026-10-31") and f_b.series.iloc[-1] == 810
    assert f_w.series.loc["2025-12-31"] == 72 and len(f_w.series) == 22
    assert 9999 not in f_b.series.values and 777 not in f_w.series.values


def test_snapshot_full_history_replaces_bad_values(tmp_path, monkeypatch):
    from src import data as data_mod
    monkeypatch.setattr(data_mod, "SNAPSHOT_DIR", tmp_path)
    idx = pd.date_range("2025-01-31", periods=4, freq="ME")
    data_mod.save_snapshot({"x": pd.Series([9.0, -6.0, 9.0, 1.0], index=idx)})
    data_mod.save_snapshot({"x": pd.Series([1.1, 1.2, 1.3, 1.4], index=idx)})
    assert list(data_mod.load_snapshot("x").values) == [1.1, 1.2, 1.3, 1.4]
