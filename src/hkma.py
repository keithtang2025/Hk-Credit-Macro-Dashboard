"""Hong Kong Monetary Authority open API (https://apidocs.hkma.gov.hk).

Every endpoint returns {"header": {...}, "result": {"datasize": n, "records": [...]}},
newest first, at most 1,000 rows per call (paged with offset).
"""
from __future__ import annotations

import re

import pandas as pd
import requests

BASE = "https://api.hkma.gov.hk/public/market-data-and-statistics/"
USER_AGENT = "hk-credit-macro-dashboard/1.0 (research dashboard)"
PAGE = 1000


def _call(path: str, q: dict, timeout: float) -> list[dict]:
    r = requests.get(BASE + path, params=q, timeout=timeout, headers={"User-Agent": USER_AGENT})
    r.raise_for_status()
    body = r.json()
    header = body.get("header", {})
    if header.get("success") is False:
        raise RuntimeError(f"HKMA {path}: {header.get('err_code')} {header.get('err_msg')}")
    return body.get("result", {}).get("records", [])


def get_records(path: str, params: dict | None = None, max_rows: int = 5000, timeout: float = 60.0) -> list[dict]:
    """Page through an endpoint. Some endpoints reject a large pagesize (HTTP 405) or a
    deep offset, so fall back to the default page size and keep whatever was fetched."""
    rows: list[dict] = []
    offset, size = 0, PAGE
    seen_first = None
    while offset < max_rows:
        q = {"offset": offset, **(params or {})}
        if size:
            q["pagesize"] = size
        try:
            batch = _call(path, q, timeout)
        except requests.HTTPError:
            if size and offset == 0:
                size = None  # endpoint does not accept pagesize: use its default page
                continue
            if rows:
                break  # deep page refused: keep what we have
            raise
        if not batch:
            break
        if seen_first == batch[0]:
            break  # endpoint ignores offset: same page again
        seen_first = batch[0]
        rows.extend(batch)
        if size and len(batch) < size:
            break
        offset += len(batch)
    return rows


def date_key(records: list[dict]) -> str:
    keys = records[0].keys() if records else []
    for k in keys:
        if k in ("end_of_month", "end_of_date", "end_of_day", "date"):
            return k
    for k in keys:
        if "date" in k or k.startswith("end_of"):
            return k
    raise KeyError(f"no date field in HKMA records: {list(keys)}")


def to_frame(records: list[dict]) -> pd.DataFrame:
    """Records -> DataFrame indexed by month-end (monthly) or day (daily).

    Annual rows that HKMA labels like '2025-00' are dropped.
    """
    if not records:
        return pd.DataFrame()
    dk = date_key(records)
    df = pd.DataFrame(records)
    raw = df[dk].astype(str).str.strip()
    monthly = raw.str.fullmatch(r"\d{4}-\d{2}")
    if monthly.all() or monthly.mean() > 0.5:
        keep = raw.str.fullmatch(r"\d{4}-(0[1-9]|1[0-2])")
        df, raw = df[keep], raw[keep]
        idx = pd.to_datetime(raw, format="%Y-%m") + pd.offsets.MonthEnd(0)
    else:
        idx = pd.to_datetime(raw, errors="coerce")
        df, idx = df[idx.notna()], idx[idx.notna()]
    df = df.drop(columns=[dk]).apply(pd.to_numeric, errors="coerce")
    df.index = pd.DatetimeIndex(idx).normalize()
    return df[~df.index.duplicated(keep="first")].sort_index()


def field(df: pd.DataFrame, name: str, key: str) -> pd.Series:
    if name not in df.columns:
        raise KeyError(f"HKMA field '{name}' missing; available: {', '.join(df.columns)}")
    s = df[name].dropna().astype(float)
    s.name = key
    return s


def yoy_growth(level: pd.Series, key: str) -> pd.Series:
    s = level.asfreq("ME")
    g = (s / s.shift(12) - 1) * 100
    g = g.dropna()
    g.name = key
    return g


def month_end_last(daily: pd.Series, key: str) -> pd.Series:
    s = daily.resample("ME").last().dropna()
    s.name = key
    return s


FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv"


