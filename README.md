# LegalEase

LegalEase is an AI-powered legal document drafting application.

## Technology Stack

Frontend:
- Streamlit

Backend:
- FastAPI
- Uvicorn

AI:
- Google Gemini
- google-genai SDK

Document generation:
- python-docx
- fpdf2
- TXT

Configuration:
- python-dotenv

Testing:
- pytest

---

# Project Structure

```text
LegalEase/

├── assets/
│   └── logo.png

├── backend/
│   ├── ai_core/
│   │   ├── __init__.py
│   │   └── gemini_generator.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   └── document_formatter.py
│   │
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── routes.py
│   └── schemas.py
│
├── frontend/
│   ├── __init__.py
│   └── app.py
│
├── tests/
│   ├── test_api.py
│   └── test_formatters.py
│
├── .env
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt