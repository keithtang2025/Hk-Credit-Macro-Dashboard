"""Hang Seng Index dividend yield and P/E ratio.

Hang Seng Indexes publishes the latest figures only (no free history file), so the
daily refresh records the reading each day and the snapshot keeps one point per month
(the last reading of the month). History therefore builds up from the first run;
older months can be added by hand in data/manual/hsi_valuation.csv.
"""
from __future__ import annotations

import io
import re
from pathlib import Path

import pandas as pd
import requests

HSI_PERFORMANCE = "https://www.hsi.com.hk/data/eng/rt/index-series/hsi/performance.do"
HSI_SITE = "https://www.hsi.com.hk"
HSI_PAGE_MODEL = HSI_SITE + "/content/wpb/hsil/en_hk/indexes/all-indexes/index-details.model.json"
HSI_FACTSHEET = "https://www.hsi.com.hk/static/uploads/contents/en/dl_centre/factsheets/hsie.pdf"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/126.0 Safari/537.36",
    "Referer": "https://www.hsi.com.hk/eng/indexes/all-indexes/hsi",
    "Accept": "application/json, text/plain, */*",
}
MANUAL = Path(__file__).resolve().parent.parent / "data" / "manual" / "hsi_valuation.csv"
DY_OK, PE_OK = (1.5, 10.0), (4.0, 40.0)  # plausible HSI ranges


def _num(v) -> float | None:
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        m = re.fullmatch(r"\s*([-+]?\d+(?:\.\d+)?)\s*%?\s*", v.replace(",", ""))
        return float(m.group(1)) if m else None
    return None


def _walk(o):
    if isinstance(o, dict):
        yield o
        for v in o.values():
            yield from _walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from _walk(v)


def _is_hsi(d: dict) -> bool:
    code = str(d.get("indexCode", d.get("code", ""))).strip().upper()
    name = str(d.get("indexName", d.get("name", ""))).strip().lower()
    return code == "HSI" or name == "hang seng index"


def _pick(d: dict, pattern: str, ok: tuple[float, float]) -> tuple[str, float] | None:
    for k, v in d.items():
        if re.search(pattern, k, re.I):
            n = _num(v)
            if n is not None and ok[0] <= n <= ok[1]:
                return k, n
    return None


def _as_of(body, entry: dict) -> pd.Timestamp:
    for src in (entry, *(d for d in _walk(body))):
        for k, v in src.items():
            if re.search(r"date|asof|as_of|time", k, re.I) and isinstance(v, (str, int)):
                t = pd.to_datetime(str(v), errors="coerce", dayfirst=False)
                if pd.notna(t) and 2000 <= t.year <= 2100:
                    return pd.Timestamp(t).tz_localize(None).normalize() if t.tzinfo else pd.Timestamp(t).normalize()
    return pd.Timestamp.now(tz="Asia/Hong_Kong").tz_localize(None).normalize()


def parse_performance(body) -> tuple[float, float | None, pd.Timestamp, str]:
    """(dividend yield %, P/E or None, as-of date, description) from the performance JSON."""
    entries = [d for d in _walk(body) if _is_hsi(d)]
    if not entries:
        raise LookupError("HSI entry not found in performance feed")
    for e in entries:
        for part in _walk(e):  # the figures may sit in a nested object
            dy = _pick(part, r"div.*yield|yield", DY_OK)
            if not dy:
                continue
            pe = _pick(part, r"^pe|p/?e.?ratio|pe_?ratio|price.?earn", PE_OK) or next(
                (x for x in (_pick(q, r"^pe|p/?e.?ratio|pe_?ratio|price.?earn", PE_OK) for q in _walk(e)) if x), None)
            how = f"performance feed fields {dy[0]}" + (f", {pe[0]}" if pe else "")
            return dy[1], (pe[1] if pe else None), _as_of(body, e), how
    raise LookupError("HSI entry has no dividend yield field; keys: " + ", ".join(entries[0].keys()))


def parse_factsheet_text(text: str) -> tuple[float, float | None, pd.Timestamp | None]:
    flat = re.sub(r"\s+", " ", text)
    # HSI factsheet "INDEX FUNDAMENTALS" table: the labels come first, then the HSI row,
    # e.g. "Index Dividend Yield (%) PE Ratio (Times) 1 - Yr 3 - Yr 5 - Yr HSI 3.14 13.04 18.29 ..."
    m = re.search(r"Dividend Yield\s*\(%\)\s*P\s*/?\s*E Ratio\s*\(Times\).{0,200}?\bHSI\s+(\d+\.\d+)\s+(\d+\.\d+)",
                  flat, re.I)
    when = re.search(r"as (?:at|of) (\d{1,2} \w{3,9} \d{4}|\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{4})", flat, re.I)
    t = pd.to_datetime(when.group(1), errors="coerce", dayfirst=True) if when else None
    t = None if t is None or pd.isna(t) else t
    if m:
        dy, pe = float(m.group(1)), float(m.group(2))
        if DY_OK[0] <= dy <= DY_OK[1]:
            return dy, (pe if PE_OK[0] <= pe <= PE_OK[1] else None), t
    dy = _after(flat, r"div(?:idend)?\.?\s*yield", DY_OK)
    if dy is None:
        raise LookupError("no dividend yield figure in the factsheet. Text near 'yield' / 'P/E': "
                          + _context(flat))
    pe = _after(flat, r"p\s*/\s*e(?:\s*ratio)?|price.?earnings", PE_OK)
    when = re.search(r"as (?:at|of) (\d{1,2} \w{3,9} \d{4}|\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{4})", flat, re.I)
    t = pd.to_datetime(when.group(1), errors="coerce", dayfirst=True) if when else None
    return dy, pe, (None if t is None or pd.isna(t) else t)


