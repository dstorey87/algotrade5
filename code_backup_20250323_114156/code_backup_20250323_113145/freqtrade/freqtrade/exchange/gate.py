"""Gate.io exchange subclass"""

import logging
# REMOVED_UNUSED_CODE: from datetime import datetime

# REMOVED_UNUSED_CODE: import ccxt

# REMOVED_UNUSED_CODE: from freqtrade.constants import BuySell
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.enums import MarginMode, PriceType, TradingMode
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.exceptions import DDosProtection, OperationalException, TemporaryError
# REMOVED_UNUSED_CODE: from freqtrade.exchange import Exchange
# REMOVED_UNUSED_CODE: from freqtrade.exchange.common import retrier
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.exchange.exchange_types import CcxtOrder, FtHas
# REMOVED_UNUSED_CODE: from freqtrade.misc import safe_value_fallback2


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class Gate(Exchange):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Gate.io exchange class. Contains adjustments needed for Freqtrade to work
# REMOVED_UNUSED_CODE:     with this exchange.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Please note that this exchange is not included in the list of exchanges
# REMOVED_UNUSED_CODE:     officially supported by the Freqtrade development team. So some features
# REMOVED_UNUSED_CODE:     may still not work as expected.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     unified_account = False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     _ft_has: FtHas = {
# REMOVED_UNUSED_CODE:         "order_time_in_force": ["GTC", "IOC"],
# REMOVED_UNUSED_CODE:         "stoploss_on_exchange": True,
# REMOVED_UNUSED_CODE:         "stoploss_order_types": {"limit": "limit"},
# REMOVED_UNUSED_CODE:         "stop_price_param": "stopPrice",
# REMOVED_UNUSED_CODE:         "stop_price_prop": "stopPrice",
# REMOVED_UNUSED_CODE:         "marketOrderRequiresPrice": True,
# REMOVED_UNUSED_CODE:         "trades_has_history": False,  # Endpoint would support this - but ccxt doesn't.
# REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     _ft_has_futures: FtHas = {
# REMOVED_UNUSED_CODE:         "needs_trading_fees": True,
# REMOVED_UNUSED_CODE:         "marketOrderRequiresPrice": False,
# REMOVED_UNUSED_CODE:         "funding_fee_candle_limit": 90,
# REMOVED_UNUSED_CODE:         "stop_price_type_field": "price_type",
# REMOVED_UNUSED_CODE:         "stop_price_type_value_mapping": {
# REMOVED_UNUSED_CODE:             PriceType.LAST: 0,
# REMOVED_UNUSED_CODE:             PriceType.MARK: 1,
# REMOVED_UNUSED_CODE:             PriceType.INDEX: 2,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     _supported_trading_mode_margin_pairs: list[tuple[TradingMode, MarginMode]] = [
# REMOVED_UNUSED_CODE:         # TradingMode.SPOT always supported and not required in this list
# REMOVED_UNUSED_CODE:         # (TradingMode.MARGIN, MarginMode.CROSS),
# REMOVED_UNUSED_CODE:         # (TradingMode.FUTURES, MarginMode.CROSS),
# REMOVED_UNUSED_CODE:         (TradingMode.FUTURES, MarginMode.ISOLATED)
# REMOVED_UNUSED_CODE:     ]
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
# REMOVED_UNUSED_CODE:                 # TODO: This should work with 4.4.34 and later.
# REMOVED_UNUSED_CODE:                 self._api.load_unified_status()
# REMOVED_UNUSED_CODE:                 is_unified = self._api.options.get("unifiedAccount")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 # Returns a tuple of bools, first for margin, second for Account
# REMOVED_UNUSED_CODE:                 if is_unified:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     self.unified_account = True
# REMOVED_UNUSED_CODE:                     logger.info("Gate: Unified account.")
# REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     self.unified_account = False
# REMOVED_UNUSED_CODE:                     logger.info("Gate: Classic account.")
# REMOVED_UNUSED_CODE:         except ccxt.DDoSProtection as e:
# REMOVED_UNUSED_CODE:             raise DDosProtection(e) from e
# REMOVED_UNUSED_CODE:         except (ccxt.OperationFailed, ccxt.ExchangeError) as e:
# REMOVED_UNUSED_CODE:             raise TemporaryError(
# REMOVED_UNUSED_CODE:                 f"Error in additional_exchange_init due to {e.__class__.__name__}. Message: {e}"
# REMOVED_UNUSED_CODE:             ) from e
# REMOVED_UNUSED_CODE:         except ccxt.BaseError as e:
# REMOVED_UNUSED_CODE:             raise OperationalException(e) from e
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
# REMOVED_UNUSED_CODE:         if ordertype == "market" and self.trading_mode == TradingMode.FUTURES:
# REMOVED_UNUSED_CODE:             params["type"] = "market"
# REMOVED_UNUSED_CODE:             params.update({"timeInForce": "IOC"})
# REMOVED_UNUSED_CODE:         return params
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def get_trades_for_order(
# REMOVED_UNUSED_CODE:         self, order_id: str, pair: str, since: datetime, params: dict | None = None
# REMOVED_UNUSED_CODE:     ) -> list:
# REMOVED_UNUSED_CODE:         trades = super().get_trades_for_order(order_id, pair, since, params)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.trading_mode == TradingMode.FUTURES:
# REMOVED_UNUSED_CODE:             # Futures usually don't contain fees in the response.
# REMOVED_UNUSED_CODE:             # As such, futures orders on gate will not contain a fee, which causes
# REMOVED_UNUSED_CODE:             # a repeated "update fee" cycle and wrong calculations.
# REMOVED_UNUSED_CODE:             # Therefore we patch the response with fees if it's not available.
# REMOVED_UNUSED_CODE:             # An alternative also containing fees would be
# REMOVED_UNUSED_CODE:             # privateFuturesGetSettleAccountBook({"settle": "usdt"})
# REMOVED_UNUSED_CODE:             pair_fees = self._trading_fees.get(pair, {})
# REMOVED_UNUSED_CODE:             if pair_fees:
# REMOVED_UNUSED_CODE:                 for idx, trade in enumerate(trades):
# REMOVED_UNUSED_CODE:                     fee = trade.get("fee", {})
# REMOVED_UNUSED_CODE:                     if fee and fee.get("cost") is None:
# REMOVED_UNUSED_CODE:                         takerOrMaker = trade.get("takerOrMaker", "taker")
# REMOVED_UNUSED_CODE:                         if pair_fees.get(takerOrMaker) is not None:
# REMOVED_UNUSED_CODE:                             trades[idx]["fee"] = {
# REMOVED_UNUSED_CODE:                                 "currency": self.get_pair_quote_currency(pair),
# REMOVED_UNUSED_CODE:                                 "cost": trade["cost"] * pair_fees[takerOrMaker],
# REMOVED_UNUSED_CODE:                                 "rate": pair_fees[takerOrMaker],
# REMOVED_UNUSED_CODE:                             }
# REMOVED_UNUSED_CODE:         return trades
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_order_id_conditional(self, order: CcxtOrder) -> str:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return safe_value_fallback2(order, order, "id_stop", "id")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def fetch_stoploss_order(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, order_id: str, pair: str, params: dict | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> CcxtOrder:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         order = self.fetch_order(order_id=order_id, pair=pair, params={"stop": True})
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if order.get("status", "open") == "closed":
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Places a real order - which we need to fetch explicitly.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             val = "trade_id" if self.trading_mode == TradingMode.FUTURES else "fired_order_id"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if new_orderid := order.get("info", {}).get(val):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 order1 = self.fetch_order(order_id=new_orderid, pair=pair, params=params)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 order1["id_stop"] = order1["id"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 order1["id"] = order_id
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 order1["type"] = "stoploss"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 order1["stopPrice"] = order.get("stopPrice")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 order1["status_stop"] = "triggered"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return order1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return order
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def cancel_stoploss_order(self, order_id: str, pair: str, params: dict | None = None) -> dict:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self.cancel_order(order_id=order_id, pair=pair, params={"stop": True})
