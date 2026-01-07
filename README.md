# PyESAPI Service

A high-performance **FastAPI** application for accessing Varian **ESAPI** (Eclipse Scripting API) over HTTP.
Built with **uv** for blazing fast dependency management.

## 🚀 Key Features

- **FastAPI Powered**: Modern, async-ready REST API.
- **Worker Thread Pattern**: Solves ESAPI's Single-Threaded Apartment (STA) constraints gracefully.
- **Data Access**: Endpoints for extracting Patient, Plan, and Dose data.
- **Hot Reload**: Seamless development experience.

## 🛠️ Project Structure

This project has been refactored from a script collection into a structured application:

```text
pyesapi/
├── app/
│   ├── main.py              # Application Entry Point
│   ├── routers/             # API Route Handlers (e.g., aria.py)
│   ├── services/            # Business Logic & ESAPI Worker
│   └── core/                # Config & Logging
├── docs/
│   └── architecture.md      # Detailed Threading Model documentation
├── pyesapi/                 # (Internal) PyESAPI library wrappers
├── pyproject.toml           # UV/Python dependencies
└── uv.lock                  # Dependency lock file
```

## ⚡ Quick Start

### Prerequisites

- **Windows OS** (Required by Varian ESAPI)
- **Python 3.11+**
- **[uv](https://github.com/astral-sh/uv)** installed.

### Installation

1. **Clone & Sync**:
   ```powershell
   git clone <repo-url>
   cd pyesapi
   uv sync
   ```

2. **Run Server**:
   ```powershell
   uv run uvicorn app.main:app --reload
   ```
   
   The server will start at `http://127.0.0.1:8000`.

### 📚 Documentation

- **Swagger UI**: Visit `http://127.0.0.1:8000/docs` for interactive API testing.
- **Architecture**: Read [docs/architecture.md](docs/architecture.md) to understand how we handle Varian's STA threading requirements.

## 🧪 Testing

We include endpoints to verify connectivity:

- `GET /info`: Checks if ESAPI is loaded and returns the current user.
- `GET /aria-test`: Performs a real DB query to fetch a sample of patients.

## 📦 Dependencies

Managed via `pyproject.toml`. Key libraries:
- `fastapi`
- `uvicorn`
- `numpy`
- `pythonnet` (via `pythoncom` for STA)
