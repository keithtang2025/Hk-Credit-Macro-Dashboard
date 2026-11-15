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


class NotData(ValueError):
    """The link returned a web page instead of a data file."""


def _json_rows(obj) -> list[list]:
    """Largest list of records anywhere in a JSON document, as header + rows."""
    best: list = []

    def walk(o):
        nonlocal best
        if isinstance(o, list):
            if o and all(isinstance(x, dict) for x in o[:20]) and len(o) > len(best):
                best = o
            for x in o[:50]:
                walk(x)
        elif isinstance(o, dict):
            for v in o.values():
                walk(v)

    walk(obj)
    if not best:
        if isinstance(obj, list) and obj and isinstance(obj[0], list):
            return obj
        raise LookupError("no records in JSON")
    keys: list[str] = []
    for rec in best:
        for k in rec:
            if k not in keys:
                keys.append(k)
    return [keys] + [[_num_or_text(str(rec.get(k))) if rec.get(k) is not None else None for k in keys] for rec in best]


def load_rows(url: str, fmt: str) -> list[list]:
    content = _get(url, timeout=180).content
    fmt = fmt.upper()
    head = content[:400].lstrip().lower()
    if head.startswith(b"<!doctype html") or head.startswith(b"<html"):
        raise NotData(f"{url} is a web page, not a data file")
    if fmt == "JSON" or head.startswith(b"{") or head.startswith(b"["):
        import json
        return _json_rows(json.loads(content.decode("utf-8-sig")))
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
        y0 = is_year_cell(row[0]) if row else None
        if y0 and len(row) > 1 and isinstance(row[1], (int, float)) and not isinstance(row[1], bool) \
                and row[1] == int(row[1]) and 1 <= row[1] <= 12:
            year = y0
            periods[r] = (pd.Timestamp(y0, int(row[1]), 1) + pd.offsets.MonthEnd(0)).normalize()
            continue
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

        def texty(row) -> bool:
            cells = [v for v in row if v not in (None, "")]
            return bool(cells) and sum(isinstance(v, str) and _num(v) is None for v in cells) >= 0.5 * len(cells)

        header_idx = [i for i in range(first) if texty(rows[i])][-3:]
        headers = [rows[i] for i in header_idx] or rows[max(0, first - 6):first]
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
        # 3) long format: the label is in the row itself; the value is in a column named
        #    like figure/value, else the row's last number
        header = rows[first - 1] if first > 0 else []
        val_col = next((c for c, h in enumerate(header) if isinstance(h, str)
                        and re.fullmatch(r"\s*(figure|value|obs_value|data|amount|count)\s*", h, re.I)), None)
        pts = {}
        for r, p in periods.items():
            row = rows[r]
            text = " ".join(_text(v) for v in row if _text(v))
            if not pat.search(text):
                continue
            if val_col is not None and val_col < len(row) and _num(row[val_col]) is not None:
                pts[p] = _num(row[val_col])
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


# ---------------------------------------------------------------- C&SD web-table API records

CSD_CORE = {"freq", "period", "sv", "svDesc", "figure", "sd_value"}


@dataclass
class CsdRule:
    freqs: tuple[str, ...]          # preferred frequency codes, best first (M3M, M, Q)
    desc: str                       # regex on svDesc (unit / transformation)
    sv_include: str = r"."          # regex on the sv code
    sv_exclude: str = r"^$"
    dim_include: str | None = None  # regex that some dimension description must match
    prefer: str = r"$^"             # regex on "sv svDesc" that wins ties


def csd_select(rows: list[list], rule: CsdRule, valid: tuple[float, float]) -> tuple[pd.Series, str, str]:
    """Pick one series from C&SD long-format records. Returns (series, how, candidate list)."""
    df = pd.DataFrame(rows[1:], columns=rows[0])
    dims = [c for c in df.columns if c not in CSD_CORE and not str(c).endswith("Desc")]
    for d in dims:  # keep totals: blank code, or description 'Total'
        desc_col = f"{d}Desc"
        blank = df[d].isna() | (df[d].astype(str).str.strip().isin(["", "None", "T", "TOT", "Total"]))
        if rule.dim_include and desc_col in df.columns:
            hit = df[desc_col].astype(str).str.contains(rule.dim_include, case=False, regex=True)
            if hit.any():
                df = df[hit]
                continue
        if blank.any():
            df = df[blank]
    df = df.copy()
    df["value"] = pd.to_numeric(df["figure"], errors="coerce")
    df["date"] = [parse_period(str(p))[0] for p in df["period"]]
    df = df.dropna(subset=["value", "date"])
    groups = []
    for (freq, sv, desc), g in df.groupby(["freq", "sv", "svDesc"], dropna=False):
        s = g.set_index("date")["value"].sort_index()
        s = s[~s.index.duplicated(keep="last")]
        groups.append((str(freq), str(sv), str(desc), s))
    listing = "; ".join(f"{f}/{sv}/{d} ({len(s)} obs, last {s.index[-1]:%Y-%m} = {s.iloc[-1]:.4g})"
                        for f, sv, d, s in groups if len(s))
    cands = []
    for f, sv, d, s in groups:
        if f not in rule.freqs or len(s) < 6:
            continue
        if not re.search(rule.desc, d, re.I) or not re.search(rule.sv_include, sv, re.I) \
                or re.search(rule.sv_exclude, sv, re.I):
            continue
        if not s.tail(12).between(*valid).all():
            continue
        score = (rule.freqs.index(f) * -1, bool(re.search(rule.prefer, f"{sv} {d}", re.I)), s.index[-1], len(s))
        cands.append((score, f, sv, d, s))
    if not cands:
        raise LookupError(f"no C&SD series fits the rule; series in table: {listing}")
    _, f, sv, d, s = max(cands, key=lambda c: c[0])
    return s, f"C&SD records freq={f} sv={sv} svDesc='{d}'", listing


