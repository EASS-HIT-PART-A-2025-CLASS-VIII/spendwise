def main():

    import streamlit as st
    from app.core.shared import load_css, get_movies_df, sidebar_nav, render_filters, cached_movies
    from app.core.client import create_movie, delete_movie

    load_css()

    movies_df = get_movies_df()
    rating_filter, year_range = render_filters(movies_df)

    st.title("Manage Movies")

    add_tab, delete_tab = st.tabs(["➕ Add Movie", "🗑️ Delete Movie"])

    with add_tab:
        st.subheader("Add a new title")
        with st.form("add_movie_form", clear_on_submit=False):
            title = st.text_input("Title")
            director = st.text_input("Director")
            year = st.number_input(
                "Year", min_value=1900, max_value=2100, value=2024, step=1
            )
            rating = st.number_input(
                "Rating", min_value=0.0, max_value=10.0, value=8.0, step=0.1
            )
            submitted = st.form_submit_button("Add Movie", use_container_width=True)

        if submitted:
            if not title or not director:
                st.error("⚠️ Please fill out both Title and Director fields.")
                st.stop()

            if rating > 10.0 or rating < 0.0:
                st.error("❌ Rating must be between 0 and 10.")
                st.stop()

            try:
                movie = create_movie(
                    title=title.strip(),
                    director=director.strip(),
                    year=int(year),
                    rating=float(rating),
                )
                st.success(f"✅ Added movie '{movie.get('title', title)}'")
                cached_movies.clear()
                st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to add movie: {e}")
                st.stop()

    with delete_tab:
        st.subheader("Remove a title")
        if movies_df.empty:
            st.caption("No movies available to delete.")
        else:
            options = {
                f"{int(row.id)} · {row.title} ({row.year})": int(row.id)
                for row in movies_df.itertuples()
            }
            selected_label = st.selectbox(
                "Pick a movie to delete",
                options=list(options.keys()),
            )
            if st.button("Delete Selected Movie", type="secondary", use_container_width=True):
                selected_id = options[selected_label]
                try:
                    delete_movie(selected_id)
                    st.success(f"🗑️ Deleted movie ID {selected_id}")
                    cached_movies.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Failed to delete movie: {e}")
