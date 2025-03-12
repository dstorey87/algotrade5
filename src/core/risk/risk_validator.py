"""
Risk Validator
=============

Validates risk management system operations and constraints.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """Represents a risk validation check result"""
    check_name: str
    passed: bool
    details: str
    timestamp: str
    metrics: Dict

class RiskValidator:
    def __init__(self, config: Dict):
        self.config = config
        self.base_path = Path(config.get('base_path', 'C:/AlgoTradPro5'))
        
        # Validation thresholds
        self.max_allowed_risk = config.get('max_risk_per_trade', 0.02)
        self.max_allowed_drawdown = config.get('max_drawdown', 0.10)
        self.min_required_win_rate = config.get('min_win_rate', 0.85)
        
        # Validation history
        self.validation_history: List[ValidationResult] = []
        
        # TODO: Add correlation validation between positions
        # TODO: Add volatility-based risk adjustments
        # TODO: Implement portfolio-wide risk validation
        
    def validate_position_risk(self, 
                             position_size: float,
                             account_size: float,
                             stop_loss: float,
                             take_profit: float) -> ValidationResult:
        """
        Validate position risk parameters
        
        Args:
            position_size: Size of the position
            account_size: Current account size
            stop_loss: Stop loss price
            take_profit: Take profit price
            
        Returns:
            ValidationResult with check details
        """
        # Calculate risk amount
        risk_amount = position_size * abs(stop_loss)
        risk_percentage = risk_amount / account_size
        
        # Calculate reward ratio
        reward_amount = position_size * abs(take_profit)
        risk_reward_ratio = reward_amount / risk_amount if risk_amount > 0 else 0
        
        # Validate risk percentage
        if risk_percentage > self.max_allowed_risk:
            result = ValidationResult(
                check_name="position_risk",
                passed=False,
                details=f"Risk {risk_percentage:.1%} exceeds max {self.max_allowed_risk:.1%}",
                timestamp=datetime.now().isoformat(),
                metrics={
                    'risk_amount': risk_amount,
                    'risk_percentage': risk_percentage,
                    'risk_reward_ratio': risk_reward_ratio
                }
            )
        else:
            result = ValidationResult(
                check_name="position_risk",
                passed=True,
                details=f"Risk {risk_percentage:.1%} within limits",
                timestamp=datetime.now().isoformat(),
                metrics={
                    'risk_amount': risk_amount,
                    'risk_percentage': risk_percentage,
                    'risk_reward_ratio': risk_reward_ratio
                }
            )
            
        self.validation_history.append(result)
        return result
        
    def validate_drawdown(self,
                         current_drawdown: float,
                         peak_capital: float,
                         current_capital: float) -> ValidationResult:
        """Validate current drawdown against limits"""
        
        if current_drawdown >= self.max_allowed_drawdown:
            result = ValidationResult(
                check_name="drawdown",
                passed=False,
                details=f"Drawdown {current_drawdown:.1%} exceeds max {self.max_allowed_drawdown:.1%}",
                timestamp=datetime.now().isoformat(),
                metrics={
                    'current_drawdown': current_drawdown,
                    'peak_capital': peak_capital,
                    'current_capital': current_capital
                }
            )
        else:
            result = ValidationResult(
                check_name="drawdown",
                passed=True,
                details=f"Drawdown {current_drawdown:.1%} within limits",
                timestamp=datetime.now().isoformat(),
                metrics={
                    'current_drawdown': current_drawdown,
                    'peak_capital': peak_capital,
                    'current_capital': current_capital
                }
            )
            
        self.validation_history.append(result)
        return result
        
    def validate_win_rate(self,
                         wins: int,
                         total_trades: int,
                         window_size: Optional[int] = None) -> ValidationResult:
        """
        Validate win rate meets minimum requirements
        
        Args:
            wins: Number of winning trades
            total_trades: Total number of trades
            window_size: Optional window size for rolling win rate
        """
        if total_trades == 0:
            win_rate = 0.0
        else:
            win_rate = wins / total_trades
            
        if win_rate < self.min_required_win_rate:
            result = ValidationResult(
                check_name="win_rate",
                passed=False,
                details=(
                    f"Win rate {win_rate:.1%} below minimum "
                    f"{self.min_required_win_rate:.1%}"
                ),
                timestamp=datetime.now().isoformat(),
                metrics={
                    'win_rate': win_rate,
                    'wins': wins,
                    'total_trades': total_trades,
                    'window_size': window_size
                }
            )
        else:
            result = ValidationResult(
                check_name="win_rate", 
                passed=True,
                details=f"Win rate {win_rate:.1%} meets minimum requirement",
                timestamp=datetime.now().isoformat(),
                metrics={
                    'win_rate': win_rate,
                    'wins': wins,
                    'total_trades': total_trades,
                    'window_size': window_size
                }
            )
            
        self.validation_history.append(result)
        return result
        
    def validate_portfolio_risk(self,
                              positions: List[Dict],
                              account_size: float) -> ValidationResult:
        """Validate overall portfolio risk"""
        # Calculate total risk exposure
        total_risk = sum(
            p['risk_amount'] for p in positions if p['risk_amount'] > 0
        )
        portfolio_risk = total_risk / account_size
        
        # Get position correlations
        # TODO: Implement position correlation analysis
        
        if portfolio_risk > self.max_allowed_risk * 2:  # Allow 2x for portfolio
            result = ValidationResult(
                check_name="portfolio_risk",
                passed=False,
                details=(
                    f"Portfolio risk {portfolio_risk:.1%} exceeds "
                    f"maximum {self.max_allowed_risk*2:.1%}"
                ),
                timestamp=datetime.now().isoformat(),
                metrics={
                    'portfolio_risk': portfolio_risk,
                    'total_risk': total_risk,
                    'position_count': len(positions)
                }
            )
        else:
            result = ValidationResult(
                check_name="portfolio_risk",
                passed=True,
                details=f"Portfolio risk {portfolio_risk:.1%} within limits",
                timestamp=datetime.now().isoformat(),
                metrics={
                    'portfolio_risk': portfolio_risk,
                    'total_risk': total_risk,
                    'position_count': len(positions)
                }
            )
            
        self.validation_history.append(result)
        return result
        
    def get_validation_summary(self) -> Dict:
        """Get summary of recent validations"""
        if not self.validation_history:
            return {
                'all_passed': True,
                'total_checks': 0,
                'failed_checks': 0,
                'last_check': None
            }
            
        recent = self.validation_history[-20:]  # Last 20 checks
        
        return {
            'all_passed': all(r.passed for r in recent),
            'total_checks': len(recent),
            'failed_checks': sum(1 for r in recent if not r.passed),
            'last_check': recent[-1].timestamp
        }
        
    def save_validation_history(self):
        """Save validation history to file"""
        history_path = self.base_path / 'risk' / 'validation_history.json'
        history_path.parent.mkdir(parents=True, exist_ok=True)
        
        history = [
            {
                'check_name': r.check_name,
                'passed': r.passed,
                'details': r.details,
                'timestamp': r.timestamp,
                'metrics': r.metrics
            }
            for r in self.validation_history
        ]
        
        import json
        with open(history_path, 'w') as f:
            json.dump(history, f, indent=2)