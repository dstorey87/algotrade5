"""
Data Management System
===================

CRITICAL REQUIREMENTS:
- SQL storage only (no transient data)
- Real-time trade tracking
- Pattern validation history
- Performance metrics logging

DATABASE SCHEMA:
1. historical_prices
2. pair_metrics
3. quantum_loop_results
4. optimization_history
5. paper_trades
6. expanded_strategies

Author: GitHub Copilot
Last Updated: 2025-03-12
"""

import logging
from typing import Dict, List, Optional, Union
from pathlib import Path
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime

logger = logging.getLogger(__name__)

class DataManager:
    """
    SQL-based data management system
    
    CRITICAL METRICS:
    - Pattern validation rate
    - Win rate tracking
    - Performance history
    - System metrics
    """
    
    def __init__(self):
        """
        Initialize data management system
        
        REQUIREMENTS:
        - Database connections
        - Table validation
        - Index optimization
        - Backup procedures
        """
        self.data_path = Path("data")
        self.analysis_db = self.data_path / "analysis.db"
        self.trading_db = self.data_path / "trading.db"
        
        # Ensure data directory exists
        self.data_path.mkdir(exist_ok=True)
        
        # Initialize databases
        self._initialize_databases()
        logger.info("Data Manager initialized with SQL storage")
        
    def _initialize_databases(self):
        """
        Initialize database schemas
        
        TABLES:
        1. Trade tracking
        2. Pattern validation
        3. Performance metrics
        4. System monitoring
        """
        try:
            # Analysis database
            with sqlite3.connect(self.analysis_db) as conn:
                c = conn.cursor()
                
                # Create pattern tracking tables
                c.execute("""
                CREATE TABLE IF NOT EXISTS validated_patterns (
                    id TEXT PRIMARY KEY,
                    pattern_name TEXT NOT NULL,
                    pair TEXT NOT NULL,
                    timeframe TEXT NOT NULL,
                    entry_timestamp TEXT NOT NULL,
                    exit_timestamp TEXT,
                    forward_score REAL NOT NULL,
                    backward_score REAL NOT NULL,
                    alignment_score REAL NOT NULL,
                    confidence REAL NOT NULL,
                    regime INTEGER NOT NULL,
                    market_conditions TEXT,
                    pattern_data TEXT,
                    validation_status TEXT,
                    paper_traded BOOLEAN DEFAULT FALSE,
                    live_traded BOOLEAN DEFAULT FALSE,
                    profit_ratio REAL,
                    validation_window INTEGER NOT NULL
                )""")
                
                # Create performance tracking
                c.execute("""
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    timestamp TEXT PRIMARY KEY,
                    win_rate REAL NOT NULL,
                    pattern_confidence REAL NOT NULL,
                    drawdown REAL NOT NULL,
                    total_trades INTEGER NOT NULL,
                    successful_trades INTEGER NOT NULL,
                    system_health TEXT,
                    gpu_metrics TEXT
                )""")
                
                # Create strategy catalog
                c.execute("""
                CREATE TABLE IF NOT EXISTS strategy_catalog (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    win_rate REAL NOT NULL,
                    profit_factor REAL NOT NULL,
                    drawdown REAL NOT NULL,
                    validation_status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    last_updated TEXT NOT NULL,
                    parameters TEXT
                )""")
                
            # Trading database
            with sqlite3.connect(self.trading_db) as conn:
                c = conn.cursor()
                
                # Create trade tracking
                c.execute("""
                CREATE TABLE IF NOT EXISTS trades (
                    id TEXT PRIMARY KEY,
                    pair TEXT NOT NULL,
                    entry_time TEXT NOT NULL,
                    exit_time TEXT,
                    entry_price REAL NOT NULL,
                    exit_price REAL,
                    volume REAL NOT NULL,
                    profit_ratio REAL,
                    strategy_id TEXT,
                    pattern_id TEXT,
                    validation_status TEXT,
                    trade_type TEXT NOT NULL
                )""")
                
                # Create market data
                c.execute("""
                CREATE TABLE IF NOT EXISTS market_data (
                    timestamp TEXT NOT NULL,
                    pair TEXT NOT NULL,
                    timeframe TEXT NOT NULL,
                    open REAL NOT NULL,
                    high REAL NOT NULL,
                    low REAL NOT NULL,
                    close REAL NOT NULL,
                    volume REAL NOT NULL,
                    PRIMARY KEY (timestamp, pair, timeframe)
                )""")
                
            logger.info("Database schemas initialized")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
            
    def store_validated_pattern(self, pattern_data: Dict) -> bool:
        """
        Store quantum-validated pattern
        
        REQUIRED DATA:
        - Pattern metrics
        - Validation status
        - Market conditions
        - Performance data
        """
        try:
            with sqlite3.connect(self.analysis_db) as conn:
                c = conn.cursor()
                
                c.execute("""
                INSERT INTO validated_patterns (
                    id, pattern_name, pair, timeframe, entry_timestamp,
                    forward_score, backward_score, alignment_score,
                    confidence, regime, market_conditions, pattern_data,
                    validation_status, validation_window
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    pattern_data['id'],
                    pattern_data['pattern_name'],
                    pattern_data['pair'],
                    pattern_data['timeframe'],
                    pattern_data['entry_timestamp'],
                    pattern_data['forward_score'],
                    pattern_data['backward_score'],
                    pattern_data['alignment_score'],
                    pattern_data['confidence'],
                    pattern_data['regime'],
                    str(pattern_data.get('market_conditions', {})),
                    str(pattern_data.get('pattern_data', [])),
                    pattern_data['validation_status'],
                    pattern_data['validation_window']
                ))
                
                return True
                
        except Exception as e:
            logger.error(f"Error storing pattern: {e}")
            return False
            
    def get_validated_patterns(self, 
                             min_confidence: float = 0.85,
                             validation_status: str = 'validated',
                             limit: int = 100) -> pd.DataFrame:
        """
        Retrieve validated patterns meeting criteria
        
        FILTERS:
        - Minimum confidence
        - Validation status
        - Recent patterns
        """
        try:
            query = """
            SELECT * FROM validated_patterns
            WHERE confidence >= ?
            AND validation_status = ?
            ORDER BY entry_timestamp DESC
            LIMIT ?
            """
            
            with sqlite3.connect(self.analysis_db) as conn:
                return pd.read_sql_query(
                    query,
                    conn,
                    params=[min_confidence, validation_status, limit]
                )
                
        except Exception as e:
            logger.error(f"Error retrieving patterns: {e}")
            return pd.DataFrame()
            
    def store_performance_metrics(self, metrics: Dict) -> bool:
        """
        Store system performance metrics
        
        METRICS:
        - Win rate
        - Pattern confidence
        - System health
        - Resource usage
        """
        try:
            with sqlite3.connect(self.analysis_db) as conn:
                c = conn.cursor()
                
                c.execute("""
                INSERT INTO performance_metrics (
                    timestamp, win_rate, pattern_confidence,
                    drawdown, total_trades, successful_trades,
                    system_health, gpu_metrics
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    datetime.now().isoformat(),
                    metrics['win_rate'],
                    metrics['pattern_confidence'],
                    metrics['drawdown'],
                    metrics['total_trades'],
                    metrics['successful_trades'],
                    str(metrics.get('system_health', {})),
                    str(metrics.get('gpu_metrics', {}))
                ))
                
                return True
                
        except Exception as e:
            logger.error(f"Error storing metrics: {e}")
            return False
            
    def get_performance_history(self, days: int = 7) -> pd.DataFrame:
        """
        Get historical performance data
        
        INCLUDES:
        - Win rate trends
        - Pattern confidence
        - System metrics
        - Resource usage
        """
        try:
            query = """
            SELECT * FROM performance_metrics
            WHERE timestamp >= datetime('now', ?)
            ORDER BY timestamp DESC
            """
            
            with sqlite3.connect(self.analysis_db) as conn:
                return pd.read_sql_query(
                    query,
                    conn,
                    params=[f"-{days} days"]
                )
                
        except Exception as e:
            logger.error(f"Error retrieving performance history: {e}")
            return pd.DataFrame()
            
    def store_trade(self, trade_data: Dict) -> bool:
        """
        Store trade details with validation
        
        REQUIRED DATA:
        - Trade parameters
        - Performance metrics
        - Validation status
        - Pattern reference
        """
        try:
            with sqlite3.connect(self.trading_db) as conn:
                c = conn.cursor()
                
                c.execute("""
                INSERT INTO trades (
                    id, pair, entry_time, entry_price,
                    volume, strategy_id, pattern_id,
                    validation_status, trade_type
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    trade_data['id'],
                    trade_data['pair'],
                    trade_data['entry_time'],
                    trade_data['entry_price'],
                    trade_data['volume'],
                    trade_data.get('strategy_id'),
                    trade_data.get('pattern_id'),
                    trade_data['validation_status'],
                    trade_data['trade_type']
                ))
                
                return True
                
        except Exception as e:
            logger.error(f"Error storing trade: {e}")
            return False
            
    def update_trade(self, trade_id: str, exit_data: Dict) -> bool:
        """
        Update trade with exit information
        
        UPDATES:
        - Exit price/time
        - Profit calculation
        - Performance metrics
        """
        try:
            with sqlite3.connect(self.trading_db) as conn:
                c = conn.cursor()
                
                c.execute("""
                UPDATE trades SET
                    exit_time = ?,
                    exit_price = ?,
                    profit_ratio = ?
                WHERE id = ?
                """, (
                    exit_data['exit_time'],
                    exit_data['exit_price'],
                    exit_data['profit_ratio'],
                    trade_id
                ))
                
                return True
                
        except Exception as e:
            logger.error(f"Error updating trade: {e}")
            return False
            
    def get_trade_history(self, days: int = 7, trade_type: str = 'all') -> pd.DataFrame:
        """
        Get historical trade data
        
        FILTERS:
        - Time period
        - Trade type
        - Performance metrics
        """
        try:
            query = """
            SELECT * FROM trades
            WHERE entry_time >= datetime('now', ?)
            """
            
            if trade_type != 'all':
                query += " AND trade_type = ?"
                params = [f"-{days} days", trade_type]
            else:
                params = [f"-{days} days"]
                
            query += " ORDER BY entry_time DESC"
            
            with sqlite3.connect(self.trading_db) as conn:
                return pd.read_sql_query(query, conn, params=params)
                
        except Exception as e:
            logger.error(f"Error retrieving trade history: {e}")
            return pd.DataFrame()
            
    def calculate_win_rate(self, days: int = 7) -> float:
        """
        Calculate win rate from trade history
        
        CRITICAL METRIC:
        - Must maintain 85% or higher
        """
        try:
            trades = self.get_trade_history(days=days)
            if trades.empty:
                return 0.0
                
            winning_trades = trades[trades['profit_ratio'] > 0]
            return len(winning_trades) / len(trades)
            
        except Exception as e:
            logger.error(f"Error calculating win rate: {e}")
            return 0.0