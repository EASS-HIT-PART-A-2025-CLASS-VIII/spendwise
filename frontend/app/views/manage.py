import streamlit as st
from app.core.shared import load_css, get_movies_df, render_filters, cached_movies
from app.core.client import create_movie, delete_movie


def check_and_show_toast():
    if "toast_message" in st.session_state:
        st.toast(st.session_state["toast_message"])
        del st.session_state["toast_message"]


def main():
    load_css()
    check_and_show_toast()

    movies_df = get_movies_df()
    render_filters(movies_df)

    st.title("Manage Movies")

    add_tab, delete_tab = st.tabs(["➕ Add Movie", "🗑️ Delete Movie"])

    with add_tab:
        st.subheader("Add a new movie")
        with st.form("add_movie_form", clear_on_submit=True):
            title = st.text_input("Title")
            director = st.text_input("Director")
            year_str = st.text_input(
                "Year (1900 to 2026)", value="2025", key="year_input"
            )
            rating_str = st.text_input(
                "Rating (0.0 to 10.0)", value="8.0", key="rating_input"
            )
            submitted = st.form_submit_button("Add Movie", use_container_width=True)

        if submitted:
            validation_failed = False
            rating_float = None
            year_int = None

            if not title or not director or not year_str or not rating_str:
                st.error("⚠️ Please fill out all fields.")
                validation_failed = True

            if not validation_failed:
                try:
                    year_int = int(year_str)
                except ValueError:
                    st.error("❌ Year must be a valid whole number.")
                    validation_failed = True

            if not validation_failed:
                if year_int < 1900 or year_int > 2026:
                    st.error("❌ Year must be between 1900 and 2026.")
                    validation_failed = True

            if not validation_failed:
                try:
                    rating_float = float(rating_str)
                except ValueError:
                    st.error("❌ Rating must be a valid number.")
                    validation_failed = True

            if not validation_failed:
                if rating_float > 10.0 or rating_float < 0.0:
                    st.error("❌ Rating must be between 0 and 10.")
                    validation_failed = True

            if not validation_failed:
                try:
                    movie = create_movie(
                        title=title.strip(),
                        director=director.strip(),
                        year=year_int,
                        rating=rating_float,
                    )
                    st.session_state["toast_message"] = (
                        f"✅ Added movie '{movie.get('title', title)}'"
                    )
                    cached_movies.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Failed to add movie: {e}")

    with delete_tab:
        st.subheader("Remove a movie")
        if movies_df.empty:
            st.caption("No movies available to delete.")
        else:
            sorted_df = movies_df.copy().sort_values(by="id", ascending=False)
            options = {
                f"{int(row.id)} · {row.title} ({row.year})": int(row.id)
                for row in sorted_df.itertuples()
            }
            selected_label = st.selectbox(
                "Pick a movie to delete",
                options=list(options.keys()),
            )
            if st.button(
                "Delete Selected Movie", type="secondary", use_container_width=True
            ):
                selected_id = options[selected_label]
                try:
                    delete_movie(selected_id)
                    st.session_state["toast_message"] = (
                        f"🗑️ Deleted movie ID {selected_id}"
                    )
                    cached_movies.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Failed to delete movie: {e}")
