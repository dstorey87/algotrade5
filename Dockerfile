FROM freqtradeorg/freqtrade:stable

# Create dependency cache directory
RUN mkdir -p /freqtrade/dependencies/site-packages

# Copy dependency files
COPY dependencies/site-packages /freqtrade/dependencies/site-packages/
COPY src/core/dependency_manager.py /freqtrade/src/core/

# Install dependencies from cache if available
RUN if [ -d "/freqtrade/dependencies/site-packages" ] && [ "$(ls -A /freqtrade/dependencies/site-packages)" ]; then \
    cp -r /freqtrade/dependencies/site-packages/* /usr/local/lib/python3.9/site-packages/; \
    else \
    echo "No cached dependencies found"; \
    fi

WORKDIR /freqtrade

# Set environment
ENV PYTHONPATH=/freqtrade/src:/freqtrade/user_data/strategies

# Health check
HEALTHCHECK --interval=60s --timeout=30s --start-period=30s --retries=3 \
    CMD curl --fail http://localhost:8080/api/v1/ping || exit 1