import logging
from typing import Any, Dict, List

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.ai_control import router as ai_router
from src.api.health_check import router as health_router
from src.api.ml_control import router as ml_router
from src.api.system_metrics import router as system_router
from src.api.trading_control import router as trading_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AlgoTradePro5 API",
    description="API for AlgoTradePro5 trading system",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(system_router, tags=["System"])
app.include_router(ml_router, tags=["Machine Learning"])
app.include_router(trading_router, tags=["Trading"])
app.include_router(health_router, tags=["Health"])
app.include_router(ai_router, tags=["AI Components"])


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "AlgoTradePro5 API",
        "version": "1.0.0",
        "description": "Control interface for AlgoTradePro5 trading system",
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("API server starting up")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("API server shutting down")
