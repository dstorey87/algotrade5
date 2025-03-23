"""
PairList Handler base class
"""

import logging
from abc import ABC, abstractmethod
from copy import deepcopy
from enum import Enum
from typing import Any, Literal, TypedDict

from freqtrade.constants import Config
from freqtrade.exceptions import OperationalException
from freqtrade.exchange import Exchange, market_is_active
from freqtrade.exchange.exchange_types import Ticker, Tickers
from freqtrade.mixins import LoggingMixin


logger = logging.getLogger(__name__)


class __PairlistParameterBase(TypedDict):
# REMOVED_UNUSED_CODE:     description: str
# REMOVED_UNUSED_CODE:     help: str


class __NumberPairlistParameter(__PairlistParameterBase):
# REMOVED_UNUSED_CODE:     type: Literal["number"]
# REMOVED_UNUSED_CODE:     default: int | float | None


class __StringPairlistParameter(__PairlistParameterBase):
# REMOVED_UNUSED_CODE:     type: Literal["string"]
# REMOVED_UNUSED_CODE:     default: str | None


class __OptionPairlistParameter(__PairlistParameterBase):
# REMOVED_UNUSED_CODE:     type: Literal["option"]
# REMOVED_UNUSED_CODE:     default: str | None
# REMOVED_UNUSED_CODE:     options: list[str]


class __ListPairListParamenter(__PairlistParameterBase):
# REMOVED_UNUSED_CODE:     type: Literal["list"]
# REMOVED_UNUSED_CODE:     default: list[str] | None


class __BoolPairlistParameter(__PairlistParameterBase):
# REMOVED_UNUSED_CODE:     type: Literal["boolean"]
# REMOVED_UNUSED_CODE:     default: bool | None


PairlistParameter = (
    __NumberPairlistParameter
    | __StringPairlistParameter
    | __OptionPairlistParameter
    | __BoolPairlistParameter
    | __ListPairListParamenter
)


class SupportsBacktesting(str, Enum):
    """
    Enum to indicate if a Pairlist Handler supports backtesting.
    """

# REMOVED_UNUSED_CODE:     YES = "yes"
    NO = "no"
# REMOVED_UNUSED_CODE:     NO_ACTION = "no_action"
# REMOVED_UNUSED_CODE:     BIASED = "biased"


