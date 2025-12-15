# 🚀 Full Stack Movie Catalogue

## 🌟 Overview
This project delivers a complete **Full Stack Movie Catalogue** application, featuring a high-performance **FastAPI** backend and an interactive **Streamlit** dashboard. It demonstrates a clean separation of concerns with a RESTful API serving data to a modern, lightweight frontend.

## 🛠️ Technology Stack

| Component | Framework / Tool | Language | Key Role |
| :--- | :--- | :--- | :--- |
| **Backend API** | **FastAPI** | Python | High-performance CRUD API. |
| **Frontend UI** | **Streamlit** | Python | Interactive data dashboard. |
| **Database** | **SQLite** | N/A | Local, file-based persistence. |
| **Orchestration** | **Docker Compose** | N/A | Defines and runs the multi-container application. |

## ▶️ Quick Start (Recommended)
The easiest way to run both the API and the dashboard is using Docker Compose.

1.  **Build and Start:** Navigate to the project root and run the following command to build the containers and start the services (API and Dashboard):

    ```bash
    docker compose up --build
    ```

2.  **Access:** Once the containers are running:
    * **Dashboard (Frontend):** 🔗 [http://localhost:8501](http://localhost:8501)
    * **API Docs (Backend):** 🔗 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ⚙️ Component Details

### 1. Backend: FastAPI Movie API
* **Role:** Provides the core logic for movie data management (Create, Read, Update, Delete).
* **Data Model:** Uses **SQLModel** (Pydantic + SQLAlchemy) with a **SQLite** database.
* **Feature:** Includes a **Typer CLI** for database seeding and management.

### 2. Frontend: Streamlit Dashboard
* **Role:** A user-friendly interface for interacting with the API.
* **Features:** List, add, and delete movies; input validation; and data export to CSV.
* **Connectivity:** Connects directly to the FastAPI container to fetch and modify data.

---