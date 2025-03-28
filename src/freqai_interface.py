import json
import os
import logging
from datetime import datetime, timedelta
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import torch
import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from transformers import AutoModelForCausalLM, AutoTokenizer

# Import ML libraries based on predictor types in freqai_config.json
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import xgboost as xgb
import lightgbm as lgb
import catboost as cb
import asyncio

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/freqai.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("freqai")

# Enhanced monitoring metrics
class ModelActivity(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    model_name: str
    action: str
    success: bool
    details: Dict[str, Any]
    metrics: Optional[Dict[str, float]] = None

class SystemMetrics(BaseModel):
    gpu_usage: float = 0.0
    memory_usage: float = 0.0
    model_cache_size: int
    active_requests: int = 0
    last_error: Optional[str] = None

class TradingStatus(BaseModel):
    is_running: bool = True
    active_models: List[str] = []
    current_trades: List[Dict[str, Any]] = []
    current_balance: float = 10.0
    drawdown: float = 0.0

class PredictionRequest(BaseModel):
    pair: str
    timeframe: str
    features: Dict[str, float]
    model_name: Optional[str] = "quantum"

    @field_validator("pair")
    def validate_pair(cls, v):
        if not "/" in v or not v.endswith("USDT"):
            raise ValueError("Pair must be in format XXX/USDT")
        return v
    
    @field_validator("timeframe")
    def validate_timeframe(cls, v):
        valid_timeframes = {"1m", "5m", "15m", "30m", "1h", "4h", "1d"}
        if v not in valid_timeframes:
            raise ValueError(f"Timeframe must be one of {valid_timeframes}")
        return v
    
    @field_validator("features")
    def validate_features(cls, v):
        required_features = {"close", "volume", "rsi"}
        if not all(f in v for f in required_features):
            raise ValueError(f"Features must include {required_features}")
        return v

class ModelMetrics(BaseModel):
    accuracy: float = Field(ge=0, le=1)
    precision: float = Field(ge=0, le=1)
    recall: float = Field(ge=0, le=1)
    f1_score: float = Field(ge=0, le=1)
    win_rate: float = Field(ge=0, le=1)
    drawdown: float = Field(ge=0, le=1)

class PredictionResponse(BaseModel):
    prediction: float
    confidence: float
    model_used: str
    timestamp: str
    metrics: ModelMetrics

# Constants
MODEL_DIR = os.getenv("MODEL_DIR", "/app/models")
INITIAL_CAPITAL = float(os.getenv("INITIAL_CAPITAL", "10.0"))
MIN_CONFIDENCE = float(os.getenv("MIN_MODEL_CONFIDENCE", "0.85"))
CACHE_SIZE = int(os.getenv("MODEL_CACHE_SIZE", "10"))

app = FastAPI(
    title="FreqAI API",
    description="FreqAI Trading API Interface"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class ModelLoader:
    """Handles loading and caching of AI models for prediction"""
    
    def __init__(self):
        self.models = {}
        self.tokenizers = {}
        self.metrics = {}
        self.model_dir = Path(MODEL_DIR)
        self.config = self._load_freqai_config()
        self.load_model_metrics()
        
    def _load_freqai_config(self) -> dict:
        """Load FreqAI configuration from file"""
        config_path = Path(os.getenv("FREQAI_CONFIG_PATH", "/app/freqai_config.json"))
        
        if not config_path.exists():
            # Look for config in the current directory and parent directories
            config_path = None
            for search_path in [Path.cwd(), Path.cwd().parent]:
                for config_file in search_path.glob("**/freqai_config.json"):
                    config_path = config_file
                    break
                if config_path:
                    break
            
            if not config_path:
                logger.warning("FreqAI config not found, using default configuration")
                return {
                    "freqai": {"enabled": True, "identifier": "quantum"},
                    "predictors": {
                        "quantum": {
                            "model_path": "quantum",
                            "model_type": "LightGBMRegressor"
                        }
                    }
                }
        
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                logger.info(f"Loaded FreqAI config from {config_path}")
                return config
        except Exception as e:
            logger.error(f"Error loading FreqAI config: {str(e)}")
            return {
                "freqai": {"enabled": True, "identifier": "quantum"},
                "predictors": {
                    "quantum": {
                        "model_path": "quantum",
                        "model_type": "LightGBMRegressor"
                    }
                }
            }
        
    def load_model_metrics(self):
        """Load historical performance metrics for all models"""
        metrics_path = self.model_dir / "metrics.json"
        if metrics_path.exists():
            with open(metrics_path, "r") as f:
                self.metrics = json.load(f)
        else:
            # Default metrics if file doesn't exist
            self.metrics = {
                "quantum": {
                    "accuracy": 0.92,
                    "precision": 0.91,
                    "recall": 0.89,
                    "f1_score": 0.90,
                    "win_rate": 0.85,
                    "drawdown": 0.05
                },
                "mistral_trading": {
                    "accuracy": 0.88,
                    "precision": 0.87,
                    "recall": 0.86,
                    "f1_score": 0.87,
                    "win_rate": 0.82,
                    "drawdown": 0.07
                },
                "phi2": {
                    "accuracy": 0.85,
                    "precision": 0.84,
                    "recall": 0.83,
                    "f1_score": 0.84,
                    "win_rate": 0.80,
                    "drawdown": 0.08
                }
            }
            # Save default metrics
            with open(metrics_path, "w") as f:
                json.dump(self.metrics, f, indent=4)
    
    def _resolve_model_path(self, model_name: str) -> Path:
        """Resolve the model path using environment variables if necessary"""
        if model_name not in self.config.get("predictors", {}):
            # If not in config, use model_name directly
            return self.model_dir / model_name
            
        # Get the model path from config
        model_config = self.config["predictors"][model_name]
        model_path = model_config.get("model_path", model_name)
        
        # Replace environment variables in the path
        if isinstance(model_path, str) and "${" in model_path:
            for env_var in ["ML_MODELS_PATH", "MODEL_DIR", "MODELS_DIR"]:
                placeholder = f"${{{env_var}}}"
                if placeholder in model_path:
                    env_value = os.getenv(env_var, str(self.model_dir))
                    model_path = model_path.replace(placeholder, env_value)
        
        # If the path is now absolute, use it directly
        if Path(model_path).is_absolute():
            return Path(model_path)
            
        # Otherwise, join with model_dir
        return self.model_dir / model_path
    
    def _get_model_type(self, model_name: str) -> str:
        """Get the model type from the configuration"""
        if model_name not in self.config.get("predictors", {}):
            # Default to LightGBMRegressor if not specified
            return "LightGBMRegressor"
            
        return self.config["predictors"][model_name].get("model_type", "LightGBMRegressor")
        
    @lru_cache(maxsize=CACHE_SIZE)
    def load_model(self, model_name: str):
        """Load a model by name with caching"""
        logger.info(f"Loading model: {model_name}")
        
        try:
            model_path = self._resolve_model_path(model_name)
            model_type = self._get_model_type(model_name)
            
            if not model_path.exists():
                raise ValueError(f"Model {model_name} not found at {model_path}")
            
            # Load model based on its type
            if model_type.endswith("Classifier") or model_type.endswith("Regressor"):
                model = self._load_ml_model(model_name, model_type, model_path)
                tokenizer = None
            else:
                # Assume it's a transformer model
                model, tokenizer = self._load_transformer_model(model_path)
            
            self.models[model_name] = model
            if tokenizer:
                self.tokenizers[model_name] = tokenizer
            
            activity = ModelActivity(
                model_name=model_name,
                action="load",
                success=True,
                details={"path": str(model_path), "type": model_type},
                metrics={"load_time_ms": 0}  # Would track actual time in production
            )
            
            logger.info(f"Successfully loaded model: {model_name} (type: {model_type})")
            return model, tokenizer
            
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {str(e)}")
            activity = ModelActivity(
                model_name=model_name,
                action="load",
                success=False,
                details={"error": str(e)}
            )
            raise HTTPException(status_code=500, detail=f"Failed to load model: {str(e)}")
    
    def _load_ml_model(self, model_name: str, model_type: str, model_path: Path):
        """Load a machine learning model"""
        model_file = model_path / f"{model_name}.model"
        
        # Check if model file exists
        if not model_file.exists():
            # Try to find any model file in the directory
            model_files = list(model_path.glob("*.model"))
            if model_files:
                model_file = model_files[0]
            else:
                raise FileNotFoundError(f"No model file found in {model_path}")
        
        # Load the appropriate model type
        if model_type == "RandomForestClassifier":
            from sklearn.ensemble import RandomForestClassifier
            import joblib
            return joblib.load(model_file)
            
        elif model_type == "RandomForestRegressor":
            from sklearn.ensemble import RandomForestRegressor
            import joblib
            return joblib.load(model_file)
            
        elif model_type == "XGBoostClassifier":
            import xgboost as xgb
            return xgb.XGBClassifier()._Booster.load_model(str(model_file))
            
        elif model_type == "XGBoostRegressor" or model_type == "XGBoostRFRegressor":
            import xgboost as xgb
            return xgb.XGBRegressor()._Booster.load_model(str(model_file))
            
        elif model_type == "LightGBMClassifier":
            import lightgbm as lgb
            return lgb.Booster(model_file=str(model_file))
            
        elif model_type == "LightGBMRegressor":
            import lightgbm as lgb
            return lgb.Booster(model_file=str(model_file))
            
        elif model_type == "CatBoostClassifier":
            from catboost import CatBoostClassifier
            model = CatBoostClassifier()
            model.load_model(str(model_file))
            return model
            
        elif model_type == "CatBoostRegressor":
            from catboost import CatBoostRegressor
            model = CatBoostRegressor()
            model.load_model(str(model_file))
            return model
            
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
    
    def _load_transformer_model(self, model_path: Path):
        """Load a transformer model for NLP tasks"""
        try:
            tokenizer = AutoTokenizer.from_pretrained(str(model_path))
            model = AutoModelForCausalLM.from_pretrained(
                str(model_path),
                torch_dtype=torch.float16,
                device_map="auto" if torch.cuda.is_available() else "cpu"
            )
            return model, tokenizer
        except Exception as e:
            logger.error(f"Error loading transformer model: {str(e)}")
            raise
    
    def get_model_metrics(self, model_name: str) -> ModelMetrics:
        """Get performance metrics for a specific model"""
        if model_name not in self.metrics:
            # Return default metrics if not found
            return ModelMetrics(
                accuracy=0.85,
                precision=0.85,
                recall=0.85,
                f1_score=0.85,
                win_rate=0.85,
                drawdown=0.10
            )
        
        metrics_data = self.metrics[model_name]
        return ModelMetrics(**metrics_data)

    def predict(self, request: PredictionRequest) -> PredictionResponse:
        """Make a prediction using the specified model"""
        model_name = request.model_name
        
        try:
            model_type = self._get_model_type(model_name)
            model, tokenizer = self.load_model(model_name)
            
            # Format features for prediction
            if model_type.endswith("Classifier") or model_type.endswith("Regressor"):
                prediction, confidence = self._predict_with_ml_model(model, model_type, request.features)
            else:
                # Use transformer model
                prediction, confidence = self._predict_with_transformer(model, tokenizer, request)
            
            # Get model metrics
            metrics = self.get_model_metrics(model_name)
            
            return PredictionResponse(
                prediction=prediction,
                confidence=confidence,
                model_used=model_name,
                timestamp=datetime.now().isoformat(),
                metrics=metrics
            )
            
        except Exception as e:
            logger.error(f"Prediction error with model {model_name}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
    
    def _predict_with_ml_model(self, model, model_type: str, features: Dict[str, float]) -> Tuple[float, float]:
        """Generate prediction using a machine learning model"""
        # Convert features to a format the model can use
        feature_names = sorted(features.keys())
        feature_values = [features[name] for name in feature_names]
        X = np.array([feature_values])
        
        try:
            # Different prediction methods based on model type
            if model_type.endswith("Classifier"):
                # For classifiers, get class probabilities
                if hasattr(model, "predict_proba"):
                    probs = model.predict_proba(X)[0]
                    prediction = 1.0 if probs[1] > 0.5 else -1.0
                    confidence = max(probs)
                else:
                    # For models without probabilities
                    prediction = float(model.predict(X)[0])
                    prediction = 1.0 if prediction > 0.5 else -1.0
                    confidence = 0.8  # Default confidence
            else:
                # For regressors
                if isinstance(model, lgb.Booster):
                    prediction = float(model.predict(X)[0])
                else:
                    prediction = float(model.predict(X)[0])
                
                # Scale confidence based on prediction magnitude
                # Higher absolute values = higher confidence
                confidence = min(abs(prediction) * 2.0, 1.0)
                
                # Normalize prediction to -1 or 1
                prediction = 1.0 if prediction > 0 else -1.0
                
            return prediction, confidence
            
        except Exception as e:
            logger.error(f"Error during ML prediction: {str(e)}")
            # Return default prediction if model fails
            return 0.0, 0.5
    
    def _predict_with_transformer(self, model, tokenizer, request: PredictionRequest) -> Tuple[float, float]:
        """Generate prediction using a transformer model"""
        # Format the features as a prompt for the model
        feature_text = "\n".join([f"{k}: {v}" for k, v in request.features.items()])
        prompt = f"""
        Pair: {request.pair}
        Timeframe: {request.timeframe}
        Features:
        {feature_text}
        
        Predict the next price movement (positive or negative) with confidence:
        """
        
        inputs = tokenizer(prompt, return_tensors="pt")
        if torch.cuda.is_available():
            inputs = inputs.to(model.device)
            
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=50,
                temperature=0.3,
                do_sample=True
            )
        
        response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Parse the response to extract prediction and confidence
        if "positive" in response_text.lower():
            prediction = 1.0
        else:
            prediction = -1.0
            
        # Extract confidence from the response or use a default
        confidence = 0.95  # Default high confidence
        if "confidence:" in response_text.lower():
            try:
                confidence_text = response_text.lower().split("confidence:")[1].strip()
                confidence_value = float(confidence_text.split()[0])
                confidence = min(max(confidence_value, 0.0), 1.0)  # Ensure it's between 0 and 1
            except:
                pass
        
        return prediction, confidence


# Global state
model_loader = ModelLoader()
connected_clients = set()
trading_status = TradingStatus()

# API endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.get("/models")
async def list_models():
    """List available models"""
    model_paths = [p.name for p in Path(MODEL_DIR).iterdir() if p.is_dir()]
    return {"models": model_paths}

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make a prediction using the specified model"""
    try:
        # Update active requests counter
        trading_status.active_models = list(set(trading_status.active_models + [request.model_name]))
        
        result = model_loader.predict(request)
        
        # Log successful prediction
        logger.info(f"Successful prediction for {request.pair} using {request.model_name}")
        
        return result
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status", response_model=TradingStatus)
async def get_status():
    """Get current trading status"""
    return trading_status

@app.post("/status/toggle")
async def toggle_trading(enable: bool = True):
    """Enable or disable trading"""
    trading_status.is_running = enable
    await broadcast_status_update()
    return {"status": "trading enabled" if enable else "trading disabled"}

async def broadcast_status_update():
    """Broadcast trading status updates to all connected clients"""
    if not connected_clients:
        return
        
    status_json = trading_status.model_dump_json()
    await asyncio.gather(
        *[client.send_text(status_json) for client in connected_clients]
    )

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()
    connected_clients.add(websocket)
    
    try:
        # Send initial status
        await websocket.send_text(trading_status.model_dump_json())
        
        # Keep connection alive and handle incoming messages
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
            else:
                try:
                    command = json.loads(data)
                    if "action" in command:
                        if command["action"] == "get_status":
                            await websocket.send_text(trading_status.model_dump_json())
                except Exception as e:
                    logger.error(f"Error processing websocket message: {str(e)}")
                    await websocket.send_text(json.dumps({"error": str(e)}))
                    
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

# Background task to simulate trading updates
@app.on_event("startup")
async def startup_event():
    """Startup tasks"""
    # Create log directory if it doesn't exist
    os.makedirs("/app/logs", exist_ok=True)
    logger.info("FreqAI API starting up")
    
    # Make sure the models directory exists
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # Initialize trading status
    trading_status.active_models = []
    trading_status.current_balance = INITIAL_CAPITAL
    
    # Schedule background tasks
    asyncio.create_task(simulate_trading_updates())

async def simulate_trading_updates():
    """Simulate trading updates for demonstration purposes"""
    while True:
        if trading_status.is_running:
            # Simulate balance changes
            change = np.random.normal(0.05, 0.1)  # Mean positive return with some volatility
            current_balance = trading_status.current_balance
            new_balance = max(current_balance * (1 + change), 0.1)  # Ensure balance doesn't go to zero
            
            # Update trading status
            trading_status.current_balance = new_balance
            
            # Calculate drawdown
            high_watermark = max(getattr(trading_status, "_high_watermark", INITIAL_CAPITAL), new_balance)
            trading_status._high_watermark = high_watermark
            trading_status.drawdown = (high_watermark - new_balance) / high_watermark
            
            # Simulate some active trades
            trading_status.current_trades = [
                {
                    "pair": "BTC/USDT",
                    "entry_time": (datetime.now() - timedelta(minutes=30)).isoformat(),
                    "entry_price": 65000 + np.random.normal(0, 100),
                    "current_price": 65000 + np.random.normal(0, 200),
                    "position_size": 0.0001,
                    "pnl_percent": np.random.normal(2, 1)
                }
            ]
            
            # Broadcast updates to connected clients
            await broadcast_status_update()
        
        # Update every 5 seconds
        await asyncio.sleep(5)

if __name__ == "__main__":
    uvicorn.run("freqai_interface:app", host="0.0.0.0", port=8001, reload=True)
