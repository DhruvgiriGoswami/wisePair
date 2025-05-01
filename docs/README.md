# WisePair

WisePair is a project mentorship and management platform designed for campus hackathons. The application facilitates team formation, idea submission, mentor matching, and project progress tracking. It helps students find suitable mentors (professors or senior students) for their hackathon projects and allows mentors to track and evaluate student progress.

## Key Features

- Student authentication and registration
- Team creation and management (up to 4 members)
- Professor and mentor matching
- Idea submission
- Meeting scheduling
- File uploads with MinIO integration
- Leaderboard system
- Email notifications

## Technology Stack

- **Backend**: Flask, SQLAlchemy, Pydantic
- **Database**: PostgreSQL
- **Storage**: MinIO
- **Authentication**: JWT
- **Deployment**: Docker, Docker Compose, Gunicorn

## Project Structure

The project follows a layered architecture with modular components:
- Models (SQLAlchemy)
- Routes (Flask Blueprints)
- Services (Business Logic)
- Schemas (Pydantic)
- Utilities

## Getting Started

### Local Development Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/wisepair.git
   cd wisepair
   ```

2. Run the setup script (Windows PowerShell):
   ```
   .\setup_wisepair.ps1
   ```

3. Run the application:
   ```
   flask run
   ```

### Docker Setup

1. Build and run with Docker Compose:
   ```
   docker-compose up
   ```

## Documentation

For detailed documentation about the project structure, API endpoints, and deployment instructions, please see the [DOCUMENTATION.md](DOCUMENTATION.md) file.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 