FROM freqtradeorg/freqtrade:stable

# Copy requirements files
COPY requirements*.txt /freqtrade/
COPY pip.conf /etc/pip.conf

# Install datasieve without dependencies first
RUN pip install --no-deps --no-cache-dir datasieve==0.1.5

# Install other FreqAI dependencies
RUN pip install --no-cache-dir -r /freqtrade/requirements-freqai-custom.txt

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