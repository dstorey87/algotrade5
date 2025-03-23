"""Kraken exchange subclass"""

import logging
# REMOVED_UNUSED_CODE: from datetime import datetime
# REMOVED_UNUSED_CODE: from typing import Any

# REMOVED_UNUSED_CODE: import ccxt
# REMOVED_UNUSED_CODE: from pandas import DataFrame

# REMOVED_UNUSED_CODE: from freqtrade.constants import BuySell
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.enums import MarginMode, TradingMode
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.exceptions import DDosProtection, OperationalException, TemporaryError
# REMOVED_UNUSED_CODE: from freqtrade.exchange import Exchange
# REMOVED_UNUSED_CODE: from freqtrade.exchange.common import retrier
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.exchange.exchange_types import CcxtBalances, FtHas, Tickers


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class Kraken(Exchange):
# REMOVED_UNUSED_CODE:     _params: dict = {"trading_agreement": "agree"}
# REMOVED_UNUSED_CODE:     _ft_has: FtHas = {
# REMOVED_UNUSED_CODE:         "stoploss_on_exchange": True,
# REMOVED_UNUSED_CODE:         "stop_price_param": "stopLossPrice",
# REMOVED_UNUSED_CODE:         "stop_price_prop": "stopLossPrice",
# REMOVED_UNUSED_CODE:         "stoploss_order_types": {"limit": "limit", "market": "market"},
# REMOVED_UNUSED_CODE:         "order_time_in_force": ["GTC", "IOC", "PO"],
# REMOVED_UNUSED_CODE:         "ohlcv_has_history": False,
# REMOVED_UNUSED_CODE:         "trades_pagination": "id",
# REMOVED_UNUSED_CODE:         "trades_pagination_arg": "since",
# REMOVED_UNUSED_CODE:         "trades_pagination_overlap": False,
# REMOVED_UNUSED_CODE:         "trades_has_history": True,
# REMOVED_UNUSED_CODE:         "mark_ohlcv_timeframe": "4h",
# REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     _supported_trading_mode_margin_pairs: list[tuple[TradingMode, MarginMode]] = [
# REMOVED_UNUSED_CODE:         # TradingMode.SPOT always supported and not required in this list
# REMOVED_UNUSED_CODE:         # (TradingMode.MARGIN, MarginMode.CROSS),
# REMOVED_UNUSED_CODE:         # (TradingMode.FUTURES, MarginMode.CROSS)
# REMOVED_UNUSED_CODE:     ]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def market_is_tradable(self, market: dict[str, Any]) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Check if the market symbol is tradable by Freqtrade.
# REMOVED_UNUSED_CODE:         Default checks + check if pair is darkpool pair.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         parent_check = super().market_is_tradable(market)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return parent_check and market.get("darkpool", False) is False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def get_tickers(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         symbols: list[str] | None = None,
# REMOVED_UNUSED_CODE:         *,
# REMOVED_UNUSED_CODE:         cached: bool = False,
# REMOVED_UNUSED_CODE:         market_type: TradingMode | None = None,
# REMOVED_UNUSED_CODE:     ) -> Tickers:
# REMOVED_UNUSED_CODE:         # Only fetch tickers for current stake currency
# REMOVED_UNUSED_CODE:         # Otherwise the request for kraken becomes too large.
# REMOVED_UNUSED_CODE:         symbols = list(self.get_markets(quote_currencies=[self._config["stake_currency"]]))
# REMOVED_UNUSED_CODE:         return super().get_tickers(symbols=symbols, cached=cached, market_type=market_type)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def consolidate_balances(self, balances: CcxtBalances) -> CcxtBalances:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Consolidate balances for the same currency.
# REMOVED_UNUSED_CODE:         Kraken returns ".F" balances if rewards is enabled.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         consolidated: CcxtBalances = {}
# REMOVED_UNUSED_CODE:         for currency, balance in balances.items():
# REMOVED_UNUSED_CODE:             base_currency = currency[:-2] if currency.endswith(".F") else currency
# REMOVED_UNUSED_CODE:             base_currency = self._api.commonCurrencies.get(base_currency, base_currency)
# REMOVED_UNUSED_CODE:             if base_currency in consolidated:
# REMOVED_UNUSED_CODE:                 consolidated[base_currency]["free"] += balance["free"]
# REMOVED_UNUSED_CODE:                 consolidated[base_currency]["used"] += balance["used"]
# REMOVED_UNUSED_CODE:                 consolidated[base_currency]["total"] += balance["total"]
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 consolidated[base_currency] = balance
# REMOVED_UNUSED_CODE:         return consolidated
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @retrier
# REMOVED_UNUSED_CODE:     def get_balances(self) -> CcxtBalances:
# REMOVED_UNUSED_CODE:         if self._config["dry_run"]:
# REMOVED_UNUSED_CODE:             return {}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             balances = self._api.fetch_balance()
# REMOVED_UNUSED_CODE:             # Remove additional info from ccxt results
# REMOVED_UNUSED_CODE:             balances.pop("info", None)
# REMOVED_UNUSED_CODE:             balances.pop("free", None)
# REMOVED_UNUSED_CODE:             balances.pop("total", None)
# REMOVED_UNUSED_CODE:             balances.pop("used", None)
# REMOVED_UNUSED_CODE:             self._log_exchange_response("fetch_balances", balances)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # Consolidate balances
# REMOVED_UNUSED_CODE:             balances = self.consolidate_balances(balances)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             orders = self._api.fetch_open_orders()
# REMOVED_UNUSED_CODE:             order_list = [
# REMOVED_UNUSED_CODE:                 (
# REMOVED_UNUSED_CODE:                     x["symbol"].split("/")[0 if x["side"] == "sell" else 1],
# REMOVED_UNUSED_CODE:                     x["remaining"] if x["side"] == "sell" else x["remaining"] * x["price"],
# REMOVED_UNUSED_CODE:                     # Don't remove the below comment, this can be important for debugging
# REMOVED_UNUSED_CODE:                     # x["side"], x["amount"],
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 for x in orders
# REMOVED_UNUSED_CODE:                 if x["remaining"] is not None and (x["side"] == "sell" or x["price"] is not None)
# REMOVED_UNUSED_CODE:             ]
# REMOVED_UNUSED_CODE:             for bal in balances:
# REMOVED_UNUSED_CODE:                 if not isinstance(balances[bal], dict):
# REMOVED_UNUSED_CODE:                     continue
# REMOVED_UNUSED_CODE:                 balances[bal]["used"] = sum(order[1] for order in order_list if order[0] == bal)
# REMOVED_UNUSED_CODE:                 balances[bal]["free"] = balances[bal]["total"] - balances[bal]["used"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             self._log_exchange_response("fetch_balances2", balances)
# REMOVED_UNUSED_CODE:             return balances
# REMOVED_UNUSED_CODE:         except ccxt.DDoSProtection as e:
# REMOVED_UNUSED_CODE:             raise DDosProtection(e) from e
# REMOVED_UNUSED_CODE:         except (ccxt.OperationFailed, ccxt.ExchangeError) as e:
# REMOVED_UNUSED_CODE:             raise TemporaryError(
# REMOVED_UNUSED_CODE:                 f"Could not get balance due to {e.__class__.__name__}. Message: {e}"
# REMOVED_UNUSED_CODE:             ) from e
# REMOVED_UNUSED_CODE:         except ccxt.BaseError as e:
# REMOVED_UNUSED_CODE:             raise OperationalException(e) from e
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _set_leverage(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         leverage: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair: str | None = None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         accept_fail: bool = False,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Kraken set's the leverage as an option in the order object, so we need to
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         add it to params
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _get_params(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         side: BuySell,
# REMOVED_UNUSED_CODE:         ordertype: str,
# REMOVED_UNUSED_CODE:         leverage: float,
# REMOVED_UNUSED_CODE:         reduceOnly: bool,
# REMOVED_UNUSED_CODE:         time_in_force: str = "GTC",
# REMOVED_UNUSED_CODE:     ) -> dict:
# REMOVED_UNUSED_CODE:         params = super()._get_params(
# REMOVED_UNUSED_CODE:             side=side,
# REMOVED_UNUSED_CODE:             ordertype=ordertype,
# REMOVED_UNUSED_CODE:             leverage=leverage,
# REMOVED_UNUSED_CODE:             reduceOnly=reduceOnly,
# REMOVED_UNUSED_CODE:             time_in_force=time_in_force,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         if leverage > 1.0:
# REMOVED_UNUSED_CODE:             params["leverage"] = round(leverage)
# REMOVED_UNUSED_CODE:         if time_in_force == "PO":
# REMOVED_UNUSED_CODE:             params.pop("timeInForce", None)
# REMOVED_UNUSED_CODE:             params["postOnly"] = True
# REMOVED_UNUSED_CODE:         return params
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def calculate_funding_fees(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         df: DataFrame,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         amount: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         is_short: bool,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         open_date: datetime,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         close_date: datetime,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         time_in_ratio: float | None = None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> float:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # ! This method will always error when run by Freqtrade because time_in_ratio is never
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # ! passed to _get_funding_fee. For kraken futures to work in dry run and backtesting
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # ! functionality must be added that passes the parameter time_in_ratio to
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # ! _get_funding_fee when using Kraken
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         calculates the sum of all funding fees that occurred for a pair during a futures trade
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param df: Dataframe containing combined funding and mark rates
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                    as `open_fund` and `open_mark`.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param amount: The quantity of the trade
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param is_short: trade direction
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param open_date: The date and time that the trade started
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param close_date: The date and time that the trade ended
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param time_in_ratio: Not used by most exchange classes
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not time_in_ratio:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"time_in_ratio is required for {self.name}._get_funding_fee"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         fees: float = 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not df.empty:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             df = df[(df["date"] >= open_date) & (df["date"] <= close_date)]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             fees = sum(df["open_fund"] * df["open_mark"] * amount * time_in_ratio)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return fees if is_short else -fees
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _get_trade_pagination_next_value(self, trades: list[dict]):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Extract pagination id for the next "from_id" value
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Applies only to fetch_trade_history by id.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if len(trades) > 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if isinstance(trades[-1].get("info"), list) and len(trades[-1].get("info", [])) > 7:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # Trade response's "last" value.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return trades[-1].get("info", [])[-1]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Fall back to timestamp if info is somehow empty.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return trades[-1].get("timestamp")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _valid_trade_pagination_id(self, pair: str, from_id: str) -> bool:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Verify trade-pagination id is valid.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Workaround for odd Kraken issue where ID is sometimes wrong.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Regular id's are in timestamp format 1705443695120072285
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # If the id is smaller than 19 characters, it's not a valid timestamp.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if len(from_id) >= 19:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.debug(f"{pair} - trade-pagination id is not valid. Fallback to timestamp.")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return False
