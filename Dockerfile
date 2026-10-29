# ==============================================================================
# DevOps Quest - Multi-Stage Hardened Production Dockerfile
#
# Stage 1 (builder): Installs Python dependencies into an isolated virtualenv.
# Stage 2 (runner):  Lightweight, unprivileged runtime with zero build tools.
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage 1: Build & Dependency Resolution
# ------------------------------------------------------------------------------
FROM python:3.13-slim-bookworm AS builder

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

# Create an isolated virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install production dependencies only (pinned versions)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ------------------------------------------------------------------------------
# Stage 2: Final Minimal Runtime Image
# ------------------------------------------------------------------------------
FROM python:3.13-slim-bookworm AS runner

# Security: Set runtime environment defaults
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    PORT=5000 \
    FLASK_ENV=production \
    FLASK_DEBUG=0 \
    DATABASE_PATH=/app/instance/devops_quest.db

WORKDIR /app

# Create a dedicated, unprivileged system group and user
RUN groupadd -r -g 10001 appgroup && \
    useradd -r -u 10001 -g appgroup -d /app -s /sbin/nologin -c "DevOps Quest Application User" appuser && \
    mkdir -p /app/instance && \
    chown -R appuser:appgroup /app

# Copy isolated virtual environment from the builder stage
COPY --from=builder --chown=appuser:appgroup /opt/venv /opt/venv

# Copy application source code with non-root ownership
COPY --chown=appuser:appgroup app/ /app/app/
COPY --chown=appuser:appgroup run.py /app/run.py

# Switch permanently to the non-root user
USER appuser

# Expose default application port (Render or Compose may override via $PORT)
EXPOSE 5000

# Automated container health check verifying the /health endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import os, sys, urllib.request; \
        url = f'http://127.0.0.1:{os.environ.get(\"PORT\", \"5000\")}/health'; \
        res = urllib.request.urlopen(url, timeout=3); \
        sys.exit(0 if res.getcode() == 200 else 1)"

# Production WSGI execution using Gunicorn with dynamic port binding
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 2 --timeout 30 --access-logfile - --error-logfile - 'app:create_app()'"]
