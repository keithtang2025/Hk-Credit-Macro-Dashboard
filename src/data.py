"""Load the dashboard's data from the snapshot the daily refresh commits."""
from __future__ import annotations

import os
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

from .specs import SERIES

ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT_DIR = ROOT / "data" / "snapshot"
MANUAL_DIR = ROOT / "data" / "manual"
ACCUMULATE = {"loan_growth", "loan_growth_hk", "loan_to_deposit", "classified_loans", "card_chargeoff"}
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "3600"))


@dataclass
class DashboardData:
    series: dict[str, pd.Series] = field(default_factory=dict)
    origin: dict[str, str] = field(default_factory=dict)
    stress: pd.DataFrame | None = None
    loaded_at: pd.Timestamp | None = None
    refreshed_at: pd.Timestamp | None = None


def load_snapshot(key: str) -> pd.Series | None:
    path = SNAPSHOT_DIR / f"{key}.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path, parse_dates=["date"])
    s = df.set_index("date")["value"].astype(float).sort_index()
    s.name = key
    return s


def save_snapshot(series: dict[str, pd.Series]) -> list[Path]:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    for key, s in series.items():
        path = SNAPSHOT_DIR / f"{key}.csv"
        old = load_snapshot(key)
        # Only series from HKMA's short summary table (about 20 periods) keep older points;
        # every other source returns its full history and replaces the file outright.
        if key in ACCUMULATE and old is not None and len(old) and len(s) and s.index[0] > old.index[0]:
            s = pd.concat([old[old.index < s.index[0]], s]).sort_index()
        pd.DataFrame({"date": s.index.strftime("%Y-%m-%d"), "value": s.values}).to_csv(path, index=False)
        written.append(path)
    return written


def _last_refresh() -> pd.Timestamp | None:
    log = ROOT / "data" / "history" / "refresh_log.csv"
    if not log.exists():
        return None
    try:
        return pd.to_datetime(pd.read_csv(log, usecols=["retrieved"])["retrieved"]).max()
    except Exception:
        return None


def build() -> DashboardData:
    d = DashboardData()
    for key in SERIES:
        s = load_snapshot(key)
        if s is not None and not s.empty:
            d.series[key] = s
            d.origin[key] = "daily"
    d.stress = pd.read_csv(MANUAL_DIR / "stress_indicators.csv")
    d.loaded_at = pd.Timestamp.now(tz="Asia/Hong_Kong")
    d.refreshed_at = _last_refresh()
    return d


_cache: dict[str, object] = {"data": None, "at": 0.0}
_lock = threading.Lock()


def get_data() -> DashboardData:
    with _lock:
        now = time.time()
        if _cache["data"] is None or now - float(_cache["at"]) > CACHE_TTL_SECONDS:
            _cache["data"] = build()
            _cache["at"] = now
        return _cache["data"]  # type: ignore[return-value]
