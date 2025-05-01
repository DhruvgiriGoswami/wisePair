# WisePair Documentation

## Table of Contents
1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Core Modules](#core-modules)
4. [Flow and Architecture](#flow-and-architecture)
5. [API Endpoints](#api-endpoints)
6. [Database Schema](#database-schema)
7. [Setting up Locally](#setting-up-locally)
8. [Deploying to AWS EC2](#deploying-to-aws-ec2)
9. [Using MinIO for File Storage](#using-minio-for-file-storage)
10. [Email Integration](#email-integration)

## Overview

WisePair is a project mentorship and management platform designed for campus hackathons. The application facilitates team formation, idea submission, mentor matching, and project progress tracking. It helps students find suitable mentors (professors or senior students) for their hackathon projects and allows mentors to track and evaluate student progress.

### Key Features

- Student authentication and registration
- Team creation and management
- Professor and mentor matching
- Idea submission
- Meeting scheduling
- File uploads
- Leaderboard system
- Email notifications

## Project Structure

The project follows a layered architecture with modular components:

```
/wise_pair
├── app/
│   ├── models/        # Database models (SQLAlchemy)
│   ├── routes/        # API endpoints (Flask Blueprints)
│   ├── services/      # Business logic
│   ├── schemas/       # Data validation (Pydantic)
│   ├── utils/         # Helper functions
│   ├── __init__.py    # Application factory
│   └── config.py      # Application configuration
├── migrations/        # Database migrations (Alembic)
├── .env               # Environment variables
├── docker-compose.yml # Docker configuration
├── Dockerfile         # Container definition
├── requirements.txt   # Python dependencies
└── run.py             # Application entry point
```

## Core Modules

### Models (`app/models/`)

Contains SQLAlchemy models that define the database schema.

- **`base.py`**: Base model with common fields and methods
- **`student.py`**: Student user model
- **`team.py`**: Team model
- **`professor.py`**: Professor mentor model
- **`mentor.py`**: Senior student mentor model
- **`requests.py`**: Models for mentorship requests
- **`idea.py`**: Project ideas model
- **`meeting.py`**: Meeting scheduling model
- **`leaderboard.py`**: Team rankings model
- **`file.py`**: File metadata model for uploads

### Routes (`app/routes/`)

Flask Blueprints that define the API endpoints.

- **`auth.py`**: Authentication endpoints (login, register)
- **`teams.py`**: Team management endpoints
- **`professors.py`**: Professor-related endpoints
- **`mentors.py`**: Senior mentor-related endpoints
- **`meetings.py`**: Meeting scheduling endpoints
- **`leaderboard.py`**: Leaderboard and ranking endpoints
- **`files.py`**: File upload and retrieval endpoints

### Services (`app/services/`)

Contains business logic separated from the route handlers.

- **`auth_service.py`**: Authentication validation
- **`team_service.py`**: Team management logic
- **`meeting_service.py`**: Meeting validation and business rules
- **`file_service.py`**: File handling with MinIO integration
- **`email_service.py`**: Email notifications via SMTP

### Schemas (`app/schemas/`)

Pydantic models for request/response validation.

- **`auth.py`**: Authentication request schemas
- **`teams.py`**: Team-related data schemas

### Utils (`app/utils/`)

Utility functions and decorators.

- **`decorators.py`**: Custom route decorators (e.g., team_leader_required)

## Flow and Architecture

The application follows a layered architecture:

1. **Client Layer**: HTTP requests from the client
2. **API Layer** (`app/routes/`): Route handlers that validate requests
3. **Service Layer** (`app/services/`): Business logic
4. **Data Access Layer** (`app/models/`): Database models and access

### Request Flow

1. Client sends an HTTP request to an endpoint
2. Flask routes the request to the appropriate handler
3. JWT authentication middleware validates the token (if protected route)
4. Route handler validates the request data using schemas or service functions
5. Service layer applies business logic
6. Data access layer interacts with the database
7. Response is returned to the client

### Key Workflows

#### User Authentication
1. User registers with email, password, and details
2. Credentials are validated and stored securely
3. JWT token is generated and returned for authenticated access

#### Team Formation
1. Student creates a team
2. Other students join the team (up to 4 members)
3. Team leader can lock the team when it's full

#### Mentorship Request
1. Team leader sends a request to a professor/senior mentor
2. Professor/mentor receives the request and can accept/reject
3. If accepted, the professor/mentor is assigned to the team

#### Meeting Scheduling
1. Team leader schedules a meeting with the mentor
2. Meeting details are stored and notifications are sent
3. After the meeting, feedback can be recorded

#### File Upload
1. Team members can upload files related to their project
2. Files are stored in MinIO and metadata is saved in the database
3. Files can be accessed via generated URLs

## API Endpoints

### Authentication
- `POST /api/auth/register`: Register a new student
- `POST /api/auth/login`: Login and get JWT token
- `GET /api/auth/profile`: Get current user profile
- `PUT /api/auth/profile`: Update user profile

### Teams
- `POST /api/teams`: Create a new team
- `GET /api/teams`: Get all teams
- `GET /api/teams/<id>`: Get team details
- `GET /api/teams/my-team`: Get current user's team
- `POST /api/teams/<id>/join`: Join a team
- `POST /api/teams/<id>/invite`: Invite a student to a team
- `POST /api/teams/<id>/lock`: Lock a team

### Professors
- `GET /api/professors`: Get all professors
- `GET /api/professors/<id>`: Get professor details
- `GET /api/professors/available`: Get professors who can accept more teams
- `POST /api/professors/request`: Request professor mentorship
- `POST /api/professors/requests/<id>/respond`: Respond to mentorship request

### Mentors
- `GET /api/mentors`: Get all mentors
- `GET /api/mentors/<id>`: Get mentor details
- `POST /api/mentors/request`: Request senior mentor
- `POST /api/mentors/requests/<id>/respond`: Respond to mentor request

### Meetings
- `POST /api/meetings`: Schedule a new meeting
- `GET /api/meetings/<id>`: Get meeting details
- `GET /api/meetings/team/<id>`: Get team meetings
- `POST /api/meetings/<id>/complete`: Mark meeting as completed
- `POST /api/meetings/<id>/cancel`: Cancel a meeting

### Leaderboard
- `GET /api/leaderboard`: Get all leaderboard entries
- `GET /api/leaderboard/top`: Get top 5 teams
- `GET /api/leaderboard/bottom`: Get bottom 5 teams
- `GET /api/leaderboard/team/<id>`: Get team leaderboard entry

### Files
- `POST /api/files/upload/team`: Upload team file
- `POST /api/files/upload/idea/<id>`: Upload idea file
- `GET /api/files/<id>`: Get file details
- `GET /api/files/team/<id>`: Get team files
- `GET /api/files/idea/<id>`: Get idea files

## Database Schema

![Database Schema]()

### Key Relationships

- **Student-Team**: Many-to-one relationship
- **Team-Professor**: Many-to-one relationship
- **Team-Mentor**: Many-to-one relationship
- **Team-Idea**: One-to-many relationship
- **Team-Meeting**: One-to-many relationship
- **Team-Leaderboard**: One-to-one relationship

## Setting up Locally

### Prerequisites
- Python 3.8+
- PostgreSQL
- MinIO (for file storage)
- Mailtrap account (for email testing)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/wisepair.git
   cd wisepair
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root with the following variables:
   ```
   FLASK_APP=wise_pair/run.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key
   JWT_SECRET_KEY=your-jwt-secret-key

   # Database
   DATABASE_URL=postgresql://postgres:password@localhost:5432/wisepair

   # MinIO Configuration
   MINIO_ENDPOINT=localhost:9000
   MINIO_ACCESS_KEY=minioadmin
   MINIO_SECRET_KEY=minioadmin
   MINIO_BUCKET_NAME=wisepair

   # SMTP Configuration
   SMTP_HOST=smtp.mailtrap.io
   SMTP_PORT=587
   SMTP_USER=your_mailtrap_user
   SMTP_PASS=your_mailtrap_pass
   SMTP_FROM_EMAIL=noreply@wisepair.com
   ```

5. **Initialize the database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Run the application**
   ```bash
   flask run
   ```

7. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

### Using Docker

Alternatively, you can use Docker Compose to run the application:

```bash
docker-compose up
```

This will start the Flask application, PostgreSQL database, and MinIO server.

## Deploying to AWS EC2

### Prerequisites
- AWS account
- EC2 instance (recommend t2.micro for testing, t2.small for production)
- Basic knowledge of AWS services

### Steps

1. **Launch an EC2 instance**
   - Choose Amazon Linux 2 AMI
   - Set up security groups to allow HTTP (80), HTTPS (443), and SSH (22)
   - Create and download the key pair

2. **Connect to your instance**
   ```bash
   ssh -i your-key.pem ec2-user@your-instance-public-dns
   ```

3. **Install dependencies**
   ```bash
   # Update packages
   sudo yum update -y
   
   # Install Git, Docker, and Docker Compose
   sudo yum install -y git docker
   sudo service docker start
   sudo usermod -a -G docker ec2-user
   
   # Install Docker Compose
   sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   
   # Install Python and pip
   sudo yum install -y python3 python3-pip
   ```

4. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/wisepair.git
   cd wisepair
   ```

5. **Configure environment variables**
   Create a `.env` file with your production settings.
   ```bash
   nano .env
   ```

6. **Deploy with Docker Compose**
   ```bash
   docker-compose up -d
   ```

7. **Set up Nginx as a reverse proxy (optional)**
   ```bash
   sudo amazon-linux-extras install nginx1
   sudo nano /etc/nginx/conf.d/wisepair.conf
   ```

   Add the following configuration:
   ```nginx
   server {
       listen 80;
       server_name your_domain.com;

       location / {
           proxy_pass http://localhost:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

   Start Nginx:
   ```bash
   sudo systemctl start nginx
   ```

8. **Set up SSL with Let's Encrypt (optional)**
   ```bash
   sudo amazon-linux-extras install epel
   sudo yum install -y certbot python-certbot-nginx
   sudo certbot --nginx -d your_domain.com
   ```

9. **Set up automatic updates and backups**
   Create a cron job for database backups:
   ```bash
   crontab -e
   ```
   
   Add the following line to back up the database daily:
   ```
   0 0 * * * docker exec wisepair_db_1 pg_dump -U postgres flaskdb > /home/ec2-user/backups/db_backup_$(date +\%Y\%m\%d).sql
   ```

## Using MinIO for File Storage

WisePair uses MinIO, an S3-compatible object storage server, for file storage.

### Local Setup

MinIO is included in the Docker Compose configuration. When using Docker Compose, MinIO will be available at:
- API: http://localhost:9000
- Console: http://localhost:9001

Default credentials:
- Access Key: minioadmin
- Secret Key: minioadmin

### Accessing the MinIO Console

1. Navigate to http://localhost:9001
2. Login with the credentials specified in your .env file
3. Create a bucket named 'wisepair' (if it doesn't exist)

### File Upload Process

1. Files are uploaded through the API endpoints
2. The application validates the file (type, size)
3. The file is uploaded to MinIO with a unique identifier
4. Metadata about the file is stored in the database
5. A public URL is generated for accessing the file

## Email Integration

WisePair integrates with email services to send notifications for:
- Team invitations
- Mentorship requests
- Meeting schedules
- Request approvals/rejections

### Setting Up Mailtrap for Development

1. Create a Mailtrap account at https://mailtrap.io
2. Create a new inbox
3. Copy the SMTP credentials to your .env file:
   ```
   SMTP_HOST=smtp.mailtrap.io
   SMTP_PORT=587
   SMTP_USER=your_mailtrap_user_from_dashboard
   SMTP_PASS=your_mailtrap_pass_from_dashboard
   ```

### Using a Production Email Service

For production, you can use services like:
- Amazon SES
- SendGrid
- Mailgun

Update your .env file with the appropriate SMTP settings for your chosen provider. 