
# CareConnect AI – Smart Hospital Contact Manager

An AI-powered healthcare contact management application
developed using Python Flask, SQLite, and Google Gemini.

## Features

- Healthcare contact management
- Add, view, edit, and delete contacts
- Search and filter contacts
- Duplicate detection
- Dashboard statistics
- AI Smart Contact Classification
- AI Administrative Email Draft Generation

## Technologies

- Python
- Flask
- SQLite
- HTML, CSS, JavaScript
- Google Gemini AI

## AI Features

### Smart Classification

Google Gemini analyzes healthcare directory information
and suggests a contact type, department, and explanation.

### Email Draft Generation

Gemini generates a professional administrative email
based on a selected contact and communication purpose.

Generated emails are reviewed by users and are not
sent automatically.

## Local Setup

1. Clone this repository.
2. Create a Python virtual environment.
3. Activate the environment.
4. Install packages:

   pip install -r requirements.txt

5. Create a `.env` file with your own configuration:

   FLASK_SECRET_KEY=replace_with_your_own_secret
   FLASK_DEBUG=0
   GEMINI_API_KEY=your_own_gemini_api_key
   GEMINI_MODEL=gemini-3.5-flash-lite

6. Run the application:

   python app.py

7. Open:

   http://127.0.0.1:5000

## Prompt Engineering Documentation

See `docs/prompt_log.md` for development prompts,
prompt improvements, challenges, and AI integration notes.

## Privacy

This application is intended for fictional or publicly
listed healthcare directory information, not patient data.

API keys, local database contents, and private configuration
files are excluded from the repository.

## Developer

Sobiya M

