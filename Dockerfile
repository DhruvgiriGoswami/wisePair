FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PYTHONPATH=/app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a wrapper script for running the app
RUN echo '#!/bin/bash\n\
cd /app\n\
python -c "from wise_pair.app import create_app; app = create_app()" > /app/wsgi.py\n\
exec gunicorn --bind 0.0.0.0:5000 wsgi:app\n' > /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

# Create non-root user for security
RUN addgroup --system app && adduser --system --group app
RUN chown -R app:app /app
USER app

# Run with the wrapper script
CMD ["/app/entrypoint.sh"]
