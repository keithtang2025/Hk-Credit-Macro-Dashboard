"""Turn the many ways Hong Kong agencies write a period into a month-end date.

Handles: 2026-09, 202609, Sep 2026, September 2026, Jul - Sep 2026 (3-month
moving periods use the last month), 2026 Q2, Q2 2026, 2Q2026, 2nd Quarter 2026,
and tables where the year sits in its own column or only on the first row of
each year (carried forward).
"""
from __future__ import annotations

import re
from datetime import date, datetime

import pandas as pd

MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
_MONTH_WORD = re.compile(r"\b(" + "|".join(MONTHS) + r")[a-z]*\.?", re.I)
_YEAR = re.compile(r"(?<!\d)(19[5-9]\d|20\d\d)(?!\d)")
_YYYYMM = re.compile(r"^\s*(19[5-9]\d|20\d\d)[-/ ]?(0[1-9]|1[0-2])\s*$")
_MMYYYY = re.compile(r"^\s*(0?[1-9]|1[0-2])[-/.](19[5-9]\d|20\d\d)\s*$")
_QUARTER = re.compile(r"(?:(?<![A-Za-z])Q\s?([1-4])(?!\d)|(?<!\d)([1-4])\s?Q(?![A-Za-z])|\b([1-4])(?:st|nd|rd|th)\s+quarter\b)", re.I)


def month_end(year: int, month: int) -> pd.Timestamp:
    return (pd.Timestamp(year, month, 1) + pd.offsets.MonthEnd(0)).normalize()


def parse_period(value, default_year: int | None = None) -> tuple[pd.Timestamp | None, int | None]:
    """(month-end timestamp or None, year seen in this cell or None)."""
    if isinstance(value, (datetime, date, pd.Timestamp)):
        t = pd.Timestamp(value)
        return month_end(t.year, t.month), t.year
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        v = int(value)
        if value == v and 195001 <= v <= 210012 and 1 <= v % 100 <= 12:
            return month_end(v // 100, v % 100), v // 100
        if value == v and 1950 <= v <= 2100:
            return None, v
        return None, None
    if not isinstance(value, str):
        return None, None
    s = value.strip()
    if not s:
        return None, None
    m = _YYYYMM.match(s)
    if m:
        return month_end(int(m.group(1)), int(m.group(2))), int(m.group(1))
    m = _MMYYYY.match(s)
    if m:
        return month_end(int(m.group(2)), int(m.group(1))), int(m.group(2))
    years = _YEAR.findall(s)
    year = int(years[-1]) if years else None
    use_year = year or default_year
    months = _MONTH_WORD.findall(s)
    if months and use_year:
        return month_end(use_year, MONTHS.index(months[-1].lower()[:3]) + 1), year
    q = _QUARTER.search(s)
    if q and use_year:
        quarter = int(next(g for g in q.groups() if g))
        return month_end(use_year, quarter * 3), year
    return None, year


def is_year_cell(value) -> int | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool) and value == int(value) and 1950 <= value <= 2100:
        return int(value)
    if isinstance(value, str) and re.fullmatch(r"\s*(19[5-9]\d|20\d\d)\s*", value):
        return int(value)
    return None
