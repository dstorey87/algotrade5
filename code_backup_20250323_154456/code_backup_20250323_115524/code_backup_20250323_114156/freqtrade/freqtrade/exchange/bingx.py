"""Bingx exchange subclass"""

import logging

from freqtrade.exchange import Exchange
from freqtrade.exchange.exchange_types import FtHas


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class Bingx(Exchange):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Bingx exchange class. Contains adjustments needed for Freqtrade to work
# REMOVED_UNUSED_CODE:     with this exchange.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     _ft_has: FtHas = {
# REMOVED_UNUSED_CODE:         "ohlcv_candle_limit": 1000,
# REMOVED_UNUSED_CODE:         "stoploss_on_exchange": True,
# REMOVED_UNUSED_CODE:         "stoploss_order_types": {"limit": "limit", "market": "market"},
# REMOVED_UNUSED_CODE:         "order_time_in_force": ["GTC", "IOC", "PO"],
# REMOVED_UNUSED_CODE:         "trades_has_history": False,  # Endpoint doesn't seem to support pagination
# REMOVED_UNUSED_CODE:     }