def fred_series(series_id: str, start: str = "2010-01-01", timeout: float = 90.0, tries: int = 2) -> pd.Series:
    """A FRED series as a daily pd.Series (no API key needed for the CSV download).

    FRED can be slow to answer cloud servers, so ask only for recent data and retry."""
    import io
    import time

    last_exc = None
    for attempt in range(tries):
        try:
            r = requests.get(FRED_CSV, params={"id": series_id, "cosd": start}, timeout=timeout,
                             headers={"User-Agent": USER_AGENT})
            r.raise_for_status()
            break
        except requests.RequestException as exc:
            last_exc = exc
            time.sleep(5 * (attempt + 1))
    else:
        raise last_exc
    df = pd.read_csv(io.StringIO(r.text))
    if df.shape[1] < 2:
        raise ValueError(f"FRED {series_id}: unexpected CSV columns {list(df.columns)}")
    s = pd.Series(pd.to_numeric(df.iloc[:, 1], errors="coerce").values,
                  index=pd.to_datetime(df.iloc[:, 0], errors="coerce")).dropna()
    return s[s.index.notna()].sort_index()


ECB_API = "https://data-api.ecb.europa.eu/service/data/EXR/"


def ecb_month_end(currency: str, timeout: float = 60.0) -> pd.Series:
    """ECB end-of-month reference rate: units of `currency` per EUR."""
    import io

    r = requests.get(f"{ECB_API}M.{currency}.EUR.SP00.E", params={"format": "csvdata", "startPeriod": "2010-01"},
                     timeout=timeout, headers={"User-Agent": USER_AGENT})
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    idx = pd.to_datetime(df["TIME_PERIOD"], format="%Y-%m") + pd.offsets.MonthEnd(0)
    return pd.Series(pd.to_numeric(df["OBS_VALUE"], errors="coerce").values, index=idx).dropna().sort_index()


def ecb_usdhkd() -> pd.Series:
    """HKD per USD as the cross of the ECB's HKD/EUR and USD/EUR month-end rates."""
    s = (ecb_month_end("HKD") / ecb_month_end("USD")).dropna()
    s.name = "usdhkd"
    return s


# ---------------------------------------------------------------- series builders

