#!/usr/bin/env python3
import logging
from pathlib import Path
from typing import List, Optional
from datetime import datetime, timedelta
import json
import sys
sys.path.append('..')

from freqtrade.commands.data_commands import start_download_data
from data_manager import DataManager

logger = logging.getLogger(__name__)

def download_market_data(pairs: List[str], 
                       timeframes: List[str],
                       timerange: Optional[str] = None,
                       exchange: str = "binance") -> None:
    """
    Download market data with persistence management
    """
    data_manager = DataManager()
    
    # Load config
    config_file = Path("user_data/config.json")
    with config_file.open() as f:
        config = json.load(f)
    
    # Update config for data download
    config.update({
        "pairs": pairs,
        "timeframes": timeframes,
        "exchange": exchange,
        "timerange": timerange,
        "datadir": "user_data/data",
        "download_trades": True
    })

    # Convert timerange to dates for database
    start_date = "20240101"  # Default if not specified
    end_date = datetime.now().strftime("%Y%m%d")
    if timerange:
        if timerange.endswith("-"):
            start_date = timerange[:-1]
        elif "-" in timerange:
            start_date, end_date = timerange.split("-")

    # Download data and register in database
    start_download_data(config)
    
    # Register downloaded data
    for pair in pairs:
        for timeframe in timeframes:
            data_path = f"user_data/data/{pair.replace('/', '_')}-{timeframe}.feather"
            data_manager.register_downloaded_data(
                pair=pair,
                timeframe=timeframe,
                start_date=start_date,
                end_date=end_date,
                data_path=data_path
            )
            logger.info(f"Registered data for {pair} {timeframe} in database")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    pairs = ["BTC/USDT", "ETH/USDT", "ADA/USDT"]
    timeframes = ["5m", "15m", "1h"]
    download_market_data(pairs, timeframes, timerange="20240101-")