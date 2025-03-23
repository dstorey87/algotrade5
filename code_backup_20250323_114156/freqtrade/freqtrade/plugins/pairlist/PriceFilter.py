"""
Price pair list filter
"""

import logging

# REMOVED_UNUSED_CODE: from freqtrade.exceptions import OperationalException
# REMOVED_UNUSED_CODE: from freqtrade.exchange.exchange_types import Ticker
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.plugins.pairlist.IPairList import IPairList, PairlistParameter, SupportsBacktesting


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class PriceFilter(IPairList):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     supports_backtesting = SupportsBacktesting.BIASED
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, *args, **kwargs) -> None:
# REMOVED_UNUSED_CODE:         super().__init__(*args, **kwargs)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._low_price_ratio = self._pairlistconfig.get("low_price_ratio", 0)
# REMOVED_UNUSED_CODE:         if self._low_price_ratio < 0:
# REMOVED_UNUSED_CODE:             raise OperationalException("PriceFilter requires low_price_ratio to be >= 0")
# REMOVED_UNUSED_CODE:         self._min_price = self._pairlistconfig.get("min_price", 0)
# REMOVED_UNUSED_CODE:         if self._min_price < 0:
# REMOVED_UNUSED_CODE:             raise OperationalException("PriceFilter requires min_price to be >= 0")
# REMOVED_UNUSED_CODE:         self._max_price = self._pairlistconfig.get("max_price", 0)
# REMOVED_UNUSED_CODE:         if self._max_price < 0:
# REMOVED_UNUSED_CODE:             raise OperationalException("PriceFilter requires max_price to be >= 0")
# REMOVED_UNUSED_CODE:         self._max_value = self._pairlistconfig.get("max_value", 0)
# REMOVED_UNUSED_CODE:         if self._max_value < 0:
# REMOVED_UNUSED_CODE:             raise OperationalException("PriceFilter requires max_value to be >= 0")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._enabled = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             (self._low_price_ratio > 0)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             or (self._min_price > 0)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             or (self._max_price > 0)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             or (self._max_value > 0)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def needstickers(self) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Boolean property defining if tickers are necessary.
# REMOVED_UNUSED_CODE:         If no Pairlist requires tickers, an empty Dict is passed
# REMOVED_UNUSED_CODE:         as tickers argument to filter_pairlist
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def short_desc(self) -> str:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Short whitelist method description - used for startup-messages
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         active_price_filters = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._low_price_ratio != 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             active_price_filters.append(f"below {self._low_price_ratio:.1%}")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._min_price != 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             active_price_filters.append(f"below {self._min_price:.8f}")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._max_price != 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             active_price_filters.append(f"above {self._max_price:.8f}")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._max_value != 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             active_price_filters.append(f"Value above {self._max_value:.8f}")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if len(active_price_filters):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return f"{self.name} - Filtering pairs priced {' or '.join(active_price_filters)}."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return f"{self.name} - No price filters configured."
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def description() -> str:
# REMOVED_UNUSED_CODE:         return "Filter pairs by price."
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def available_parameters() -> dict[str, PairlistParameter]:
# REMOVED_UNUSED_CODE:         return {
# REMOVED_UNUSED_CODE:             "low_price_ratio": {
# REMOVED_UNUSED_CODE:                 "type": "number",
# REMOVED_UNUSED_CODE:                 "default": 0,
# REMOVED_UNUSED_CODE:                 "description": "Low price ratio",
# REMOVED_UNUSED_CODE:                 "help": (
# REMOVED_UNUSED_CODE:                     "Remove pairs where a price move of 1 price unit (pip) is above this ratio."
# REMOVED_UNUSED_CODE:                 ),
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "min_price": {
# REMOVED_UNUSED_CODE:                 "type": "number",
# REMOVED_UNUSED_CODE:                 "default": 0,
# REMOVED_UNUSED_CODE:                 "description": "Minimum price",
# REMOVED_UNUSED_CODE:                 "help": "Remove pairs with a price below this value.",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "max_price": {
# REMOVED_UNUSED_CODE:                 "type": "number",
# REMOVED_UNUSED_CODE:                 "default": 0,
# REMOVED_UNUSED_CODE:                 "description": "Maximum price",
# REMOVED_UNUSED_CODE:                 "help": "Remove pairs with a price above this value.",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "max_value": {
# REMOVED_UNUSED_CODE:                 "type": "number",
# REMOVED_UNUSED_CODE:                 "default": 0,
# REMOVED_UNUSED_CODE:                 "description": "Maximum value",
# REMOVED_UNUSED_CODE:                 "help": "Remove pairs with a value (price * amount) above this value.",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _validate_pair(self, pair: str, ticker: Ticker | None) -> bool:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Check if one price-step (pip) is > than a certain barrier.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pair: Pair that's currently validated
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param ticker: ticker dict as returned from ccxt.fetch_ticker
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: True if the pair can stay, false if it should be removed
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if ticker and "last" in ticker and ticker["last"] is not None and ticker.get("last") != 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             price: float = ticker["last"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.log_once(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"Removed {pair} from whitelist, because "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "ticker['last'] is empty (Usually no trade in the last 24h).",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 logger.info,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Perform low_price_ratio check.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._low_price_ratio != 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             compare = self._exchange.price_get_one_pip(pair, price)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             changeperc = compare / price
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if changeperc > self._low_price_ratio:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.log_once(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     f"Removed {pair} from whitelist, because 1 unit is {changeperc:.3%}",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     logger.info,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Perform low_amount check
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._max_value != 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             market = self._exchange.markets[pair]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             limits = market["limits"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if limits["amount"]["min"] is not None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 min_amount = limits["amount"]["min"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 min_precision = market["precision"]["amount"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 min_value = min_amount * price
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if self._exchange.precisionMode == 4:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     # tick size
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     next_value = (min_amount + min_precision) * price
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     # Decimal places
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     min_precision = pow(0.1, min_precision)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     next_value = (min_amount + min_precision) * price
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 diff = next_value - min_value
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if diff > self._max_value:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     self.log_once(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         f"Removed {pair} from whitelist, "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         f"because min value change of {diff} > {self._max_value}.",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         logger.info,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     return False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Perform min_price check.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._min_price != 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if price < self._min_price:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.log_once(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     f"Removed {pair} from whitelist, because last price < {self._min_price:.8f}",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     logger.info,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Perform max_price check.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._max_price != 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if price > self._max_price:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.log_once(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     f"Removed {pair} from whitelist, because last price > {self._max_price:.8f}",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     logger.info,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return True
