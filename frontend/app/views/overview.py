def main():
    import streamlit as st
    from app.core.shared import load_css, get_movies_df, render_filters, render_metrics, render_charts

    load_css()

    movies_df = get_movies_df()

    rating_filter, year_range = render_filters(movies_df)

    # Apply filters
    filtered_df = movies_df.copy()
    if not filtered_df.empty:
        filtered_df = filtered_df[
            (filtered_df["rating"] >= rating_filter)
            & (filtered_df["year"].between(year_range[0], year_range[1]))
        ]

    st.title("🎬 FastAPI Movie Dashboard")

    render_metrics(filtered_df)

    if not filtered_df.empty:
        st.divider()
        render_charts(filtered_df)

        st.divider()
        st.subheader("📋 Movie Library")
        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=420,
            hide_index=True,
            column_config={
                "id": st.column_config.NumberColumn("ID", format="%d"),
                "title": st.column_config.TextColumn("Title"),
                "director": st.column_config.TextColumn("Director"),
                "year": st.column_config.NumberColumn("Year", format="%d"),
                "rating": st.column_config.NumberColumn("Rating", format="%.1f"),
            },
        )

