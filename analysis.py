"""Market data, TA-Lib indicators, and Plotly chart builders."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Callable, Literal

PriceColumn = Literal["Close", "High", "Low"]

import pandas as pd
import plotly.graph_objects as go
import talib
import yfinance as yf
from plotly.subplots import make_subplots

from i18n import chart as chart_label
from i18n import fib_price_column
from i18n import pattern as pattern_text
from i18n import s

OHLCV_COLUMNS = ["Close", "High", "Low", "Open", "Volume"]


@dataclass(frozen=True)
class PatternSpec:
    """How to render a candlestick pattern on the price chart."""

    column: str
    symbol: str
    color: str
    size: int = 14
    filter_fn: Callable[[pd.Series], pd.Series] | None = None


PATTERN_SPECS: dict[str, PatternSpec] = {
    "doji_star": PatternSpec(
        column="DOJISTAR",
        symbol="star",
        color="yellow",
    ),
    "harami": PatternSpec(
        column="HARAMI",
        symbol="diamond",
        color="cyan",
    ),
    "hammer": PatternSpec(
        column="HAMMER",
        symbol="circle",
        color="green",
    ),
    "inverted_hammer": PatternSpec(
        column="INVERTEDHAMMER",
        symbol="triangle-up",
        color="orange",
    ),
    "shooting_star": PatternSpec(
        column="SHOOTINGSTAR",
        symbol="triangle-down",
        color="magenta",
    ),
    "bullish_engulfing": PatternSpec(
        column="ENGULFING",
        symbol="star",
        color="blue",
        size=16,
        filter_fn=lambda s: s == 100,
    ),
    "bearish_engulfing": PatternSpec(
        column="ENGULFING",
        symbol="star-diamond",
        color="red",
        size=16,
        filter_fn=lambda s: s == -100,
    ),
}

DEFAULT_PATTERN_KEYS = list(PATTERN_SPECS.keys())

BULLISH_PATTERN_KEYS = frozenset({"hammer", "inverted_hammer", "bullish_engulfing"})
BEARISH_PATTERN_KEYS = frozenset({"shooting_star", "bearish_engulfing"})
NEUTRAL_PATTERN_KEYS = frozenset({"doji_star", "harami"})
RECENT_TRADING_DAYS = 20
SMA_CROSS_BULL_COL = "SMA_CROSS_BULL"
SMA_CROSS_BEAR_COL = "SMA_CROSS_BEAR"
FIB_RATIOS = [0.0, 0.618, 1.0, 1.618, 2.618]
FIB_POINT_COLORS = {"A": "lime", "B": "gold", "C": "deepskyblue"}


def download_ohlcv(
    ticker: str,
    start: date | str,
    end: date | str,
) -> pd.DataFrame:
    """Download OHLCV from Yahoo Finance and normalize column names."""
    raw = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=False)
    if raw.empty:
        raise ValueError(s("error_no_data", ticker=ticker))

    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.droplevel(-1)

    if "Adj Close" in raw.columns:
        if "Close" in raw.columns:
            raw = raw.drop(columns=["Adj Close"])
        else:
            raw = raw.rename(columns={"Adj Close": "Close"})

    missing = [c for c in OHLCV_COLUMNS if c not in raw.columns]
    if missing:
        raise ValueError(s("error_missing_columns", columns=missing))

    df = raw.loc[:, OHLCV_COLUMNS].copy()
    for col in OHLCV_COLUMNS:
        if isinstance(df[col], pd.DataFrame):
            df[col] = df[col].iloc[:, 0]
    return df


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Add SMA overlays and TA-Lib candlestick pattern columns."""
    out = df.copy()
    out["SMA20"] = talib.SMA(out["Close"], timeperiod=20)
    out["SMA50"] = talib.SMA(out["Close"], timeperiod=50)
    out[SMA_CROSS_BULL_COL] = (
        (out["SMA20"] > out["SMA50"]) & (out["SMA20"].shift(1) <= out["SMA50"].shift(1))
    ).astype(int)
    out[SMA_CROSS_BEAR_COL] = (
        (out["SMA20"] < out["SMA50"]) & (out["SMA20"].shift(1) >= out["SMA50"].shift(1))
    ).astype(int)

    open_, high, low, close = out["Open"], out["High"], out["Low"], out["Close"]
    out["DOJISTAR"] = talib.CDLDOJISTAR(open_, high, low, close)
    out["HARAMI"] = talib.CDLHARAMI(open_, high, low, close)
    out["HAMMER"] = talib.CDLHAMMER(open_, high, low, close)
    out["INVERTEDHAMMER"] = talib.CDLINVERTEDHAMMER(open_, high, low, close)
    out["SHOOTINGSTAR"] = talib.CDLSHOOTINGSTAR(open_, high, low, close)
    out["ENGULFING"] = talib.CDLENGULFING(open_, high, low, close)
    return out