def _after(flat: str, label: str, ok: tuple[float, float], span: int = 60) -> float | None:
    """First number in range within `span` characters after the label."""
    for m in re.finditer(label, flat, re.I):
        for n in re.finditer(r"(?<![\d.])(\d{1,2}\.\d{1,2})(?![\d.])", flat[m.end():m.end() + span]):
            v = float(n.group(1))
            if ok[0] <= v <= ok[1]:
                return v
    return None


def _context(flat: str) -> str:
    bits = [flat[max(0, m.start() - 80):m.end() + 120] for m in re.finditer(r"yield|p\s*/\s*e", flat, re.I)][:6]
    return " || ".join(bits) if bits else "none found; text starts: " + flat[:600]


def _manual() -> dict[str, pd.Series]:
    if not MANUAL.exists():
        return {}
    df = pd.read_csv(MANUAL, parse_dates=["date"]).set_index("date").sort_index()
    df.index = df.index + pd.offsets.MonthEnd(0)
    out = {}
    for col, key in (("dividend_yield", "hsi_dividend_yield"), ("pe_ratio", "hsi_pe")):
        if col in df:
            s = pd.to_numeric(df[col], errors="coerce").dropna()
            if len(s):
                s.name = key
                out[key] = s
    return out


def _with_manual(key: str, latest: pd.Series, manual: dict[str, pd.Series]) -> pd.Series:
    """History file first; a daily reading is only added for months after the file ends."""
    m = manual.get(key)
    if m is None or m.empty:
        return latest
    s = pd.concat([m, latest[latest.index > m.index[-1]]]).sort_index()
    s.name = key
    return s


def _links(obj) -> list[str]:
    """Data-looking paths inside the site's page model JSON."""
    found = []
    for s in re.findall(r"[\"'](/[^\"'\s<>]+|https?://www\.hsi\.com\.hk/[^\"'\s<>]+)[\"']", str(obj)):
        if re.search(r"\.json|\.do\b|/api/|/data/|servlet|\.csv|\.xlsx?", s, re.I) and s not in found:
            found.append(s)
    rank = lambda u: (not re.search(r"perform|index-?detail|indicator|statistic|fundament|valuat|hsi", u, re.I), len(u))
    return sorted(found, key=rank)


def _from_page_model(report: list[str]) -> tuple[float, float | None, pd.Timestamp, str]:
    r = requests.get(HSI_PAGE_MODEL, headers=HEADERS, timeout=60)
    r.raise_for_status()
    body = r.json()
    try:
        return parse_performance(body)[:3] + ("page model JSON",)
    except LookupError:
        pass
    links = _links(body)
    report.append(f"page model: {len(links)} data-looking links: " + "; ".join(links[:25]))
    tried = []
    for link in links[:12]:
        url = link if link.startswith("http") else HSI_SITE + link
        for u in ([url.replace("{seriesCode}", "hsi").replace("${seriesCode}", "hsi")]
                  + ([url + ("&" if "?" in url else "?") + "seriesCode=hsi"] if "seriesCode" not in url else [])):
            try:
                resp = requests.get(u, headers=HEADERS, timeout=45)
                tried.append(f"{u} -> {resp.status_code}")
                if resp.ok and "json" in resp.headers.get("content-type", "") + u:
                    dy, pe, when, how = parse_performance(resp.json())
                    return dy, pe, when, f"{u} ({how})"
            except Exception as exc:
                tried.append(f"{u} -> {exc.__class__.__name__}")
    raise LookupError("no HSI figures via page model; tried " + "; ".join(tried[:20]))


def fetch_hsi(report: list[str]) -> dict[str, pd.Series]:
    problems = []
    dy = pe = when = None
    how = ""
    try:
        dy, pe, when, how = _from_page_model(report)
    except Exception as exc:
        problems.append(f"page model: {exc.__class__.__name__}: {str(exc)[:1500]}")
    if dy is None:
        try:
            r = requests.get(HSI_PERFORMANCE, headers=HEADERS, timeout=60)
            r.raise_for_status()
            dy, pe, when, how = parse_performance(r.json())
        except Exception as exc:
            problems.append(f"performance feed: {exc.__class__.__name__}: {str(exc)[:300]}")
    if dy is None:
        try:
            from pypdf import PdfReader

            r = requests.get(HSI_FACTSHEET, headers={**HEADERS, "Accept": "application/pdf"}, timeout=90)
            r.raise_for_status()
            text = "\n".join(p.extract_text() or "" for p in PdfReader(io.BytesIO(r.content)).pages[:3])
            report.append("factsheet text near 'yield' / 'P/E': " + _context(re.sub(r"\s+", " ", text))[:2500])
            dy, pe, when = parse_factsheet_text(text)
            how = "HSI factsheet PDF"
        except Exception as exc:
            problems.append(f"factsheet: {exc.__class__.__name__}: {str(exc)[:300]}")
    for p in problems:
        report.append(f"note: {p}")
    if dy is None:
        raise LookupError("HSI dividend yield unavailable: " + " | ".join(problems))
    when = when or pd.Timestamp.now(tz="Asia/Hong_Kong").tz_localize(None).normalize()
    month = (when + pd.offsets.MonthEnd(0)).normalize()
    manual = _manual()
    out = {"hsi_dividend_yield": _with_manual("hsi_dividend_yield",
                                               pd.Series([dy], index=[month], name="hsi_dividend_yield"), manual)}
    if pe is not None:
        out["hsi_pe"] = _with_manual("hsi_pe", pd.Series([pe], index=[month], name="hsi_pe"), manual)
    report.append(f"hsi_dividend_yield: {how}; as of {when:%Y-%m-%d} = {dy:.2f}%"
                  + (f", P/E {pe:.2f}" if pe is not None else ", P/E not found"))
    return out
