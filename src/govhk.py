"""C&SD, RVD and ORO data via DATA.GOV.HK.

DATA.GOV.HK runs CKAN, so `package_show` lists every file in a dataset with its
current download URL. Each run we look the files up by name, download them and
find the series by row/column labels (agency tables move cells around between
releases). Anything not found is described in the source report so the label
patterns can be tuned.
"""
from __future__ import annotations

import csv
import io
import re
from dataclasses import dataclass

import pandas as pd
import requests

from .periods import is_year_cell, parse_period
from .xlsx_scan import describe, find_series, load_sheets

CKAN = "https://data.gov.hk/en-data/api/3/action/package_show"
USER_AGENT = "Mozilla/5.0 (compatible; hk-credit-macro-dashboard/1.0)"


def _get(url: str, timeout: float = 90.0, **kw) -> requests.Response:
    r = requests.get(url, timeout=timeout, headers={"User-Agent": USER_AGENT}, **kw)
    r.raise_for_status()
    return r


def resources(package_id: str) -> list[dict]:
    body = _get(CKAN, params={"id": package_id}).json()
    if not body.get("success", True):
        raise LookupError(f"DATA.GOV.HK: package {package_id} not found")
    return body["result"].get("resources", [])


def pick(res: list[dict], name_pattern: str, formats=("CSV", "XLSX", "XLS"), exclude: str | None = None) -> list[dict]:
    pat, exc = re.compile(name_pattern, re.I), re.compile(exclude, re.I) if exclude else None
    out = []
    for r in res:
        name, fmt = r.get("name", ""), (r.get("format") or "").upper()
        if pat.search(name) and fmt in formats and not (exc and exc.search(name)):
            out.append(r)
    return sorted(out, key=lambda r: formats.index((r.get("format") or "").upper()))


def load_rows(url: str, fmt: str) -> list[list]:
    content = _get(url, timeout=180).content
    fmt = fmt.upper()
    if fmt == "XLSX":
        sheets = load_sheets(content, max_rows=5000)
        return [row for rows in sheets.values() for row in rows + [[]]]
    if fmt == "XLS":
        frames = pd.read_excel(io.BytesIO(content), sheet_name=None, header=None)
        rows = []
        for df in frames.values():
            rows += df.where(pd.notna(df), None).values.tolist() + [[]]
        return rows
    for enc in ("utf-8-sig", "big5hkscs", "cp950", "latin-1"):
        try:
            text = content.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    rows = []
    for row in csv.reader(io.StringIO(text)):
        rows.append([_num_or_text(c) for c in row])
    return rows


def _num_or_text(c: str):
    s = c.strip()
    if s == "":
        return None
    t = s.replace(",", "")
    if re.fullmatch(r"-?\d+(\.\d+)?", t):
        return float(t) if "." in t else int(t)
    return s


def _text(v) -> str:
    return v.strip() if isinstance(v, str) else ""


def _num(v) -> float | None:
    if isinstance(v, bool) or v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        t = v.strip().replace(",", "").rstrip("%")
        try:
            return float(t)
        except ValueError:
            return None
    return None


@dataclass
class Found:
    series: pd.Series
    how: str


