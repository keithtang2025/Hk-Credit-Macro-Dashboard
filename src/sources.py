"""Run every source; one failing source never blocks the others."""
from __future__ import annotations

import pandas as pd

from . import govhk, hkma, market

HISTORY_START = pd.Timestamp("2010-01-01")


def fetch_all() -> tuple[dict[str, pd.Series], dict[str, str], str]:
    series: dict[str, pd.Series] = {}
    errors: dict[str, str] = {}
    report = ["# Source report (written by the daily refresh)", ""]

    def run(name, fn):
        report.append(f"## {name}")
        lines: list[str] = []
        try:
            got = fn(lines)
            series.update(got)
            if not got:
                errors[name] = "no series found"
        except Exception as exc:  # network, layout or parse failure
            errors[name] = f"{exc.__class__.__name__}: {str(exc).splitlines()[0] if str(exc) else ''}"
            lines.append(f"FAILED {exc.__class__.__name__}: {exc}")
        report.extend(lines + [""])

    def hkma_source(lines):
        got, text = hkma.fetch_hkma()
        lines.append(text)
        return got

    run("HKMA open API", hkma_source)
    run("C&SD (via DATA.GOV.HK)", govhk.fetch_csd)
    run("RVD property price index (via DATA.GOV.HK)", govhk.fetch_rvd)
    run("RVD rental yields (via DATA.GOV.HK)", govhk.fetch_rvd_yields)
    run("Official Receiver's Office (via DATA.GOV.HK)", govhk.fetch_oro)
    run("Hang Seng Indexes (dividend yield, P/E)", market.fetch_hsi)

    series = {k: s[s.index >= HISTORY_START] for k, s in series.items() if s is not None and len(s)}
    return series, errors, "\n".join(report)
