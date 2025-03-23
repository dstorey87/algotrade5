# REMOVED_UNUSED_CODE: from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import uvicorn
import os
from typing import List, Dict, Any

class TradingStatus(BaseModel):
# REMOVED_UNUSED_CODE:     is_running: bool
# REMOVED_UNUSED_CODE:     active_models: List[str] = []
# REMOVED_UNUSED_CODE:     current_trades: List[Dict[str, Any]] = []
# REMOVED_UNUSED_CODE:     current_balance: float = 10.0
# REMOVED_UNUSED_CODE:     drawdown: float = 0.0

app = FastAPI(title="FreqAI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://frontend:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REMOVED_UNUSED_CODE: @app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

# REMOVED_UNUSED_CODE: @app.get("/api/v1/status", response_model=TradingStatus)
async def get_status():
    return {
        "is_running": True,
        "active_models": [],
        "current_trades": [],
        "current_balance": float(os.getenv("INITIAL_CAPITAL", "10.0")),
        "drawdown": 0.0
    }

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=int(os.getenv("API_PORT", 8001)),
        reload=True
    )
