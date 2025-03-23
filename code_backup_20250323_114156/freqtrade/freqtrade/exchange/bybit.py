"""Bybit exchange subclass"""

import logging
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from datetime import datetime, timedelta
# REMOVED_UNUSED_CODE: from typing import Any

# REMOVED_UNUSED_CODE: import ccxt

# REMOVED_UNUSED_CODE: from freqtrade.constants import BuySell
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.enums import MarginMode, PriceType, TradingMode
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.exceptions import DDosProtection, ExchangeError, OperationalException, TemporaryError
# REMOVED_UNUSED_CODE: from freqtrade.exchange import Exchange
# REMOVED_UNUSED_CODE: from freqtrade.exchange.common import retrier
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.exchange.exchange_types import CcxtOrder, FtHas
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.util.datetime_helpers import dt_now, dt_ts


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class Bybit(Exchange):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Bybit exchange class. Contains adjustments needed for Freqtrade to work
# REMOVED_UNUSED_CODE:     with this exchange.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Please note that this exchange is not included in the list of exchanges
# REMOVED_UNUSED_CODE:     officially supported by the Freqtrade development team. So some features
# REMOVED_UNUSED_CODE:     may still not work as expected.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     unified_account = False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     _ft_has: FtHas = {
# REMOVED_UNUSED_CODE:         "ohlcv_has_history": True,
# REMOVED_UNUSED_CODE:         "order_time_in_force": ["GTC", "FOK", "IOC", "PO"],
# REMOVED_UNUSED_CODE:         "ws_enabled": True,
# REMOVED_UNUSED_CODE:         "trades_has_history": False,  # Endpoint doesn't support pagination
# REMOVED_UNUSED_CODE:         "exchange_has_overrides": {
# REMOVED_UNUSED_CODE:             # Bybit spot does not support fetch_order
# REMOVED_UNUSED_CODE:             # Unless the account is unified.
# REMOVED_UNUSED_CODE:             # TODO: Can be removed once bybit fully forces all accounts to unified mode.
# REMOVED_UNUSED_CODE:             "fetchOrder": False,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE:     _ft_has_futures: FtHas = {
# REMOVED_UNUSED_CODE:         "ohlcv_has_history": True,
# REMOVED_UNUSED_CODE:         "mark_ohlcv_timeframe": "4h",
# REMOVED_UNUSED_CODE:         "funding_fee_timeframe": "8h",
# REMOVED_UNUSED_CODE:         "funding_fee_candle_limit": 200,
# REMOVED_UNUSED_CODE:         "stoploss_on_exchange": True,
# REMOVED_UNUSED_CODE:         "stoploss_order_types": {"limit": "limit", "market": "market"},
# REMOVED_UNUSED_CODE:         # bybit response parsing fails to populate stopLossPrice
# REMOVED_UNUSED_CODE:         "stop_price_prop": "stopPrice",
# REMOVED_UNUSED_CODE:         "stop_price_type_field": "triggerBy",
# REMOVED_UNUSED_CODE:         "stop_price_type_value_mapping": {
# REMOVED_UNUSED_CODE:             PriceType.LAST: "LastPrice",
# REMOVED_UNUSED_CODE:             PriceType.MARK: "MarkPrice",
# REMOVED_UNUSED_CODE:             PriceType.INDEX: "IndexPrice",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "exchange_has_overrides": {
# REMOVED_UNUSED_CODE:             "fetchOrder": True,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     _supported_trading_mode_margin_pairs: list[tuple[TradingMode, MarginMode]] = [
# REMOVED_UNUSED_CODE:         # TradingMode.SPOT always supported and not required in this list
# REMOVED_UNUSED_CODE:         # (TradingMode.FUTURES, MarginMode.CROSS),
# REMOVED_UNUSED_CODE:         (TradingMode.FUTURES, MarginMode.ISOLATED)
# REMOVED_UNUSED_CODE:     ]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def _ccxt_config(self) -> dict:
# REMOVED_UNUSED_CODE:         # Parameters to add directly to ccxt sync/async initialization.
# REMOVED_UNUSED_CODE:         # ccxt defaults to swap mode.
# REMOVED_UNUSED_CODE:         config = {}
# REMOVED_UNUSED_CODE:         if self.trading_mode == TradingMode.SPOT:
# REMOVED_UNUSED_CODE:             config.update({"options": {"defaultType": "spot"}})
# REMOVED_UNUSED_CODE:         config.update(super()._ccxt_config)
# REMOVED_UNUSED_CODE:         return config
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def market_is_future(self, market: dict[str, Any]) -> bool:
# REMOVED_UNUSED_CODE:         main = super().market_is_future(market)
# REMOVED_UNUSED_CODE:         # For ByBit, we'll only support USDT markets for now.
# REMOVED_UNUSED_CODE:         return main and market["settle"] == "USDT"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @retrier
# REMOVED_UNUSED_CODE:     def additional_exchange_init(self) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Additional exchange initialization logic.
# REMOVED_UNUSED_CODE:         .api will be available at this point.
# REMOVED_UNUSED_CODE:         Must be overridden in child methods if required.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             if not self._config["dry_run"]:
# REMOVED_UNUSED_CODE:                 if self.trading_mode == TradingMode.FUTURES:
# REMOVED_UNUSED_CODE:                     position_mode = self._api.set_position_mode(False)
# REMOVED_UNUSED_CODE:                     self._log_exchange_response("set_position_mode", position_mode)
# REMOVED_UNUSED_CODE:                 is_unified = self._api.is_unified_enabled()
# REMOVED_UNUSED_CODE:                 # Returns a tuple of bools, first for margin, second for Account
# REMOVED_UNUSED_CODE:                 if is_unified and len(is_unified) > 1 and is_unified[1]:
# REMOVED_UNUSED_CODE:                     self.unified_account = True
# REMOVED_UNUSED_CODE:                     logger.info(
# REMOVED_UNUSED_CODE:                         "Bybit: Unified account. Assuming dedicated subaccount for this bot."
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE:                     self.unified_account = False
# REMOVED_UNUSED_CODE:                     logger.info("Bybit: Standard account.")
# REMOVED_UNUSED_CODE:         except ccxt.DDoSProtection as e:
# REMOVED_UNUSED_CODE:             raise DDosProtection(e) from e
# REMOVED_UNUSED_CODE:         except (ccxt.OperationFailed, ccxt.ExchangeError) as e:
# REMOVED_UNUSED_CODE:             raise TemporaryError(
# REMOVED_UNUSED_CODE:                 f"Error in additional_exchange_init due to {e.__class__.__name__}. Message: {e}"
# REMOVED_UNUSED_CODE:             ) from e
# REMOVED_UNUSED_CODE:         except ccxt.BaseError as e:
# REMOVED_UNUSED_CODE:             raise OperationalException(e) from e
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _lev_prep(self, pair: str, leverage: float, side: BuySell, accept_fail: bool = False):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.trading_mode != TradingMode.SPOT:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             params = {"leverage": leverage}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.set_margin_mode(pair, self.margin_mode, accept_fail=True, params=params)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._set_leverage(leverage, pair, accept_fail=True)
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
# REMOVED_UNUSED_CODE:         if self.trading_mode == TradingMode.FUTURES and self.margin_mode:
# REMOVED_UNUSED_CODE:             params["position_idx"] = 0
# REMOVED_UNUSED_CODE:         return params
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _order_needs_price(self, side: BuySell, ordertype: str) -> bool:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Bybit requires price for market orders - but only for classic accounts,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # and only in spot mode
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ordertype != "market"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             or (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 side == "buy" and not self.unified_account and self.trading_mode == TradingMode.SPOT
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             or self._ft_has.get("marketOrderRequiresPrice", False)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def dry_run_liquidation_price(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         open_rate: float,  # Entry price of position
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         is_short: bool,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         amount: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         stake_amount: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         leverage: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         wallet_balance: float,  # Or margin balance
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         open_trades: list,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> float | None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Important: Must be fetching data from cached values as this is used by backtesting!
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         PERPETUAL:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:          bybit:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:           https://www.bybithelp.com/HelpCenterKnowledge/bybitHC_Article?language=en_US&id=000001067
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Long:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Liquidation Price = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             Entry Price * (1 - Initial Margin Rate + Maintenance Margin Rate)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             - Extra Margin Added/ Contract)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Short:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Liquidation Price = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             Entry Price * (1 + Initial Margin Rate - Maintenance Margin Rate)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             + Extra Margin Added/ Contract)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Implementation Note: Extra margin is currently not used.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pair: Pair to calculate liquidation price for
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param open_rate: Entry price of position
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param is_short: True if the trade is a short, false otherwise
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param amount: Absolute value of position size incl. leverage (in base currency)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param stake_amount: Stake amount - Collateral in settle currency.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param leverage: Leverage used for this position.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param trading_mode: SPOT, MARGIN, FUTURES, etc.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param margin_mode: Either ISOLATED or CROSS
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param wallet_balance: Amount of margin_mode in the wallet being used to trade
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             Cross-Margin Mode: crossWalletBalance
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             Isolated-Margin Mode: isolatedWalletBalance
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param open_trades: List of other open trades in the same wallet
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         market = self.markets[pair]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         mm_ratio, _ = self.get_maintenance_ratio_and_amt(pair, stake_amount)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.trading_mode == TradingMode.FUTURES and self.margin_mode == MarginMode.ISOLATED:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if market["inverse"]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 raise OperationalException("Freqtrade does not yet support inverse contracts")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             initial_margin_rate = 1 / leverage
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # See docstring - ignores extra margin!
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if is_short:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return open_rate * (1 + initial_margin_rate - mm_ratio)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return open_rate * (1 - initial_margin_rate + mm_ratio)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "Freqtrade only supports isolated futures for leverage trading"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_funding_fees(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, pair: str, amount: float, is_short: bool, open_date: datetime
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> float:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Fetch funding fees, either from the exchange (live) or calculates them
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         based on funding rate/mark price history
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pair: The quote/base pair of the trade
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param is_short: trade direction
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param amount: Trade amount
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param open_date: Open date of the trade
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: funding fee since open_date
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :raises: ExchangeError if something goes wrong.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Bybit does not provide "applied" funding fees per position.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.trading_mode == TradingMode.FUTURES:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return self._fetch_and_calculate_funding_fees(pair, amount, is_short, open_date)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             except ExchangeError:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 logger.warning(f"Could not update funding fees for {pair}.")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return 0.0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def fetch_orders(
# REMOVED_UNUSED_CODE:         self, pair: str, since: datetime, params: dict | None = None
# REMOVED_UNUSED_CODE:     ) -> list[CcxtOrder]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Fetch all orders for a pair "since"
# REMOVED_UNUSED_CODE:         :param pair: Pair for the query
# REMOVED_UNUSED_CODE:         :param since: Starting time for the query
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         # On bybit, the distance between since and "until" can't exceed 7 days.
# REMOVED_UNUSED_CODE:         # we therefore need to split the query into multiple queries.
# REMOVED_UNUSED_CODE:         orders = []
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         while since < dt_now():
# REMOVED_UNUSED_CODE:             until = since + timedelta(days=7, minutes=-1)
# REMOVED_UNUSED_CODE:             orders += super().fetch_orders(pair, since, params={"until": dt_ts(until)})
# REMOVED_UNUSED_CODE:             since = until
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return orders
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def fetch_order(self, order_id: str, pair: str, params: dict | None = None) -> CcxtOrder:
# REMOVED_UNUSED_CODE:         if self.exchange_has("fetchOrder"):
# REMOVED_UNUSED_CODE:             # Set acknowledged to True to avoid ccxt exception
# REMOVED_UNUSED_CODE:             params = {"acknowledged": True}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         order = super().fetch_order(order_id, pair, params)
# REMOVED_UNUSED_CODE:         if not order:
# REMOVED_UNUSED_CODE:             order = self.fetch_order_emulated(order_id, pair, {})
# REMOVED_UNUSED_CODE:         if (
# REMOVED_UNUSED_CODE:             order.get("status") == "canceled"
# REMOVED_UNUSED_CODE:             and order.get("filled") == 0.0
# REMOVED_UNUSED_CODE:             and order.get("remaining") == 0.0
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             # Canceled orders will have "remaining=0" on bybit.
# REMOVED_UNUSED_CODE:             order["remaining"] = None
# REMOVED_UNUSED_CODE:         return order
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @retrier
# REMOVED_UNUSED_CODE:     def get_leverage_tiers(self) -> dict[str, list[dict]]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Cache leverage tiers for 1 day, since they are not expected to change often, and
# REMOVED_UNUSED_CODE:         bybit requires pagination to fetch all tiers.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Load cached tiers
# REMOVED_UNUSED_CODE:         tiers_cached = self.load_cached_leverage_tiers(
# REMOVED_UNUSED_CODE:             self._config["stake_currency"], timedelta(days=1)
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         if tiers_cached:
# REMOVED_UNUSED_CODE:             return tiers_cached
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Fetch tiers from exchange
# REMOVED_UNUSED_CODE:         tiers = super().get_leverage_tiers()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.cache_leverage_tiers(tiers, self._config["stake_currency"])
# REMOVED_UNUSED_CODE:         return tiers