def series_from_rows(rows: list[list], label_pattern: str, default_year: int | None = None,
                     valid: tuple[float, float] | None = None, min_points: int = 6) -> Found:
    """Find a labelled series in a table, trying several layouts."""
    pat = re.compile(label_pattern, re.I)
    candidates: list[Found] = []

    def ok(s: pd.Series) -> bool:
        if len(s) < min_points:
            return False
        return valid is None or s.tail(12).between(*valid).all()

    # 1) dates in one row or column, labels beside them (generic scanner)
    for m in find_series({"t": rows}, label_pattern, min_points=min_points):
        if ok(m.series):
            candidates.append(Found(m.series, f"label '{m.label}' ({m.orientation})"))

    # 2) one period per row, year possibly in its own column or carried forward
    year = default_year
    periods: dict[int, pd.Timestamp] = {}
    for r, row in enumerate(rows):
        found = None
        for v in row[:3]:
            y = is_year_cell(v)
            if y:
                year = y
                continue
            p, y2 = parse_period(v, year)
            if y2:
                year = y2
            if p is not None:
                found = p
                break
        if found is not None:
            periods[r] = found
    if len(periods) >= min_points:
        first = min(periods)
        width = max((len(x) for x in rows), default=0)
        headers = rows[max(0, first - 6):first]
        labels = []
        for c in range(width):
            parts = []
            for h in headers:
                t = _text(h[c]) if c < len(h) else ""
                parts.append(t)
            labels.append(" ".join(p for p in parts if p))
        for c, lab in enumerate(labels):
            if not lab or not pat.search(lab):
                continue
            pts = {}
            for r, p in periods.items():
                v = _num(rows[r][c]) if c < len(rows[r]) else None
                if v is not None:
                    pts[p] = v
            s = pd.Series(pts, dtype=float).sort_index()
            s = s[~s.index.duplicated(keep="last")]
            if ok(s):
                candidates.append(Found(s, f"column '{lab}' with periods by row"))
        # 3) long format: the label is in the row itself, value is the row's last number
        pts = {}
        for r, p in periods.items():
            row = rows[r]
            text = " ".join(_text(v) for v in row if _text(v))
            if not pat.search(text):
                continue
            nums = [_num(v) for v in row[1:] if not is_year_cell(v) and parse_period(v, year)[0] is None]
            nums = [n for n in nums if n is not None]
            if nums:
                pts[p] = nums[-1]
        s = pd.Series(pts, dtype=float).sort_index()
        if ok(s):
            candidates.append(Found(s, "row label, last numeric cell (long format)"))

    if not candidates:
        raise LookupError(f"no series matching /{label_pattern}/")
    best = max(candidates, key=lambda f: (f.series.index[-1], len(f.series)))
    best.series = best.series[~best.series.index.duplicated(keep="last")]
    return best


def yoy_change(level: pd.Series) -> pd.Series:
    s = level.asfreq("ME") if _monthly(level) else level
    lag = 12 if _monthly(level) else 4
    return ((s / s.shift(lag) - 1) * 100).dropna()


def _monthly(s: pd.Series) -> bool:
    return len(s) > 2 and s.index.to_series().diff().dt.days.median() < 45


def rolling_12m(monthly: pd.Series) -> pd.Series:
    return monthly.asfreq("ME").rolling(12, min_periods=12).sum().dropna()


# ---------------------------------------------------------------- source definitions

@dataclass
class TableSpec:
    key: str
    packages: tuple[str, ...]  # tried in order
    resource_pattern: str
    label_patterns: tuple[str, ...]  # tried in order
    valid: tuple[float, float]
    resource_exclude: str | None = None


CSD_SPECS = [
    TableSpec("unemployment", ("hk-censtatd-tablechart-210-06101",), r"\[English\]",
              (r"unemployment rate.*seasonally adjusted|seasonally adjusted.*unemployment rate",
               r"^\s*unemployment rate"), (0.5, 15)),
    TableSpec("cpi_yoy", ("hk-censtatd-tablechart-510-60001",), r"\[English\]",
              (r"composite.*(year-on-year|% change|change over)|(year-on-year|% change).*composite",
               r"composite"), (-10, 20)),
    TableSpec("gdp_yoy", ("hk-censtatd-tablechart-310-31001", "hk-censtatd-tablechart-310-31003",
                          "hk-censtatd-tablechart-310-30001"), r"\[English\]",
              (r"(gdp|gross domestic product).*(real|chained).*(change|year-on-year)|"
               r"(year-on-year|% change).*(real|chained)",
               r"real terms|chained.*change"), (-15, 20)),
]


def fetch_table(spec: TableSpec, report: list[str]) -> pd.Series:
    errors = []
    for pkg in spec.packages:
        try:
            res = resources(pkg)
        except Exception as exc:
            errors.append(f"{pkg}: {exc}")
            continue
        chosen = pick(res, spec.resource_pattern, exclude=spec.resource_exclude)
        if not chosen:
            errors.append(f"{pkg}: no resource matching /{spec.resource_pattern}/ among "
                          + "; ".join(f"{r.get('name')} [{r.get('format')}]" for r in res[:12]))
            continue
        r = chosen[0]
        rows = load_rows(r["url"], r.get("format", "CSV"))
        for lp in spec.label_patterns:
            try:
                f = series_from_rows(rows, lp, valid=spec.valid)
                f.series.name = spec.key
                report.append(f"{spec.key}: {pkg} / {r.get('name')} -> {f.how}; {len(f.series)} obs, "
                              f"latest {f.series.index[-1]:%Y-%m} = {f.series.iloc[-1]:.4g}")
                return f.series
            except LookupError as exc:
                errors.append(f"{pkg}: {exc}")
        errors.append(f"{pkg} layout ({r.get('name')}):\n" + describe({"table": rows[:400]},
                      r"unemploy|composite|gdp|domestic|change|seasonal|year|period", max_lines=30))
    raise LookupError(f"{spec.key} not found\n" + "\n".join(errors))


