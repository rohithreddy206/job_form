# Candidate Application Form - Modular Architecture

A professional, full-stack candidate application form built with FastAPI, MySQL, and Jinja2.

## Project Structure

```
form/
├── app/
│   ├── main.py             # FastAPI entry point
│   ├── config/             # Settings & Environment configs
│   │   └── settings.py
│   ├── database/           # DB connection & session handling
│   │   └── connection.py
│   ├── models/             # Database models
│   ├── schemas/            # Pydantic schemas (Validation)
│   │   └── candidate.py
│   ├── routes/             # API Endpoints
│   │   └── candidate_routes.py
│   ├── services/           # Business Logic
│   │   └── candidate_service.py
│   ├── utils/              # Helper functions
│   │   └── file_helpers.py
│   ├── static/             # CSS/JS Assets
│   └── templates/          # HTML Templates
├── uploads/                # Resume uploads destination
├── .env                    # Environment variables
├── requirements.txt
└── README.md
```

## Setup & Running

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   Update the `.env` file with your MySQL credentials.

3. **Run the Application**:
   **Important**: Run this command from the `form/` directory (the project root).
   ```bash
   uvicorn app.main:app --reload
   ```
   The application will be available at `http://localhost:8000`.

## Features
- Multi-section application form with progress tracking.
- Secure file upload (PDF, DOC, DOCX) with size validation.
- MySQL persistence for candidate data.
- Modular architecture for scalability and maintainability.
