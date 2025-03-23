"""
PairList manager class
"""

import logging
from functools import partial

from cachetools import TTLCache, cached

from freqtrade.constants import Config, ListPairsWithTimeframes
from freqtrade.data.dataprovider import DataProvider
from freqtrade.enums import CandleType
from freqtrade.enums.runmode import RunMode
from freqtrade.exceptions import OperationalException
from freqtrade.exchange.exchange_types import Tickers
from freqtrade.mixins import LoggingMixin
from freqtrade.plugins.pairlist.IPairList import IPairList, SupportsBacktesting
from freqtrade.plugins.pairlist.pairlist_helpers import expand_pairlist
from freqtrade.resolvers import PairListResolver


logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class PairListManager(LoggingMixin):
# REMOVED_UNUSED_CODE:     def __init__(self, exchange, config: Config, dataprovider: DataProvider | None = None) -> None:
# REMOVED_UNUSED_CODE:         self._exchange = exchange
# REMOVED_UNUSED_CODE:         self._config = config
# REMOVED_UNUSED_CODE:         self._whitelist = self._config["exchange"].get("pair_whitelist")
# REMOVED_UNUSED_CODE:         self._blacklist = self._config["exchange"].get("pair_blacklist", [])
# REMOVED_UNUSED_CODE:         self._pairlist_handlers: list[IPairList] = []
# REMOVED_UNUSED_CODE:         self._tickers_needed = False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._dataprovider: DataProvider | None = dataprovider
# REMOVED_UNUSED_CODE:         for pairlist_handler_config in self._config.get("pairlists", []):
# REMOVED_UNUSED_CODE:             pairlist_handler = PairListResolver.load_pairlist(
# REMOVED_UNUSED_CODE:                 pairlist_handler_config["method"],
# REMOVED_UNUSED_CODE:                 exchange=exchange,
# REMOVED_UNUSED_CODE:                 pairlistmanager=self,
# REMOVED_UNUSED_CODE:                 config=config,
# REMOVED_UNUSED_CODE:                 pairlistconfig=pairlist_handler_config,
# REMOVED_UNUSED_CODE:                 pairlist_pos=len(self._pairlist_handlers),
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             self._tickers_needed |= pairlist_handler.needstickers
# REMOVED_UNUSED_CODE:             self._pairlist_handlers.append(pairlist_handler)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not self._pairlist_handlers:
# REMOVED_UNUSED_CODE:             raise OperationalException("No Pairlist Handlers defined")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self._tickers_needed and not self._exchange.exchange_has("fetchTickers"):
# REMOVED_UNUSED_CODE:             invalid = ". ".join([p.name for p in self._pairlist_handlers if p.needstickers])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 "Exchange does not support fetchTickers, therefore the following pairlists "
# REMOVED_UNUSED_CODE:                 "cannot be used. Please edit your config and restart the bot.\n"
# REMOVED_UNUSED_CODE:                 f"{invalid}."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._check_backtest()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         refresh_period = config.get("pairlist_refresh_period", 3600)
# REMOVED_UNUSED_CODE:         LoggingMixin.__init__(self, logger, refresh_period)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _check_backtest(self) -> None:
# REMOVED_UNUSED_CODE:         if self._config["runmode"] not in (RunMode.BACKTEST, RunMode.EDGE, RunMode.HYPEROPT):
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         pairlist_errors: list[str] = []
# REMOVED_UNUSED_CODE:         noaction_pairlists: list[str] = []
# REMOVED_UNUSED_CODE:         biased_pairlists: list[str] = []
# REMOVED_UNUSED_CODE:         for pairlist_handler in self._pairlist_handlers:
# REMOVED_UNUSED_CODE:             if pairlist_handler.supports_backtesting == SupportsBacktesting.NO:
# REMOVED_UNUSED_CODE:                 pairlist_errors.append(pairlist_handler.name)
# REMOVED_UNUSED_CODE:             if pairlist_handler.supports_backtesting == SupportsBacktesting.NO_ACTION:
# REMOVED_UNUSED_CODE:                 noaction_pairlists.append(pairlist_handler.name)
# REMOVED_UNUSED_CODE:             if pairlist_handler.supports_backtesting == SupportsBacktesting.BIASED:
# REMOVED_UNUSED_CODE:                 biased_pairlists.append(pairlist_handler.name)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if noaction_pairlists:
# REMOVED_UNUSED_CODE:             logger.warning(
# REMOVED_UNUSED_CODE:                 f"Pairlist Handlers {', '.join(noaction_pairlists)} do not generate "
# REMOVED_UNUSED_CODE:                 "any changes during backtesting. While it's safe to leave them enabled, they will "
# REMOVED_UNUSED_CODE:                 "not behave like in dry/live modes. "
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if biased_pairlists:
# REMOVED_UNUSED_CODE:             logger.warning(
# REMOVED_UNUSED_CODE:                 f"Pairlist Handlers {', '.join(biased_pairlists)} will introduce a lookahead bias "
# REMOVED_UNUSED_CODE:                 "to your backtest results, as they use today's data - which inheritly suffers from "
# REMOVED_UNUSED_CODE:                 "'winner bias'."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         if pairlist_errors:
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 f"Pairlist Handlers {', '.join(pairlist_errors)} do not support backtesting."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def whitelist(self) -> list[str]:
# REMOVED_UNUSED_CODE:         """The current whitelist"""
# REMOVED_UNUSED_CODE:         return self._whitelist
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def blacklist(self) -> list[str]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         The current blacklist
# REMOVED_UNUSED_CODE:         -> no need to overwrite in subclasses
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return self._blacklist
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def expanded_blacklist(self) -> list[str]:
# REMOVED_UNUSED_CODE:         """The expanded blacklist (including wildcard expansion)"""
# REMOVED_UNUSED_CODE:         return expand_pairlist(self._blacklist, self._exchange.get_markets().keys())
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def name_list(self) -> list[str]:
# REMOVED_UNUSED_CODE:         """Get list of loaded Pairlist Handler names"""
# REMOVED_UNUSED_CODE:         return [p.name for p in self._pairlist_handlers]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def short_desc(self) -> list[dict]:
# REMOVED_UNUSED_CODE:         """List of short_desc for each Pairlist Handler"""
# REMOVED_UNUSED_CODE:         return [{p.name: p.short_desc()} for p in self._pairlist_handlers]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @cached(TTLCache(maxsize=1, ttl=1800))
# REMOVED_UNUSED_CODE:     def _get_cached_tickers(self) -> Tickers:
# REMOVED_UNUSED_CODE:         return self._exchange.get_tickers()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def refresh_pairlist(self) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Run pairlist through all configured Pairlist Handlers."""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Tickers should be cached to avoid calling the exchange on each call.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         tickers: dict = {}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._tickers_needed:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             tickers = self._get_cached_tickers()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Generate the pairlist with first Pairlist Handler in the chain
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pairlist = self._pairlist_handlers[0].gen_pairlist(tickers)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Process all Pairlist Handlers in the chain
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # except for the first one, which is the generator.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for pairlist_handler in self._pairlist_handlers[1:]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             pairlist = pairlist_handler.filter_pairlist(pairlist, tickers)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Validation against blacklist happens after the chain of Pairlist Handlers
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # to ensure blacklist is respected.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pairlist = self.verify_blacklist(pairlist, logger.warning)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.log_once(f"Whitelist with {len(pairlist)} pairs: {pairlist}", logger.info)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._whitelist = pairlist
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def verify_blacklist(self, pairlist: list[str], logmethod) -> list[str]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Verify and remove items from pairlist - returning a filtered pairlist.
# REMOVED_UNUSED_CODE:         Logs a warning or info depending on `aswarning`.
# REMOVED_UNUSED_CODE:         Pairlist Handlers explicitly using this method shall use
# REMOVED_UNUSED_CODE:         `logmethod=logger.info` to avoid spamming with warning messages
# REMOVED_UNUSED_CODE:         :param pairlist: Pairlist to validate
# REMOVED_UNUSED_CODE:         :param logmethod: Function that'll be called, `logger.info` or `logger.warning`.
# REMOVED_UNUSED_CODE:         :return: pairlist - blacklisted pairs
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             blacklist = self.expanded_blacklist
# REMOVED_UNUSED_CODE:         except ValueError as err:
# REMOVED_UNUSED_CODE:             logger.error(f"Pair blacklist contains an invalid Wildcard: {err}")
# REMOVED_UNUSED_CODE:             return []
# REMOVED_UNUSED_CODE:         log_once = partial(self.log_once, logmethod=logmethod)
# REMOVED_UNUSED_CODE:         for pair in pairlist.copy():
# REMOVED_UNUSED_CODE:             if pair in blacklist:
# REMOVED_UNUSED_CODE:                 log_once(f"Pair {pair} in your blacklist. Removing it from whitelist...")
# REMOVED_UNUSED_CODE:                 pairlist.remove(pair)
# REMOVED_UNUSED_CODE:         return pairlist
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def verify_whitelist(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, pairlist: list[str], logmethod, keep_invalid: bool = False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> list[str]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Verify and remove items from pairlist - returning a filtered pairlist.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Logs a warning or info depending on `aswarning`.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Pairlist Handlers explicitly using this method shall use
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         `logmethod=logger.info` to avoid spamming with warning messages
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pairlist: Pairlist to validate
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param logmethod: Function that'll be called, `logger.info` or `logger.warning`
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param keep_invalid: If sets to True, drops invalid pairs silently while expanding regexes.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: pairlist - whitelisted pairs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             whitelist = expand_pairlist(pairlist, self._exchange.get_markets().keys(), keep_invalid)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         except ValueError as err:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             logger.error(f"Pair whitelist contains an invalid Wildcard: {err}")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return whitelist
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def create_pair_list(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, pairs: list[str], timeframe: str | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> ListPairsWithTimeframes:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Create list of pair tuples with (pair, timeframe)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return [
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 pair,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 timeframe or self._config["timeframe"],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self._config.get("candle_type_def", CandleType.SPOT),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for pair in pairs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ]
