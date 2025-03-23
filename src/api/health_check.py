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
# REMOVED_UNUSED_CODE: async def get_health_status() -> Dict[str, Any]:
# REMOVED_UNUSED_CODE:     """Get overall system health status"""
# REMOVED_UNUSED_CODE:     try:
# REMOVED_UNUSED_CODE:         if not health_checker:
# REMOVED_UNUSED_CODE:             raise HTTPException(
# REMOVED_UNUSED_CODE:                 status_code=503, detail="Health checker not initialized"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         status = health_checker.get_system_health_status()
# REMOVED_UNUSED_CODE:         return {
# REMOVED_UNUSED_CODE:             "timestamp": datetime.now().isoformat(),
# REMOVED_UNUSED_CODE:             "status": status["overall_status"],
# REMOVED_UNUSED_CODE:             "components": status["components"],
# REMOVED_UNUSED_CODE:             "issues": status.get("issues", []),
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE:     except Exception as e:
# REMOVED_UNUSED_CODE:         logger.error(f"Error retrieving health status: {e}")
# REMOVED_UNUSED_CODE:         raise HTTPException(status_code=500, detail=str(e))


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
# REMOVED_UNUSED_CODE: async def check_component_health(component_id: str) -> Dict[str, Any]:
# REMOVED_UNUSED_CODE:     """Run health check on a specific component"""
# REMOVED_UNUSED_CODE:     try:
# REMOVED_UNUSED_CODE:         if not health_checker:
# REMOVED_UNUSED_CODE:             raise HTTPException(
# REMOVED_UNUSED_CODE:                 status_code=503, detail="Health checker not initialized"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         component_health = health_checker.check_component(component_id)
# REMOVED_UNUSED_CODE:         if not component_health:
# REMOVED_UNUSED_CODE:             raise HTTPException(
# REMOVED_UNUSED_CODE:                 status_code=404, detail=f"Component {component_id} not found"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return {
# REMOVED_UNUSED_CODE:             "timestamp": datetime.now().isoformat(),
# REMOVED_UNUSED_CODE:             "component_id": component_id,
# REMOVED_UNUSED_CODE:             "health": component_health,
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE:     except HTTPException:
# REMOVED_UNUSED_CODE:         raise
# REMOVED_UNUSED_CODE:     except Exception as e:
# REMOVED_UNUSED_CODE:         logger.error(f"Error checking component health: {e}")
# REMOVED_UNUSED_CODE:         raise HTTPException(status_code=500, detail=str(e))
