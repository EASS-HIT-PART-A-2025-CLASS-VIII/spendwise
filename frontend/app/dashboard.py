import streamlit as st
import pandas as pd
from client import list_movies, create_movie, delete_movie  # ✅ Correct local import

st.set_page_config(page_title="🎬 Movie Dashboard", layout="wide")
st.title("🎬 FastAPI Movie Dashboard")
# ----------------------------
# Cached GET requests
# ----------------------------
@st.cache_data(ttl=30)
def cached_movies():
    return list_movies()


# ----------------------------
# Fetch and show all movies
# ----------------------------
with st.spinner("Fetching movies..."):
    try:
        movies = cached_movies()
    except Exception as e:
        st.error(f"❌ Failed to fetch movies: {e}")
        st.stop()

if not movies:
    st.info("No movies found. Add some below 👇")
    movies_df = pd.DataFrame(columns=["id", "title", "director", "year", "rating"])
else:
    movies_df = pd.DataFrame(movies)
    if "id" in movies_df.columns:
        movies_df = movies_df[["id", "title", "director", "year", "rating"]]
    movies_df["year"] = movies_df["year"].astype(str)
    st.metric("Total movies", len(movies_df))

    st.dataframe(
        movies_df.to_dict(orient="records"),
        height=400,
        use_container_width=True,
        column_config={"index": None},
    )

# ----------------------------
# Add movie form
# ----------------------------
st.subheader("➕ Add a New Movie")

with st.form("add_movie_form", clear_on_submit=False):
    title = st.text_input("Title")
    director = st.text_input("Director")
    year = st.number_input("Year", min_value=1900, max_value=2100, value=2024)
    rating = st.number_input("Rating", min_value=0.0, max_value=20.0, value=8.0, step=0.1)
    submitted = st.form_submit_button("Add Movie")

if submitted:
    # ✅ Input validation
    if not title or not director:
        st.error("⚠️ Please fill out both Title and Director fields.")
        st.stop()

    if rating > 10.0 or rating < 0.0:
        st.error("❌ Rating must be between 0 and 10.")
        # Clear the rating value so it cannot be reused accidentally
        st.session_state["Rating"] = 0.0
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

# ----------------------------
# Delete movie section
# ----------------------------
st.subheader("🗑️ Delete a Movie")

if not movies_df.empty:
    selected_id = st.selectbox("Select movie to delete by ID:", movies_df["id"])
    if st.button("Delete Selected Movie"):
        try:
            delete_movie(int(selected_id))
            st.success(f"🗑️ Deleted movie ID {selected_id}")
            cached_movies.clear()
            st.rerun()
        except Exception as e:
            st.error(f"❌ Failed to delete movie: {e}")
else:
    st.caption("No movies available to delete.")

# ----------------------------
# Refresh button
# ----------------------------
st.divider()
if st.button("🔄 Refresh List"):
    cached_movies.clear()
    st.rerun()

# ----------------------------
# Export to CSV (with download)
# ----------------------------
st.divider()
st.subheader("💾 Export Movies to CSV")

if not movies_df.empty:
    csv_data = movies_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download CSV",
        data=csv_data,
        file_name="movies_export.csv",
        mime="text/csv",
        help="Click to download the movie list as a CSV file",
    )
else:
    st.caption("No movies available to export.")