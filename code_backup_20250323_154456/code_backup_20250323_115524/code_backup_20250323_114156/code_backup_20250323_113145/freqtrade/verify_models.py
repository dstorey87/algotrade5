#!/usr/bin/env python
import os
import sys
import logging
from pathlib import Path
from freqtrade.configuration import Configuration
from freqtrade.resolvers import StrategyResolver
from user_data.freqaimodels.LLMPredictor import LLMPredictor
from user_data.freqaimodels.prediction_models import DeepSeekV2Model, MistralTradingModel, DBRXFinanceModel

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def verify_models():
    try:
        # Verify model directory structure inside container
        model_paths = {
            'LLM Models': {
                'base': '/freqtrade/aimodels/llm_models',
                'models': ['deepseek', 'mistral', 'qwen']
            },
            'ML Models': {
                'base': '/freqtrade/aimodels/ml_models',
                'models': ['deepseek', 'mistral', 'dbrx']
            }
        }
        
        # Check base directories and model subdirectories
        for category, paths in model_paths.items():
            base_path = Path(paths['base'])
            logger.info(f"Checking {category} at {base_path}")
            
            if not base_path.exists():
                logger.error(f"{category} base path not found: {base_path}")
                return False
                
            for model in paths['models']:
                model_path = base_path / model
                placeholder = model_path / '.placeholder'
                
                if not model_path.exists():
                    logger.error(f"{category} - {model} path not found: {model_path}")
                    return False
                if not placeholder.exists():
                    logger.warning(f"{category} - {model} placeholder missing: {placeholder}")
                
                logger.info(f"{category} - {model} directory verified: {model_path}")
            
        logger.info("Model paths verified")

        # Test loading each model
        models = {
            'DeepSeekV2': DeepSeekV2Model(),
            'MistralTrading': MistralTradingModel(),
            'DBRX': DBRXFinanceModel(),
            'LLM': LLMPredictor()
        }

        for name, model in models.items():
            try:
                logger.info(f"Initializing {name}")
                if hasattr(model, 'load_model'):
                    model.load_model("/freqtrade/aimodels")
                logger.info(f"{name} initialized successfully")
            except Exception as e:
                logger.error(f"Error initializing {name}: {e}")
                return False

        logger.info("All models verified successfully")
        return True

    except Exception as e:
        logger.error(f"Verification failed: {e}")
        return False

if __name__ == "__main__":
    try:
        logger.info("Starting model verification...")
        success = verify_models()
        if success:
            logger.info("Model verification completed successfully")
            sys.exit(0)
        else:
            logger.error("Model verification failed")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Error during verification: {e}")
        sys.exit(1)
