"""Daily refresh: HKMA API plus C&SD, RVD and ORO files from DATA.GOV.HK.

Run by the scheduled GitHub Action. Updates data/snapshot/*.csv, appends new
and revised values to data/history/, and writes data/debug/source_report.md.
Exits non-zero only if every source failed.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.data import save_snapshot  # noqa: E402
from src.history import record  # noqa: E402
from src.sources import fetch_all  # noqa: E402
from src.specs import SERIES  # noqa: E402


def main() -> int:
    series, errors, report = fetch_all()
    debug = ROOT / "data" / "debug"
    debug.mkdir(parents=True, exist_ok=True)
    (debug / "source_report.md").write_text(report, encoding="utf-8")

    for path in save_snapshot(series):
        print(f"updated {path.name}")
    for name, err in errors.items():
        print(f"FAILED {name}: {err}", file=sys.stderr)
    counts = record(series, errors)
    missing = [k for k in SERIES if k not in series]
    print(f"{len(series)} of {len(SERIES)} series refreshed" + (f"; missing: {', '.join(missing)}" if missing else ""))
    print(f"history: {counts['new']} new values, {counts['revised']} revisions archived")
    return 0 if series else 1


if __name__ == "__main__":
    raise SystemExit(main())
