import logging
from datetime import datetime
# REMOVED_UNUSED_CODE: from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query

# Import health check components
from src.core.system_health_checker import SystemHealthChecker
from src.monitoring.system_monitor import SystemMonitor
# REMOVED_UNUSED_CODE: from src.utils.utils import handle_exceptions

router = APIRouter(prefix="/api/v1/health")
logger = logging.getLogger(__name__)

# Initialize components
try:
    health_checker = SystemHealthChecker()
    system_monitor = SystemMonitor()
except Exception as e:
    logger.error(f"Failed to initialize health components: {e}")
    health_checker = None
    system_monitor = None


# REMOVED_UNUSED_CODE: @router.get("/status")
async def get_health_status() -> Dict[str, Any]:
    """Get overall system health status"""
    try:
        if not health_checker:
            raise HTTPException(
                status_code=503, detail="Health checker not initialized"
            )

        status = health_checker.get_system_health_status()
        return {
            "timestamp": datetime.now().isoformat(),
            "status": status["overall_status"],
            "components": status["components"],
            "issues": status.get("issues", []),
        }
    except Exception as e:
        logger.error(f"Error retrieving health status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/components")
async def get_component_health(
    component_type: Optional[str] = Query(None, description="Filter by component type"),
) -> Dict[str, Any]:
    """Get detailed health status of system components"""
    try:
        if not health_checker:
            raise HTTPException(
                status_code=503, detail="Health checker not initialized"
            )

        components = health_checker.get_component_health(component_type)
        return {
            "timestamp": datetime.now().isoformat(),
            "components": components,
            "total_count": len(components),
        }
    except Exception as e:
        logger.error(f"Error retrieving component health: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/diagnostics")
async def run_system_diagnostics() -> Dict[str, Any]:
    """Run comprehensive system diagnostics"""
    try:
        if not health_checker:
            raise HTTPException(
                status_code=503, detail="Health checker not initialized"
            )

        diagnostics = health_checker.run_system_diagnostics()
        return {
            "timestamp": datetime.now().isoformat(),
            "diagnostics": diagnostics,
            "status": "completed",
        }
    except Exception as e:
        logger.error(f"Error running diagnostics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resources")
async def get_resource_utilization() -> Dict[str, Any]:
    """Get detailed resource utilization metrics"""
    try:
        if not system_monitor:
            raise HTTPException(
                status_code=503, detail="System monitor not initialized"
            )

        resources = system_monitor.get_resource_utilization()
        return {"timestamp": datetime.now().isoformat(), "resources": resources}
    except Exception as e:
        logger.error(f"Error retrieving resource utilization: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/gpu")
async def get_gpu_status() -> Dict[str, Any]:
    """Get detailed GPU status and metrics"""
    try:
        if not system_monitor:
            raise HTTPException(
                status_code=503, detail="System monitor not initialized"
            )

        gpu_status = system_monitor.get_gpu_status()
        return {
            "timestamp": datetime.now().isoformat(),
            "gpu": gpu_status,
            "available": gpu_status.get("available", False),
        }
    except Exception as e:
        logger.error(f"Error retrieving GPU status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/database")
async def get_database_health() -> Dict[str, Any]:
    """Get database health and status"""
    try:
        if not health_checker:
            raise HTTPException(
                status_code=503, detail="Health checker not initialized"
            )

        db_health = health_checker.get_database_health()
        return {
            "timestamp": datetime.now().isoformat(),
            "database": db_health,
            "status": db_health.get("status", "unknown"),
        }
    except Exception as e:
        logger.error(f"Error retrieving database health: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# REMOVED_UNUSED_CODE: @router.post("/check/{component_id}")
async def check_component_health(component_id: str) -> Dict[str, Any]:
    """Run health check on a specific component"""
    try:
        if not health_checker:
            raise HTTPException(
                status_code=503, detail="Health checker not initialized"
            )

        component_health = health_checker.check_component(component_id)
        if not component_health:
            raise HTTPException(
                status_code=404, detail=f"Component {component_id} not found"
            )

        return {
            "timestamp": datetime.now().isoformat(),
            "component_id": component_id,
            "health": component_health,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error checking component health: {e}")
        raise HTTPException(status_code=500, detail=str(e))
