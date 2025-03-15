# syntax=docker/dockerfile:1.4

# Stage 1: Builder with cached dependencies
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /build

# Copy cached dependencies first
COPY docker/programdata/pip_cache /root/.cache/pip
COPY docker/programdata/model_cache /root/.cache/huggingface
COPY docker/programdata/dependency_cache /root/.cache/deps

# Install build dependencies using existing cache
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY requirements*.txt ./
COPY dependencies/site-packages ./dependencies/site-packages/

# Install dependencies using cache
RUN --mount=type=cache,target=/root/.cache/pip,id=pip \
    pip install --no-cache-dir --prefix=/build -r requirements.txt && \
    if [ -f "requirements-quantum.txt" ]; then \
        pip install --no-cache-dir --prefix=/build -r requirements-quantum.txt; \
    fi && \
    if [ -f "requirements-freqai.txt" ]; then \
        pip install --no-cache-dir --prefix=/build -r requirements-freqai.txt; \
    fi && \
    if [ -d "dependencies/site-packages" ]; then \
        cp -r dependencies/site-packages/* /build/lib/python3.11/site-packages/; \
    fi

# Stage 2: Final image
FROM freqtradeorg/freqtrade:stable

# Copy installed packages from builder
COPY --from=builder /build/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /root/.cache/pip /root/.cache/pip
COPY --from=builder /root/.cache/huggingface /root/.cache/huggingface
COPY --from=builder /root/.cache/deps /root/.cache/deps

# Create directory structure
WORKDIR /freqtrade
RUN mkdir -p /freqtrade/user_data/strategies/utils

# Copy strategy files
COPY user_data/strategies /freqtrade/user_data/strategies/

# Set environment variables
ENV PYTHONPATH=/freqtrade/user_data/strategies:/freqtrade/src:/freqtrade

# Health check
HEALTHCHECK --interval=60s --timeout=30s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/api/v1/ping || exit 1

# Default command
CMD ["trade", "--strategy", "QuantumHybridStrategy", "--config", "/freqtrade/user_data/config.json"]