def main():
    import streamlit as st
    from app.core.shared import load_css, get_movies_df, sidebar_nav, render_filters

    # Load CSS
    load_css()

    movies_df = get_movies_df()
    rating_filter, year_range = render_filters(movies_df)

    st.title("Exports")
    st.subheader("Download your data")
    if movies_df.empty:
        st.caption("No movies available to export.")
    else:
        csv_data = movies_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download CSV",
            data=csv_data,
            file_name="movies_export.csv",
            mime="text/csv",
            help="Click to download the movie list as a CSV file",
            use_container_width=True,
        )

