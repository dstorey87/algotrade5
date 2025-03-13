"""
Risk Manager
===========

Handles all risk management aspects including:
- Position sizing
- Stop loss management
- Drawdown monitoring
- Capital allocation

Author: GitHub Copilot
Last Updated: 2025-03-12
"""

import logging
from typing import Dict, Optional, Tuple
from enum import Enum
from pathlib import Path
import sqlite3
from datetime import datetime
import json

from error_manager import ErrorManager, ErrorSeverity

logger = logging.getLogger(__name__)

class RiskLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class RiskManager:
    def __init__(self, initial_capital: float = 10.0):
        """Initialize risk manager with initial capital"""
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.error_manager = ErrorManager()
        
        # Risk limits
        self.max_position_size = 0.02  # 2% max per trade
        self.max_drawdown = 0.10      # 10% max drawdown
        self.trailing_stop_pct = 0.02  # 2% trailing stop
        
        # Current state
        self.open_positions: Dict = {}
        self.drawdown_high = initial_capital
        
    def calculate_position_size(self, price: float, risk_level: RiskLevel) -> float:
        """Calculate safe position size based on risk level"""
        try:
            # Base position size on Kelly Criterion
            win_rate = self._get_strategy_win_rate()
            win_loss_ratio = self._get_win_loss_ratio()
            
            kelly_fraction = win_rate - ((1 - win_rate) / win_loss_ratio)
            kelly_fraction = min(kelly_fraction, self.max_position_size)
            
            # Adjust for risk level
            risk_multiplier = {
                RiskLevel.LOW: 0.5,
                RiskLevel.MEDIUM: 0.75,
                RiskLevel.HIGH: 1.0,
                RiskLevel.CRITICAL: 0.25  # Reduce size on critical risk
            }
            
            position_size = self.current_capital * kelly_fraction * risk_multiplier[risk_level]
            
            # Ensure position size doesn't exceed limits
            max_allowed = self.current_capital * self.max_position_size
            return min(position_size, max_allowed)
            
        except Exception as e:
            self.error_manager.log_error(
                f"Position size calculation failed: {str(e)}",
                ErrorSeverity.HIGH.value,
                "RiskManager"
            )
            return 0.0
            
    def update_position(self, symbol: str, quantity: float, price: float) -> bool:
        """Update or create a position"""
        try:
            if symbol in self.open_positions:
                self.open_positions[symbol].update({
                    'quantity': quantity,
                    'current_price': price,
                    'last_updated': datetime.now().isoformat()
                })
            else:
                self.open_positions[symbol] = {
                    'quantity': quantity,
                    'entry_price': price,
                    'current_price': price,
                    'high_price': price,
                    'stop_loss': price * (1 - self.trailing_stop_pct),
                    'created_at': datetime.now().isoformat(),
                    'last_updated': datetime.now().isoformat()
                }
            return True
            
        except Exception as e:
            self.error_manager.log_error(
                f"Position update failed: {str(e)}",
                ErrorSeverity.HIGH.value,
                "RiskManager"
            )
            return False
            
    def check_stop_loss(self, symbol: str, current_price: float) -> Tuple[bool, str]:
        """Check if stop loss is triggered"""
        try:
            if symbol not in self.open_positions:
                return False, "Position not found"
                
            position = self.open_positions[symbol]
            
            # Update high price if needed
            if current_price > position['high_price']:
                position['high_price'] = current_price
                # Update trailing stop
                position['stop_loss'] = current_price * (1 - self.trailing_stop_pct)
                
            # Check stop loss
            if current_price <= position['stop_loss']:
                return True, "Stop loss triggered"
                
            return False, "Position within limits"
            
        except Exception as e:
            self.error_manager.log_error(
                f"Stop loss check failed: {str(e)}",
                ErrorSeverity.HIGH.value,
                "RiskManager"
            )
            return True, f"Error checking stop loss: {str(e)}"
            
    def update_capital(self, new_capital: float) -> bool:
        """Update current capital and check drawdown"""
        try:
            self.current_capital = new_capital
            
            # Update drawdown high water mark
            if new_capital > self.drawdown_high:
                self.drawdown_high = new_capital
                
            # Calculate current drawdown
            drawdown = (self.drawdown_high - new_capital) / self.drawdown_high
            
            # Check max drawdown
            if drawdown > self.max_drawdown:
                self.error_manager.log_error(
                    f"Max drawdown exceeded: {drawdown:.2%}",
                    ErrorSeverity.HIGH.value,
                    "RiskManager"
                )
                return False
                
            return True
            
        except Exception as e:
            self.error_manager.log_error(
                f"Capital update failed: {str(e)}",
                ErrorSeverity.HIGH.value,
                "RiskManager"
            )
            return False
            
    def _get_strategy_win_rate(self) -> float:
        """Get current strategy win rate from database"""
        try:
            data_path = Path.home() / "AlgoTradPro5" / "data"
            db_path = data_path / "analysis.db"
            
            with sqlite3.connect(db_path) as conn:
                c = conn.cursor()
                c.execute("""
                    SELECT 
                        COUNT(CASE WHEN profit > 0 THEN 1 END) * 1.0 / COUNT(*) as win_rate
                    FROM trades 
                    WHERE closed_at > datetime('now', '-7 days')
                """)
                win_rate = c.fetchone()[0] or 0.5  # Default to 0.5 if no data
                
            return float(win_rate)
            
        except Exception as e:
            logger.error(f"Failed to get win rate: {e}")
            return 0.5  # Conservative default
            
    def _get_win_loss_ratio(self) -> float:
        """Get current win/loss ratio from database"""
        try:
            data_path = Path.home() / "AlgoTradPro5" / "data"
            db_path = data_path / "analysis.db"
            
            with sqlite3.connect(db_path) as conn:
                c = conn.cursor()
                c.execute("""
                    SELECT 
                        ABS(AVG(CASE WHEN profit > 0 THEN profit END) / 
                        AVG(CASE WHEN profit < 0 THEN profit END)) as win_loss_ratio
                    FROM trades 
                    WHERE closed_at > datetime('now', '-7 days')
                """)
                ratio = c.fetchone()[0] or 1.0  # Default to 1.0 if no data
                
            return float(ratio)
            
        except Exception as e:
            logger.error(f"Failed to get win/loss ratio: {e}")
            return 1.0  # Conservative default
            
    def get_risk_metrics(self) -> Dict:
        """Get current risk metrics"""
        try:
            return {
                'current_capital': self.current_capital,
                'drawdown': (self.drawdown_high - self.current_capital) / self.drawdown_high,
                'open_positions': len(self.open_positions),
                'win_rate': self._get_strategy_win_rate(),
                'win_loss_ratio': self._get_win_loss_ratio(),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get risk metrics: {e}")
            return {}