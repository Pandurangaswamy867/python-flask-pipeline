
# =========================
# Build Stage
# =========================

FROM python:3.11-slim AS build

# Set working directory
WORKDIR /app

# Copy application file
COPY app.py .

# Install Flask
RUN pip install --no-cache-dir --prefix=/install flask

# =========================
# Runtime Stage
# =========================

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy installed Python packages
COPY --from=build /install /usr/local

# Copy application file
COPY --from=build /app/app.py .

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Flask configuration
ENV FLASK_APP=app.py

# Expose Flask port
EXPOSE 5000

# Start Flask application
CMD ["python", "app.py"]
