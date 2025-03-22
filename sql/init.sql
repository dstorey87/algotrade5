-- Initialize AlgoTradePro5 Database
-- =================================
-- All trading data is persisted here to support the
-- AI-driven pattern analysis and quantum loop strategy

-- Core Tables
CREATE TABLE IF NOT EXISTS trade_history (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    pair VARCHAR(20) NOT NULL,
    type VARCHAR(4) NOT NULL,
    price DECIMAL(18,8) NOT NULL,
    amount DECIMAL(18,8) NOT NULL,
    cost DECIMAL(18,8) NOT NULL
);

CREATE TABLE IF NOT EXISTS model_performance (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    accuracy DECIMAL(5,2) NOT NULL,
    profit_factor DECIMAL(8,4) NOT NULL
);

-- Pattern Analysis Tables
CREATE TABLE IF NOT EXISTS trading_patterns (
    id SERIAL PRIMARY KEY,
    pattern_name VARCHAR(100) NOT NULL,
    description TEXT,
    first_detected TIMESTAMP NOT NULL,
    last_updated TIMESTAMP NOT NULL,
    win_rate DECIMAL(5,2) NOT NULL,
    total_trades INTEGER NOT NULL,
    successful_trades INTEGER NOT NULL,
    min_profit_ratio DECIMAL(8,4),
    max_profit_ratio DECIMAL(8,4),
    avg_profit_ratio DECIMAL(8,4) NOT NULL,
    market_regime VARCHAR(50),
    confidence_score DECIMAL(5,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS pattern_performance (
    id SERIAL PRIMARY KEY,
    pattern_id INTEGER REFERENCES trading_patterns(id),
    timestamp TIMESTAMP NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    timeframe VARCHAR(10) NOT NULL,
    win_rate DECIMAL(5,2) NOT NULL,
    profit_ratio DECIMAL(8,4) NOT NULL,
    trade_count INTEGER NOT NULL,
    market_regime VARCHAR(50)
);

-- Market Regime Tracking
CREATE TABLE IF NOT EXISTS market_regimes (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    timeframe VARCHAR(10) NOT NULL,
    regime_type VARCHAR(50) NOT NULL,
    volatility DECIMAL(8,4) NOT NULL,
    trend_strength DECIMAL(5,2) NOT NULL,
    volume_profile VARCHAR(20),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP
);

-- Quantum Loop Results
CREATE TABLE IF NOT EXISTS quantum_loop_results (
    id SERIAL PRIMARY KEY,
    strategy_name VARCHAR(100) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    pair VARCHAR(20) NOT NULL,
    timeframe VARCHAR(10) NOT NULL,
    total_trades INTEGER NOT NULL,
    win_rate DECIMAL(5,2) NOT NULL,
    profit_factor DECIMAL(8,4) NOT NULL,
    max_drawdown DECIMAL(8,4) NOT NULL,
    sharpe_ratio DECIMAL(5,2),
    return_percentage DECIMAL(8,4) NOT NULL,
    runtime_seconds INTEGER,
    parameters JSONB
);

-- Trade Recommendations
CREATE TABLE IF NOT EXISTS trade_recommendations (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    symbol VARCHAR(20) NOT NULL, 
    pattern_id INTEGER REFERENCES trading_patterns(id),
    confidence DECIMAL(5,2) NOT NULL,
    profit_factor DECIMAL(8,4) NOT NULL,
    regime VARCHAR(50) NOT NULL,
    entry_price DECIMAL(18,8),
    target_price DECIMAL(18,8),
    stop_loss DECIMAL(18,8),
    risk_ratio DECIMAL(5,2),
    executed BOOLEAN DEFAULT FALSE,
    execution_timestamp TIMESTAMP,
    result VARCHAR(10),
    actual_profit_ratio DECIMAL(8,4)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_trade_history_pair ON trade_history(pair);
CREATE INDEX IF NOT EXISTS idx_trade_history_timestamp ON trade_history(timestamp);
CREATE INDEX IF NOT EXISTS idx_pattern_performance_pattern_id ON pattern_performance(pattern_id);
CREATE INDEX IF NOT EXISTS idx_trading_patterns_win_rate ON trading_patterns(win_rate);
CREATE INDEX IF NOT EXISTS idx_market_regimes_symbol_regime ON market_regimes(symbol, regime_type);
CREATE INDEX IF NOT EXISTS idx_quantum_loop_win_rate ON quantum_loop_results(win_rate);

-- Create views for easier reporting
CREATE OR REPLACE VIEW v_top_patterns AS
SELECT 
    tp.pattern_name,
    tp.win_rate,
    tp.total_trades,
    tp.successful_trades,
    tp.avg_profit_ratio,
    tp.market_regime,
    tp.confidence_score
FROM 
    trading_patterns tp
WHERE 
    tp.total_trades >= 10
ORDER BY 
    tp.win_rate DESC, tp.avg_profit_ratio DESC;

CREATE OR REPLACE VIEW v_market_regime_summary AS
SELECT 
    mr.regime_type,
    COUNT(*) as occurrence_count,
    AVG(mr.volatility) as avg_volatility,
    AVG(mr.trend_strength) as avg_trend_strength,
    AVG(EXTRACT(EPOCH FROM (mr.end_time - mr.start_time))/3600) as avg_duration_hours
FROM 
    market_regimes mr
WHERE 
    mr.end_time IS NOT NULL
GROUP BY 
    mr.regime_type
ORDER BY 
    occurrence_count DESC;