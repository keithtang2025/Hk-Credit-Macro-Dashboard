"""Series shown on the dashboard and how each feeds the risk scorecard."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SeriesInfo:
    label: str
    source: str
    unit: str = "%"


SERIES: dict[str, SeriesInfo] = {
    # rates and liquidity
    "base_rate": SeriesInfo("HKMA base rate", "HKMA"),
    "hibor_1m": SeriesInfo("1-month HIBOR fixing", "HKMA"),
    "hibor_3m": SeriesInfo("3-month HIBOR fixing", "HKMA"),
    "aggregate_balance": SeriesInfo("Aggregate balance", "HKMA", "HK$ bn"),
    "usdhkd": SeriesInfo("USD/HKD spot", "HKMA / FRED / ECB", "HKD"),
    # banking asset quality
    "classified_loans": SeriesInfo("Classified loan ratio (retail banks)", "HKMA"),
    "mortgage_delinquency": SeriesInfo("Mortgage delinquency ratio (3m+)", "HKMA"),
    "card_chargeoff": SeriesInfo("Credit card charge-off ratio", "HKMA"),
    "loan_growth": SeriesInfo("Total loans, year-on-year growth", "HKMA"),
    "loan_growth_hk": SeriesInfo("Loans for use in Hong Kong, y/y growth", "HKMA"),
    "loan_to_deposit": SeriesInfo("Loan-to-deposit ratio", "HKMA"),
    # property
    "home_price_index": SeriesInfo("Private domestic price index (all classes)", "RVD", "index"),
    "home_price_yoy": SeriesInfo("Home prices, year-on-year change", "RVD"),
    "rental_yield": SeriesInfo("Residential rental yield (average of classes A to E)", "RVD"),
    "rental_yield_class_a": SeriesInfo("Residential rental yield, Class A (under 40 m2)", "RVD"),
    "rental_yield_class_e": SeriesInfo("Residential rental yield, Class E (160 m2 and over)", "RVD"),
    "rental_yield_spread": SeriesInfo("Rental yield less 1-month HIBOR", "RVD / HKMA", "pp"),
    # equity market
    "hsi_dividend_yield": SeriesInfo("Hang Seng Index dividend yield", "Hang Seng Indexes"),
    "hsi_pe": SeriesInfo("Hang Seng Index P/E ratio", "Hang Seng Indexes", "times"),
    "hkex_mb_yield": SeriesInfo("Main Board average dividend yield", "HKEX"),
    "hkex_mb_pe": SeriesInfo("Main Board average P/E ratio", "HKEX", "times"),
    # economy
    "unemployment": SeriesInfo("Unemployment rate (seasonally adjusted)", "C&SD"),
    "cpi_yoy": SeriesInfo("Composite CPI, year-on-year", "C&SD"),
    "gdp_yoy": SeriesInfo("Real GDP, year-on-year", "C&SD"),
    # corporate and personal insolvency
    "winding_up_petitions": SeriesInfo("Compulsory winding-up petitions, monthly", "ORO", "petitions"),
    "winding_up_petitions_12m": SeriesInfo("Winding-up petitions, last 12 months", "ORO", "petitions"),
    "bankruptcy_petitions": SeriesInfo("Bankruptcy petitions, monthly", "ORO", "petitions"),
    "bankruptcy_petitions_12m": SeriesInfo("Bankruptcy petitions, last 12 months", "ORO", "petitions"),
}


@dataclass(frozen=True)
class ScoreItem:
    key: str
    label: str
    higher_is_worse: bool
    note: str = ""


SCORE_ITEMS: list[ScoreItem] = [
    ScoreItem("base_rate", "HKMA base rate", True),
    ScoreItem("hibor_1m", "1-month HIBOR", True, "Most new mortgages are priced off HIBOR"),
    ScoreItem("aggregate_balance", "Aggregate balance (HK$ bn)", False,
              "A smaller balance means tighter interbank liquidity"),
    ScoreItem("usdhkd", "USD/HKD", True, "Nearer 7.85 (weak side) signals capital outflow and tighter liquidity"),
    ScoreItem("unemployment", "Unemployment rate", True),
    ScoreItem("gdp_yoy", "Real GDP growth (y/y)", False),
    ScoreItem("cpi_yoy", "Composite CPI (y/y)", True),
    ScoreItem("home_price_yoy", "Home prices (y/y, RVD)", False),
    ScoreItem("rental_yield_spread", "Rental yield less 1M HIBOR (pp)", False,
              "Carry on a home: a thinner or negative gap means rent covers less of a HIBOR mortgage"),
    ScoreItem("mortgage_delinquency", "Mortgage delinquency ratio", True),
    ScoreItem("classified_loans", "Classified loan ratio", True),
    ScoreItem("card_chargeoff", "Credit card charge-off ratio", True),
    ScoreItem("winding_up_petitions_12m", "Winding-up petitions, 12 months", True),
    ScoreItem("bankruptcy_petitions_12m", "Bankruptcy petitions, 12 months", True),
]

DERIVED = {"rental_yield_spread"}
AUTOMATED_KEYS = set(SERIES) - DERIVED
