"""
AlgoTradePro5 Risk Management Module
==================================

CRITICAL REQUIREMENTS:
- Maximum 2% risk per trade
- Maximum 10% drawdown
- 85% minimum win rate
- Quantum validation required
- Initial capital £10

VALIDATION GATES:
1. Position sizing
2. Stop loss levels
3. Portfolio risk
4. Win rate tracking

Author: GitHub Copilot
Last Updated: 2025-03-12
"""

import logging
from typing import Dict, List, Optional, Tuple, Union
from datetime import datetime
import pandas as pd
import numpy as np
from pathlib import Path

from freqtrade.persistence import Trade
from config_manager import get_config
from error_manager import ErrorManager, ErrorSeverity

logger = logging.getLogger(__name__)

class RiskManager:
    """Manages all trading risk parameters and validation"""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize risk management with strict validation"""
        self.config = config or get_config()
        self.error_manager = ErrorManager()
        
        # Load trading configuration
        trading_config = self.config['trading_config']
        self.max_risk_per_trade = trading_config.get('max_risk_per_trade', 0.02)
        self.max_drawdown = trading_config.get('max_drawdown', 0.10)
        self.win_rate_threshold = trading_config.get('win_rate_threshold', 0.85)
        self.warning_win_rate = trading_config.get('warning_win_rate', 0.87)
        
        # State tracking
        self.initial_capital = 10.0  # £10 initial capital (locked)
        self.current_drawdown = 0.0
        self.trading_enabled = True
        self.quantum_validated = False
        self.trade_history: List[Dict] = []
        
        logger.info("Risk Manager initialized with strict validation")
        
    def calculate_kelly_position(self, win_rate: float, win_loss_ratio: float) -> float:
        """
        Calculate position size using Kelly Criterion
        f* = p - (1-p)/b where:
        p = probability of win
        b = win/loss ratio
        """
        if win_rate <= 0 or win_loss_ratio <= 0:
            return 0.0
        
        kelly_fraction = win_rate - (1 - win_rate) / win_loss_ratio
        # Limit to max 2% risk
        return min(kelly_fraction, self.max_risk_per_trade)
        
    def calculate_fixed_fractional_size(self, current_capital: float) -> float:
        """Calculate position size using fixed fractional method"""
        return current_capital * self.max_risk_per_trade
        
    def calculate_stop_loss(self, 
                          entry_price: float, 
                          current_price: float,
                          atr: Optional[float] = None) -> Tuple[float, str]:
        """
        Calculate stop loss price using various methods
        Returns: (stop_loss_price, method_used)
        """
        # Fixed stop loss (2% below entry)
        fixed_stop = entry_price * 0.98
        
        # Trailing stop (2% below current price)
        trailing_stop = current_price * 0.98
        
        # Volatility-based stop if ATR provided
        if atr is not None:
            volatility_stop = current_price - (2 * atr)
            # Use the highest (most conservative) stop loss
            return max(fixed_stop, trailing_stop, volatility_stop), "volatility"
            
        # Default to the higher of fixed/trailing
        return max(fixed_stop, trailing_stop), "trailing"
        
    def update_drawdown(self, current_capital: float) -> None:
        """
        Update current drawdown and check against limits
        """
        drawdown = (self.initial_capital - current_capital) / self.initial_capital
        self.current_drawdown = max(self.current_drawdown, drawdown)
        
        if self.current_drawdown >= self.max_drawdown:
            logger.warning(f"Maximum drawdown reached: {self.current_drawdown:.2%}")
            self._trigger_emergency_stop()
            self.error_manager.log_error(
                "Maximum drawdown limit reached",
                ErrorSeverity.HIGH.value,
                "RiskManagement"
            )
            
    def check_trade_risk(self, trade: Trade) -> bool:
        """
        Verify if a trade meets risk management criteria
        """
        # Check if trading is allowed
        if not self.trading_enabled:
            logger.warning("Trading is currently disabled due to risk limits")
            return False
            
        # Check win rate requirement
        current_win_rate = self.calculate_win_rate()
        if current_win_rate < self.win_rate_threshold:
            logger.warning(f"Current win rate {current_win_rate:.2%} below threshold {self.win_rate_threshold:.2%}")
            return False
            
        # Verify quantum loop validation
        if not self.quantum_validated:
            logger.warning("Trade not validated by quantum loop backtesting")
            return False
            
        # Verify position size
        if trade.stake_amount > self.calculate_fixed_fractional_size(trade.stake_amount):
            logger.warning(f"Trade size {trade.stake_amount} exceeds risk limits")
            return False
            
        return True
        
    def check_portfolio_risk(self, positions: List[Dict]) -> bool:
        """
        Validate overall portfolio risk exposure
        """
        total_risk = sum(p.get('risk_amount', 0.0) for p in positions)
        portfolio_risk = total_risk / self.initial_capital
        
        # Allow up to 2x single position risk for portfolio
        if portfolio_risk > self.max_risk_per_trade * 2:
            logger.warning(f"Portfolio risk {portfolio_risk:.2%} exceeds limits")
            return False
            
        return True
        
    def _trigger_emergency_stop(self) -> None:
        """
        Handle emergency stop when risk limits are breached
        """
        logger.error("EMERGENCY STOP TRIGGERED - Risk limits exceeded")
        self.trading_enabled = False
        self.error_manager.log_error(
            "Emergency stop triggered",
            ErrorSeverity.CRITICAL.value,
            "RiskManagement"
        )
        
    def reset_risk_state(self) -> None:
        """
        Reset risk management state (requires manual intervention)
        """
        self.current_drawdown = 0.0
        self.trading_enabled = True
        logger.info("Risk management state has been reset")
        
    def get_risk_metrics(self) -> Dict:
        """
        Return current risk metrics for monitoring
        """
        return {
            "current_drawdown": self.current_drawdown,
            "trading_enabled": self.trading_enabled,
            "max_risk_per_trade": self.max_risk_per_trade,
            "max_drawdown_limit": self.max_drawdown,
            "current_win_rate": self.calculate_win_rate(),
            "win_rate_threshold": self.win_rate_threshold,
            "quantum_validated": self.quantum_validated,
            "initial_capital": self.initial_capital,
            "trade_count": len(self.trade_history)
        }
        
    def update_trade_history(self, trade: Trade, is_win: bool) -> None:
        """
        Update trade history with new trade result
        """
        self.trade_history.append({
            "trade": trade,
            "is_win": is_win,
            "timestamp": datetime.now().isoformat()
        })
        # Keep only last 100 trades to prevent memory bloat
        if len(self.trade_history) > 100:
            self.trade_history.pop(0)
            
    def calculate_win_rate(self) -> float:
        """
        Calculate current win rate from trade history
        """
        if not self.trade_history:
            return 0.0
        wins = sum(1 for trade in self.trade_history if trade["is_win"])
        return wins / len(self.trade_history)
        
    def set_quantum_validation(self, validated: bool) -> None:
        """
        Update quantum validation status
        """
        self.quantum_validated = validated
        logger.info(f"Quantum validation status updated to: {validated}")
        
# Create global instance
_risk_manager = RiskManager()

def get_risk_manager() -> RiskManager:
    """Global function to get risk manager instance"""
    return _risk_manager