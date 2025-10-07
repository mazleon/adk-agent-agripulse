# ============================================================================
# AgriPulse AI - Optimized Multi-Stage Dockerfile
# ============================================================================
# Stage 1: Builder - Install dependencies and prepare application
# Stage 2: Runtime - Minimal production image
# ============================================================================

# ============================================================================
# STAGE 1: Builder
# ============================================================================
FROM python:3.13-slim AS builder

# Set build arguments
ARG DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /build

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv (fast Python package installer)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install Python dependencies using uv
# Create virtual environment and install all dependencies
RUN uv venv /opt/venv && \
    . /opt/venv/bin/activate && \
    uv pip install --no-cache -r pyproject.toml

# ============================================================================
# STAGE 2: Runtime
# ============================================================================
FROM python:3.13-slim AS runtime

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_SERVER_FILE_WATCHER_TYPE=none

# Create non-root user for security
RUN groupadd -r agripulse && \
    useradd -r -g agripulse -u 1000 -m -s /bin/bash agripulse

# Set working directory
WORKDIR /app

# Install runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY --chown=agripulse:agripulse . .

# Create necessary directories with proper permissions
RUN mkdir -p /app/logs /app/.streamlit && \
    chown -R agripulse:agripulse /app

# Copy Streamlit configuration
COPY --chown=agripulse:agripulse deployment/streamlit_config.toml /app/.streamlit/config.toml

# Switch to non-root user
USER agripulse

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8501/_stcore/health')" || exit 1

# Expose Streamlit port
EXPOSE 8501

# Set entrypoint
ENTRYPOINT ["streamlit", "run"]

# Default command
CMD ["main.py", "--server.port=8501", "--server.address=0.0.0.0"]
