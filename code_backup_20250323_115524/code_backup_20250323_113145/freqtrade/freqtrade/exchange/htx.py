"""HTX exchange subclass"""

import logging

# REMOVED_UNUSED_CODE: from freqtrade.constants import BuySell
# REMOVED_UNUSED_CODE: from freqtrade.exchange import Exchange
# REMOVED_UNUSED_CODE: from freqtrade.exchange.exchange_types import FtHas


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class Htx(Exchange):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     HTX exchange class. Contains adjustments needed for Freqtrade to work
# REMOVED_UNUSED_CODE:     with this exchange.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     _ft_has: FtHas = {
# REMOVED_UNUSED_CODE:         "stoploss_on_exchange": True,
# REMOVED_UNUSED_CODE:         "stop_price_param": "stopPrice",
# REMOVED_UNUSED_CODE:         "stop_price_prop": "stopPrice",
# REMOVED_UNUSED_CODE:         "stoploss_order_types": {"limit": "stop-limit"},
# REMOVED_UNUSED_CODE:         "l2_limit_range": [5, 10, 20],
# REMOVED_UNUSED_CODE:         "l2_limit_range_required": False,
# REMOVED_UNUSED_CODE:         "ohlcv_candle_limit_per_timeframe": {
# REMOVED_UNUSED_CODE:             "1w": 500,
# REMOVED_UNUSED_CODE:             "1M": 500,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "trades_has_history": False,  # Endpoint doesn't have a "since" parameter
# REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _get_stop_params(self, side: BuySell, ordertype: str, stop_price: float) -> dict:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         params = self._params.copy()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         params.update(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "stopPrice": stop_price,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "operator": "lte",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             }
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return params
