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

# HKEX moved its site; the report name stayed (the bulletin page loads
# "data=rpt_Stock_market_highlights_YYMM"), so try the known locations in turn.
PATTERNS = [
    "https://www.hkex.com.hk/eng/stat/smstat/mthbull/rpt_Stock_market_highlights_{yymm}.htm",
    "https://www.hkex.com.hk/-/media/HKEX-Market/Market-Data/Statistics/Consolidated-Reports/Monthly-Bulletin/rpt_Stock_market_highlights_{yymm}.htm",
    "https://www.hkex.com.hk/eng/stat/smstat/mthbull/rpt_stock_market_highlights_{yymm}.htm",
    "https://www.hkex.com.hk/-/media/HKEX-Market/Market-Data/Statistics/Consolidated-Reports/Monthly-Bulletin/rpt_Stock_market_highlights_{yymm}.html",
]
PAGE = PATTERNS[0]
BULLETIN = "https://www.hkex.com.hk/Market-Data/Statistics/Consolidated-Reports/Monthly-Bulletin?sc_lang=en"
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


def _discover(session, report: list[str]) -> list[str]:
    """Look in the bulletin page (and its scripts) for where the monthly reports live."""
    found: list[str] = []
    try:
        page = session.get(BULLETIN, headers=HEADERS, timeout=30).text
    except requests.RequestException as exc:
        report.append(f"hkex discovery: bulletin page {exc.__class__.__name__}")
        return found
    hits = set(re.findall(r"[\"'(]([^\"'()\s]*(?:mthbull|rpt_|Monthly-Bulletin/)[^\"'()\s]*)", page))
    scripts = [s for s in re.findall(r"<script[^>]+src=[\"']([^\"']+)", page)][:15]
    for src in scripts:
        url = src if src.startswith("http") else "https://www.hkex.com.hk" + src
        try:
            js = session.get(url, headers=HEADERS, timeout=30).text
        except requests.RequestException:
            continue
        for h in re.findall(r"[\"']([^\"'\s]*(?:mthbull|rpt_|Monthly-Bulletin/|smstat)[^\"'\s]*)[\"']", js):
            hits.add(h)
    report.append("hkex discovery: " + ("; ".join(sorted(hits)[:30]) if hits else "no report paths in page or "
                                       f"{len(scripts)} scripts"))
    for h in hits:
        if "{" in h or "rpt_" not in h and "mthbull" not in h:
            continue
        base = h if h.startswith("http") else "https://www.hkex.com.hk" + ("" if h.startswith("/") else "/") + h
        m = re.search(r"rpt_Stock_market_highlights_\d{4}", base, re.I)
        if m:
            found.append(base[:m.start()] + "rpt_Stock_market_highlights_{yymm}" + base[m.end():])
    return found


def fetch_hkex(report: list[str]) -> dict[str, pd.Series]:
    from .data import load_snapshot  # local import: data imports specs only

    have_pe, have_dy = load_snapshot("hkex_mb_pe"), load_snapshot("hkex_mb_yield")
    last = have_dy.index[-1] if have_dy is not None and len(have_dy) else None
    months = _months(last, pd.Timestamp.now(tz="Asia/Hong_Kong").tz_localize(None))
    pe, dy, statuses = {}, {}, []
    session = requests.Session()
    patterns = list(PATTERNS)
    requests_made = 0
    for i, m in enumerate(months):
        if i == 3 and not dy:  # nothing for the latest months: look for the new location once
            patterns = _discover(session, report) + patterns
        hit = False
        for pat in list(patterns):
            url = pat.format(yymm=m.strftime("%y%m"))
            try:
                r = session.get(url, headers=HEADERS, timeout=30)
            except requests.RequestException as exc:
                statuses.append(f"{m:%Y-%m}: {exc.__class__.__name__}")
                continue
            if r.status_code != 200:
                continue
            got = parse_page(r.text)
            p, y = got["pe"][0], got["yield"][0]
            if y is None or not DY_OK[0] <= y <= DY_OK[1]:
                statuses.append(f"{m:%Y-%m}: {url} has no 'Average yield' row; text starts " + _text(r.text)[:200])
                continue
            dy[m] = y
            if p is not None and PE_OK[0] <= p <= PE_OK[1]:
                pe[m] = p
            patterns.remove(pat)
            patterns.insert(0, pat)  # keep using what works
            hit = True
            break
        if not hit:
            statuses.append(f"{m:%Y-%m}: not found")
        # Pages from before the site move may still exist, so keep going through a gap
        # in recent months; only a request budget stops the backfill.
        requests_made += len(patterns) if not hit else 1
        if requests_made > 1200:
            statuses.append(f"{m:%Y-%m}: request budget reached, continuing next run")
            break
    if statuses:
        gaps = [s for s in statuses if s.endswith("not found")]
        other = [s for s in statuses if not s.endswith("not found")]
        if gaps:
            report.append(f"hkex: {len(gaps)} month(s) not found, newest {gaps[0][:7]}, oldest {gaps[-1][:7]}")
        if other:
            report.append("hkex notes: " + " | ".join(other[:6]))
    if not dy and (have_dy is None or have_dy.empty):
        raise LookupError("HKEX monthly bulletin: no pages parsed; tried " + ", ".join(
            p.format(yymm=months[0].strftime("%y%m")) for p in PATTERNS))
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