def pattern_signal_mask(series: pd.Series, spec: PatternSpec) -> pd.Series:
    if spec.filter_fn is not None:
        return spec.filter_fn(series)
    return series != 0


def _apply_chart_theme(fig: go.Figure, title: str) -> None:
    """High-contrast labels and legend on a dark chart background."""
    fig.update_layout(
        template="plotly_dark",
        title=dict(text=title, font=dict(color="#fafafa", size=20)),
        font=dict(color="#e8eaed", size=13),
        paper_bgcolor="#0e1117",
        plot_bgcolor="#1a1f2e",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(26, 31, 46, 0.95)",
            bordercolor="rgba(255, 255, 255, 0.35)",
            borderwidth=1,
            font=dict(color="#f5f5f5", size=12),
        ),
        hoverlabel=dict(
            bgcolor="#262b3d",
            bordercolor="#9aa0a6",
            font=dict(color="#ffffff", size=13),
        ),
        separators=".,",
        xaxis_rangeslider_visible=False,
    )
    fig.update_xaxes(
        color="#e8eaed",
        tickfont=dict(color="#e0e3e8", size=12),
        tickformat="%d/%m/%Y",
        linecolor="rgba(255, 255, 255, 0.25)",
        mirror=False,
    )
    fig.update_yaxes(
        color="#e8eaed",
        tickfont=dict(color="#e0e3e8", size=12),
        gridcolor="rgba(255, 255, 255, 0.12)",
        zerolinecolor="rgba(255, 255, 255, 0.2)",
        linecolor="rgba(255, 255, 255, 0.25)",
        mirror=False,
    )


def build_candlestick_with_volume(df: pd.DataFrame, ticker: str) -> go.Figure:
    """Base chart: candlesticks, SMA 20/50, and volume."""
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_width=[0.2, 0.7],
    )

    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name=ticker,
            increasing_line_color="#00cc94",
            decreasing_line_color="#ff6059",
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["SMA20"],
            mode="lines",
            line=dict(color="orange", width=2),
            name=chart_label("sma20"),
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["SMA50"],
            mode="lines",
            line=dict(color="#6eb6ff", width=2),
            name=chart_label("sma50"),
        ),
        row=1,
        col=1,
    )

    colors = [
        "#00cc94" if close >= open_ else "#ff6059"
        for open_, close in zip(df["Open"], df["Close"])
    ]

    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df["Volume"],
            marker_color=colors,
            name=chart_label("volume"),
        ),
        row=2,
        col=1,
    )

    _apply_chart_theme(fig, ticker)
    fig.update_layout(height=900)
    fig.update_xaxes(showgrid=False)
    fig.update_traces(
        hovertemplate=(
            "Fecha: %{x|%d/%m/%Y}<br>"
            "Apertura: %{open:.2f}<br>"
            "Máximo: %{high:.2f}<br>"
            "Mínimo: %{low:.2f}<br>"
            "Cierre: %{close:.2f}<extra></extra>"
        ),
        selector=dict(type="candlestick"),
    )
    fig.update_traces(
        hovertemplate="Volumen: %{y:,.0f}<extra></extra>",
        selector=dict(type="bar"),
    )

    return fig


