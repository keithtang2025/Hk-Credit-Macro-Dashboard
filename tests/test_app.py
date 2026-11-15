import numpy as np
import pandas as pd
import pytest

from src import data as data_mod
from src import sources
from src.scorecard import build_scorecard, signal, summary, RISING, EASING
from src.specs import SERIES


def _fake_series():
    rng = np.random.default_rng(0)
    m = pd.date_range("2018-01-31", "2026-10-31", freq="ME")
    q = pd.date_range("2018-03-31", "2026-09-30", freq="QE")
    out = {}
    for key in SERIES:
        idx = q if key in ("gdp_yoy", "classified_loans") else m
        base = {"usdhkd": 7.8, "aggregate_balance": 100, "home_price_index": 300}.get(key, 2.0)
        if key.endswith("_12m") or key.endswith("petitions"):
            base = 80 if "winding" in key else 800
            if key.endswith("_12m"):
                base *= 12
        out[key] = pd.Series(base + rng.normal(0, base * 0.02, len(idx)), index=idx, name=key)
    return out


def test_signal():
    assert signal(4.75, 5.75, True) == EASING
    assert signal(4.0, 3.0, True) == RISING


def test_empty_state_before_first_refresh(tmp_path, monkeypatch):
    monkeypatch.setattr(data_mod, "SNAPSHOT_DIR", tmp_path)
    d = data_mod.build()
    assert d.series == {}
    score = build_scorecard(d.series, d.origin, d.stress)
    assert len(score) == 2  # manual negative-equity rows only
    import app
    monkeypatch.setattr(app, "get_data", lambda: d)
    assert app.serve_layout() is not None


def test_full_layout_with_data(tmp_path, monkeypatch):
    monkeypatch.setattr(data_mod, "SNAPSHOT_DIR", tmp_path)
    data_mod.save_snapshot(_fake_series())
    d = data_mod.build()
    assert set(d.series) == set(SERIES)
    score = build_scorecard(d.series, d.origin, d.stress)
    up, total = summary(score)
    assert total >= up and total >= 10
    import app
    monkeypatch.setattr(app, "get_data", lambda: d)
    assert app.serve_layout() is not None


def test_fetch_all_isolates_failures(monkeypatch):
    idx = pd.date_range("2025-01-31", periods=6, freq="ME")
    monkeypatch.setattr(sources.hkma, "fetch_hkma", lambda: ({"base_rate": pd.Series(4.0, index=idx)}, "ok"))

    def boom(report):
        raise RuntimeError("site down")

    monkeypatch.setattr(sources.govhk, "fetch_csd", lambda report: {"unemployment": pd.Series(3.9, index=idx)})
    monkeypatch.setattr(sources.govhk, "fetch_rvd", boom)
    monkeypatch.setattr(sources.govhk, "fetch_oro", lambda report: {})
    # stub every source so the test never touches the network
    monkeypatch.setattr(sources.govhk, "fetch_rvd_yields", lambda report: {})
    monkeypatch.setattr(sources.market, "fetch_hsi", boom)
    monkeypatch.setattr(sources.hkex, "fetch_hkex", lambda report: {})
    series, errors, report = sources.fetch_all()
    assert set(series) == {"base_rate", "unemployment"}
    assert "RVD property price index (via DATA.GOV.HK)" in errors and "site down" in report
