"""Kucoin exchange subclass."""

import logging

from freqtrade.constants import BuySell
from freqtrade.exchange import Exchange
from freqtrade.exchange.exchange_types import CcxtOrder, FtHas


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class Kucoin(Exchange):
# REMOVED_UNUSED_CODE:     """Kucoin exchange class.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Contains adjustments needed for Freqtrade to work with this exchange.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Please note that this exchange is not included in the list of exchanges
# REMOVED_UNUSED_CODE:     officially supported by the Freqtrade development team. So some features
# REMOVED_UNUSED_CODE:     may still not work as expected.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     _ft_has: FtHas = {
# REMOVED_UNUSED_CODE:         "stoploss_on_exchange": True,
# REMOVED_UNUSED_CODE:         "stop_price_param": "stopPrice",
# REMOVED_UNUSED_CODE:         "stop_price_prop": "stopPrice",
# REMOVED_UNUSED_CODE:         "stoploss_order_types": {"limit": "limit", "market": "market"},
# REMOVED_UNUSED_CODE:         "l2_limit_range": [20, 100],
# REMOVED_UNUSED_CODE:         "l2_limit_range_required": False,
# REMOVED_UNUSED_CODE:         "order_time_in_force": ["GTC", "FOK", "IOC"],
# REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _get_stop_params(self, side: BuySell, ordertype: str, stop_price: float) -> dict:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         params = self._params.copy()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         params.update({"stopPrice": stop_price, "stop": "loss"})
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return params
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def create_order(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         *,
# REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE:         ordertype: str,
# REMOVED_UNUSED_CODE:         side: BuySell,
# REMOVED_UNUSED_CODE:         amount: float,
# REMOVED_UNUSED_CODE:         rate: float,
# REMOVED_UNUSED_CODE:         leverage: float,
# REMOVED_UNUSED_CODE:         reduceOnly: bool = False,
# REMOVED_UNUSED_CODE:         time_in_force: str = "GTC",
# REMOVED_UNUSED_CODE:     ) -> CcxtOrder:
# REMOVED_UNUSED_CODE:         res = super().create_order(
# REMOVED_UNUSED_CODE:             pair=pair,
# REMOVED_UNUSED_CODE:             ordertype=ordertype,
# REMOVED_UNUSED_CODE:             side=side,
# REMOVED_UNUSED_CODE:             amount=amount,
# REMOVED_UNUSED_CODE:             rate=rate,
# REMOVED_UNUSED_CODE:             leverage=leverage,
# REMOVED_UNUSED_CODE:             reduceOnly=reduceOnly,
# REMOVED_UNUSED_CODE:             time_in_force=time_in_force,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         # Kucoin returns only the order-id.
# REMOVED_UNUSED_CODE:         # ccxt returns status = 'closed' at the moment - which is information ccxt invented.
# REMOVED_UNUSED_CODE:         # Since we rely on status heavily, we must set it to 'open' here.
# REMOVED_UNUSED_CODE:         # ref: https://github.com/ccxt/ccxt/pull/16674, (https://github.com/ccxt/ccxt/pull/16553)
# REMOVED_UNUSED_CODE:         if not self._config["dry_run"]:
# REMOVED_UNUSED_CODE:             res["type"] = ordertype
# REMOVED_UNUSED_CODE:             res["status"] = "open"
# REMOVED_UNUSED_CODE:         return res
