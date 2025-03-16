"""
Trade Journal Manager
===================

CRITICAL REQUIREMENTS:
- Real-time trade tracking
- Win rate monitoring (85% target)
- Growth tracking (£10 to £1000)
- Pattern validation logging

TRACKING METRICS:
1. Trade performance
2. Pattern validation
3. Growth progress
4. Risk management

Author: GitHub Copilot
Last Updated: 2025-03-12
"""

import logging
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
from data_manager import DataManager

logger = logging.getLogger(__name__)


class TradeJournal:
    """
    Trade journaling and performance tracking

    CRITICAL METRICS:
    - Win rate (85% minimum)
    - Growth rate (~100% daily)
    - Pattern confidence
    - Risk compliance
    """

    def __init__(self):
        """
        Initialize trade journal

        COMPONENTS:
        - Database connection
        - Performance tracking
        - Alert system
        - Report generation
        """
        self.data_manager = DataManager()
        self.initial_capital = 10.0  # £10 starting capital
        self.target_capital = 1000.0  # £1000 target
        self.min_win_rate = 0.85  # 85% minimum
        self.max_days = 7  # 7-day target

        # Initialize journal
        self._initialize_journal()
        logger.info("Trade Journal initialized with strict requirements")

    def _initialize_journal(self):
        """
        Initialize journal database

        TABLES:
        1. Trade records
        2. Pattern validations
        3. Performance metrics
        4. System logs
        """
        try:
            with sqlite3.connect("data/journal.db") as conn:
                c = conn.cursor()

                # Trade records
                c.execute("""
                CREATE TABLE IF NOT EXISTS trade_records (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    pair TEXT NOT NULL,
                    entry_price REAL NOT NULL,
                    exit_price REAL,
                    volume REAL NOT NULL,
                    pattern_id TEXT,
                    validation_status TEXT,
                    profit_ratio REAL,
                    win_rate_at_time REAL,
                    growth_progress REAL,
                    risk_percentage REAL,
                    notes TEXT
                )""")

                # Performance tracking
                c.execute("""
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    timestamp TEXT PRIMARY KEY,
                    current_capital REAL NOT NULL,
                    win_rate REAL NOT NULL,
                    drawdown REAL NOT NULL,
                    validated_patterns INTEGER NOT NULL,
                    daily_profit REAL NOT NULL,
                    time_remaining TEXT
                )""")

            logger.info("Journal database initialized")

        except Exception as e:
            logger.error(f"Journal initialization failed: {e}")
            raise

    def log_trade(self, trade_data: Dict) -> bool:
        """
        Log trade with performance metrics

        REQUIRED DATA:
        - Trade parameters
        - Pattern validation
        - Performance impact
        - Risk metrics
        """
        try:
            # Calculate metrics
            current_win_rate = self.calculate_win_rate()
            growth_progress = self.calculate_growth_progress()

            # CRITICAL: Validate trade
            if not self._validate_trade(trade_data):
                logger.error("Trade validation failed")
                return False

            # Store trade record
            with sqlite3.connect("data/journal.db") as conn:
                c = conn.cursor()

                c.execute(
                    """
                INSERT INTO trade_records (
                    id, timestamp, pair, entry_price, volume,
                    pattern_id, validation_status, win_rate_at_time,
                    growth_progress, risk_percentage
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        trade_data["id"],
                        datetime.now().isoformat(),
                        trade_data["pair"],
                        trade_data["entry_price"],
                        trade_data["volume"],
                        trade_data.get("pattern_id"),
                        trade_data.get("validation_status"),
                        current_win_rate,
                        growth_progress,
                        trade_data.get("risk_percentage", 0.0),
                    ),
                )

                # Update performance metrics
                self._update_performance_metrics()

            return True

        except Exception as e:
            logger.error(f"Error logging trade: {e}")
            return False

    def update_trade(self, trade_id: str, exit_data: Dict) -> bool:
        """
        Update trade with exit information

        UPDATES:
        - Exit price
        - Profit calculation
        - Win rate impact
        - Growth progress
        """
        try:
            with sqlite3.connect("data/journal.db") as conn:
                c = conn.cursor()

                # Calculate profit ratio
                trade = self.get_trade(trade_id)
                if trade is None:
                    logger.error(f"Trade not found: {trade_id}")
                    return False

                profit_ratio = (exit_data["exit_price"] - trade["entry_price"]) / trade[
                    "entry_price"
                ]

                # Update trade record
                c.execute(
                    """
                UPDATE trade_records SET
                    exit_price = ?,
                    profit_ratio = ?
                WHERE id = ?
                """,
                    (exit_data["exit_price"], profit_ratio, trade_id),
                )

                # Update performance metrics
                self._update_performance_metrics()

                # CRITICAL: Check win rate after update
                if self.calculate_win_rate() < self.min_win_rate:
                    logger.warning("Win rate dropped below minimum threshold")

            return True

        except Exception as e:
            logger.error(f"Error updating trade: {e}")
            return False

    def _validate_trade(self, trade_data: Dict) -> bool:
        """
        Validate trade parameters

        REQUIREMENTS:
        1. Pattern validation
        2. Risk limits
        3. Position sizing
        4. Growth alignment
        """
        try:
            # Check pattern validation
            if not trade_data.get("validation_status") == "validated":
                logger.error("Trade pattern not validated")
                return False

            # Verify risk percentage
            if trade_data.get("risk_percentage", 0.0) > 0.02:  # 2% max risk
                logger.error("Trade exceeds risk limit")
                return False

            # Verify position sizing
            current_capital = self.get_current_capital()
            max_position = current_capital * 0.02  # 2% max position
            if trade_data["volume"] * trade_data["entry_price"] > max_position:
                logger.error("Position size exceeds limit")
                return False

            return True

        except Exception as e:
            logger.error(f"Trade validation failed: {e}")
            return False

    def _update_performance_metrics(self):
        """
        Update performance tracking

        METRICS:
        1. Current capital
        2. Win rate
        3. Growth progress
        4. Time remaining
        """
        try:
            current_capital = self.get_current_capital()
            win_rate = self.calculate_win_rate()
            drawdown = self.calculate_drawdown()
            validated_patterns = self.count_validated_patterns()
            daily_profit = self.calculate_daily_profit()
            time_remaining = self.calculate_time_remaining()

            with sqlite3.connect("data/journal.db") as conn:
                c = conn.cursor()

                c.execute(
                    """
                INSERT INTO performance_metrics (
                    timestamp, current_capital, win_rate,
                    drawdown, validated_patterns, daily_profit,
                    time_remaining
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        datetime.now().isoformat(),
                        current_capital,
                        win_rate,
                        drawdown,
                        validated_patterns,
                        daily_profit,
                        time_remaining.isoformat() if time_remaining else None,
                    ),
                )

        except Exception as e:
            logger.error(f"Error updating performance metrics: {e}")

    def calculate_win_rate(self, days: int = None) -> float:
        """
        Calculate current win rate

        CRITICAL METRIC:
        - Must maintain 85% or higher
        """
        try:
            query = """
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN profit_ratio > 0 THEN 1 ELSE 0 END) as wins
            FROM trade_records
            WHERE exit_price IS NOT NULL
            """

            if days:
                query += f" AND timestamp >= datetime('now', '-{days} days')"

            with sqlite3.connect("data/journal.db") as conn:
                df = pd.read_sql_query(query, conn)

            if df.iloc[0]["total"] == 0:
                return 0.0

            win_rate = df.iloc[0]["wins"] / df.iloc[0]["total"]

            # CRITICAL: Log if below threshold
            if win_rate < self.min_win_rate:
                logger.warning(
                    f"Win rate {win_rate:.2%} below minimum {self.min_win_rate:.2%}"
                )

            return win_rate

        except Exception as e:
            logger.error(f"Error calculating win rate: {e}")
            return 0.0

    def calculate_growth_progress(self) -> float:
        """
        Calculate progress to £1000 target

        TRACKING:
        - Starting from £10
        - Target £1000
        - 7-day limit
        """
        try:
            current_capital = self.get_current_capital()
            return (current_capital - self.initial_capital) / (
                self.target_capital - self.initial_capital
            )

        except Exception as e:
            logger.error(f"Error calculating growth progress: {e}")
            return 0.0

    def get_current_capital(self) -> float:
        """
        Get current account capital

        TRACKING:
        - Starting capital: £10
        - Include all profits/losses
        """
        try:
            query = """
            SELECT SUM(volume * profit_ratio) as total_profit
            FROM trade_records
            WHERE exit_price IS NOT NULL
            """

            with sqlite3.connect("data/journal.db") as conn:
                df = pd.read_sql_query(query, conn)

            total_profit = df.iloc[0]["total_profit"] or 0.0
            return self.initial_capital + total_profit

        except Exception as e:
            logger.error(f"Error getting current capital: {e}")
            return self.initial_capital

    def calculate_drawdown(self) -> float:
        """
        Calculate current drawdown

        LIMIT:
        - Maximum 10% drawdown
        """
        try:
            query = """
            SELECT timestamp,
                   SUM(volume * profit_ratio) OVER (ORDER BY timestamp) as running_profit
            FROM trade_records
            WHERE exit_price IS NOT NULL
            ORDER BY timestamp
            """

            with sqlite3.connect("data/journal.db") as conn:
                df = pd.read_sql_query(query, conn)

            if df.empty:
                return 0.0

            # Calculate running balance
            df["balance"] = self.initial_capital + df["running_profit"]
            peak = df["balance"].expanding().max()
            drawdown = (peak - df["balance"]) / peak

            return float(drawdown.iloc[-1])

        except Exception as e:
            logger.error(f"Error calculating drawdown: {e}")
            return 0.0

    def get_trade(self, trade_id: str) -> Optional[Dict]:
        """
        Get trade details by ID

        INCLUDES:
        - Trade parameters
        - Performance impact
        - Validation status
        """
        try:
            query = "SELECT * FROM trade_records WHERE id = ?"

            with sqlite3.connect("data/journal.db") as conn:
                df = pd.read_sql_query(query, conn, params=[trade_id])

            if df.empty:
                return None

            return df.iloc[0].to_dict()

        except Exception as e:
            logger.error(f"Error retrieving trade: {e}")
            return None

    def calculate_risk_adjusted_returns(self, window_days: int = 7) -> float:
        """Calculate Sharpe-like ratio for risk-adjusted returns"""
        try:
            with sqlite3.connect("data/journal.db") as conn:
                df = pd.read_sql_query(
                    """
                    SELECT daily_profit
                    FROM performance_metrics
                    WHERE timestamp >= date('now', ?)
                    """,
                    conn,
                    params=(f"-{window_days} days",),
                )
                if len(df) < 2:
                    return 0.0
                return df["daily_profit"].mean() / df["daily_profit"].std()
        except Exception as e:
            logger.error(f"Error calculating risk-adjusted returns: {e}")
            return 0.0

    def analyze_pattern_correlations(self) -> Dict[str, float]:
        """Analyze success rate of different trading patterns"""
        try:
            with sqlite3.connect("data/journal.db") as conn:
                df = pd.read_sql_query(
                    """
                    SELECT pattern_id, validation_status
                    FROM trade_records
                    WHERE pattern_id IS NOT NULL
                    """,
                    conn,
                )
                pattern_success = df.groupby("pattern_id")["validation_status"].mean()
                return pattern_success.to_dict()
        except Exception as e:
            logger.error(f"Error analyzing pattern correlations: {e}")
            return {}

    def get_performance_report(self) -> Dict:
        """
        Generate comprehensive performance report

        INCLUDES:
        1. Current metrics
        2. Progress to targets
        3. Risk analysis
        4. Time remaining
        """
        report = {
            "current_capital": self.get_current_capital(),
            "win_rate": self.calculate_win_rate(),
            "growth_progress": self.calculate_growth_progress(),
            "drawdown": self.calculate_drawdown(),
            "validated_patterns": self.count_validated_patterns(),
            "daily_profit": self.calculate_daily_profit(),
            "time_remaining": self.calculate_time_remaining(),
            "timestamp": datetime.now().isoformat(),
            "risk_adjusted_returns": self.calculate_risk_adjusted_returns(),
            "pattern_correlations": self.analyze_pattern_correlations(),
            "rolling_win_rate": self.calculate_win_rate(days=3),  # 3-day rolling window
        }
        return report

    def count_validated_patterns(self) -> int:
        """Count validated trading patterns"""
        try:
            with sqlite3.connect("data/journal.db") as conn:
                c = conn.cursor()
                c.execute("""
                SELECT COUNT(DISTINCT pattern_id)
                FROM trade_records
                WHERE validation_status = 'validated'
                """)
                return c.fetchone()[0]
        except Exception as e:
            logger.error(f"Error counting patterns: {e}")
            return 0

    def calculate_daily_profit(self) -> float:
        """Calculate average daily profit"""
        try:
            query = """
            SELECT AVG(daily_profit) as avg_profit
            FROM (
                SELECT DATE(timestamp) as trade_date,
                       SUM(volume * profit_ratio) as daily_profit
                FROM trade_records
                WHERE exit_price IS NOT NULL
                GROUP BY DATE(timestamp)
            )
            """

            with sqlite3.connect("data/journal.db") as conn:
                df = pd.read_sql_query(query, conn)
                return float(df.iloc[0]["avg_profit"] or 0.0)

        except Exception as e:
            logger.error(f"Error calculating daily profit: {e}")
            return 0.0

    def calculate_time_remaining(self) -> Optional[timedelta]:
        """
        Calculate time remaining to target

        DEADLINE:
        - 7 days from first trade
        """
        try:
            query = "SELECT MIN(timestamp) as start_date FROM trade_records"

            with sqlite3.connect("data/journal.db") as conn:
                df = pd.read_sql_query(query, conn)

            if df.empty or pd.isnull(df.iloc[0]["start_date"]):
                return None

            start_date = pd.to_datetime(df.iloc[0]["start_date"])
            deadline = start_date + timedelta(days=self.max_days)
            remaining = deadline - datetime.now()

            return remaining if remaining.total_seconds() > 0 else timedelta(0)

        except Exception as e:
            logger.error(f"Error calculating time remaining: {e}")
            return None
