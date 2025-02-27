# Job Application API

This is a Django Rest Framework (DRF) API for managing job applications, job recommendations, and resume feedback.

## Features
- Create, list, update, and delete job applications.
- Get personalized job recommendations.
- Receive resume feedback.
- User authentication with JWT.

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL (or any other relational database of your choice)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/FestusMike/AI_Copilot_Assesssment_Test.git
   cd AI_Copilot_Assesssment_Test
   ```
2. Create and activate a virtual environment:

   **Linux/macOS:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Update `.env` with your database credentials and secret key.

5. Apply database migrations:
    ```bash
   python manage.py makemigrations users
   python manage.py makemigrations jobs
   python manage.py migrate
   ```
6. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```
7. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Running Tests
This project uses `pytest` for testing.
1. Run tests using pytest:
   ```bash
   pytest
   ```

## Some API Endpoints
- `POST /api/v1/job-applications` - Create a job application
- `GET /api/v1/job-applications` - List all job applications
- `GET /api/v1/job-applications/{id}` - Retrieve a specific job application
- `PATCH /api/v1/job-applications/{id}` - Update a job application
- `DELETE /api/v1/job-applications/{id}` - Delete a job application
- `GET /api/v1/job-recommendations` - List job recommendations
- `POST /api/v1/resume-feedback` - Submit a resume for feedback

## API Documentation
Access the live API documentation at:
[Live Docs URL](https://ai-copilot-assessment-test.onrender.com/api/v1/docs)
