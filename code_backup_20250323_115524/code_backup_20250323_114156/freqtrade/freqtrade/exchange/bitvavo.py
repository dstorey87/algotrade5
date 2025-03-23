"""Bitvavo exchange subclass."""

import logging

# REMOVED_UNUSED_CODE: from ccxt import DECIMAL_PLACES

# REMOVED_UNUSED_CODE: from freqtrade.exchange import Exchange
# REMOVED_UNUSED_CODE: from freqtrade.exchange.exchange_types import FtHas


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class Bitvavo(Exchange):
# REMOVED_UNUSED_CODE:     """Bitvavo exchange class.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Contains adjustments needed for Freqtrade to work with this exchange.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Please note that this exchange is not included in the list of exchanges
# REMOVED_UNUSED_CODE:     officially supported by the Freqtrade development team. So some features
# REMOVED_UNUSED_CODE:     may still not work as expected.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     _ft_has: FtHas = {
# REMOVED_UNUSED_CODE:         "ohlcv_candle_limit": 1440,
# REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def precisionMode(self) -> int:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Exchange ccxt precisionMode
# REMOVED_UNUSED_CODE:         Override due to https://github.com/ccxt/ccxt/issues/20408
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return DECIMAL_PLACES