def add_sma_crossover_markers(fig: go.Figure, df: pd.DataFrame) -> go.Figure:
    """Mark days when SMA 20 crosses above or below SMA 50."""
    if SMA_CROSS_BULL_COL not in df.columns:
        return fig

    bull_mask = df[SMA_CROSS_BULL_COL] == 1
    if bull_mask.any():
        fig.add_trace(
            go.Scatter(
                x=df.index[bull_mask],
                y=df.loc[bull_mask, "SMA20"],
                mode="markers",
                marker=dict(symbol="triangle-up", color="lime", size=12, line=dict(width=1)),
                name=chart_label("sma_cross_bull"),
            ),
            row=1,
            col=1,
        )

    bear_mask = df[SMA_CROSS_BEAR_COL] == 1
    if bear_mask.any():
        fig.add_trace(
            go.Scatter(
                x=df.index[bear_mask],
                y=df.loc[bear_mask, "SMA20"],
                mode="markers",
                marker=dict(symbol="triangle-down", color="red", size=12, line=dict(width=1)),
                name=chart_label("sma_cross_bear"),
            ),
            row=1,
            col=1,
        )
    return fig


def add_pattern_markers(
    fig: go.Figure,
    df: pd.DataFrame,
    pattern_keys: list[str],
) -> go.Figure:
    """Overlay selected candlestick pattern markers on row 1."""
    for key in pattern_keys:
        spec = PATTERN_SPECS[key]
        if spec.column not in df.columns:
            continue

        mask = pattern_signal_mask(df[spec.column], spec)
        indices = df.index[mask]
        if len(indices) == 0:
            continue

        fig.add_trace(
            go.Scatter(
                x=indices,
                y=df.loc[indices, "Close"],
                mode="markers",
                marker=dict(
                    symbol=spec.symbol,
                    color=spec.color,
                    size=spec.size,
                    line=dict(color="black", width=1),
                ),
                name=pattern_text(key)["label"],
            ),
            row=1,
            col=1,
        )
    return fig


def build_chart(
    df: pd.DataFrame,
    ticker: str,
    pattern_keys: list[str] | None = None,
) -> go.Figure:
    """Full chart with optional pattern overlays."""
    fig = build_candlestick_with_volume(df, ticker)
    add_sma_crossover_markers(fig, df)
    if pattern_keys:
        add_pattern_markers(fig, df, pattern_keys)
    return fig


def price_at(df: pd.DataFrame, index_value, column: PriceColumn = "Close") -> float:
    """Return the selected OHLC field at a trading date."""
    return float(df.loc[index_value, column])


def calc_fib_extension_levels(
    price_a: float,
    price_b: float,
    price_c: float,
    ratios: list[float] | None = None,
) -> list[tuple[float, float]]:
    """Fibonacci extension: level = C + ratio * (B - A)."""
    impulse = price_b - price_a
    selected = FIB_RATIOS if ratios is None else ratios
    return [(ratio, price_c + ratio * impulse) for ratio in selected]


def add_fib_swing_markers(
    fig: go.Figure,
    swing_points: list[tuple[str, object, float]],
) -> go.Figure:
    """Draw A/B/C markers and optional connecting line."""
    if not swing_points:
        return fig

    labels = [label for label, _, _ in swing_points]
    indices = [idx for _, idx, _ in swing_points]
    prices = [price for _, _, price in swing_points]

    fig.add_trace(
        go.Scatter(
            x=indices,
            y=prices,
            mode="lines+markers" if len(swing_points) > 1 else "markers",
            line=dict(color="white", width=2, dash="dash"),
            marker=dict(
                size=14,
                color=[FIB_POINT_COLORS[label] for label in labels],
            ),
            name=s("fib_swing_legend"),
        ),
        row=1,
        col=1,
    )

    for label, idx, price in swing_points:
        color = FIB_POINT_COLORS[label]
        fig.add_annotation(
            x=idx,
            y=price,
            xref="x",
            yref="y",
            text=f"{label}<br>{price:.2f}",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=color,
            ax=0,
            ay=-30 if label == "B" else 30,
            font=dict(color=color, size=12),
            bgcolor="rgba(26, 31, 46, 0.95)",
            bordercolor=color,
            borderwidth=1,
            row=1,
            col=1,
        )
    return fig


