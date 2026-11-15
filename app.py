"""Hong Kong Credit Risk Macro Dashboard (Plotly Dash).

Run locally:   python app.py
Production:    gunicorn app:server
"""
from __future__ import annotations

import os

import pandas as pd
from dash import Dash, dash_table, dcc, html

from src import charts
from src.data import get_data
from src.scorecard import EASING, RISING, build_scorecard, summary
from src.specs import SERIES

app = Dash(__name__, title="Hong Kong Credit Risk Macro Dashboard")
server = app.server
CONFIG = {"displayModeBar": False, "responsive": True}


def _when(s: pd.Series | None) -> str:
    if s is None or s.empty:
        return ""
    d = s.index[-1]
    if len(s) > 2 and s.index.to_series().diff().dt.days.median() > 45:
        return f"Q{(d.month - 1) // 3 + 1} {d.year}"
    return d.strftime("%b %Y")


def kpi(label: str, s: pd.Series | None, fmt: str, sub: str) -> html.Div:
    value = fmt.format(float(s.iloc[-1])) if s is not None and not s.empty else "n/a"
    when = _when(s)
    return html.Div(className="card kpi", children=[
        html.Div(f"{label}, {when}" if when else label, className="muted small"),
        html.Div(value, className="big"), html.Div(sub, className="muted small"),
    ])


def card(title: str, note: str, fig, cid: str) -> html.Div:
    return html.Div(className="card", id=cid, children=[
        html.H3(title), html.P(note, className="muted small"),
        dcc.Graph(figure=fig, config=CONFIG, style={"height": "300px"}),
    ])


def section(title: str, sid: str, cards: list) -> html.Section:
    return html.Section(id=sid, children=[html.H2(title, className="section-title"), html.Div(className="grid", children=cards)])


def scorecard_table(df: pd.DataFrame):
    if df.empty:
        return html.P("The scorecard fills in after the first daily refresh.", className="muted")
    cols = ["Indicator", "Latest", "Period", "Prior", "Prior period", "Signal", "Source"]
    return dash_table.DataTable(
        data=df[cols].to_dict("records"),
        columns=[{"name": c, "id": c, "type": "numeric" if c in ("Latest", "Prior") else "text",
                  "format": {"specifier": ",.2~f"} if c in ("Latest", "Prior") else None} for c in cols],
        tooltip_data=[{"Indicator": n} if n else {} for n in df["Note"].fillna("")],
        style_as_list_view=True, style_table={"overflowX": "auto"},
        style_header={"fontWeight": 600, "backgroundColor": "#f8fafc", "color": "#475569", "fontSize": 12},
        style_cell={"fontFamily": "Inter, system-ui, sans-serif", "fontSize": 13, "padding": "8px 10px",
                    "textAlign": "left", "border": "none", "borderBottom": "1px solid #e5e7eb"},
        style_cell_conditional=[{"if": {"column_id": c}, "textAlign": "right"} for c in ("Latest", "Prior")],
        style_data_conditional=[
            {"if": {"filter_query": f'{{Signal}} = "{RISING}"', "column_id": "Signal"}, "color": "#dc2626", "fontWeight": 600},
            {"if": {"filter_query": f'{{Signal}} = "{EASING}"', "column_id": "Signal"}, "color": "#16a34a", "fontWeight": 600},
        ],
    )


def status_table(d) -> html.Table:
    rows = []
    for key, info in SERIES.items():
        s = d.series.get(key)
        origin = d.origin.get(key, "missing")
        rows.append(html.Tr([html.Td(info.label), html.Td(info.source), html.Td(_when(s) or "n/a"),
                             html.Td(origin, className=f"badge {origin}")]))
    return html.Table(className="status", children=[
        html.Thead(html.Tr([html.Th("Series"), html.Th("Source"), html.Th("Latest obs."), html.Th("Data")])),
        html.Tbody(rows),
    ])


def serve_layout():
    d = get_data()
    s = d.series
    score = build_scorecard(s, d.origin, d.stress)
    n_up, n_cmp = summary(score) if not score.empty else (0, 0)
    n_have = sum(1 for k in SERIES if k in s)
    refreshed = f"Data last refreshed {d.refreshed_at:%d %b %Y}. " if d.refreshed_at is not None else ""

    return html.Div(className="page", children=[
        html.Header(children=[
            html.H1("Hong Kong: macro drivers of credit risk"),
            html.P(f"{refreshed}{n_have} of {len(SERIES)} series loaded from HKMA, C&SD, RVD and the Official "
                   f"Receiver's Office, refreshed daily. Negative equity figures are updated quarterly by hand.",
                   className="muted small"),
            html.P(className="takeaway", children=[
                "Of the indicators with a comparison point, ", html.B(str(n_up)), " of ", html.B(str(n_cmp)),
                " are moving toward higher credit risk.",
            ]),
        ]),
        html.Div(className="kpis", children=[
            kpi("HKMA base rate", s.get("base_rate"), "{:.2f}%", "Discount Window base rate"),
            kpi("1-month HIBOR", s.get("hibor_1m"), "{:.2f}%", "HKAB fixing, month end"),
            kpi("Unemployment", s.get("unemployment"), "{:.1f}%", "Seasonally adjusted"),
            kpi("Home prices", s.get("home_price_yoy"), "{:+.1f}%", "Year on year, RVD"),
            kpi("Mortgage delinquency", s.get("mortgage_delinquency"), "{:.2f}%", "Overdue 3 months or more"),
        ]),
        html.Section(className="card", id="scorecard", children=[
            html.H2("Credit risk scorecard"),
            html.P("Signal compares the latest print with the one about 12 months earlier (or the previous print "
                   "where history is short), in the direction that worsens borrower credit quality. Hover an "
                   "indicator for notes.", className="muted small"),
            scorecard_table(score),
        ]),
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
        html.Details(className="card", children=[
            html.Summary("Data sources and status"),
            status_table(d),
            html.P("All series are refreshed each morning by a GitHub Action and committed as a snapshot. Manual "
                   "series (data/manual): HKMA quarterly survey of residential mortgages in negative equity.",
                   className="muted small"),
        ]),
        html.Footer("Built with Plotly Dash. Data: Hong Kong Monetary Authority, Census and Statistics Department, "
                    "Rating and Valuation Department, Official Receiver's Office (via DATA.GOV.HK); USD/HKD from HKMA, the Federal Reserve "
                    "H.10 release via FRED, or ECB reference rates. Not investment advice.",
                    className="muted small"),
    ])


app.layout = serve_layout

if __name__ == "__main__":
    app.run(debug=os.getenv("DEBUG", "0") == "1", host="0.0.0.0", port=int(os.getenv("PORT", "8050")))
