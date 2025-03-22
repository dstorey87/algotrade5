from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import uvicorn
import os
from typing import List, Dict, Any

class TradingStatus(BaseModel):
    is_running: bool
    active_models: List[str] = []
    current_trades: List[Dict[str, Any]] = []
    current_balance: float = 10.0
    drawdown: float = 0.0

app = FastAPI(title="FreqAI Interface")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://frontend:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/status", response_model=TradingStatus)
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
        "freqai_interface:app",
        host="0.0.0.0",
        port=int(os.getenv("API_PORT", 8001)),
        reload=True
    )
