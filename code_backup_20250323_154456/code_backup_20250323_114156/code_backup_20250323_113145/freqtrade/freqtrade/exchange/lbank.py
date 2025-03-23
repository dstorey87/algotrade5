"""Lbank exchange subclass"""

import logging

from freqtrade.exchange import Exchange
from freqtrade.exchange.exchange_types import FtHas


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class Lbank(Exchange):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Lbank exchange class. Contains adjustments needed for Freqtrade to work
# REMOVED_UNUSED_CODE:     with this exchange.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     _ft_has: FtHas = {
# REMOVED_UNUSED_CODE:         "ohlcv_candle_limit": 1998,  # lower than the allowed 2000 to avoid current_candle issue
# REMOVED_UNUSED_CODE:         "trades_has_history": False,
# REMOVED_UNUSED_CODE:     }
