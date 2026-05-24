"""Streamlit UI for candlestick charts and TA-Lib pattern overlays."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from analysis import (
    DEFAULT_PATTERN_KEYS,
    PATTERN_SPECS,
    SMA_CROSS_BEAR_COL,
    SMA_CROSS_BULL_COL,
    PriceColumn,
    add_indicators,
    build_chart,
    build_fib_extension_chart,
    build_ticker_summary,
    calc_fib_extension_levels,
    default_date_range,
    default_fib_dates,
    download_ohlcv,
    fib_date_label,
    price_at,
    sma_cross_hit_count,
    validate_fib_points,
)
from i18n import (
    MEMBERS,
    TICKER_GROUPS,
    considerations,
    fib_price_column,
    label_dataframe_column,
    pattern,
    s,
    sma_cross_text,
    ticker_catalog,
)

TICKER_OWNER: dict[str, str] = {
    symbol: owner for owner, symbols in TICKER_GROUPS.items() for symbol in symbols
}

PRESET_TICKERS = [symbol for symbols in TICKER_GROUPS.values() for symbol in symbols]


def preset_ticker_label(symbol: str) -> str:
    return f"{symbol} — {TICKER_OWNER[symbol]}"


st.set_page_config(page_title=s("page_title"), layout="wide")
st.title(s("title"))

default_start, default_end = default_date_range()

with st.sidebar:
    st.header(s("market_data"))
    preset = st.selectbox(
        s("ticker"),
        options=PRESET_TICKERS,
        index=0,
        format_func=preset_ticker_label,
    )
    search = st.text_input(
        s("search_symbol"),
        value="",
        placeholder=s("search_placeholder"),
    ).strip()
    ticker = (search or preset).upper()
    start = st.date_input(s("start"), value=default_start)
    end = st.date_input(s("end"), value=default_end)

    st.header(s("indicators"))
    selected_keys = []
    for key in DEFAULT_PATTERN_KEYS:
        label = pattern(key)["label"]
        if st.checkbox(label, value=True, key=f"indicator_{key}"):
            selected_keys.append(key)

    load = st.button(s("load_refresh"), type="primary", use_container_width=True)

if not ticker:
    st.warning(s("enter_ticker"))
    st.stop()

if start >= end:
    st.error(s("start_before_end"))
    st.stop()

if load or "df" not in st.session_state or st.session_state.get("ticker") != ticker:
    with st.spinner(s("downloading", ticker=ticker)):
        try:
            df = download_ohlcv(ticker, start, end)
            df = add_indicators(df)
        except Exception as exc:
            st.error(str(exc))
            st.stop()

    st.session_state["df"] = df
    st.session_state["ticker"] = ticker
    st.session_state["start"] = start
    st.session_state["end"] = end

tab_dashboard, tab_fibonacci, tab_tickers, tab_considerations, tab_members = st.tabs(
    [
        s("tab_dashboard"),
        s("tab_fibonacci"),
        s("tab_tickers"),
        s("tab_considerations"),
        s("tab_members"),
    ]
)

with tab_members:
    st.subheader(s("members_title"))
    st.markdown(s("members_intro"))
    for index, member in enumerate(MEMBERS):
        st.markdown(f"**{member['name']}**")
        st.markdown(f"[{member['email']}](mailto:{member['email']})")
        if index < len(MEMBERS) - 1:
            st.divider()

with tab_considerations:
    st.subheader(s("considerations"))
    st.markdown(considerations())

with tab_tickers:
    st.markdown(s("tickers_intro"))
    entries = [
        (owner, symbol)
        for owner, symbols in TICKER_GROUPS.items()
        for symbol in symbols
    ]
    for index, (owner, symbol) in enumerate(entries):
        info = ticker_catalog(symbol)
        st.markdown(f"**{symbol}** — {info['name']}")
        st.caption(s("tickers_owner_label", owner=owner))
        st.write(info["description"])
        if index < len(entries) - 1:
            st.divider()

with tab_fibonacci:
    st.subheader(s("fib_title"))
    st.markdown(s("fib_intro"))

    if "df" not in st.session_state:
        st.info(s("fib_load_data_prompt"))
    else:
        df = st.session_state["df"]
        active_ticker = st.session_state["ticker"]
        trading_dates = list(df.index)
        default_a, default_b, default_c = default_fib_dates(df)
        price_options: list[PriceColumn] = ["Close", "High", "Low"]

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown(f"**{s('fib_point_a')}**")
            price_col_a = st.selectbox(
                s("fib_price_field"),
                options=price_options,
                format_func=fib_price_column,
                key="fib_price_a",
            )
            idx_a = st.selectbox(
                s("fib_date"),
                options=trading_dates,
                index=trading_dates.index(default_a),
                format_func=lambda idx: fib_date_label(df, idx, price_col_a),
                key="fib_date_a",
            )
        with col_b:
            st.markdown(f"**{s('fib_point_b')}**")
            price_col_b = st.selectbox(
                s("fib_price_field"),
                options=price_options,
                format_func=fib_price_column,
                key="fib_price_b",
            )
            idx_b = st.selectbox(
                s("fib_date"),
                options=trading_dates,
                index=trading_dates.index(default_b),
                format_func=lambda idx: fib_date_label(df, idx, price_col_b),
                key="fib_date_b",
            )
        with col_c:
            st.markdown(f"**{s('fib_point_c')}**")
            price_col_c = st.selectbox(
                s("fib_price_field"),
                options=price_options,
                format_func=fib_price_column,
                key="fib_price_c",
            )
            idx_c = st.selectbox(
                s("fib_date"),
                options=trading_dates,
                index=trading_dates.index(default_c),
                format_func=lambda idx: fib_date_label(df, idx, price_col_c),
                key="fib_date_c",
            )

        calculate_fib = st.button(
            s("fib_calculate"),
            type="primary",
            use_container_width=True,
            key="fib_calculate",
        )

        validation_error = validate_fib_points(idx_a, idx_b, idx_c)
        if validation_error:
            st.warning(s(validation_error))
        elif calculate_fib:
            price_a = price_at(df, idx_a, price_col_a)
            price_b = price_at(df, idx_b, price_col_b)
            price_c = price_at(df, idx_c, price_col_c)
            impulse = price_b - price_a

            fig = build_fib_extension_chart(
                df,
                active_ticker,
                idx_a,
                idx_b,
                idx_c,
                price_col_a=price_col_a,
                price_col_b=price_col_b,
                price_col_c=price_col_c,
            )
            st.plotly_chart(fig, use_container_width=True)

            st.subheader(s("fib_levels_title"))
            st.caption(
                s(
                    "fib_levels_caption",
                    impulse=impulse,
                    price_c=price_c,
                )
            )
            levels = calc_fib_extension_levels(price_a, price_b, price_c)
            levels_df = pd.DataFrame(
                levels,
                columns=[s("fib_ratio"), s("fib_level")],
            )
            st.dataframe(levels_df, use_container_width=True, hide_index=True)

with tab_dashboard:
    if "df" not in st.session_state:
        st.info(s("load_data_prompt"))
    else:
        df = st.session_state["df"]
        active_ticker = st.session_state["ticker"]

        fig = build_chart(df, active_ticker, pattern_keys=selected_keys)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader(s("ticker_summary", ticker=active_ticker))
        st.markdown(build_ticker_summary(df, active_ticker))
        st.caption(s("summary_disclaimer"))

        st.subheader(s("sma_cross_hits"))
        st.caption(s("hits_caption"))
        sma_cols = st.columns(2)
        for col, kind, cross_col in zip(
            sma_cols,
            ("bull", "bear"),
            (SMA_CROSS_BULL_COL, SMA_CROSS_BEAR_COL),
            strict=True,
        ):
            text = sma_cross_text(kind)
            with col:
                st.metric(text["label"], sma_cross_hit_count(df, cross_col))
                st.caption(text["description"])

        st.subheader(s("indicator_hits"))
        st.caption(s("hits_caption"))
        cols = st.columns(2)
        for i, key in enumerate(DEFAULT_PATTERN_KEYS):
            spec = PATTERN_SPECS[key]
            text = pattern(key)
            if spec.filter_fn is not None:
                hits = int(spec.filter_fn(df[spec.column]).sum())
            else:
                hits = int((df[spec.column] != 0).sum())
            with cols[i % 2]:
                st.metric(text["label"], hits)
                st.caption(text["description"])

        with st.expander(s("raw_data")):
            pattern_cols = sorted({spec.column for spec in PATTERN_SPECS.values()})
            display_cols = [
                "Open",
                "High",
                "Low",
                "Close",
                "Volume",
                "SMA20",
                "SMA50",
                SMA_CROSS_BULL_COL,
                SMA_CROSS_BEAR_COL,
            ] + pattern_cols
            raw = df[display_cols].tail(10).rename(columns=label_dataframe_column)
            st.dataframe(raw, use_container_width=True)
