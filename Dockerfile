FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Copy requirements files first for better caching
COPY requirements*.txt ./
COPY dependencies/site-packages ./dependencies/site-packages

# Install dependencies into /build
RUN pip install --no-cache-dir --prefix=/build -r requirements.txt \
    && if [ -f "requirements-quantum.txt" ]; then pip install --no-cache-dir --prefix=/build -r requirements-quantum.txt; fi \
    && if [ -d "dependencies/site-packages" ]; then cp -r dependencies/site-packages/* /build/lib/python3.11/site-packages/; fi

FROM freqtradeorg/freqtrade:stable

WORKDIR /freqtrade

# Copy installed packages from builder
COPY --from=builder /build/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Create directory structure
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