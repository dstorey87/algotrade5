#!/usr/bin/env python3
"""Error management system for AlgoTradPro5"""
import logging
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Dict, Optional, Union
import json

logger = logging.getLogger(__name__)

class ErrorLevel(Enum):
    """Error severity levels"""
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()

class ErrorCode(Enum):
    """System error codes"""
    # AI/ML Errors
    MODEL_LOAD_ERROR = auto()
    MODEL_INFERENCE_ERROR = auto()
    MODEL_CONFIDENCE_ERROR = auto()
    MODEL_NOT_FOUND = auto()
    
    # Trading Errors
    TRADE_EXECUTION_ERROR = auto()
    INSUFFICIENT_CONFIDENCE = auto()
    POSITION_SIZE_ERROR = auto()
    RISK_LIMIT_ERROR = auto()
    
    # System Errors
    DATABASE_ERROR = auto()
    CONFIG_ERROR = auto()
    FREQTRADE_ERROR = auto()
    BACKTEST_ERROR = auto()
    BACKTEST_EXECUTION_ERROR = auto()

class ErrorManager:
    """Manages system errors and FreqTrade integration"""
    
    def __init__(self):
        self._initialize_logging()
        self.error_counts = {level: 0 for level in ErrorLevel}
        self.error_history = []
        self.trading_enabled = True
        self.min_confidence_threshold = 0.75  # 75% minimum confidence

    def _initialize_logging(self):
        """Initialize error logging"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        handler = logging.FileHandler(log_dir / "error_manager.log")
        handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        logger.addHandler(handler)

    def log_error(self, 
                 code: ErrorCode, 
                 message: str, 
                 level: ErrorLevel,
                 metadata: Optional[Dict] = None) -> bool:
        """Log error and handle system response"""
        try:
            # Record error
            error_data = {
                'timestamp': datetime.now().isoformat(),
                'code': code.name,
                'message': message,
                'level': level.name,
                'metadata': metadata or {}
            }
            
            # Update counts and history
            self.error_counts[level] += 1
            self.error_history.append(error_data)
            
            # Log error
            logger.error(f"{code.name}: {message}")
            
            # Handle critical AI/ML errors
            if self._is_ai_ml_error(code):
                self._handle_ai_ml_error(error_data)
            
            # Update FreqTrade UI
            self._update_freqtrade_status(error_data)
            
            return True

        except Exception as e:
            logger.critical(f"Error in error manager: {str(e)}")
            return False

    def _is_ai_ml_error(self, code: ErrorCode) -> bool:
        """Check if error is AI/ML related"""
        return code in [
            ErrorCode.MODEL_LOAD_ERROR,
            ErrorCode.MODEL_INFERENCE_ERROR,
            ErrorCode.MODEL_CONFIDENCE_ERROR,
            ErrorCode.MODEL_NOT_FOUND
        ]

    def _handle_ai_ml_error(self, error_data: Dict):
        """Handle AI/ML errors with graceful degradation"""
        try:
            # Disable trading if AI/ML system is not functioning
            self.trading_enabled = False
            
            # Log critical error
            logger.critical(
                f"AI/ML system failure: {error_data['code']} - {error_data['message']}"
            )
            
            # Notify FreqTrade
            self._update_freqtrade_status({
                'type': 'error',
                'message': 'AI/ML system disabled - Trading suspended',
                'code': error_data['code'],
                'level': 'CRITICAL'
            })
            
            # Write error state to disk
            self._save_error_state(error_data)

        except Exception as e:
            logger.critical(f"Error handling AI/ML failure: {str(e)}")

    def check_model_confidence(self, confidence: float) -> Union[bool, Dict]:
        """Validate model confidence meets minimum threshold"""
        if confidence < self.min_confidence_threshold:
            error_data = {
                'code': ErrorCode.INSUFFICIENT_CONFIDENCE,
                'message': f'Model confidence {confidence:.2%} below minimum threshold {self.min_confidence_threshold:.2%}',
                'level': ErrorLevel.WARNING,
                'metadata': {
                    'confidence': confidence,
                    'threshold': self.min_confidence_threshold
                }
            }
            
            self.log_error(
                ErrorCode.INSUFFICIENT_CONFIDENCE,
                error_data['message'],
                ErrorLevel.WARNING,
                error_data['metadata']
            )
            
            return {
                'valid': False,
                'error': error_data
            }
            
        return {
            'valid': True,
            'confidence': confidence
        }

    def _update_freqtrade_status(self, message: Dict):
        """Update FreqTrade UI with error status"""
        try:
            from freqtrade.rpc import RPCManager
            
            # Format message for FreqTrade
            ft_message = {
                'type': 'status',
                'status': 'error',
                'error': message.get('message', ''),
                'code': message.get('code', 'UNKNOWN'),
                'level': message.get('level', 'ERROR')
            }
            
            # Add trading status
            if not self.trading_enabled:
                ft_message['trading_disabled'] = True
                ft_message['reason'] = 'AI/ML system failure'
            
            # Send to FreqTrade
            rpc = RPCManager({"bot_name": "AlgoTradPro5"})
            rpc.send_msg(ft_message)

        except Exception as e:
            logger.error(f"Error updating FreqTrade status: {str(e)}")

    def _save_error_state(self, error_data: Dict):
        """Save error state to disk"""
        try:
            state_file = Path("data/error_state.json")
            state_file.parent.mkdir(exist_ok=True)
            
            state = {
                'timestamp': datetime.now().isoformat(),
                'trading_enabled': self.trading_enabled,
                'last_error': error_data,
                'error_counts': {k.name: v for k, v in self.error_counts.items()},
                'recent_history': self.error_history[-10:]  # Last 10 errors
            }
            
            with open(state_file, 'w') as f:
                json.dump(state, f, indent=2)

        except Exception as e:
            logger.error(f"Error saving error state: {str(e)}")

    def get_error_summary(self) -> Dict:
        """Get summary of error status"""
        return {
            'trading_enabled': self.trading_enabled,
            'error_counts': {k.name: v for k, v in self.error_counts.items()},
            'recent_errors': self.error_history[-5:],  # Last 5 errors
            'ai_ml_status': 'operational' if self.trading_enabled else 'disabled'
        }

    def reset_error_state(self) -> bool:
        """Reset error state after recovery"""
        try:
            self.error_counts = {level: 0 for level in ErrorLevel}
            self.error_history = []
            self.trading_enabled = True
            
            # Update FreqTrade
            self._update_freqtrade_status({
                'type': 'status',
                'status': 'operational',
                'message': 'Error state reset - System operational',
                'level': 'INFO'
            })
            
            # Clear error state file
            state_file = Path("data/error_state.json")
            if state_file.exists():
                state_file.unlink()
            
            return True

        except Exception as e:
            logger.error(f"Error resetting error state: {str(e)}")
            return False

if __name__ == "__main__":
    # Test error manager
    error_manager = ErrorManager()
    
    # Test AI/ML error handling
    error_manager.log_error(
        ErrorCode.MODEL_LOAD_ERROR,
        "Failed to load AI model",
        ErrorLevel.CRITICAL,
        {'model': 'deep_learning_v1'}
    )
    
    # Test confidence check
    result = error_manager.check_model_confidence(0.6)  # Below 75% threshold
    print(f"Confidence check result: {result}")
    
    # Get error summary
    summary = error_manager.get_error_summary()
    print(f"Error summary: {json.dumps(summary, indent=2)}")