def add_fib_level_lines(
    fig: go.Figure,
    df: pd.DataFrame,
    price_a: float,
    price_b: float,
    price_c: float,
    ratios: list[float] | None = None,
) -> go.Figure:
    """Draw horizontal Fibonacci extension levels."""
    x_start = df.index[0]
    x_end = df.index[-1]
    for ratio, level in calc_fib_extension_levels(price_a, price_b, price_c, ratios):
        fig.add_shape(
            type="line",
            xref="x",
            yref="y",
            x0=x_start,
            y0=level,
            x1=x_end,
            y1=level,
            line=dict(color="purple", width=2, dash="dot"),
            opacity=0.7,
            layer="below",
            row=1,
            col=1,
        )
        fig.add_annotation(
            x=x_end,
            y=level,
            xref="x",
            yref="y",
            text=s("fib_level_label", ratio=ratio),
            showarrow=False,
            font=dict(color="purple", size=11),
            xanchor="left",
            row=1,
            col=1,
        )
    return fig


def add_fib_extension(
    fig: go.Figure,
    df: pd.DataFrame,
    idx_a,
    price_a: float,
    idx_b,
    price_b: float,
    idx_c,
    price_c: float,
    ratios: list[float] | None = None,
) -> go.Figure:
    """Draw swing points A/B/C and horizontal Fibonacci extension levels."""
    swing_points = [
        ("A", idx_a, price_a),
        ("B", idx_b, price_b),
        ("C", idx_c, price_c),
    ]
    add_fib_swing_markers(fig, swing_points)
    add_fib_level_lines(fig, df, price_a, price_b, price_c, ratios)
    return fig


def build_fib_extension_chart(
    df: pd.DataFrame,
    ticker: str,
    idx_a,
    idx_b,
    idx_c,
    price_col_a: PriceColumn = "Close",
    price_col_b: PriceColumn = "Close",
    price_col_c: PriceColumn = "Close",
) -> go.Figure:
    """Candlestick chart with user-selected Fibonacci swing points and levels."""
    fig = build_candlestick_with_volume(df, ticker)
    add_fib_extension(
        fig,
        df,
        idx_a,
        price_at(df, idx_a, price_col_a),
        idx_b,
        price_at(df, idx_b, price_col_b),
        idx_c,
        price_at(df, idx_c, price_col_c),
    )
    return fig


def fib_date_label(
    df: pd.DataFrame,
    index_value,
    price_column: PriceColumn,
) -> str:
    """Human-readable label for date select boxes."""
    return s(
        "fib_date_option",
        date=_format_index_date(index_value),
        column=fib_price_column(price_column),
        price=price_at(df, index_value, price_column),
    )