def fetch_hkma() -> tuple[dict[str, pd.Series], str]:
    """All HKMA series. Each endpoint fails independently."""
    out: dict[str, pd.Series] = {}
    notes, errors = [], []

    def step(name, fn):
        try:
            got = fn()
            out.update(got)
            for k, s in got.items():
                notes.append(f"{k}: {name}; {len(s)} obs, latest {s.index[-1]:%Y-%m} = {s.iloc[-1]:.4g}")
        except Exception as exc:  # network, HTTP, schema
            errors.append(f"{name}: {exc.__class__.__name__}: {exc}")

    def banking():
        df = to_frame(get_records("monthly-statistical-bulletin/financial/banking-statistics"))
        res = {
            "card_chargeoff": field(df, "chroff_ratio_of_crcard_rece", "card_chargeoff"),
            "loan_growth": yoy_growth(field(df, "loans_total", "x"), "loan_growth"),
            "loan_growth_hk": yoy_growth(field(df, "loans_in_hk", "x"), "loan_growth_hk"),
        }
        cl = field(df, "classif_loans", "classified_loans")
        if len(cl) and cl.tail(8).between(0, 20).all():  # a ratio (% of retail bank loans), not HK$ m
            res["classified_loans"] = cl
        ldr = (field(df, "loans_total", "x") / field(df, "cust_deposits_total", "x") * 100).dropna()
        ldr.name = "loan_to_deposit"
        res["loan_to_deposit"] = ldr
        return res

    def mortgage_survey():
        df = to_frame(get_records("monthly-statistical-bulletin/banking/residential-mortgage-survey",
                                  {"segment": "new"}))
        return {"mortgage_delinquency": field(df, "delinquency_ratio", "mortgage_delinquency")}

    def hibor():
        df = to_frame(get_records("monthly-statistical-bulletin/er-ir/hk-interbank-ir-endperiod",
                                  {"segment": "hibor.fixing"}))
        return {"hibor_1m": field(df, "ir_1m", "hibor_1m"), "hibor_3m": field(df, "ir_3m", "hibor_3m")}

    def base_rate():
        df = to_frame(get_records("monthly-statistical-bulletin/monetary-operation/disc-win-liquid-adj-win-rates-endperiod"))
        return {"base_rate": field(df, "disc_win_base_rate", "base_rate")}

    def liquidity():
        df = to_frame(get_records("daily-monetary-statistics/daily-figures-interbank-liquidity", max_rows=6000))
        res = {"aggregate_balance": month_end_last(field(df, "closing_balance", "x") / 1000, "aggregate_balance")}
        try:  # daily base rate keeps the current month current between bulletins
            res["base_rate_daily"] = month_end_last(field(df, "disc_win_base_rate", "x"), "base_rate_daily")
        except KeyError:
            pass
        return res

    def usdhkd():
        """HKD per USD. The end-of-period endpoint has refused requests, so try alternatives."""
        tries = [("monthly-statistical-bulletin/er-ir/er-eeri-endperiod", "usd", False),
                 ("monthly-statistical-bulletin/er-ir/hkd-fer-endperiod", None, False),
                 ("monthly-statistical-bulletin/er-ir/hkd-fer-daily", None, True),
                 ("monthly-statistical-bulletin/er-ir/er-eeri-daily", "usd", True),
                 ("monthly-statistical-bulletin/financial/monetary-statistics", "exrate_hkd_usd", False)]
        problems = []
        for path, name, daily in tries:
            try:
                df = to_frame(get_records(path, max_rows=3000))
                if name is None:  # forward-rate tables: use their spot-rate column
                    name = next((c for c in df.columns if re.search(r"spot", c, re.I)), None)
                    if name is None:
                        raise KeyError(f"no spot column; fields: {', '.join(df.columns)}")
                s = field(df, name, "usdhkd")
                if daily:
                    s = month_end_last(s, "usdhkd")
                s = s[(s > 7.0) & (s < 8.5)]  # HKD per USD around the 7.75-7.85 band
                if len(s):
                    notes.append(f"usdhkd source: {path}")
                    return {"usdhkd": s}
                problems.append(f"{path}: no values in range")
            except Exception as exc:
                problems.append(f"{path}: {exc.__class__.__name__}: {str(exc)[:120]}")
        # HKMA's exchange-rate endpoints refuse GitHub's servers (HTTP 405), so fall back to the
        # Federal Reserve H.10 noon buying rate in New York, HKD per USD, via FRED.
        try:
            s = month_end_last(fred_series("DEXHKUS"), "usdhkd")
            s = s[(s > 7.0) & (s < 8.5)]
            if len(s):
                notes.append("usdhkd source: FRED DEXHKUS (Federal Reserve H.10), month-end; HKMA endpoints refused: "
                             + "; ".join(p.split(":")[0] for p in problems))
                return {"usdhkd": s}
            problems.append("FRED DEXHKUS: no values in range")
        except Exception as exc:
            problems.append(f"FRED DEXHKUS: {exc.__class__.__name__}: {str(exc)[:120]}")
        # Last resort: ECB month-end HKD and USD reference rates (both per EUR), crossed
        try:
            s = ecb_usdhkd()
            s = s[(s > 7.0) & (s < 8.5)]
            if len(s):
                notes.append("usdhkd source: ECB reference rates, HKD/EUR divided by USD/EUR, month-end; earlier "
                             "sources failed: " + "; ".join(p.split(":")[0] for p in problems))
                return {"usdhkd": s}
            problems.append("ECB cross rate: no values in range")
        except Exception as exc:
            problems.append(f"ECB cross rate: {exc.__class__.__name__}: {str(exc)[:120]}")
        raise LookupError("; ".join(problems))

    step("HKMA banking statistics", banking)
    step("HKMA residential mortgage survey", mortgage_survey)
    step("HKMA HIBOR fixings", hibor)
    step("HKMA base rate", base_rate)
    step("HKMA daily interbank liquidity", liquidity)
    step("HKMA exchange rates", usdhkd)

    # one base-rate series: monthly bulletin extended by the daily figures
    if "base_rate_daily" in out:
        daily = out.pop("base_rate_daily")
        monthly = out.get("base_rate", pd.Series(dtype=float, name="base_rate"))
        merged = pd.concat([monthly, daily[~daily.index.isin(monthly.index)]]).sort_index()
        merged.name = "base_rate"
        out["base_rate"] = merged

    report = "\n".join(notes + ([""] + [f"FAILED {e}" for e in errors] if errors else []))
    if not out:
        raise RuntimeError("all HKMA endpoints failed\n" + report)
    return out, report
