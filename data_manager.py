#!/usr/bin/env python3
"""Data Manager for AlgoTradPro5"""
import logging
import sqlite3
from datetime import datetime
import pandas as pd
import json
import uuid
from typing import Dict, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class DataManager:
    """Manages data storage and retrieval for AlgoTradPro5"""
    
    def __init__(self):
        self.db_path = Path('freqtrade/user_data/data')
        self.db_path.mkdir(exist_ok=True)
        self._initialize_database()

    def _initialize_database(self):
        """Initialize database tables"""
        try:
            with sqlite3.connect(self.db_path / 'analysis.db') as conn:
                c = conn.cursor()
                
                # Create downloaded data tracking table
                c.execute("""
                CREATE TABLE IF NOT EXISTS downloaded_data (
                    pair TEXT NOT NULL,
                    timeframe TEXT NOT NULL,
                    start_date TEXT NOT NULL,
                    end_date TEXT NOT NULL,
                    last_updated TEXT NOT NULL,
                    data_path TEXT NOT NULL,
                    PRIMARY KEY (pair, timeframe)
                )""")
                
                # Create successful patterns table
                c.execute("""
                CREATE TABLE IF NOT EXISTS successful_patterns (
                    pattern_name TEXT NOT NULL,
                    win_rate REAL NOT NULL,
                    total_trades INTEGER NOT NULL,
                    successful_trades INTEGER NOT NULL,
                    avg_profit_ratio REAL,
                    timestamp TEXT NOT NULL,
                    market_regime TEXT,
                    PRIMARY KEY (pattern_name, market_regime)
                )""")
                
                # Create backtest conditions table
                c.execute("""
                CREATE TABLE IF NOT EXISTS backtest_conditions (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    timerange TEXT NOT NULL,
                    success_rate REAL NOT NULL,
                    total_trades INTEGER NOT NULL,
                    profit_factor REAL,
                    market_regime TEXT,
                    patterns TEXT,
                    volume_profile TEXT,
                    parameters TEXT,
                    blacklisted BOOLEAN DEFAULT FALSE,
                    blacklist_reason TEXT
                )""")

                # Create quantum validated patterns table
                c.execute("""
                CREATE TABLE IF NOT EXISTS quantum_validated_patterns (
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
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error initializing database: {e}")

    def store_quantum_validated_pattern(self, pattern_data: Dict):
        """Store quantum-validated pattern details"""
        try:
            with sqlite3.connect(self.db_path / 'analysis.db') as conn:
                c = conn.cursor()
                
                c.execute("""
                INSERT INTO quantum_validated_patterns
                (id, pattern_name, pair, timeframe, entry_timestamp,
                forward_score, backward_score, alignment_score,
                confidence, regime, market_conditions, pattern_data,
                validation_status, validation_window)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(uuid.uuid4()),
                    pattern_data['pattern_name'],
                    pattern_data['pair'],
                    pattern_data['timeframe'],
                    pattern_data['entry_timestamp'],
                    pattern_data['forward_score'],
                    pattern_data['backward_score'],
                    pattern_data['alignment_score'],
                    pattern_data['confidence'],
                    pattern_data['regime'],
                    json.dumps(pattern_data.get('market_conditions', {})),
                    json.dumps(pattern_data.get('pattern_data', {})),
                    pattern_data.get('validation_status', 'pending'),
                    pattern_data['validation_window']
                ))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error storing quantum pattern: {e}")

    def get_validated_patterns(self, 
                             min_confidence: float = 0.85,
                             validation_status: str = 'validated',
                             limit: int = 100) -> pd.DataFrame:
        """Get quantum-validated patterns meeting criteria"""
        try:
            query = """
            SELECT * FROM quantum_validated_patterns
            WHERE confidence >= ?
            AND validation_status = ?
            ORDER BY confidence DESC, alignment_score DESC
            LIMIT ?
            """
            
            with sqlite3.connect(self.db_path / 'analysis.db') as conn:
                return pd.read_sql_query(
                    query,
                    conn,
                    params=[min_confidence, validation_status, limit]
                )
                
        except Exception as e:
            logger.error(f"Error getting validated patterns: {e}")
            return pd.DataFrame()

    def update_pattern_trade_status(self, pattern_id: str, trade_data: Dict):
        """Update pattern with trade execution results"""
        try:
            with sqlite3.connect(self.db_path / 'analysis.db') as conn:
                c = conn.cursor()
                
                c.execute("""
                UPDATE quantum_validated_patterns
                SET paper_traded = ?,
                    live_traded = ?,
                    exit_timestamp = ?,
                    profit_ratio = ?
                WHERE id = ?
                """, (
                    trade_data.get('paper_traded', False),
                    trade_data.get('live_traded', False),
                    trade_data.get('exit_timestamp'),
                    trade_data.get('profit_ratio'),
                    pattern_id
                ))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error updating pattern trade status: {e}")

    def get_pattern_last_updates(self):
        """Get most recent pattern updates"""
        try:
            query = """
            SELECT pattern_name, max(last_updated)
            FROM successful_patterns
            GROUP BY pattern_name
            """
            
            with sqlite3.connect(self.db_path / 'analysis.db') as conn:
                return pd.read_sql_query(query, conn)
                
        except Exception as e:
            logger.error(f"Error getting pattern updates: {e}")
            return pd.DataFrame()          

    def catalog_successful_pattern(self, pattern_data: Dict):
        """Store successful pattern in database"""
        try:
            with sqlite3.connect(self.db_path / 'analysis.db') as conn:
                c = conn.cursor()
                
                c.execute("""
                INSERT OR REPLACE INTO successful_patterns
                (pattern_name, win_rate, total_trades, successful_trades,
                avg_profit_ratio, timestamp, market_regime)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    pattern_data['pattern_name'],
                    pattern_data['win_rate'],
                    pattern_data['total_trades'],
                    pattern_data['successful_trades'],
                    pattern_data.get('avg_profit_ratio', 0.0),
                    pattern_data['timestamp'],
                    pattern_data.get('market_regime', 'unknown')
                ))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error cataloging pattern: {e}")

    def get_top_patterns(self, 
                        min_trades: int = 10,
                        limit: int = 10) -> pd.DataFrame:
        """Get top performing patterns"""
        try:
            query = """
            SELECT * FROM successful_patterns 
            WHERE total_trades >= ?
            ORDER BY win_rate DESC, total_trades DESC
            LIMIT ?
            """
            
            with sqlite3.connect(self.db_path / 'analysis.db') as conn:
                return pd.read_sql_query(
                    query,
                    conn,
                    params=[min_trades, limit]
                )
                
        except Exception as e:
            logger.error(f"Error getting top patterns: {e}")
            return pd.DataFrame()

    def catalog_backtest_condition(self, condition: Dict):
        """Store backtest condition"""
        try:
            with sqlite3.connect(self.db_path / 'analysis.db') as conn:
                c = conn.cursor()
                
                c.execute("""
                INSERT INTO backtest_conditions
                (id, timestamp, timerange, success_rate, total_trades,
                profit_factor, market_regime, patterns, volume_profile,
                parameters, blacklisted, blacklist_reason)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    condition.get('id', str(uuid.uuid4())),
                    condition['timestamp'],
                    condition['timerange'],
                    condition['success_rate'],
                    condition['total_trades'],
                    condition.get('profit_factor', 0.0),
                    condition.get('market_regime', 'unknown'),
                    ','.join(condition.get('patterns', [])),
                    json.dumps(condition.get('volume_profile', {})),
                    json.dumps(condition.get('parameters', {})),
                    condition.get('blacklisted', False),
                    condition.get('blacklist_reason', '')
                ))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error cataloging condition: {e}")

    def get_winning_conditions(self, 
                             min_trades: int = 10,
                             min_success_rate: float = 0.6) -> pd.DataFrame:
        """Get successful trading conditions"""
        try:
            query = """
            SELECT * FROM backtest_conditions
            WHERE total_trades >= ?
            AND success_rate >= ?
            AND NOT blacklisted
            ORDER BY success_rate DESC, profit_factor DESC
            """
            
            with sqlite3.connect(self.db_path / 'analysis.db') as conn:
                return pd.read_sql_query(
                    query,
                    conn,
                    params=[min_trades, min_success_rate]
                )
                
        except Exception as e:
            logger.error(f"Error getting winning conditions: {e}")
            return pd.DataFrame()

    def update_pattern_performance(self, performance_data: Dict):
        """Update pattern performance metrics"""
        try:
            with sqlite3.connect(self.db_path / 'analysis.db') as conn:
                c = conn.cursor()
                
                c.execute("""
                INSERT OR REPLACE INTO pattern_performance
                (pattern_name, symbol, timeframe, win_rate, profit_ratio,
                trade_count, last_updated, market_regime)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    performance_data['pattern_name'],
                    performance_data['symbol'],
                    performance_data['timeframe'],
                    performance_data['win_rate'],
                    performance_data['profit_ratio'],
                    performance_data['trade_count'],
                    datetime.now().isoformat(),
                    performance_data.get('market_regime', 'unknown')
                ))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error updating pattern performance: {e}")

    def get_pattern_regime_stats(self, pattern: str) -> pd.DataFrame:
        """Get pattern performance across different market regimes"""
        try:
            query = """
            SELECT 
                market_regime,
                COUNT(*) as total_occurrences,
                AVG(win_rate) as avg_win_rate,
                AVG(profit_ratio) as avg_profit_ratio,
                SUM(trade_count) as total_trades
            FROM pattern_performance
            WHERE pattern_name = ?
            GROUP BY market_regime
            ORDER BY avg_win_rate DESC
            """
            
            with sqlite3.connect(self.db_path / 'analysis.db') as conn:
                return pd.read_sql_query(query, conn, params=[pattern])
                
        except Exception as e:
            logger.error(f"Error getting regime stats: {e}")
            return pd.DataFrame()

    def get_recent_performance(self, 
                             days: int = 30,
                             min_trades: int = 5) -> pd.DataFrame:
        """Get recent pattern performance"""
        try:
            query = """
            SELECT 
                pattern_name,
                AVG(win_rate) as avg_win_rate,
                AVG(profit_ratio) as avg_profit,
                SUM(trade_count) as total_trades,
                COUNT(DISTINCT market_regime) as regime_count
            FROM pattern_performance
            WHERE last_updated >= datetime('now', ?)
            GROUP BY pattern_name
            HAVING total_trades >= ?
            ORDER BY avg_win_rate DESC, avg_profit DESC
            """
            
            with sqlite3.connect(self.db_path / 'analysis.db') as conn:
                return pd.read_sql_query(
                    query,
                    conn,
                    params=[f"-{days} days", min_trades]
                )
                
        except Exception as e:
            logger.error(f"Error getting recent performance: {e}")
            return pd.DataFrame()

    def get_market_regime_summary(self) -> pd.DataFrame:
        """Get performance summary by market regime"""
        try:
            query = """
            SELECT 
                market_regime,
                COUNT(DISTINCT pattern_name) as unique_patterns,
                AVG(win_rate) as avg_win_rate,
                AVG(profit_ratio) as avg_profit,
                SUM(trade_count) as total_trades
            FROM pattern_performance
            GROUP BY market_regime
            ORDER BY avg_win_rate DESC
            """
            
            with sqlite3.connect(self.db_path / 'analysis.db') as conn:
                return pd.read_sql_query(query, conn)
                
        except Exception as e:
            logger.error(f"Error getting regime summary: {e}")
            return pd.DataFrame()