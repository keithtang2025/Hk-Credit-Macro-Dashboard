"""HKEX Main Board average P/E ratio and average dividend yield (monthly bulletin).

HKEX publishes one "Stock market highlights" page per month, e.g.
https://www.hkex.com.hk/eng/stat/smstat/mthbull/rpt_Stock_market_highlights_1702.htm
with rows "Average P/E ratio (times)" and "Average yield (%)" for that month and the
same month a year earlier. The first run backfills from 2010; later runs only ask for
months not yet in the snapshot (plus the last two, in case of revisions).
"""
from __future__ import annotations

import re
from html import unescape

import pandas as pd
import requests

PAGE = "https://www.hkex.com.hk/eng/stat/smstat/mthbull/rpt_Stock_market_highlights_{yymm}.htm"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; hk-credit-macro-dashboard/1.0)"}
START = pd.Timestamp("2010-01-31")
PE_OK, DY_OK = (3.0, 60.0), (0.5, 15.0)


def _text(html: str) -> str:
    t = re.sub(r"(?is)<(script|style).*?</\1>", " ", html)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", unescape(t)).replace("\xa0", " ")


def _first_two(text: str, label: str) -> tuple[float | None, float | None]:
    """The first two numbers after the label: this month, then the same month a year earlier."""
    m = re.search(label, text, re.I)
    if not m:
        return None, None
    nums = [float(n.replace(",", "")) for n in re.findall(r"(?<![\w.])(\d[\d,]*(?:\.\d+)?)(?![\w.])", text[m.end():m.end() + 60])]
    nums += [None, None]
    return nums[0], nums[1]


def parse_page(html: str) -> dict[str, tuple[float | None, float | None]]:
    """{'pe': (this month, a year earlier), 'yield': (...)} from one bulletin page."""
    text = _text(html)
    return {"pe": _first_two(text, r"Average P\s*/\s*E ratio\s*\(times\)"),
            "yield": _first_two(text, r"Average (?:dividend )?yield\s*\(%\)")}


def _months(last_have: pd.Timestamp | None, today: pd.Timestamp) -> list[pd.Timestamp]:
    end = (today - pd.offsets.MonthEnd(1)).normalize()  # last complete month
    start = START if last_have is None else max(START, last_have - pd.offsets.MonthEnd(2))
    return list(pd.date_range(start, end, freq="ME"))[::-1]  # newest first


def fetch_hkex(report: list[str]) -> dict[str, pd.Series]:
    from .data import load_snapshot  # local import: data imports specs only

    have_pe, have_dy = load_snapshot("hkex_mb_pe"), load_snapshot("hkex_mb_yield")
    last = have_dy.index[-1] if have_dy is not None and len(have_dy) else None
    months = _months(last, pd.Timestamp.now(tz="Asia/Hong_Kong").tz_localize(None))
    pe, dy, misses, statuses = {}, {}, 0, []
    session = requests.Session()
    for m in months:
        url = PAGE.format(yymm=m.strftime("%y%m"))
        try:
            r = session.get(url, headers=HEADERS, timeout=30)
        except requests.RequestException as exc:
            statuses.append(f"{m:%Y-%m}: {exc.__class__.__name__}")
            misses += 1
        else:
            if r.status_code != 200:
                statuses.append(f"{m:%Y-%m}: HTTP {r.status_code}")
                misses += 1
            else:
                got = parse_page(r.text)
                p, y = got["pe"][0], got["yield"][0]
                if p is not None and PE_OK[0] <= p <= PE_OK[1]:
                    pe[m] = p
                if y is not None and DY_OK[0] <= y <= DY_OK[1]:
                    dy[m] = y
                    misses = 0
                else:
                    statuses.append(f"{m:%Y-%m}: page found but no 'Average yield' row; text starts "
                                    + _text(r.text)[:300])
                    misses += 1
        # The newest month may not be published yet; give up only after a run of misses
        if misses >= 4 and not dy:
            break
        if misses >= 6:
            break
    if statuses:
        report.append("hkex notes: " + " | ".join(statuses[:8]))
    if not dy and (have_dy is None or have_dy.empty):
        raise LookupError("HKEX monthly bulletin: no pages parsed (first tried "
                          + PAGE.format(yymm=months[0].strftime("%y%m")) + ")")
    out = {}
    for key, new, old in (("hkex_mb_yield", dy, have_dy), ("hkex_mb_pe", pe, have_pe)):
        s = pd.Series(new, dtype=float).sort_index()
        if old is not None and len(old):
            s = pd.concat([old[~old.index.isin(s.index)], s]).sort_index()
        if len(s):
            s.name = key
            out[key] = s
    if "hkex_mb_yield" in out:
        s = out["hkex_mb_yield"]
        report.append(f"hkex_mb_yield: {len(dy)} month(s) fetched this run; {len(s)} obs, "
                      f"latest {s.index[-1]:%Y-%m} = {s.iloc[-1]:.2f}%"
                      + (f"; P/E {out['hkex_mb_pe'].iloc[-1]:.2f}" if "hkex_mb_pe" in out else ""))
    return out