def fetch_csd(report: list[str]) -> dict[str, pd.Series]:
    out = {}
    for spec in CSD_SPECS:
        try:
            out[spec.key] = fetch_table(spec, report)
        except Exception as exc:
            report.append(f"FAILED {spec.key}: {exc}")
    return out


RVD_PACKAGE = "hk-rvd-tsinfo_rvd-property-market-statistics"


def fetch_rvd(report: list[str]) -> dict[str, pd.Series]:
    res = resources(RVD_PACKAGE)
    chosen = pick(res, r"Price Indices by Class \(Territory-wide\) - Monthly", formats=("CSV", "XLSX", "XLS"))
    if not chosen:
        raise LookupError("RVD: monthly territory-wide price index file not found among "
                          + "; ".join(r.get("name", "") for r in res[:30]))
    r = chosen[0]
    rows = load_rows(r["url"], r.get("format", "CSV"))
    last_exc = None
    for lp in (r"all classes|^\s*overall|all\s*$|territory-wide", r"index"):
        try:
            f = series_from_rows(rows, lp, valid=(30, 600))
            idx = f.series
            idx.name = "home_price_index"
            yoy = yoy_change(idx)
            yoy.name = "home_price_yoy"
            report.append(f"home_price_index: {r.get('name')} -> {f.how}; {len(idx)} obs, "
                          f"latest {idx.index[-1]:%Y-%m} = {idx.iloc[-1]:.1f}")
            return {"home_price_index": idx, "home_price_yoy": yoy}
        except LookupError as exc:
            last_exc = exc
    raise LookupError(f"RVD: {last_exc}\n" + describe({"table": rows[:200]}, r"class|index|all|month|year"))


ORO_PACKAGE = "hk-oro-oro-statistics"


def _oro_series(res: list[dict], name_pattern: str, key: str, valid: tuple[float, float], report: list[str]) -> pd.Series:
    files = pick(res, name_pattern, formats=("CSV", "XLSX", "XLS"),
                 exclude=r"search|individual voluntary|IVA|Chinese|中文|annual statistics on number")
    files = [f for f in files if not re.search(r"\((traditional|simplified) chinese\)", f.get("name", ""), re.I)]
    if not files:
        raise LookupError(f"ORO: no file matching /{name_pattern}/")
    parts, used, problems = [], [], []
    for f in files:
        name = f.get("name", "")
        years = re.findall(r"(?<!\d)(20\d\d)(?!\d)", name)
        default_year = int(years[-1]) if years else None
        rows = None
        try:
            rows = load_rows(f["url"], f.get("format", "CSV"))
            found = series_from_rows(rows, r"petition", default_year=default_year, valid=valid, min_points=3)
            parts.append(found.series)
            used.append(f"{name} ({found.how})")
        except Exception as exc:
            problems.append((name, exc, rows))
    if not parts:
        name, exc, rows = problems[0]
        detail = describe({"table": rows[:120]}, r"petition|month|order|total") if rows else ""
        raise LookupError(f"ORO {key}: {exc} in {name}\n{detail}")
    s = pd.concat(parts).sort_index()
    s = s[~s.index.duplicated(keep="last")]
    s.name = key
    report.append(f"{key}: {len(used)} ORO file(s); {len(s)} obs, latest {s.index[-1]:%Y-%m} = {s.iloc[-1]:.0f}")
    return s


def fetch_oro(report: list[str]) -> dict[str, pd.Series]:
    res = resources(ORO_PACKAGE)
    out = {}
    for key, pattern, valid in (("winding_up_petitions", r"compulsory winding", (0, 1000)),
                                ("bankruptcy_petitions", r"bankruptc", (0, 5000))):
        try:
            m = _oro_series(res, pattern, key, valid, report)
            out[key] = m
            r12 = rolling_12m(m)
            if len(r12):
                r12.name = f"{key}_12m"
                out[f"{key}_12m"] = r12
        except Exception as exc:
            report.append(f"FAILED {key}: {exc}\nORO files: " + "; ".join(
                f"{r.get('name')} [{r.get('format')}]" for r in res[:40]))
    return out
