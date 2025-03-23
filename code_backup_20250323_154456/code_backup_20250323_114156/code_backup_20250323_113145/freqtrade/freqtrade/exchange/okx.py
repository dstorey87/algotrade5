import logging
from datetime import timedelta

import ccxt

from freqtrade.constants import BuySell
from freqtrade.enums import CandleType, MarginMode, PriceType, TradingMode
from freqtrade.exceptions import (
    DDosProtection,
    OperationalException,
    RetryableOrderError,
    TemporaryError,
)
from freqtrade.exchange import Exchange, date_minus_candles
from freqtrade.exchange.common import API_RETRY_COUNT, retrier
from freqtrade.exchange.exchange_types import CcxtOrder, FtHas
from freqtrade.misc import safe_value_fallback2
from freqtrade.util import dt_now, dt_ts


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class Okx(Exchange):
# REMOVED_UNUSED_CODE:     """Okx exchange class.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Contains adjustments needed for Freqtrade to work with this exchange.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     _ft_has: FtHas = {
# REMOVED_UNUSED_CODE:         "ohlcv_candle_limit": 100,  # Warning, special case with data prior to X months
# REMOVED_UNUSED_CODE:         "mark_ohlcv_timeframe": "4h",
# REMOVED_UNUSED_CODE:         "funding_fee_timeframe": "8h",
# REMOVED_UNUSED_CODE:         "stoploss_order_types": {"limit": "limit"},
# REMOVED_UNUSED_CODE:         "stoploss_on_exchange": True,
# REMOVED_UNUSED_CODE:         "trades_has_history": False,  # Endpoint doesn't have a "since" parameter
# REMOVED_UNUSED_CODE:         "ws_enabled": True,
# REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE:     _ft_has_futures: FtHas = {
# REMOVED_UNUSED_CODE:         "tickers_have_quoteVolume": False,
# REMOVED_UNUSED_CODE:         "stop_price_type_field": "slTriggerPxType",
# REMOVED_UNUSED_CODE:         "stop_price_type_value_mapping": {
# REMOVED_UNUSED_CODE:             PriceType.LAST: "last",
# REMOVED_UNUSED_CODE:             PriceType.MARK: "index",
# REMOVED_UNUSED_CODE:             PriceType.INDEX: "mark",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "ws_enabled": True,
# REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     _supported_trading_mode_margin_pairs: list[tuple[TradingMode, MarginMode]] = [
# REMOVED_UNUSED_CODE:         # TradingMode.SPOT always supported and not required in this list
# REMOVED_UNUSED_CODE:         # (TradingMode.MARGIN, MarginMode.CROSS),
# REMOVED_UNUSED_CODE:         # (TradingMode.FUTURES, MarginMode.CROSS),
# REMOVED_UNUSED_CODE:         (TradingMode.FUTURES, MarginMode.ISOLATED),
# REMOVED_UNUSED_CODE:     ]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     net_only = True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     _ccxt_params: dict = {"options": {"brokerId": "ffb5405ad327SUDE"}}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def ohlcv_candle_limit(
# REMOVED_UNUSED_CODE:         self, timeframe: str, candle_type: CandleType, since_ms: int | None = None
# REMOVED_UNUSED_CODE:     ) -> int:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Exchange ohlcv candle limit
# REMOVED_UNUSED_CODE:         OKX has the following behaviour:
# REMOVED_UNUSED_CODE:         * 300 candles for up-to-date data
# REMOVED_UNUSED_CODE:         * 100 candles for historic data
# REMOVED_UNUSED_CODE:         * 100 candles for additional candles (not futures or spot).
# REMOVED_UNUSED_CODE:         :param timeframe: Timeframe to check
# REMOVED_UNUSED_CODE:         :param candle_type: Candle-type
# REMOVED_UNUSED_CODE:         :param since_ms: Starting timestamp
# REMOVED_UNUSED_CODE:         :return: Candle limit as integer
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if candle_type in (CandleType.FUTURES, CandleType.SPOT) and (
# REMOVED_UNUSED_CODE:             not since_ms or since_ms > (date_minus_candles(timeframe, 300).timestamp() * 1000)
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             return 300
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return super().ohlcv_candle_limit(timeframe, candle_type, since_ms)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @retrier
# REMOVED_UNUSED_CODE:     def additional_exchange_init(self) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Additional exchange initialization logic.
# REMOVED_UNUSED_CODE:         .api will be available at this point.
# REMOVED_UNUSED_CODE:         Must be overridden in child methods if required.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             if self.trading_mode == TradingMode.FUTURES and not self._config["dry_run"]:
# REMOVED_UNUSED_CODE:                 accounts = self._api.fetch_accounts()
# REMOVED_UNUSED_CODE:                 self._log_exchange_response("fetch_accounts", accounts)
# REMOVED_UNUSED_CODE:                 if len(accounts) > 0:
# REMOVED_UNUSED_CODE:                     self.net_only = accounts[0].get("info", {}).get("posMode") == "net_mode"
# REMOVED_UNUSED_CODE:         except ccxt.DDoSProtection as e:
# REMOVED_UNUSED_CODE:             raise DDosProtection(e) from e
# REMOVED_UNUSED_CODE:         except (ccxt.OperationFailed, ccxt.ExchangeError) as e:
# REMOVED_UNUSED_CODE:             raise TemporaryError(
# REMOVED_UNUSED_CODE:                 f"Error in additional_exchange_init due to {e.__class__.__name__}. Message: {e}"
# REMOVED_UNUSED_CODE:             ) from e
# REMOVED_UNUSED_CODE:         except ccxt.BaseError as e:
# REMOVED_UNUSED_CODE:             raise OperationalException(e) from e
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _get_posSide(self, side: BuySell, reduceOnly: bool):
# REMOVED_UNUSED_CODE:         if self.net_only:
# REMOVED_UNUSED_CODE:             return "net"
# REMOVED_UNUSED_CODE:         if not reduceOnly:
# REMOVED_UNUSED_CODE:             # Enter
# REMOVED_UNUSED_CODE:             return "long" if side == "buy" else "short"
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             # Exit
# REMOVED_UNUSED_CODE:             return "long" if side == "sell" else "short"
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
# REMOVED_UNUSED_CODE:             params["tdMode"] = self.margin_mode.value
# REMOVED_UNUSED_CODE:             params["posSide"] = self._get_posSide(side, reduceOnly)
# REMOVED_UNUSED_CODE:         return params
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __fetch_leverage_already_set(self, pair: str, leverage: float, side: BuySell) -> bool:
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             res_lev = self._api.fetch_leverage(
# REMOVED_UNUSED_CODE:                 symbol=pair,
# REMOVED_UNUSED_CODE:                 params={
# REMOVED_UNUSED_CODE:                     "mgnMode": self.margin_mode.value,
# REMOVED_UNUSED_CODE:                     "posSide": self._get_posSide(side, False),
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             self._log_exchange_response("get_leverage", res_lev)
# REMOVED_UNUSED_CODE:             already_set = all(float(x["lever"]) == leverage for x in res_lev["data"])
# REMOVED_UNUSED_CODE:             return already_set
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         except ccxt.BaseError:
# REMOVED_UNUSED_CODE:             # Assume all errors as "not set yet"
# REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @retrier
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _lev_prep(self, pair: str, leverage: float, side: BuySell, accept_fail: bool = False):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.trading_mode != TradingMode.SPOT and self.margin_mode is not None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 res = self._api.set_leverage(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     leverage=leverage,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     symbol=pair,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     params={
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         "mgnMode": self.margin_mode.value,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         "posSide": self._get_posSide(side, False),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     },
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self._log_exchange_response("set_leverage", res)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             except ccxt.DDoSProtection as e:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 raise DDosProtection(e) from e
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             except (ccxt.OperationFailed, ccxt.ExchangeError) as e:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 already_set = self.__fetch_leverage_already_set(pair, leverage, side)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if not already_set:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     raise TemporaryError(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         f"Could not set leverage due to {e.__class__.__name__}. Message: {e}"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     ) from e
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             except ccxt.BaseError as e:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 raise OperationalException(e) from e
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_max_pair_stake_amount(self, pair: str, price: float, leverage: float = 1.0) -> float:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.trading_mode == TradingMode.SPOT:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return float("inf")  # Not actually inf, but this probably won't matter for SPOT
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if pair not in self._leverage_tiers:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return float("inf")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair_tiers = self._leverage_tiers[pair]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return pair_tiers[-1]["maxNotional"] / leverage
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _get_stop_params(self, side: BuySell, ordertype: str, stop_price: float) -> dict:
# REMOVED_UNUSED_CODE:         params = super()._get_stop_params(side, ordertype, stop_price)
# REMOVED_UNUSED_CODE:         if self.trading_mode == TradingMode.FUTURES and self.margin_mode:
# REMOVED_UNUSED_CODE:             params["tdMode"] = self.margin_mode.value
# REMOVED_UNUSED_CODE:             params["posSide"] = self._get_posSide(side, True)
# REMOVED_UNUSED_CODE:         return params
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _convert_stop_order(self, pair: str, order_id: str, order: CcxtOrder) -> CcxtOrder:
# REMOVED_UNUSED_CODE:         if (
# REMOVED_UNUSED_CODE:             order.get("status", "open") == "closed"
# REMOVED_UNUSED_CODE:             and (real_order_id := order.get("info", {}).get("ordId")) is not None
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             # Once a order triggered, we fetch the regular followup order.
# REMOVED_UNUSED_CODE:             order_reg = self.fetch_order(real_order_id, pair)
# REMOVED_UNUSED_CODE:             self._log_exchange_response("fetch_stoploss_order1", order_reg)
# REMOVED_UNUSED_CODE:             order_reg["id_stop"] = order_reg["id"]
# REMOVED_UNUSED_CODE:             order_reg["id"] = order_id
# REMOVED_UNUSED_CODE:             order_reg["type"] = "stoploss"
# REMOVED_UNUSED_CODE:             order_reg["status_stop"] = "triggered"
# REMOVED_UNUSED_CODE:             return order_reg
# REMOVED_UNUSED_CODE:         order = self._order_contracts_to_amount(order)
# REMOVED_UNUSED_CODE:         order["type"] = "stoploss"
# REMOVED_UNUSED_CODE:         return order
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @retrier(retries=API_RETRY_COUNT)
# REMOVED_UNUSED_CODE:     def fetch_stoploss_order(
# REMOVED_UNUSED_CODE:         self, order_id: str, pair: str, params: dict | None = None
# REMOVED_UNUSED_CODE:     ) -> CcxtOrder:
# REMOVED_UNUSED_CODE:         if self._config["dry_run"]:
# REMOVED_UNUSED_CODE:             return self.fetch_dry_run_order(order_id)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             params1 = {"stop": True}
# REMOVED_UNUSED_CODE:             order_reg = self._api.fetch_order(order_id, pair, params=params1)
# REMOVED_UNUSED_CODE:             self._log_exchange_response("fetch_stoploss_order", order_reg)
# REMOVED_UNUSED_CODE:             return self._convert_stop_order(pair, order_id, order_reg)
# REMOVED_UNUSED_CODE:         except (ccxt.OrderNotFound, ccxt.InvalidOrder):
# REMOVED_UNUSED_CODE:             pass
# REMOVED_UNUSED_CODE:         except ccxt.DDoSProtection as e:
# REMOVED_UNUSED_CODE:             raise DDosProtection(e) from e
# REMOVED_UNUSED_CODE:         except (ccxt.OperationFailed, ccxt.ExchangeError) as e:
# REMOVED_UNUSED_CODE:             raise TemporaryError(
# REMOVED_UNUSED_CODE:                 f"Could not get order due to {e.__class__.__name__}. Message: {e}"
# REMOVED_UNUSED_CODE:             ) from e
# REMOVED_UNUSED_CODE:         except ccxt.BaseError as e:
# REMOVED_UNUSED_CODE:             raise OperationalException(e) from e
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return self._fetch_stop_order_fallback(order_id, pair)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _fetch_stop_order_fallback(self, order_id: str, pair: str) -> CcxtOrder:
# REMOVED_UNUSED_CODE:         params2 = {"stop": True, "ordType": "conditional"}
# REMOVED_UNUSED_CODE:         for method in (
# REMOVED_UNUSED_CODE:             self._api.fetch_open_orders,
# REMOVED_UNUSED_CODE:             self._api.fetch_closed_orders,
# REMOVED_UNUSED_CODE:             self._api.fetch_canceled_orders,
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 orders = method(pair, params=params2)
# REMOVED_UNUSED_CODE:                 orders_f = [order for order in orders if order["id"] == order_id]
# REMOVED_UNUSED_CODE:                 if orders_f:
# REMOVED_UNUSED_CODE:                     order = orders_f[0]
# REMOVED_UNUSED_CODE:                     return self._convert_stop_order(pair, order_id, order)
# REMOVED_UNUSED_CODE:             except (ccxt.OrderNotFound, ccxt.InvalidOrder):
# REMOVED_UNUSED_CODE:                 pass
# REMOVED_UNUSED_CODE:             except ccxt.DDoSProtection as e:
# REMOVED_UNUSED_CODE:                 raise DDosProtection(e) from e
# REMOVED_UNUSED_CODE:             except (ccxt.OperationFailed, ccxt.ExchangeError) as e:
# REMOVED_UNUSED_CODE:                 raise TemporaryError(
# REMOVED_UNUSED_CODE:                     f"Could not get order due to {e.__class__.__name__}. Message: {e}"
# REMOVED_UNUSED_CODE:                 ) from e
# REMOVED_UNUSED_CODE:             except ccxt.BaseError as e:
# REMOVED_UNUSED_CODE:                 raise OperationalException(e) from e
# REMOVED_UNUSED_CODE:         raise RetryableOrderError(f"StoplossOrder not found (pair: {pair} id: {order_id}).")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_order_id_conditional(self, order: CcxtOrder) -> str:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if order.get("type", "") == "stop":
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return safe_value_fallback2(order, order, "id_stop", "id")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return order["id"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def cancel_stoploss_order(self, order_id: str, pair: str, params: dict | None = None) -> dict:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         params1 = {"stop": True}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # 'ordType': 'conditional'
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         #
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self.cancel_order(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             order_id=order_id,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             pair=pair,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             params=params1,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _fetch_orders_emulate(self, pair: str, since_ms: int) -> list[CcxtOrder]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         orders = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         orders = self._api.fetch_closed_orders(pair, since=since_ms)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if since_ms < dt_ts(dt_now() - timedelta(days=6, hours=23)):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Regular fetch_closed_orders only returns 7 days of data.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Force usage of "archive" endpoint, which returns 3 months of data.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             params = {"method": "privateGetTradeOrdersHistoryArchive"}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             orders_hist = self._api.fetch_closed_orders(pair, since=since_ms, params=params)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             orders.extend(orders_hist)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         orders_open = self._api.fetch_open_orders(pair, since=since_ms)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         orders.extend(orders_open)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return orders
