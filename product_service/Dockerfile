FROM python:2.7

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python-dev

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=myproject.settings

# Expose the port Django runs on
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--workers=3", "product_service.wsgi:application", "--bind", "0.0.0.0:8000"]