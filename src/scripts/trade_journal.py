#!/usr/bin/env python3
"""Trade Journal with pattern analysis and success tracking"""
import logging
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import sqlite3
import json

logger = logging.getLogger(__name__)

class TradeJournal:
    """Tracks and analyzes trading patterns and outcomes"""
    
    def __init__(self, db_path: str = 'data/trading.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS trade_patterns (
                    id INTEGER PRIMARY KEY,
                    pattern_name TEXT,
                    timestamp TEXT,
                    symbol TEXT,
                    timeframe TEXT,
                    entry_price REAL,
                    exit_price REAL,
                    profit_ratio REAL,
                    market_conditions TEXT,
                    indicators TEXT,
                    success INTEGER,
                    trade_duration INTEGER,
                    market_regime TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS pattern_performance (
                    pattern_name TEXT PRIMARY KEY,
                    total_trades INTEGER,
                    winning_trades INTEGER,
                    losing_trades INTEGER,
                    win_rate REAL,
                    avg_profit_ratio REAL,
                    best_market_regime TEXT,
                    updated_at TEXT,
                    performance_data TEXT
                )
            """)

    def log_trade(self, trade_data: Dict):
        """Log a trade with its pattern analysis"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Extract pattern information
                patterns = trade_data.get('patterns', '').split(',')
                market_conditions = json.dumps(trade_data.get('market_conditions', {}))
                indicators = json.dumps(trade_data.get('indicators', {}))
                
                # Store trade pattern
                for pattern in patterns:
                    if not pattern.strip():
                        continue
                        
                    conn.execute("""
                        INSERT INTO trade_patterns (
                            pattern_name, timestamp, symbol, timeframe,
                            entry_price, exit_price, profit_ratio,
                            market_conditions, indicators, success,
                            trade_duration, market_regime
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        pattern.strip(),
                        trade_data.get('timestamp', datetime.now().isoformat()),
                        trade_data.get('symbol', ''),
                        trade_data.get('timeframe', ''),
                        trade_data.get('entry_price', 0.0),
                        trade_data.get('exit_price', 0.0),
                        trade_data.get('profit_ratio', 0.0),
                        market_conditions,
                        indicators,
                        1 if trade_data.get('profit_ratio', 0) > 0 else 0,
                        trade_data.get('trade_duration', 0),
                        trade_data.get('market_regime', 'unknown')
                    ))
                
                # Update pattern performance
                self._update_pattern_performance(pattern.strip(), trade_data)
                
        except Exception as e:
            logger.error(f"Error logging trade: {e}")

    def _update_pattern_performance(self, pattern: str, trade_data: Dict):
        """Update pattern performance metrics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Get existing performance data
                cursor = conn.execute(
                    "SELECT * FROM pattern_performance WHERE pattern_name = ?",
                    (pattern,)
                )
                existing = cursor.fetchone()
                
                profit_ratio = trade_data.get('profit_ratio', 0)
                is_win = profit_ratio > 0
                
                if existing:
                    # Update existing pattern performance
                    conn.execute("""
                        UPDATE pattern_performance
                        SET total_trades = total_trades + 1,
                            winning_trades = winning_trades + ?,
                            losing_trades = losing_trades + ?,
                            win_rate = CAST(winning_trades + ? AS REAL) / (total_trades + 1),
                            avg_profit_ratio = ((avg_profit_ratio * total_trades) + ?) / (total_trades + 1),
                            updated_at = ?
                        WHERE pattern_name = ?
                    """, (
                        1 if is_win else 0,
                        0 if is_win else 1,
                        1 if is_win else 0,
                        profit_ratio,
                        datetime.now().isoformat(),
                        pattern
                    ))
                else:
                    # Insert new pattern performance
                    conn.execute("""
                        INSERT INTO pattern_performance (
                            pattern_name, total_trades, winning_trades,
                            losing_trades, win_rate, avg_profit_ratio,
                            best_market_regime, updated_at, performance_data
                        ) VALUES (?, 1, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        pattern,
                        1 if is_win else 0,
                        0 if is_win else 1,
                        1.0 if is_win else 0.0,
                        profit_ratio,
                        trade_data.get('market_regime', 'unknown'),
                        datetime.now().isoformat(),
                        '{}'
                    ))
                    
        except Exception as e:
            logger.error(f"Error updating pattern performance: {e}")

    def get_recent_trades(self, days: int = 30) -> pd.DataFrame:
        """Get recent trades with pattern analysis"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
                
                query = """
                    SELECT * FROM trade_patterns 
                    WHERE timestamp > ?
                    ORDER BY timestamp DESC
                """
                
                return pd.read_sql_query(query, conn, params=(cutoff_date,))
                
        except Exception as e:
            logger.error(f"Error getting recent trades: {e}")
            return pd.DataFrame()

    def get_pattern_stats(self, pattern: str) -> Dict:
        """Get detailed statistics for a specific pattern"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                query = """
                    SELECT 
                        COUNT(*) as total_trades,
                        SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as winning_trades,
                        AVG(CASE WHEN success = 1 THEN profit_ratio ELSE 0 END) as avg_win_profit,
                        AVG(CASE WHEN success = 0 THEN profit_ratio ELSE 0 END) as avg_loss_profit,
                        market_regime,
                        AVG(trade_duration) as avg_duration
                    FROM trade_patterns
                    WHERE pattern_name = ?
                    GROUP BY market_regime
                """
                
                df = pd.read_sql_query(query, conn, params=(pattern,))
                
                if df.empty:
                    return {}
                    
                return {
                    'pattern_name': pattern,
                    'total_trades': int(df['total_trades'].sum()),
                    'winning_trades': int(df['winning_trades'].sum()),
                    'win_rate': float(df['winning_trades'].sum() / df['total_trades'].sum()),
                    'avg_win_profit': float(df['avg_win_profit'].mean()),
                    'avg_loss_profit': float(df['avg_loss_profit'].mean()),
                    'regime_performance': df.to_dict('records'),
                    'avg_duration': float(df['avg_duration'].mean())
                }
                
        except Exception as e:
            logger.error(f"Error getting pattern stats: {e}")
            return {}