from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging

# Import AI components
from src.core.ai_model_manager import AIModelManager
from src.llm.llm_manager import LLMManager
from src.utils.utils import handle_exceptions

router = APIRouter(prefix="/api/v1/ai")
logger = logging.getLogger(__name__)

# Initialize managers
try:
    ai_model_manager = AIModelManager()
    llm_manager = LLMManager()
except Exception as e:
    logger.error(f"Failed to initialize AI components: {e}")
    ai_model_manager = None
    llm_manager = None

@router.get("/llm/models")
async def get_available_llm_models() -> Dict[str, Any]:
    """Get list of all available LLM models"""
    try:
        if not llm_manager:
            raise HTTPException(status_code=503, detail="LLM manager not initialized")
        
        models = llm_manager.get_available_models()
        return {
            "timestamp": datetime.now().isoformat(),
            "models": models,
            "total_count": len(models)
        }
    except Exception as e:
        logger.error(f"Error retrieving LLM models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/llm/generate")
async def generate_llm_response(
    model_id: str,
    prompt: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate a response using an LLM model"""
    try:
        if not llm_manager:
            raise HTTPException(status_code=503, detail="LLM manager not initialized")
            
        # Validate model availability
        if not llm_manager.is_model_available(model_id):
            raise HTTPException(status_code=404, detail=f"Model {model_id} not found")
            
        # Generate response
        start_time = datetime.now()
        response = llm_manager.generate_response(model_id, prompt)
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return {
            "timestamp": datetime.now().isoformat(),
            "model_id": model_id,
            "response": response,
            "processing_time_ms": processing_time
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating LLM response: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/quantum/status")
async def get_quantum_system_status() -> Dict[str, Any]:
    """Get status of quantum computing components"""
    try:
        if not ai_model_manager:
            raise HTTPException(status_code=503, detail="AI model manager not initialized")
            
        quantum_status = ai_model_manager.get_quantum_status()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "quantum_system": quantum_status,
            "is_available": quantum_status.get("available", False)
        }
    except Exception as e:
        logger.error(f"Error retrieving quantum status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/quantum/execute")
async def execute_quantum_circuit(
    circuit_data: Dict[str, Any],
    background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """Execute a quantum circuit operation"""
    try:
        if not ai_model_manager:
            raise HTTPException(status_code=503, detail="AI model manager not initialized")
            
        # Check quantum system availability
        quantum_status = ai_model_manager.get_quantum_status()
        if not quantum_status.get("available", False):
            raise HTTPException(status_code=503, detail="Quantum system not available")
            
        # Execute in background to avoid blocking
        task_id = ai_model_manager.submit_quantum_job(circuit_data)
        background_tasks.add_task(ai_model_manager.process_quantum_job, task_id)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "task_id": task_id,
            "status": "submitted",
            "message": "Quantum job submitted for processing"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error executing quantum circuit: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/quantum/jobs/{task_id}")
async def get_quantum_job_status(task_id: str) -> Dict[str, Any]:
    """Get status of a quantum computing job"""
    try:
        if not ai_model_manager:
            raise HTTPException(status_code=503, detail="AI model manager not initialized")
            
        job_status = ai_model_manager.get_quantum_job_status(task_id)
        if not job_status:
            raise HTTPException(status_code=404, detail=f"Quantum job {task_id} not found")
            
        return {
            "timestamp": datetime.now().isoformat(),
            "task_id": task_id,
            "status": job_status
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving quantum job status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/strategies/analyze")
async def analyze_trading_strategy(
    strategy_id: str,
    timeframe: str = "1d",
    pair: str = "BTC/USDT"
) -> Dict[str, Any]:
    """Analyze a trading strategy using AI"""
    try:
        if not llm_manager:
            raise HTTPException(status_code=503, detail="LLM manager not initialized")
            
        analysis = llm_manager.analyze_strategy(strategy_id, timeframe, pair)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "strategy_id": strategy_id,
            "analysis": analysis,
            "recommendation": analysis.get("recommendation", None)
        }
    except Exception as e:
        logger.error(f"Error analyzing strategy: {e}")
        raise HTTPException(status_code=500, detail=str(e))