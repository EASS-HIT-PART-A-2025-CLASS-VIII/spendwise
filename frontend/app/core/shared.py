import altair as alt
import pandas as pd
import streamlit as st
from pathlib import Path

from app.core.client import  list_movies


# CSS loader (safe, absolute path, works everywhere)
def load_css(path: str | Path = None) -> None:
    if path is None:
        # Stylesheet always lives next to this shared.py file
        path = Path(__file__).parent / "styles.css"

    css_path = Path(path)
    if not css_path.exists():
        return

    css_text = css_path.read_text(encoding="utf-8")
    st.markdown(f"<style>{css_text}</style>", unsafe_allow_html=True)


# Cached movie fetch
@st.cache_data(ttl=30)
def cached_movies() -> list[dict]:
    return list_movies()



# Dataframe builder
def build_dataframe(raw_movies: list[dict]) -> pd.DataFrame:
    if not raw_movies:
        return pd.DataFrame(columns=["id", "title", "director", "year", "rating"])

    df = pd.DataFrame(raw_movies)

    expected_cols = ["id", "title", "director", "year", "rating"]
    for col in expected_cols:
        if col not in df.columns:
            df[col] = None

    df = df[expected_cols]

    df["year"] = pd.to_numeric(df["year"], errors="coerce").fillna(0).astype(int)
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    return df


def get_movies_df() -> pd.DataFrame:
    try:
        return build_dataframe(cached_movies())
    except Exception as e:
        st.error(f"❌ Failed to fetch movies: {e}")
        st.stop()



# Sidebar active navigation badge

def sidebar_nav(current_page: str):
    st.sidebar.markdown(
        f"""
        <style>
        .nav-active {{
            background-color: #1e293b;
            font-weight: 600;
            padding: 8px 12px;
            border-radius: 6px;
            margin-bottom: 10px;
            color: white;
        }}
        </style>
        <div class="nav-active">{current_page}</div>
        """,
        unsafe_allow_html=True,
    )


def render_filters(movies_df: pd.DataFrame):
    """Render rating and year filters from sidebar and return (rating_filter, year_range)."""

    if movies_df.empty:
        return 0.0, (0, 0)

    # Rating filter
    rating_filter = st.sidebar.slider(
        "Minimum rating to visualize",
        min_value=0.0,
        max_value=10.0,
        value=0.0,
        step=0.5,
    )

    # Year filter
    year_min, year_max = int(movies_df["year"].min()), int(movies_df["year"].max())

    if year_min == year_max:
        st.sidebar.caption(f"Year filter fixed at {year_min}")
        year_range = (year_min, year_max)
    else:
        year_range = st.sidebar.slider(
            "Year range",
            min_value=year_min,
            max_value=year_max,
            value=(year_min, year_max),
        )

    st.sidebar.caption(" ")

    # Refresh button
    if st.sidebar.button("🔄 Refresh data", use_container_width=True):
        cached_movies.clear()
        st.rerun()

    return rating_filter, year_range


def render_metrics(df: pd.DataFrame) -> None:
    if df.empty:
        st.info("No movies yet. Add one from the Manage tab to see analytics.")
        return

    # Inject CSS for small caption text
    st.markdown("""
    <style>
        .small-caption {
            font-size: 0.75rem !important;
            margin-top: -10px !important;
            opacity: 0.8;
        }
    </style>
    """, unsafe_allow_html=True)

    cols = st.columns(4)

    avg_rating = df["rating"].mean()
    newest_year = df["year"].max()
    oldest_year = df["year"].min()
    top_director = df["director"].mode().iloc[0] if df["director"].notna().any() else "N/A"

    # Truncate long names with ellipsis
    max_len = 18
    if isinstance(top_director, str) and len(top_director) > max_len:
        cutoff = top_director.rfind(" ", 0, max_len - 1)
        top_display = (
            top_director[: cutoff if cutoff != -1 else max_len - 1].rstrip() + "…"
        )
    else:
        top_display = top_director

    cols[0].metric("🎞 Total Movies", len(df))
    cols[1].metric("⭐ Avg Rating", f"{avg_rating:.1f} / 10")
    cols[2].metric("📅 Year Span", f"{oldest_year} → {newest_year}")
    cols[3].metric("🎬 Top Director", top_display)

    # smaller caption under top director
    if top_display != top_director:
        cols[3].markdown(f"<div class='small-caption'>{top_director}</div>", unsafe_allow_html=True)


@st.cache_resource
def _register_altair_theme():
    def _streamlit_dark_theme():
        return {
            "config": {
                "background": "transparent",
                "view": {"stroke": "transparent"},
                "axis": {"labelColor": "#e2e8f0", "titleColor": "#e2e8f0"},
                "title": {"color": "#e2e8f0"},
            }
        }

    alt.themes.register("streamlit_dark", _streamlit_dark_theme)
    alt.themes.enable("streamlit_dark")



# Charts (rating distribution, year frequency, top directors)

def render_charts(df: pd.DataFrame) -> None:
    if df.empty:
        return

    _register_altair_theme()

    # Rating distribution
    rating_chart = (
        alt.Chart(df)
        .mark_bar(color="#f97316")
        .encode(
            x=alt.X("rating:Q", bin=alt.Bin(step=0.5), title="Rating"),
            y=alt.Y("count()", title="Movies"),
            tooltip=["count()"],
        )
        .properties(height=320, title="Rating Distribution")
    )

    # Year frequency area chart
    year_chart = (
        alt.Chart(df)
        .mark_area(
            line={"color": "#10b981"},
            color=alt.Gradient(
                gradient="linear",
                stops=[
                    alt.GradientStop(color="#34d399", offset=0),
                    alt.GradientStop(color="#0f172a", offset=1),
                ],
            ),
        )
        .encode(
            x=alt.X("year:O", title="Year"),
            y=alt.Y("count()", title="Movies Released"),
            tooltip=[
                alt.Tooltip("year:O", title="Year"),
                alt.Tooltip("count()", title="Movies"),
            ],
        )
        .properties(height=320, title="Movies by Year")
    )

    # Directors frequency bar chart
    director_chart = (
        alt.Chart(df)
        .mark_bar(color="#38bdf8")
        .encode(
            y=alt.Y("director:N", sort=alt.Sort("-x"), title="Director"),
            x=alt.X("count():Q", title="Movies"),
            tooltip=["count()"],
        )
        .properties(height=320, title="Top Directors")
    )

    left, right = st.columns((1, 1))
    left.altair_chart(rating_chart, use_container_width=True)
    right.altair_chart(year_chart, use_container_width=True)

    st.altair_chart(director_chart, use_container_width=True)