# REMOVED_UNUSED_CODE: class IPairList(LoggingMixin, ABC):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     is_pairlist_generator = False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     supports_backtesting: SupportsBacktesting = SupportsBacktesting.NO
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         exchange: Exchange,
# REMOVED_UNUSED_CODE:         pairlistmanager,
# REMOVED_UNUSED_CODE:         config: Config,
# REMOVED_UNUSED_CODE:         pairlistconfig: dict[str, Any],
# REMOVED_UNUSED_CODE:         pairlist_pos: int,
# REMOVED_UNUSED_CODE:     ) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         :param exchange: Exchange instance
# REMOVED_UNUSED_CODE:         :param pairlistmanager: Instantiated Pairlist manager
# REMOVED_UNUSED_CODE:         :param config: Global bot configuration
# REMOVED_UNUSED_CODE:         :param pairlistconfig: Configuration for this Pairlist Handler - can be empty.
# REMOVED_UNUSED_CODE:         :param pairlist_pos: Position of the Pairlist Handler in the chain
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self._enabled = True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._exchange: Exchange = exchange
# REMOVED_UNUSED_CODE:         self._pairlistmanager = pairlistmanager
# REMOVED_UNUSED_CODE:         self._config = config
# REMOVED_UNUSED_CODE:         self._pairlistconfig = pairlistconfig
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._pairlist_pos = pairlist_pos
# REMOVED_UNUSED_CODE:         self.refresh_period = self._pairlistconfig.get("refresh_period", 1800)
# REMOVED_UNUSED_CODE:         LoggingMixin.__init__(self, logger, self.refresh_period)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def name(self) -> str:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Gets name of the class
# REMOVED_UNUSED_CODE:         -> no need to overwrite in subclasses
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return self.__class__.__name__
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     @abstractmethod
# REMOVED_UNUSED_CODE:     def needstickers(self) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Boolean property defining if tickers are necessary.
# REMOVED_UNUSED_CODE:         If no Pairlist requires tickers, an empty Dict is passed
# REMOVED_UNUSED_CODE:         as tickers argument to filter_pairlist
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     @abstractmethod
# REMOVED_UNUSED_CODE:     def description() -> str:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Return description of this Pairlist Handler
# REMOVED_UNUSED_CODE:         -> Please overwrite in subclasses
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return ""
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def available_parameters() -> dict[str, PairlistParameter]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Return parameters used by this Pairlist Handler, and their type
# REMOVED_UNUSED_CODE:         contains a dictionary with the parameter name as key, and a dictionary
# REMOVED_UNUSED_CODE:         with the type and default value.
# REMOVED_UNUSED_CODE:         -> Please overwrite in subclasses
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return {}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def refresh_period_parameter() -> dict[str, PairlistParameter]:
# REMOVED_UNUSED_CODE:         return {
# REMOVED_UNUSED_CODE:             "refresh_period": {
# REMOVED_UNUSED_CODE:                 "type": "number",
# REMOVED_UNUSED_CODE:                 "default": 1800,
# REMOVED_UNUSED_CODE:                 "description": "Refresh period",
# REMOVED_UNUSED_CODE:                 "help": "Refresh period in seconds",
# REMOVED_UNUSED_CODE:             }
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @abstractmethod
# REMOVED_UNUSED_CODE:     def short_desc(self) -> str:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Short whitelist method description - used for startup-messages
# REMOVED_UNUSED_CODE:         -> Please overwrite in subclasses
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _validate_pair(self, pair: str, ticker: Ticker | None) -> bool:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Check one pair against Pairlist Handler's specific conditions.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Either implement it in the Pairlist Handler or override the generic
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         filter_pairlist() method.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pair: Pair that's currently validated
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param ticker: ticker dict as returned from ccxt.fetch_ticker
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: True if the pair can stay, false if it should be removed
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         raise NotImplementedError()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def gen_pairlist(self, tickers: Tickers) -> list[str]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Generate the pairlist.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         This method is called once by the pairlistmanager in the refresh_pairlist()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         method to supply the starting pairlist for the chain of the Pairlist Handlers.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Pairlist Filters (those Pairlist Handlers that cannot be used at the first
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         position in the chain) shall not override this base implementation --
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         it will raise the exception if a Pairlist Handler is used at the first
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         position in the chain.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param tickers: Tickers (from exchange.get_tickers). May be cached.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: List of pairs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         raise OperationalException(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "This Pairlist Handler should not be used "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "at the first position in the list of Pairlist Handlers."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def filter_pairlist(self, pairlist: list[str], tickers: Tickers) -> list[str]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Filters and sorts pairlist and returns the whitelist again.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Called on each bot iteration - please use internal caching if necessary
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         This generic implementation calls self._validate_pair() for each pair
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         in the pairlist.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Some Pairlist Handlers override this generic implementation and employ
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         own filtration.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pairlist: pairlist to filter or sort
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param tickers: Tickers (from exchange.get_tickers). May be cached.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: new whitelist
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._enabled:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Copy list since we're modifying this list
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for p in deepcopy(pairlist):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # Filter out assets
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if not self._validate_pair(p, tickers[p] if p in tickers else None):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     pairlist.remove(p)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return pairlist
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def verify_blacklist(self, pairlist: list[str], logmethod) -> list[str]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Proxy method to verify_blacklist for easy access for child classes.
# REMOVED_UNUSED_CODE:         :param pairlist: Pairlist to validate
# REMOVED_UNUSED_CODE:         :param logmethod: Function that'll be called, `logger.info` or `logger.warning`.
# REMOVED_UNUSED_CODE:         :return: pairlist - blacklisted pairs
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return self._pairlistmanager.verify_blacklist(pairlist, logmethod)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def verify_whitelist(
# REMOVED_UNUSED_CODE:         self, pairlist: list[str], logmethod, keep_invalid: bool = False
# REMOVED_UNUSED_CODE:     ) -> list[str]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Proxy method to verify_whitelist for easy access for child classes.
# REMOVED_UNUSED_CODE:         :param pairlist: Pairlist to validate
# REMOVED_UNUSED_CODE:         :param logmethod: Function that'll be called, `logger.info` or `logger.warning`
# REMOVED_UNUSED_CODE:         :param keep_invalid: If sets to True, drops invalid pairs silently while expanding regexes.
# REMOVED_UNUSED_CODE:         :return: pairlist - whitelisted pairs
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return self._pairlistmanager.verify_whitelist(pairlist, logmethod, keep_invalid)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _whitelist_for_active_markets(self, pairlist: list[str]) -> list[str]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Check available markets and remove pair from whitelist if necessary
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pairlist: the sorted list of pairs the user might want to trade
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: the list of pairs the user wants to trade without those unavailable or
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         black_listed
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         markets = self._exchange.markets
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not markets:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "Markets not loaded. Make sure that exchange is initialized correctly."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         sanitized_whitelist: list[str] = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for pair in pairlist:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # pair is not in the generated dynamic market or has the wrong stake currency
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if pair not in markets:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.log_once(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     f"Pair {pair} is not compatible with exchange "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     f"{self._exchange.name}. Removing it from whitelist..",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     logger.warning,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if not self._exchange.market_is_tradable(markets[pair]):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.log_once(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     f"Pair {pair} is not tradable with Freqtrade. Removing it from whitelist..",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     logger.warning,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if self._exchange.get_pair_quote_currency(pair) != self._config["stake_currency"]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.log_once(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     f"Pair {pair} is not compatible with your stake currency "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     f"{self._config['stake_currency']}. Removing it from whitelist..",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     logger.warning,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Check if market is active
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             market = markets[pair]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if not market_is_active(market):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.log_once(f"Ignoring {pair} from whitelist. Market is not active.", logger.info)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if pair not in sanitized_whitelist:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 sanitized_whitelist.append(pair)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # We need to remove pairs that are unknown
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return sanitized_whitelist
