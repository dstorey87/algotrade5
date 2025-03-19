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