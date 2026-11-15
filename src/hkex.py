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
    # current site: one JSON per month (found by the discovery step on 15 Nov 2026)
    "https://www.hkex.com.hk/eng/stat/smstat/mthbull/MonthlyBulletin_{yymm}.json",
    # old site: one HTML page per month (still served for 2016-07 to 2017-09)
    "https://www.hkex.com.hk/eng/stat/smstat/mthbull/rpt_Stock_market_highlights_{yymm}.htm",
]
MAX_REQUESTS, MAX_SECONDS = 150, 240
from pathlib import Path  # noqa: E402

MISSING = Path(__file__).resolve().parent.parent / "data" / "history" / "hkex_missing_months.txt"


def _known_missing() -> set[str]:
    return set(MISSING.read_text().split()) if MISSING.exists() else set()  # per run; the backfill continues on later runs
PAGE = PATTERNS[1]
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
    return {"pe": _first_two(text, r"Average (?:P\s*/\s*E|price[\s-]*earnings?) ratios?\s*\((?:times|x)\)"),
            "yield": _first_two(text, r"Average (?:dividend )?yield\s*\(%\)")}


def _flatten(o, out: list[str]) -> list[str]:
    if isinstance(o, dict):
        for v in o.values():
            _flatten(v, out)
    elif isinstance(o, list):
        for v in o:
            _flatten(v, out)
    elif o is not None:
        out.append(str(o))
    return out


def parse_any(resp_text: str, url: str) -> dict[str, tuple[float | None, float | None]]:
    """Bulletin JSON (any nesting; HTML fragments inside are fine) or an HTML page."""
    if url.endswith(".json"):
        import json
        try:
            return parse_page(" ".join(_flatten(json.loads(resp_text), [])))
        except ValueError:
            pass
    return parse_page(resp_text)


def _months(have: pd.Series | None, today: pd.Timestamp) -> list[pd.Timestamp]:
    """Months still to fetch, newest first: every missing month since START, plus the
    last two held (HKEX can revise them)."""
    end = (today - pd.offsets.MonthEnd(1)).normalize()  # last complete month
    allm = pd.date_range(START, end, freq="ME")
    if have is None or have.empty:
        return list(allm)[::-1]
    held = set(have.index.normalize())
    recent = set(have.index[-2:].normalize())
    return [m for m in allm[::-1] if m not in held or m in recent]


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
        if "{" in h or ("rpt_" not in h and "mthbull" not in h):
            continue
        base = h if h.startswith("http") else "https://www.hkex.com.hk" + ("" if h.startswith("/") else "/") + h
        m = re.search(r"(rpt_Stock_market_highlights_|MonthlyBulletin_)\d{4}", base, re.I)
        if m:
            pat = base[:m.start()] + m.group(1) + "{yymm}" + base[m.end():]
            if pat not in found and pat not in PATTERNS:
                found.append(pat)
    return found


def fetch_hkex(report: list[str]) -> dict[str, pd.Series]:
    import time

    from .data import load_snapshot  # local import: data imports specs only

    have_pe, have_dy = load_snapshot("hkex_mb_pe"), load_snapshot("hkex_mb_yield")
    today = pd.Timestamp.now(tz="Asia/Hong_Kong").tz_localize(None)
    skip = _known_missing()
    months = [m for m in _months(have_dy, today) if m.strftime("%Y-%m") not in skip]
    newly_missing: list[str] = []
    pe, dy, statuses = {}, {}, []
    session = requests.Session()
    patterns = list(PATTERNS)
    made, t0 = 0, time.monotonic()
    for i, m in enumerate(months):
        if i == 3 and not dy and (have_dy is None or have_dy.empty):
            patterns = _discover(session, report) + patterns
        hit = False
        for pat in list(patterns):
            url = pat.format(yymm=m.strftime("%y%m"))
            made += 1
            try:
                r = session.get(url, headers=HEADERS, timeout=20)
            except requests.RequestException as exc:
                statuses.append(f"{m:%Y-%m}: {exc.__class__.__name__}")
                continue
            if r.status_code != 200:
                continue
            got = parse_any(r.text, url)
            p, y = got["pe"][0], got["yield"][0]
            if y is None or not DY_OK[0] <= y <= DY_OK[1]:
                flat = _text(" ".join(_flatten(__import__("json").loads(r.text), []))) if url.endswith(".json") \
                    and r.text.lstrip().startswith(("{", "[")) else _text(r.text)
                near = [flat[max(0, k.start() - 100):k.end() + 150] for k in re.finditer(r"yield|P\s*/\s*E|earning", flat, re.I)][:3]
                statuses.append(f"{m:%Y-%m}: {url} has no 'Average yield'; "
                                + (" || ".join(near) if near else "starts " + flat[:400]))
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
            if m < today - pd.DateOffset(months=6):  # long published: HKEX does not have it
                newly_missing.append(m.strftime("%Y-%m"))
        if made >= MAX_REQUESTS or time.monotonic() - t0 > MAX_SECONDS:
            statuses.append(f"{m:%Y-%m}: stopped after {made} requests, the rest continue next run")
            break
    if newly_missing:
        try:
            MISSING.parent.mkdir(parents=True, exist_ok=True)
            MISSING.write_text("\n".join(sorted(skip | set(newly_missing))) + "\n")
        except OSError:
            pass
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
