"""Dashboard content shared by the Dash app (app.py) and the static GitHub Pages build
(scripts/build_static.py): KPI cards and chart sections, as plain data."""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from . import charts


@dataclass
class Kpi:
    label: str
    series: pd.Series | None
    fmt: str
    sub: str


@dataclass
class Card:
    title: str
    note: str
    fig: object
    cid: str


@dataclass
class Section:
    title: str
    sid: str
    cards: list


def kpi(label, s, fmt, sub) -> Kpi:
    return Kpi(label, s, fmt, sub)


def card(title, note, fig, cid) -> Card:
    return Card(title, note, fig, cid)


def section(title, sid, cards) -> Section:
    return Section(title, sid, cards)


def kpis(s: dict[str, pd.Series]) -> list[Kpi]:
    return [
            kpi("HKMA base rate", s.get("base_rate"), "{:.2f}%", "Discount Window base rate"),
            kpi("1-month HIBOR", s.get("hibor_1m"), "{:.2f}%", "HKAB fixing, month end"),
            kpi("Unemployment", s.get("unemployment"), "{:.1f}%", "Seasonally adjusted"),
            kpi("Home prices", s.get("home_price_yoy"), "{:+.1f}%", "Year on year, RVD"),
            kpi("Rental yield", s.get("rental_yield"), "{:.2f}%", "Average of classes A to E, RVD"),
            kpi("HSI dividend yield", s.get("hsi_dividend_yield"), "{:.2f}%", "Hang Seng Index"),
            kpi("Mortgage delinquency", s.get("mortgage_delinquency"), "{:.2f}%", "Overdue 3 months or more"),
    ]


