#!/usr/bin/env python3
"""
FreqAI Service
==============

Main service for FreqAI in AlgoTradePro5. This script acts as the entry point
for the FreqAI container and provides an API for interacting with FreqAI models.

Author: GitHub Copilot
Last Updated: 2023-07-21
"""

import argparse
import json
import logging
import os
import signal
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Add the project root to the Python path
sys.path.append("/app")

# Import core modules
from core.models.freqai_interface import FreqAIInterface

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join("/app/logs", "freqai_service.log")),
    ],
)
logger = logging.getLogger("freqai_service")

# Create the FastAPI app
app = FastAPI(
    title="AlgoTradePro5 FreqAI Service",
    description="AI-driven trading system API for FreqAI models",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, this should be restricted
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
freqai_interface = None
startup_time = datetime.now()


@app.on_event("startup")
async def startup_event():
    """Initialize the FreqAI interface on startup"""
    global freqai_interface
    
    logger.info("Starting FreqAI service")
    
    try:
        # Load configuration
        config_path = os.environ.get("CONFIG_PATH", "/app/freqai_config.json")
        
        if not os.path.exists(config_path):
            logger.error(f"Configuration file not found: {config_path}")
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
            
        with open(config_path, "r") as f:
            config = json.load(f)
            
        # Initialize FreqAI interface
        freqai_interface = FreqAIInterface(config)
        
        logger.info("FreqAI service started successfully")
    except Exception as e:
        logger.error(f"Error starting FreqAI service: {e}")
        sys.exit(1)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "AlgoTradePro5 FreqAI Service",
        "status": "running",
        "uptime": str(datetime.now() - startup_time),
        "version": "1.0.0",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "uptime": str(datetime.now() - startup_time),
        "freqai_status": "running" if freqai_interface else "not initialized",
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/analyze")
async def analyze_patterns(request: Request):
    """Analyze trade patterns from historical data"""
    if not freqai_interface:
        raise HTTPException(status_code=503, detail="FreqAI interface not initialized")
        
    try:
        data = await request.json()
        trades_data = data.get("trades", [])
        
        if not trades_data:
            return JSONResponse(
                status_code=400,
                content={"error": "No trade data provided"},
            )
            
        # Convert to DataFrame
        trades_df = pd.DataFrame(trades_data)
        
        # Analyze patterns
        patterns = freqai_interface.analyze_trade_patterns(trades_df)
        
        return {
            "patterns": patterns,
            "timestamp": datetime.now().isoformat(),
            "status": "success",
        }
    except Exception as e:
        logger.error(f"Error analyzing patterns: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/recommend")
async def recommend_trades(request: Request):
    """Generate trade recommendations based on current market conditions"""
    if not freqai_interface:
        raise HTTPException(status_code=503, detail="FreqAI interface not initialized")
        
    try:
        data = await request.json()
        conditions = data.get("conditions", {})
        
        if not conditions:
            return JSONResponse(
                status_code=400,
                content={"error": "No market conditions provided"},
            )
            
        # Generate recommendations
        recommendations = freqai_interface.recommend_trades(conditions)
        
        return {
            "recommendations": recommendations,
            "timestamp": datetime.now().isoformat(),
            "status": "success",
        }
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/update")
async def update_models(request: Request):
    """Update models with new trade data"""
    if not freqai_interface:
        raise HTTPException(status_code=503, detail="FreqAI interface not initialized")
        
    try:
        data = await request.json()
        new_data = data.get("trades", [])
        
        if not new_data:
            return JSONResponse(
                status_code=400,
                content={"error": "No trade data provided for model update"},
            )
            
        # Convert to DataFrame
        new_data_df = pd.DataFrame(new_data)
        
        # Update models
        success = freqai_interface.update_model(new_data_df)
        
        return {
            "success": success,
            "timestamp": datetime.now().isoformat(),
            "status": "success" if success else "failed",
        }
    except Exception as e:
        logger.error(f"Error updating models: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/performance")
async def get_performance():
    """Get model performance metrics"""
    if not freqai_interface:
        raise HTTPException(status_code=503, detail="FreqAI interface not initialized")
        
    try:
        # Generate performance report
        report = freqai_interface.get_performance_report()
        
        return {
            "report": report,
            "timestamp": datetime.now().isoformat(),
            "status": "success",
        }
    except Exception as e:
        logger.error(f"Error generating performance report: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def handle_sigterm(signum, frame):
    """Handle SIGTERM signal gracefully"""
    logger.info("Received SIGTERM signal, shutting down...")
    sys.exit(0)


def main():
    """Main entry point for the FreqAI service"""
    parser = argparse.ArgumentParser(description="AlgoTradePro5 FreqAI Service")
    parser.add_argument(
        "--port", type=int, default=8081, help="Port to run the service on"
    )
    parser.add_argument(
        "--host", type=str, default="0.0.0.0", help="Host to run the service on"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level",
    )
    
    args = parser.parse_args()
    
    # Configure logging level
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    # Set up signal handlers
    signal.signal(signal.SIGTERM, handle_sigterm)
    
    # Create log directory if it doesn't exist
    Path("/app/logs").mkdir(exist_ok=True, parents=True)
    
    # Start the FastAPI app
    logger.info(f"Starting FreqAI service on {args.host}:{args.port}")
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()