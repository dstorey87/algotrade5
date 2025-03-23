import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query

# Import trading components
from src.core.risk_manager import RiskManager
from src.core.strategy_engine import StrategyEngine
from src.utils.utils import handle_exceptions

router = APIRouter(prefix="/api/v1/trading")
logger = logging.getLogger(__name__)

# Initialize components
try:
    risk_manager = RiskManager()
    strategy_engine = StrategyEngine()
except Exception as e:
    logger.error(f"Failed to initialize trading components: {e}")
    risk_manager = None
    strategy_engine = None


@router.get("/status")
async def get_trading_status() -> Dict[str, Any]:
    """Get current trading system status"""
    try:
        if not strategy_engine:
            raise HTTPException(
                status_code=503, detail="Strategy engine not initialized"
            )

        status = strategy_engine.get_trading_status()
        return {
            "timestamp": datetime.now().isoformat(),
            "trading_enabled": status["trading_enabled"],
            "active_strategy": status["active_strategy"],
            "position_count": status["position_count"],
            "last_trade_time": status["last_trade_time"],
        }
    except Exception as e:
        logger.error(f"Error retrieving trading status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/start")
async def start_trading(strategy_id: Optional[str] = None) -> Dict[str, Any]:
    """Start trading with optional strategy selection"""
    try:
        if not strategy_engine:
            raise HTTPException(
                status_code=503, detail="Strategy engine not initialized"
            )

        result = strategy_engine.start_trading(strategy_id)
        return {
            "timestamp": datetime.now().isoformat(),
            "success": result["success"],
            "message": result["message"],
            "active_strategy": result.get("active_strategy", None),
        }
    except Exception as e:
        logger.error(f"Error starting trading: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stop")
async def stop_trading(
    emergency: bool = Query(False, description="Emergency stop all positions"),
) -> Dict[str, Any]:
    """Stop trading system with option for emergency stop"""
    try:
        if not strategy_engine:
            raise HTTPException(
                status_code=503, detail="Strategy engine not initialized"
            )

        result = strategy_engine.stop_trading(emergency)
        return {
            "timestamp": datetime.now().isoformat(),
            "success": result["success"],
            "message": result["message"],
            "emergency_stop": emergency,
        }
    except Exception as e:
        logger.error(f"Error stopping trading: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/strategies")
async def get_available_strategies() -> Dict[str, Any]:
    """Get list of all available trading strategies"""
    try:
        if not strategy_engine:
            raise HTTPException(
                status_code=503, detail="Strategy engine not initialized"
            )

        strategies = strategy_engine.get_available_strategies()
        return {
            "timestamp": datetime.now().isoformat(),
            "strategies": strategies,
            "total_count": len(strategies),
        }
    except Exception as e:
        logger.error(f"Error retrieving strategies: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/strategies/{strategy_id}")
async def get_strategy_details(strategy_id: str) -> Dict[str, Any]:
    """Get detailed information about a specific strategy"""
    try:
        if not strategy_engine:
            raise HTTPException(
                status_code=503, detail="Strategy engine not initialized"
            )

        strategy = strategy_engine.get_strategy_details(strategy_id)
        if not strategy:
            raise HTTPException(
                status_code=404, detail=f"Strategy {strategy_id} not found"
            )

        return {
            "timestamp": datetime.now().isoformat(),
            "strategy_id": strategy_id,
            "details": strategy,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving strategy details: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/strategies/{strategy_id}/activate")
async def activate_strategy(strategy_id: str) -> Dict[str, Any]:
    """Activate a specific trading strategy"""
    try:
        if not strategy_engine:
            raise HTTPException(
                status_code=503, detail="Strategy engine not initialized"
            )

        result = strategy_engine.activate_strategy(strategy_id)
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])

        return {
            "timestamp": datetime.now().isoformat(),
            "success": result["success"],
            "message": result["message"],
            "active_strategy": strategy_id,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error activating strategy: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/performance")
async def get_trading_performance(
    timeframe: str = Query("1d", description="Time period for performance metrics"),
) -> Dict[str, Any]:
    """Get trading performance metrics"""
    try:
        if not strategy_engine:
            raise HTTPException(
                status_code=503, detail="Strategy engine not initialized"
            )

        performance = strategy_engine.get_performance_metrics(timeframe)
        return {
            "timestamp": datetime.now().isoformat(),
            "timeframe": timeframe,
            "performance": performance,
        }
    except Exception as e:
        logger.error(f"Error retrieving performance metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/risk")
async def get_risk_metrics() -> Dict[str, Any]:
    """Get current risk metrics"""
    try:
        if not risk_manager:
            raise HTTPException(status_code=503, detail="Risk manager not initialized")

        risk_metrics = risk_manager.get_risk_metrics()
        return {"timestamp": datetime.now().isoformat(), "risk_metrics": risk_metrics}
    except Exception as e:
        logger.error(f"Error retrieving risk metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/risk/update")
async def update_risk_parameters(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Update risk management parameters"""
    try:
        if not risk_manager:
            raise HTTPException(status_code=503, detail="Risk manager not initialized")

        result = risk_manager.update_parameters(parameters)
        return {
            "timestamp": datetime.now().isoformat(),
            "success": result["success"],
            "message": result["message"],
            "updated_parameters": result.get("updated_parameters", []),
        }
    except Exception as e:
        logger.error(f"Error updating risk parameters: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/execute_trade")
async def execute_manual_trade(trade_data: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a manual trade"""
    try:
        if not strategy_engine:
            raise HTTPException(
                status_code=503, detail="Strategy engine not initialized"
            )

        # Validate against risk parameters
        if risk_manager:
            risk_check = risk_manager.validate_trade(trade_data)
            if not risk_check["valid"]:
                raise HTTPException(status_code=400, detail=risk_check["reason"])

        # Execute trade
        result = strategy_engine.execute_manual_trade(trade_data)

        return {
            "timestamp": datetime.now().isoformat(),
            "success": result["success"],
            "message": result["message"],
            "trade_id": result.get("trade_id", None),
            "order_details": result.get("order_details", None),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error executing trade: {e}")
        raise HTTPException(status_code=500, detail=str(e))
