"""Hyperliquid exchange subclass"""

import logging
# REMOVED_UNUSED_CODE: from copy import deepcopy
# REMOVED_UNUSED_CODE: from datetime import datetime

# REMOVED_UNUSED_CODE: from freqtrade.constants import BuySell
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.enums import MarginMode, TradingMode
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.exceptions import ExchangeError, OperationalException
# REMOVED_UNUSED_CODE: from freqtrade.exchange import Exchange
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.exchange.exchange_types import CcxtOrder, FtHas
# REMOVED_UNUSED_CODE: from freqtrade.util.datetime_helpers import dt_from_ts


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class Hyperliquid(Exchange):
# REMOVED_UNUSED_CODE:     """Hyperliquid exchange class.
# REMOVED_UNUSED_CODE:     Contains adjustments needed for Freqtrade to work with this exchange.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     _ft_has: FtHas = {
# REMOVED_UNUSED_CODE:         "ohlcv_has_history": False,
# REMOVED_UNUSED_CODE:         "l2_limit_range": [20],
# REMOVED_UNUSED_CODE:         "trades_has_history": False,
# REMOVED_UNUSED_CODE:         "tickers_have_bid_ask": False,
# REMOVED_UNUSED_CODE:         "stoploss_on_exchange": False,
# REMOVED_UNUSED_CODE:         "exchange_has_overrides": {"fetchTrades": False},
# REMOVED_UNUSED_CODE:         "marketOrderRequiresPrice": True,
# REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE:     _ft_has_futures: FtHas = {
# REMOVED_UNUSED_CODE:         "stoploss_on_exchange": True,
# REMOVED_UNUSED_CODE:         "stoploss_order_types": {"limit": "limit"},
# REMOVED_UNUSED_CODE:         "stop_price_prop": "stopPrice",
# REMOVED_UNUSED_CODE:         "funding_fee_timeframe": "1h",
# REMOVED_UNUSED_CODE:         "funding_fee_candle_limit": 500,
# REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     _supported_trading_mode_margin_pairs: list[tuple[TradingMode, MarginMode]] = [
# REMOVED_UNUSED_CODE:         (TradingMode.FUTURES, MarginMode.ISOLATED)
# REMOVED_UNUSED_CODE:     ]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def _ccxt_config(self) -> dict:
# REMOVED_UNUSED_CODE:         # ccxt Hyperliquid defaults to swap
# REMOVED_UNUSED_CODE:         config = {}
# REMOVED_UNUSED_CODE:         if self.trading_mode == TradingMode.SPOT:
# REMOVED_UNUSED_CODE:             config.update({"options": {"defaultType": "spot"}})
# REMOVED_UNUSED_CODE:         config.update(super()._ccxt_config)
# REMOVED_UNUSED_CODE:         return config
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_max_leverage(self, pair: str, stake_amount: float | None) -> float:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # There are no leverage tiers
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.trading_mode == TradingMode.FUTURES:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return self.markets[pair]["limits"]["leverage"]["max"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return 1.0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _lev_prep(self, pair: str, leverage: float, side: BuySell, accept_fail: bool = False):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.trading_mode != TradingMode.SPOT:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Hyperliquid expects leverage to be an int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             leverage = int(leverage)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Hyperliquid needs the parameter leverage.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Don't use _set_leverage(), as this sets margin back to cross
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.set_margin_mode(pair, self.margin_mode, params={"leverage": leverage})
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def dry_run_liquidation_price(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         open_rate: float,  # Entry price of position
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         is_short: bool,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         amount: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         stake_amount: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         leverage: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         wallet_balance: float,  # Or margin balance
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         open_trades: list,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> float | None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Optimized
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Docs: https://hyperliquid.gitbook.io/hyperliquid-docs/trading/liquidations
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Below can be done in fewer lines of code, but like this it matches the documentation.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Tested with 196 unique ccxt fetch_positions() position outputs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         - Only first output per position where pnl=0.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         - Compare against returned liquidation price
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Positions: 197 Average deviation: 0.00028980% Max deviation: 0.01309453%
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Positions info:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         {'leverage': {1.0: 23, 2.0: 155, 3.0: 8, 4.0: 7, 5.0: 4},
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         'side': {'long': 133, 'short': 64},
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         'symbol': {'BTC/USDC:USDC': 81,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                    'DOGE/USDC:USDC': 20,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                    'ETH/USDC:USDC': 53,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                    'SOL/USDC:USDC': 43}}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Defining/renaming variables to match the documentation
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         isolated_margin = wallet_balance
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         position_size = amount
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         price = open_rate
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         position_value = price * position_size
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         max_leverage = self.markets[pair]["limits"]["leverage"]["max"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Docs: The maintenance margin is half of the initial margin at max leverage,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         #       which varies from 3-50x. In other words, the maintenance margin is between 1%
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         #       (for 50x max leverage assets) and 16.7% (for 3x max leverage assets)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         #       depending on the asset
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # The key thing here is 'Half of the initial margin at max leverage'.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # A bit ambiguous, but this interpretation leads to accurate results:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         #       1. Start from the position value
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         #       2. Assume max leverage, calculate the initial margin by dividing the position value
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         #          by the max leverage
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         #       3. Divide this by 2
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         maintenance_margin_required = position_value / max_leverage / 2
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Docs: margin_available (isolated) = isolated_margin - maintenance_margin_required
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         margin_available = isolated_margin - maintenance_margin_required
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Docs: The maintenance margin is half of the initial margin at max leverage
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # The docs don't explicitly specify maintenance leverage, but this works.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Double because of the statement 'half of the initial margin at max leverage'
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         maintenance_leverage = max_leverage * 2
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Docs: l = 1 / MAINTENANCE_LEVERAGE (Using 'll' to comply with PEP8: E741)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ll = 1 / maintenance_leverage
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Docs: side = 1 for long and -1 for short
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         side = -1 if is_short else 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Docs: liq_price = price - side * margin_available / position_size / (1 - l * side)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         liq_price = price - side * margin_available / position_size / (1 - ll * side)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.trading_mode == TradingMode.FUTURES:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return liq_price
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
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Hyperliquid does not have fetchFundingHistory
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.trading_mode == TradingMode.FUTURES:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return self._fetch_and_calculate_funding_fees(pair, amount, is_short, open_date)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             except ExchangeError:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 logger.warning(f"Could not update funding fees for {pair}.")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return 0.0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _adjust_hyperliquid_order(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         order: dict,
# REMOVED_UNUSED_CODE:     ) -> dict:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Adjusts order response for Hyperliquid
# REMOVED_UNUSED_CODE:         :param order: Order response from Hyperliquid
# REMOVED_UNUSED_CODE:         :return: Adjusted order response
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if (
# REMOVED_UNUSED_CODE:             order["average"] is None
# REMOVED_UNUSED_CODE:             and order["status"] in ("canceled", "closed")
# REMOVED_UNUSED_CODE:             and order["filled"] > 0
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             # Hyperliquid does not fill the average price in the order response
# REMOVED_UNUSED_CODE:             # Fetch trades to calculate the average price to have the actual price
# REMOVED_UNUSED_CODE:             # the order was executed at
# REMOVED_UNUSED_CODE:             trades = self.get_trades_for_order(
# REMOVED_UNUSED_CODE:                 order["id"], order["symbol"], since=dt_from_ts(order["timestamp"])
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if trades:
# REMOVED_UNUSED_CODE:                 total_amount = sum(t["amount"] for t in trades)
# REMOVED_UNUSED_CODE:                 order["average"] = (
# REMOVED_UNUSED_CODE:                     sum(t["price"] * t["amount"] for t in trades) / total_amount
# REMOVED_UNUSED_CODE:                     if total_amount
# REMOVED_UNUSED_CODE:                     else None
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:         return order
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def fetch_order(self, order_id: str, pair: str, params: dict | None = None) -> CcxtOrder:
# REMOVED_UNUSED_CODE:         order = super().fetch_order(order_id, pair, params)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         order = self._adjust_hyperliquid_order(order)
# REMOVED_UNUSED_CODE:         self._log_exchange_response("fetch_order2", order)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return order
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def fetch_orders(
# REMOVED_UNUSED_CODE:         self, pair: str, since: datetime, params: dict | None = None
# REMOVED_UNUSED_CODE:     ) -> list[CcxtOrder]:
# REMOVED_UNUSED_CODE:         orders = super().fetch_orders(pair, since, params)
# REMOVED_UNUSED_CODE:         for idx, order in enumerate(deepcopy(orders)):
# REMOVED_UNUSED_CODE:             order2 = self._adjust_hyperliquid_order(order)
# REMOVED_UNUSED_CODE:             orders[idx] = order2
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._log_exchange_response("fetch_orders2", orders)
# REMOVED_UNUSED_CODE:         return orders
