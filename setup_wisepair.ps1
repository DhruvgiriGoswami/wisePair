# Setup script for WisePair application on Windows
# This script creates a virtual environment, installs dependencies,
# and prepares the development environment

# Create .env file if it doesn't exist
if (-not (Test-Path -Path '.env')) {
    Write-Host "Creating .env file..." -ForegroundColor Green
    @"
FLASK_APP=wise_pair/run.py
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET_KEY=dev-jwt-secret-key-change-in-production

# Database
DATABASE_URL=postgresql://postgres:password@db:5432/flaskdb

# MinIO Configuration
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=wisepair

# SMTP Configuration
SMTP_HOST=smtp.mailtrap.io
SMTP_PORT=587
SMTP_USER=your_mailtrap_user
SMTP_PASS=your_mailtrap_pass
SMTP_FROM_EMAIL=noreply@wisepair.com
"@ | Out-File -FilePath '.env' -Encoding utf8
    Write-Host ".env file created. Remember to update with your actual credentials." -ForegroundColor Yellow
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path -Path 'venv')) {
    Write-Host "Creating virtual environment..." -ForegroundColor Green
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
. .\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Green
pip install -r requirements.txt

# Install package in development mode
Write-Host "Installing package in development mode..." -ForegroundColor Green
pip install -e .

# Initialize the database (if Flask Migrate is set up)
Write-Host "Would you like to initialize the database? (y/n)" -ForegroundColor Yellow
$init_db = Read-Host

if ($init_db -eq "y") {
    Write-Host "Initializing database..." -ForegroundColor Green
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
}

Write-Host @"

Setup complete! To run the application:
    flask run

Or use Docker Compose:
    docker-compose up

"@ -ForegroundColor Green 