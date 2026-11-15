"""Plotly figures for the dashboard."""
from __future__ import annotations

import math

import pandas as pd
import plotly.graph_objects as go

BLUE, ORANGE, TEAL, GREY, RED, PURPLE = "#2563eb", "#ea580c", "#0d9488", "#94a3b8", "#dc2626", "#7c3aed"
PALETTE = [BLUE, ORANGE, TEAL, PURPLE]


def _base(fig: go.Figure, ysuffix: str = "%", height: int = 300) -> go.Figure:
    fig.update_layout(
        template="plotly_white", height=height, margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0), hovermode="x unified",
        font=dict(family="Inter, system-ui, sans-serif", size=12),
    )
    fig.update_yaxes(ticksuffix=ysuffix, gridcolor="#eef2f7", zeroline=False)
    fig.update_xaxes(showgrid=False)
    return fig


def empty(msg: str = "Fills in after the first daily refresh") -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(text=msg, showarrow=False, font=dict(color=GREY))
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return _base(fig)


def _trim(s: pd.Series, years: int) -> pd.Series:
    return s[s.index >= s.index[-1] - pd.DateOffset(years=years)]


def _last_label(fig, s: pd.Series, color: str, fmt: str):
    fig.add_annotation(x=s.index[-1], y=s.iloc[-1], text=fmt.format(s.iloc[-1]), showarrow=False,
                       yshift=14, xanchor="right", font=dict(color=color))


def lines(parts: list[tuple[pd.Series | None, str]], years: int = 6, fmt: str = "{:.2f}%",
          ysuffix: str = "%", step: bool = False, label_last: bool = True, band=None) -> go.Figure:
    parts = [(s, n) for s, n in parts if s is not None and not s.empty]
    if not parts:
        return empty()
    fig = go.Figure()
    if band:
        fig.add_hrect(y0=band[0], y1=band[1], fillcolor="#16a34a", opacity=0.08, line_width=0,
                      annotation_text=band[2], annotation_position="top left",
                      annotation_font=dict(color="#15803d", size=11))
    for i, (s, name) in enumerate(parts):
        s = _trim(s, years)
        color = PALETTE[i % len(PALETTE)]
        fig.add_trace(go.Scatter(x=s.index, y=s.values, name=name, mode="lines" if len(s) > 40 else "lines+markers",
                                 line=dict(color=color, width=2, shape="hv" if step else "linear"),
                                 marker=dict(size=4), hovertemplate=fmt.replace("{:", "%{y:").replace("}", "}")))
        if label_last:
            _last_label(fig, s, color, fmt)
    fig = _base(fig, ysuffix)
    if len(parts) == 1:
        fig.update_layout(showlegend=False)
    return fig


def bars(s: pd.Series | None, years: int = 6, fmt: str = "{:.1f}%", ysuffix: str = "%",
         neg_bad: bool = True, quarterly: bool = False) -> go.Figure:
    if s is None or s.empty:
        return empty()
    s = _trim(s, years)
    labels = [f"Q{(d.month - 1) // 3 + 1} {d.year}" for d in s.index] if quarterly else s.index
    colors = [RED if (v < 0 and neg_bad) else BLUE for v in s.values]
    fig = go.Figure(go.Bar(x=labels, y=s.values, marker_color=colors,
                           text=[fmt.format(v) for v in s.values] if len(s) <= 16 else None,
                           textposition="outside", hovertemplate="%{x}: " + fmt.replace("{:", "%{y:") + "<extra></extra>"))
    fig = _base(fig, ysuffix)
    fig.update_layout(hovermode="closest")
    fig.add_hline(y=0, line_color=GREY, line_width=1)
    return fig


def _nice_step(raw: float) -> float:
    if raw <= 0:
        return 1.0
    mag = 10 ** math.floor(math.log10(raw))
    for f in (1, 2, 2.5, 5, 10):
        if f * mag >= raw:
            return f * mag
    return 10 * mag


def monthly_with_12m(monthly: pd.Series | None, r12: pd.Series | None, years: int = 6) -> go.Figure:
    if monthly is None or monthly.empty:
        return empty()
    m = _trim(monthly, years)
    fig = go.Figure(go.Bar(x=m.index, y=m.values, name="Monthly", marker_color=GREY,
                           hovertemplate="%{x|%b %Y}: %{y:,.0f}<extra></extra>"))
    if r12 is not None and not r12.empty:
        r = r12[r12.index >= m.index[0]]
        fig.add_trace(go.Scatter(x=r.index, y=r.values, name="Rolling 12 months (right)", yaxis="y2",
                                 line=dict(color=ORANGE, width=2.5), hovertemplate="%{y:,.0f}<extra></extra>"))
        ls, rs = _nice_step(m.max() / 4), _nice_step(r.max() / 4)
        fig.update_layout(yaxis=dict(range=[0, ls * 4.05], tick0=0, dtick=ls),
                          yaxis2=dict(overlaying="y", side="right", showgrid=False, tickformat=",.0f",
                                      range=[0, rs * 4.05], tick0=0, dtick=rs))
    fig = _base(fig, ysuffix="")
    fig.update_yaxes(tickformat=",.0f")
    return fig


def peg(s: pd.Series | None, years: int = 6) -> go.Figure:
    """USD/HKD inside the 7.75-7.85 Linked Exchange Rate band."""
    if s is None or s.empty:
        return empty()
    s = _trim(s, years)
    fig = go.Figure()
    for y, txt in ((7.85, "Weak-side limit 7.85"), (7.75, "Strong-side limit 7.75")):
        fig.add_hline(y=y, line_dash="dot", line_color=RED if y == 7.85 else TEAL,
                      annotation_text=txt, annotation_position="bottom left" if y == 7.85 else "top left",
                      annotation_font=dict(size=11))
    fig.add_trace(go.Scatter(x=s.index, y=s.values, mode="lines+markers", line=dict(color=BLUE, width=2),
                             marker=dict(size=4), name="USD/HKD", hovertemplate="%{y:.4f}<extra></extra>"))
    fig = _base(fig, ysuffix="")
    fig.update_yaxes(range=[7.73, 7.87], tickformat=".2f")
    fig.update_layout(showlegend=False)
    return fig
