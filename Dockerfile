FROM freqtradeorg/freqtrade:stable

WORKDIR /freqtrade

# Copy strategy and dependencies first
COPY --chown=ftuser:ftuser user_data/strategies /freqtrade/user_data/strategies/
COPY --chown=ftuser:ftuser src/quantum /freqtrade/src/quantum/
COPY --chown=ftuser:ftuser requirements*.txt ./

USER root
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r requirements-quantum.txt \
    && pip install --no-cache-dir lightgbm

USER ftuser

# Set environment variables
ENV PYTHONPATH=/freqtrade/src:/freqtrade/user_data/strategies

# Health check
HEALTHCHECK --interval=60s --timeout=30s --start-period=30s --retries=3 \
    CMD curl --fail http://localhost:8080/api/v1/ping || exit 1