def default_fib_dates(df: pd.DataFrame) -> tuple:
    """Spread default A/B/C picks across the loaded range."""
    n = len(df)
    if n < 3:
        idx = df.index[-1]
        return idx, idx, idx
    positions = [max(0, n // 4 - 1), max(0, n // 2 - 1), n - 1]
    return tuple(df.index[pos] for pos in positions)


def validate_fib_points(idx_a, idx_b, idx_c) -> str | None:
    """Return an i18n error key when A/B/C are invalid, else None."""
    if idx_a == idx_b or idx_b == idx_c or idx_a == idx_c:
        return "fib_error_distinct"
    if not (idx_a < idx_b < idx_c):
        return "fib_error_order"
    return None


def default_date_range() -> tuple[date, date]:
    end = date.today()
    start = end - timedelta(days=365)
    return start, end


def _format_index_date(index_value) -> str:
    if hasattr(index_value, "strftime"):
        return index_value.strftime("%Y-%m-%d")
    return str(index_value)[:10]


def pattern_hit_count(df: pd.DataFrame, key: str) -> int:
    spec = PATTERN_SPECS[key]
    return int(pattern_signal_mask(df[spec.column], spec).sum())


def sma_cross_hit_count(df: pd.DataFrame, column: str) -> int:
    if column not in df.columns:
        return 0
    return int((df[column] == 1).sum())


def _last_cross_date(df: pd.DataFrame, column: str):
    if column not in df.columns:
        return None
    hits = df.index[df[column] == 1]
    if len(hits) == 0:
        return None
    return hits[-1]


def build_ticker_summary(df: pd.DataFrame, ticker: str) -> str:
    """Plain-language summary from price trend and all candlestick indicators."""
    lines: list[str] = [
        s(
            "summary_intro",
            ticker=ticker,
            start=_format_index_date(df.index.min()),
            end=_format_index_date(df.index.max()),
        )
    ]

    trend = df.dropna(subset=["SMA20", "SMA50"])
    if trend.empty:
        lines.append(s("summary_trend_unknown"))
    else:
        last = trend.iloc[-1]
        close = float(last["Close"])
        sma20 = float(last["SMA20"])
        sma50 = float(last["SMA50"])
        if close > sma20 and close > sma50:
            lines.append(s("summary_trend_up", close=close))
        elif close < sma20 and close < sma50:
            lines.append(s("summary_trend_down", close=close))
        else:
            lines.append(
                s("summary_trend_mixed", close=close, sma20=sma20, sma50=sma50)
            )

        if len(df) > RECENT_TRADING_DAYS:
            prior = float(df["Close"].iloc[-(RECENT_TRADING_DAYS + 1)])
            pct = (close / prior - 1.0) * 100.0
            lines.append(s("summary_trend_short", pct=pct))

        if sma20 > sma50:
            lines.append(s("summary_sma_position_above"))
        elif sma20 < sma50:
            lines.append(s("summary_sma_position_below"))
        else:
            lines.append(s("summary_sma_position_equal"))

        bull_crosses = sma_cross_hit_count(df, SMA_CROSS_BULL_COL)
        bear_crosses = sma_cross_hit_count(df, SMA_CROSS_BEAR_COL)
        lines.append(
            s("summary_sma_cross_period", bull=bull_crosses, bear=bear_crosses)
        )
        if bull_crosses == 0 and bear_crosses == 0:
            lines.append(s("summary_sma_cross_none"))
        else:
            last_bull = _last_cross_date(df, SMA_CROSS_BULL_COL)
            if last_bull is not None:
                lines.append(
                    s(
                        "summary_sma_cross_last_bull",
                        date=_format_index_date(last_bull),
                    )
                )
            last_bear = _last_cross_date(df, SMA_CROSS_BEAR_COL)
            if last_bear is not None:
                lines.append(
                    s(
                        "summary_sma_cross_last_bear",
                        date=_format_index_date(last_bear),
                    )
                )

        recent_bull = sma_cross_hit_count(df.tail(RECENT_TRADING_DAYS), SMA_CROSS_BULL_COL)
        recent_bear = sma_cross_hit_count(df.tail(RECENT_TRADING_DAYS), SMA_CROSS_BEAR_COL)
        if recent_bull or recent_bear:
            lines.append(
                s(
                    "summary_sma_cross_recent",
                    bull=recent_bull,
                    bear=recent_bear,
                )
            )

    recent = df.tail(RECENT_TRADING_DAYS)
    recent_hits: list[tuple[str, int]] = []
    for key in DEFAULT_PATTERN_KEYS:
        spec = PATTERN_SPECS[key]
        count = int(pattern_signal_mask(recent[spec.column], spec).sum())
        if count:
            recent_hits.append((pattern_text(key)["label"], count))

    if recent_hits:
        lines.append(s("summary_recent_title"))
        for label, count in recent_hits:
            lines.append(s("summary_recent_item", label=label, count=count))
    else:
        lines.append(s("summary_recent_none"))

    bullish = sum(pattern_hit_count(df, k) for k in BULLISH_PATTERN_KEYS)
    bearish = sum(pattern_hit_count(df, k) for k in BEARISH_PATTERN_KEYS)
    neutral = sum(pattern_hit_count(df, k) for k in NEUTRAL_PATTERN_KEYS)
    total_patterns = bullish + bearish + neutral

    lines.append(s("summary_overall_title"))
    if total_patterns == 0:
        lines.append(s("summary_overall_none"))
    else:
        lines.append(s("summary_overall_bullish", count=bullish))
        lines.append(s("summary_overall_bearish", count=bearish))
        lines.append(s("summary_overall_neutral", count=neutral))
        if neutral >= max(bullish, bearish) + 2 and neutral > 0:
            lines.append(s("summary_overall_read_neutral_heavy"))
        elif bullish > bearish:
            lines.append(s("summary_overall_read_bullish"))
        elif bearish > bullish:
            lines.append(s("summary_overall_read_bearish"))
        else:
            lines.append(s("summary_overall_read_balanced"))

    return "\n\n".join(lines)
