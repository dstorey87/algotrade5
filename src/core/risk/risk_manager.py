"""
Risk Manager
===========

Enforces position sizing and risk control.

REQUIREMENTS:
- Max 1-2% risk per trade (£0.10 - £0.20 on £10)
- Kelly Criterion implementation
- Hard stop at 10% drawdown
- Continuous monitoring
"""

from typing import Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging
import numpy as np
from pathlib import Path
import json

logger = logging.getLogger(__name__)

@dataclass
class RiskMetrics:
    """Risk assessment metrics"""
    position_size: float
    risk_amount: float
    kelly_fraction: float
    current_drawdown: float
    max_allowed_loss: float
    risk_reward_ratio: float
    timestamp: str

class RiskManager:
    def __init__(self, config: Dict):
        """Initialize risk manager"""
        self.config = config
        self.base_path = Path(config.get('base_path', 'C:/AlgoTradPro5'))
        
        # Initial capital
        self.initial_capital = config.get('initial_capital', 10.0)
        self.current_capital = self.initial_capital
        
        # Risk limits
        self.max_risk_per_trade = config.get('max_risk_per_trade', 0.02)
        self.max_drawdown = config.get('max_drawdown', 0.10)
        self.min_win_rate = config.get('min_win_rate', 0.85)
        
        # Kelly Criterion parameters
        self.kelly_fraction = config.get('kelly_fraction', 0.5)  # Half-Kelly for safety
        
        # Position tracking
        self.open_positions: Dict[str, Dict] = {}
        self.position_history: List[Dict] = []
        
        # State tracking
        self.peak_capital = self.initial_capital
        self.current_drawdown = 0.0
        self.trading_allowed = True
        
        # TODO: Add dynamic risk adjustment
        # TODO: Implement position correlation analysis
        # TODO: Add volatility-based position sizing
        
    def calculate_position_size(self,
                              symbol: str,
                              entry_price: float,
                              stop_loss: float,
                              win_rate: float,
                              reward_ratio: float) -> RiskMetrics:
        """
        Calculate allowed position size with Kelly Criterion
        
        Args:
            symbol: Trading pair symbol
            entry_price: Planned entry price
            stop_loss: Stop loss price
            win_rate: Expected win rate
            reward_ratio: Risk/reward ratio
            
        Returns:
            RiskMetrics with position details
        """
        if not self.trading_allowed:
            logger.warning("Trading halted due to risk limits")
            return self._create_zero_position()
            
        # Calculate Kelly Criterion
        kelly_f = self._calculate_kelly(win_rate, reward_ratio)
        
        # Apply safety fraction
        kelly_f *= self.kelly_fraction
        
        # Calculate maximum position size
        max_risk_amount = self.current_capital * self.max_risk_per_trade
        
        # Calculate position size based on stop loss
        risk_per_unit = abs(entry_price - stop_loss)
        if risk_per_unit == 0:
            logger.error("Invalid stop loss - equal to entry price")
            return self._create_zero_position()
            
        # Use the smaller of Kelly and max risk
        risk_amount = min(
            kelly_f * self.current_capital,
            max_risk_amount
        )
        
        position_size = risk_amount / risk_per_unit
        
        # Create metrics
        metrics = RiskMetrics(
            position_size=position_size,
            risk_amount=risk_amount,
            kelly_fraction=kelly_f,
            current_drawdown=self.current_drawdown,
            max_allowed_loss=max_risk_amount,
            risk_reward_ratio=reward_ratio,
            timestamp=datetime.now().isoformat()
        )
        
        # Log position details
        logger.info(
            f"Position sizing for {symbol}: "
            f"size={position_size:.4f}, "
            f"risk={risk_amount:.2f} ({(risk_amount/self.current_capital)*100:.1f}%)"
        )
        
        return metrics
        
    def update_position(self,
                       symbol: str,
                       current_price: float,
                       pnl: float,
                       timestamp: Optional[str] = None):
        """Update position and check risk limits"""
        if symbol in self.open_positions:
            position = self.open_positions[symbol]
            position['current_price'] = current_price
            position['pnl'] = pnl
            position['last_update'] = timestamp or datetime.now().isoformat()
            
            # Update capital
            self.current_capital += pnl
            
            # Update peak capital
            if self.current_capital > self.peak_capital:
                self.peak_capital = self.current_capital
                
            # Calculate drawdown
            self.current_drawdown = (
                (self.peak_capital - self.current_capital) / self.peak_capital
            )
            
            # Check drawdown limit
            if self.current_drawdown >= self.max_drawdown:
                self._halt_trading(
                    f"Maximum drawdown reached: {self.current_drawdown:.1%}"
                )
                
    def close_position(self, symbol: str, final_pnl: float):
        """Close position and update history"""
        if symbol in self.open_positions:
            position = self.open_positions.pop(symbol)
            position['final_pnl'] = final_pnl
            position['close_time'] = datetime.now().isoformat()
            
            self.position_history.append(position)
            self._save_position_history()
            
    def _calculate_kelly(self, win_rate: float, reward_ratio: float) -> float:
        """Calculate Kelly Criterion fraction"""
        # f* = p - (1-p)/b where:
        # f* = Kelly fraction
        # p = probability of win
        # b = win/loss ratio
        
        if win_rate < self.min_win_rate:
            logger.warning(
                f"Win rate {win_rate:.1%} below minimum {self.min_win_rate:.1%}"
            )
            return 0.0
            
        kelly_f = win_rate - (1 - win_rate) / reward_ratio
        
        # Kelly can be negative - in that case don't trade
        return max(0, kelly_f)
        
    def _create_zero_position(self) -> RiskMetrics:
        """Create metrics for zero position size"""
        return RiskMetrics(
            position_size=0.0,
            risk_amount=0.0,
            kelly_fraction=0.0,
            current_drawdown=self.current_drawdown,
            max_allowed_loss=0.0,
            risk_reward_ratio=0.0,
            timestamp=datetime.now().isoformat()
        )
        
    def _halt_trading(self, reason: str):
        """Halt trading and log reason"""
        self.trading_allowed = False
        logger.error(f"Trading halted: {reason}")
        
        # Save halt state
        halt_path = self.base_path / 'risk' / 'trading_halt.json'
        halt_path.parent.mkdir(parents=True, exist_ok=True)
        
        halt_state = {
            'timestamp': datetime.now().isoformat(),
            'reason': reason,
            'metrics': {
                'current_capital': self.current_capital,
                'peak_capital': self.peak_capital,
                'drawdown': self.current_drawdown
            }
        }
        
        with open(halt_path, 'w') as f:
            json.dump(halt_state, f, indent=2)
            
    def _save_position_history(self):
        """Save position history to file"""
        history_path = self.base_path / 'risk' / 'position_history.json'
        history_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(history_path, 'w') as f:
            json.dump(self.position_history, f, indent=2)
            
    def get_risk_metrics(self) -> Dict[str, float]:
        """Get current risk metrics"""
        return {
            'current_capital': self.current_capital,
            'peak_capital': self.peak_capital,
            'drawdown': self.current_drawdown,
            'open_positions': len(self.open_positions),
            'total_positions': len(self.position_history),
            'win_rate': self._calculate_win_rate(),
            'trading_allowed': self.trading_allowed
        }
        
    def _calculate_win_rate(self) -> float:
        """Calculate historical win rate"""
        if not self.position_history:
            return 0.0
            
        wins = sum(1 for p in self.position_history if p['final_pnl'] > 0)
        return wins / len(self.position_history)