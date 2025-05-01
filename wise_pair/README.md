# WisePair - Project Management Platform

WisePair is a comprehensive project mentorship and management platform designed for campus hackathons. It facilitates team formation, idea submission, mentor matching, and project progress tracking.

## Features

- **User Authentication**: JWT-based authentication with student registration/login
- **Team Management**: Create/join teams, invite members, lock teams when full
- **Idea Submission**: Submit and track project ideas
- **Mentorship System**: Request and manage mentorship from professors and senior students
- **Meeting Scheduler**: Schedule and track feedback meetings with mentors
- **Leaderboard**: Score-based team rankings
- **File Storage**: Upload and manage project files via MinIO (S3-compatible)
- **Email Integration**: Notifications for key events via Mailtrap

## Tech Stack

- **Backend**: Flask with Blueprints
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Storage**: MinIO (S3-compatible)
- **Email**: Mailtrap SMTP
- **Containerization**: Docker & Docker Compose

## Project Structure

```
/wise_pair
├── app/
│   ├── models/        # Database models
│   ├── routes/        # API endpoints
│   ├── services/      # Business logic
│   ├── schemas/       # Request/response validation
│   ├── utils/         # Helper utilities
│   └── config.py      # Configuration
├── migrations/        # Database migrations
├── .env               # Environment variables
├── docker-compose.yml # Docker services configuration
├── Dockerfile         # Flask app container definition
├── requirements.txt   # Python dependencies
└── run.py             # Application entry point
```

## Setup & Installation

### Prerequisites

- Docker and Docker Compose
- Git

### Getting Started

1. Clone the repository
2. Navigate to the project directory
3. Create an `.env` file with required environment variables (see `.env.example`)
4. Start the services with Docker Compose:

```bash
docker-compose up
```

5. The API will be available at: http://localhost:5000
6. MinIO console will be available at: http://localhost:9001

## API Endpoints

The application provides the following main API endpoints:

- **Authentication**: `/api/auth/register`, `/api/auth/login`
- **Teams**: `/api/teams`
- **Mentorship**: `/api/professors`, `/api/mentors`
- **Meetings**: `/api/meetings`
- **Leaderboard**: `/api/leaderboard`
- **Files**: `/api/files`

## Development

For local development without Docker:

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables
4. Run the application:
   ```bash
   flask run
   ```

## Database Migrations

To create or update database migrations:

```bash
flask db migrate -m "Migration message"
flask db upgrade
``` 