def sections(s: dict[str, pd.Series]) -> list[Section]:
    return [
        section("Rates and liquidity", "rates", [
            card("Policy rate and HIBOR", "HKMA base rate and HKAB HIBOR fixings, month end, %.",
                 charts.lines([(s.get("base_rate"), "Base rate"), (s.get("hibor_1m"), "1M HIBOR"),
                               (s.get("hibor_3m"), "3M HIBOR")], label_last=False), "c-rates"),
            card("Aggregate balance", "Banks' clearing balances at the HKMA, month end, HK$ billion. Falls when the peg is defended.",
                 charts.lines([(s.get("aggregate_balance"), "Aggregate balance")], fmt="{:,.0f}", ysuffix=""), "c-agg"),
            card("USD/HKD and the peg", "HKD per USD, month end, within the 7.75 to 7.85 Convertibility Undertaking band. Federal Reserve H.10 rate (via FRED) or ECB reference rates where HKMA's feed is unavailable.",
                 charts.peg(s.get("usdhkd")), "c-peg"),
        ]),
        section("Property and mortgages", "property", [
            card("Home prices", "RVD private domestic price index, all classes, year-on-year change %. Red bars are declines.",
                 charts.bars(s.get("home_price_yoy"), years=4), "c-hpi"),
            card("Home price index", "RVD private domestic price index, all classes (1999 = 100).",
                 charts.lines([(s.get("home_price_index"), "All classes")], years=15, fmt="{:.1f}", ysuffix=""), "c-hpi-level"),
            card("Mortgage delinquency", "Residential mortgages overdue more than 3 months, % of outstanding. HKMA survey.",
                 charts.lines([(s.get("mortgage_delinquency"), "Delinquency ratio")], years=10), "c-mdr"),
        ]),
        section("Yields and valuation", "yields", [
            card("Rental yield and funding cost", "RVD private domestic rental yields (annual rent as % of price), "
                 "average of classes A to E, Class A (under 40 m2) and Class E (160 m2 and over), against 1-month HIBOR, "
                 "which prices most new mortgages.",
                 charts.lines([(s.get("rental_yield"), "Average A to E"),
                               (s.get("rental_yield_class_a"), "Class A (small)"),
                               (s.get("rental_yield_class_e"), "Class E (large)"),
                               (s.get("hibor_1m"), "1M HIBOR")], years=10, label_last=False), "c-ryield"),
            card("Rental yield gap", "Rental yield less 1-month HIBOR, percentage points. Red bars mean rent earns "
                 "less than the HIBOR funding cost, which leaves investors and buyers more exposed.",
                 charts.bars(s.get("rental_yield_spread"), years=4, fmt="{:+.1f}", ysuffix=" pp"), "c-rgap"),
            card("Stock, property and cash yields", "Hang Seng Index dividend yield vs residential rental yield and "
                 "3-month HIBOR, %. HSI history from Hang Seng Indexes' dividend yield report "
                 "(data/manual/hsi_valuation.csv); later months from the monthly factsheet.",
                 charts.lines([(s.get("hsi_dividend_yield"), "HSI dividend yield"),
                               (s.get("rental_yield"), "Rental yield"), (s.get("hibor_3m"), "3M HIBOR")],
                              years=10, label_last=False), "c-yields"),
            card("Hang Seng Index P/E", "Month-end weighted average P/E ratio, times. History from Hang Seng Indexes' "
                 "P/E report (data/manual/hsi_valuation.csv); later months from the monthly factsheet.",
                 charts.lines([(s.get("hsi_pe"), "HSI P/E")], years=20, fmt="{:.1f}x", ysuffix="x"), "c-pe"),
        ]),
        section("Banking asset quality", "banks", [
            card("Classified loans", "Classified loan ratio of retail banks, % of total loans. Quarterly.",
                 charts.lines([(s.get("classified_loans"), "Classified loans")], years=10), "c-classified"),
            card("Credit card charge-offs", "Charge-off ratio of credit card receivables, % (annualised).",
                 charts.lines([(s.get("card_chargeoff"), "Charge-off ratio")], years=10), "c-cards"),
            card("Loan growth", "Year-on-year growth in loans and advances, %.",
                 charts.lines([(s.get("loan_growth"), "Total loans"), (s.get("loan_growth_hk"), "For use in Hong Kong")],
                              label_last=False), "c-loans"),
        ]),
        section("Economy and corporate stress", "economy", [
            card("Unemployment", "Seasonally adjusted unemployment rate, %. C&SD.",
                 charts.lines([(s.get("unemployment"), "Unemployment")], years=10, fmt="{:.1f}%"), "c-unemp"),
            card("Real GDP growth", "Year-on-year change in real GDP, %. C&SD. Red bars are contractions.",
                 charts.bars(s.get("gdp_yoy"), years=5, quarterly=True), "c-gdp"),
            card("Inflation", "Composite CPI, year-on-year change, %. C&SD.",
                 charts.lines([(s.get("cpi_yoy"), "Composite CPI")], fmt="{:.1f}%"), "c-cpi"),
            card("Compulsory winding-up petitions", "Petitions presented to the court: monthly and rolling 12 months. ORO.",
                 charts.monthly_with_12m(s.get("winding_up_petitions"), s.get("winding_up_petitions_12m")), "c-wu"),
            card("Bankruptcy petitions", "Petitions presented: monthly and rolling 12 months. ORO.",
                 charts.monthly_with_12m(s.get("bankruptcy_petitions"), s.get("bankruptcy_petitions_12m")), "c-bk"),
            card("Loan-to-deposit ratio", "Total loans as % of total customer deposits, all authorized institutions.",
                 charts.lines([(s.get("loan_to_deposit"), "Loan-to-deposit")], years=10, fmt="{:.1f}%"), "c-ldr"),
        ]),
    ]


HEADER_SOURCES = ("HKMA, C&SD, RVD, the Official Receiver's Office and Hang Seng Indexes")
STATUS_NOTE = ("All series are refreshed each day by a GitHub Action and committed as a snapshot. Manual series "
               "(data/manual): HKMA quarterly survey of residential mortgages in negative equity, and the Hang Seng "
               "Indexes P/E and dividend yield history (later months come from the monthly factsheet).")
FOOTER = ("Data: Hong Kong Monetary Authority, Census and Statistics Department, Rating and Valuation Department, "
          "Official Receiver's Office (via DATA.GOV.HK); Hang Seng Indexes; USD/HKD from HKMA, the Federal Reserve "
          "H.10 release via FRED, or ECB reference rates. Not investment advice.")
