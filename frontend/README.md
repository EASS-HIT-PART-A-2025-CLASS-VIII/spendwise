# 🎨 Streamlit Dashboard

The **Streamlit dashboard** provides a simple interface for viewing, adding, deleting, and exporting movies.

---

## ▶️ Run the Dashboard

Make sure the backend (FastAPI) is running first:

```bash
cd backend
uv run uvicorn app.main:app --reload
```

Then start the dashboard:

```bash
cd frontend
uv run streamlit run app/dashboard.py
```

Access it at [http://localhost:8501](http://localhost:8501)

---

## 🧩 Features

- 📋 List all movies from the FastAPI backend
- ➕ Add new movies with input validation (rating between 0–10)  
- 🗑️ Delete existing movies  
- 🔄 View graphs of movie ratings/years
- 💾 Export movies to CSV

---