# ---------------------------------------------------------------- source definitions

@dataclass
class TableSpec:
    key: str
    packages: tuple[str, ...]  # tried in order
    resource_pattern: str
    label_patterns: tuple[str, ...]  # tried in order
    valid: tuple[float, float]
    resource_exclude: str | None = None
    csd: CsdRule | None = None


CSD_SPECS = [
    TableSpec("unemployment", ("hk-censtatd-tablechart-210-06101",), r"\[English\]",
              (r"(?=.*unemployment rate)(?=.*seasonally adjusted)(?!.*(not|non)[- ]seasonally)",
               r"(?=.*unemployment rate)(?!.*under)"), (0.5, 15),
              csd=CsdRule(freqs=("M3M", "M"), desc=r"%", sv_include=r"^(SAUR|UR)$", prefer=r"^SAUR")),
    TableSpec("cpi_yoy", ("hk-censtatd-tablechart-510-60001",), r"\[English\]",
              (r"(?=.*composite)(?=.*(year-on-year|% change|change over|yoy))",
               r"(?=.*(year-on-year|% change|change over))(?!.*(cpi\s*\(a\)|cpi\s*\(b\)|cpi\s*\(c\)))"), (-10, 20),
              csd=CsdRule(freqs=("M",), desc=r"year-on-year", sv_include=r"^CC_", prefer=r"^CC_")),
    TableSpec("gdp_yoy", ("hk-censtatd-tablechart-310-31001", "hk-censtatd-tablechart-310-31003",
                          "hk-censtatd-tablechart-310-30001"), r"\[English\]",
              (r"(?=.*(gdp|gross domestic product))(?=.*(real|chained))(?=.*(change|year-on-year))",
               r"(?=.*(real terms|chained))(?=.*change)"), (-15, 20),
              csd=CsdRule(freqs=("Q",), desc=r"year-on-year", sv_include=r"^CON$")),
]


def fetch_table(spec: TableSpec, report: list[str]) -> pd.Series:
    errors = []
    for pkg in spec.packages:
        try:
            res = resources(pkg)
        except Exception as exc:
            errors.append(f"{pkg}: {exc}")
            continue
        chosen = pick(res, spec.resource_pattern, formats=("JSON", "XLSX", "CSV", "XLS"),
                      exclude=spec.resource_exclude)
        if not chosen:
            errors.append(f"{pkg}: no resource matching /{spec.resource_pattern}/ among "
                          + "; ".join(f"{r.get('name')} [{r.get('format')}]" for r in res[:12]))
            continue
        for r in chosen:
            label = f"{r.get('name')} [{r.get('format')}] {r.get('url')}"
            try:
                rows = load_rows(r["url"], r.get("format", "CSV"))
            except Exception as exc:
                errors.append(f"{pkg}: {label}: {exc.__class__.__name__}: {exc}")
                continue
            if spec.csd and rows and {"sv", "figure", "period"} <= set(map(str, rows[0])):
                try:
                    s, how, listing = csd_select(rows, spec.csd, spec.valid)
                    s.name = spec.key
                    report.append(f"{spec.key}: {pkg} -> {how}; {len(s)} obs, latest {s.index[-1]:%Y-%m} = {s.iloc[-1]:.4g}")
                    report.append(f"  (all series in {pkg}: {listing[:2500]})")
                    return s
                except LookupError as exc:
                    errors.append(f"{pkg}: {exc}"[:4000])
                    continue
            for lp in spec.label_patterns:
                try:
                    f = series_from_rows(rows, lp, valid=spec.valid)
                    f.series.name = spec.key
                    report.append(f"{spec.key}: {pkg} / {label} -> {f.how}; {len(f.series)} obs, "
                                  f"latest {f.series.index[-1]:%Y-%m} = {f.series.iloc[-1]:.4g}")
                    return f.series
                except LookupError as exc:
                    errors.append(f"{pkg}: {label}: {exc}")
            errors.append(f"{pkg} layout of {label}:\n" + describe({"table": rows[:400]},
                          r"unemploy|composite|gdp|domestic|change|seasonal|year|period|sv|figure", max_lines=30))
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


YIELD_CLASSES = "ABCDE"


def _class_pattern(c: str) -> str:
    return rf"^\s*class\s*{c}\b(?!\s*[,&])(?!.*remark)"


def fetch_rvd_yields(report: list[str]) -> dict[str, pd.Series]:
    """RVD private domestic rental yields, % (annual rent / price), monthly by class.

    RVD publishes yields by flat size class (A smallest to E largest) without an
    all-class figure, so the dashboard shows the simple average of the classes and Class A."""
    res = resources(RVD_PACKAGE)
    chosen = (pick(res, r"Private Domestic - Property Market Yields - Monthly")
              or pick(res, r"Property Market Yields.*Monthly")
              or pick(res, r"Property Market Yields"))
    if not chosen:
        raise LookupError("RVD: property market yields file not found among "
                          + "; ".join(r.get("name", "") for r in res[:40]))
    r = chosen[0]
    rows = load_rows(r["url"], r.get("format", "CSV"))
    valid = (0.3, 15.0)
    classes: dict[str, pd.Series] = {}
    for c in YIELD_CLASSES:
        try:
            classes[c] = series_from_rows(rows, _class_pattern(c.lower()), valid=valid).series
        except LookupError:
            pass
    overall = None
    try:
        overall = series_from_rows(rows, r"all classes|^\s*overall|average", valid=valid).series
    except LookupError:
        pass
    if not classes and overall is None:
        raise LookupError(f"RVD yields: no class columns in {r.get('name')}\n"
                          + describe({"table": rows[:200]}, r"class|yield|month|year|%"))
    if overall is None:
        frame = pd.concat(classes, axis=1).dropna(how="all")
        overall = frame.mean(axis=1)
        how = f"average of classes {', '.join(classes)}"
    else:
        how = "all-classes column"
    out = {}
    overall = overall.dropna()
    overall.name = "rental_yield"
    out["rental_yield"] = overall
    if "A" in classes:
        a = classes["A"].dropna()
        a.name = "rental_yield_class_a"
        out["rental_yield_class_a"] = a
    report.append(f"rental_yield: {r.get('name')} -> {how}; {len(overall)} obs, "
                  f"latest {overall.index[-1]:%Y-%m} = {overall.iloc[-1]:.2f}%")
    for c, s in classes.items():
        report.append(f"  class {c}: latest {s.index[-1]:%Y-%m} = {s.iloc[-1]:.2f}%")
    return out


ORO_PACKAGE = "hk-oro-oro-statistics"


def _oro_series(res: list[dict], name_pattern: str, key: str, valid: tuple[float, float], report: list[str]) -> pd.Series:
    files = pick(res, name_pattern, formats=("CSV", "XLSX", "XLS", "JSON"),
                 exclude=r"search|individual voluntary|IVA|Chinese|中文|annual statistics on number|profile|percentage|type")
    monthly = [f for f in files if re.search(r"month", f.get("name", ""), re.I)]
    files = monthly or files
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
    combined = [r for r in pick(res, r"^\s*Statistics on Compulsory Winding-up and Bankruptcy", formats=("CSV", "XLSX", "XLS"))
                if not re.search(r"chinese", r.get("name", ""), re.I)]
    if combined:
        r = combined[0]
        rows = load_rows(r["url"], r.get("format", "CSV"))
        for key, pattern, valid in (("winding_up_petitions", r"winding-?\s?up petition", (0, 1000)),
                                    ("bankruptcy_petitions", r"bankruptcy petition", (0, 5000))):
            try:
                f = series_from_rows(rows, pattern, valid=valid)
                m = f.series
                m.name = key
                out[key] = m
                r12 = rolling_12m(m)
                if len(r12):
                    r12.name = f"{key}_12m"
                    out[f"{key}_12m"] = r12
                report.append(f"{key}: {r.get('name')} -> {f.how}; {len(m)} obs, latest {m.index[-1]:%Y-%m} = {m.iloc[-1]:.0f}")
            except LookupError as exc:
                report.append(f"FAILED {key} in {r.get('name')}: {exc}\n" + describe({"t": rows[:60]}, r"petition|month|year"))
        if out:
            return out
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
            names = sorted({r.get("name", "") for r in res if "(English)" in r.get("name", "")
                            or not re.search(r"chinese", r.get("name", ""), re.I)})
            report.append(f"FAILED {key}: {exc}\nAll ORO English files ({len(names)}):\n- " + "\n- ".join(names))
    return out
