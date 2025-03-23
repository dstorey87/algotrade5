"""Binance exchange subclass"""

import logging
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from datetime import datetime, timezone
# REMOVED_UNUSED_CODE: from pathlib import Path

# REMOVED_UNUSED_CODE: import ccxt
# REMOVED_UNUSED_CODE: from pandas import DataFrame

# REMOVED_UNUSED_CODE: from freqtrade.constants import DEFAULT_DATAFRAME_COLUMNS
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.enums import CandleType, MarginMode, PriceType, TradingMode
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.exceptions import DDosProtection, OperationalException, TemporaryError
# REMOVED_UNUSED_CODE: from freqtrade.exchange import Exchange
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.exchange.binance_public_data import concat_safe, download_archive_ohlcv
# REMOVED_UNUSED_CODE: from freqtrade.exchange.common import retrier
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.exchange.exchange_types import FtHas, Tickers
# REMOVED_UNUSED_CODE: from freqtrade.exchange.exchange_utils_timeframe import timeframe_to_msecs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.misc import deep_merge_dicts, json_load
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.util.datetime_helpers import dt_from_ts, dt_ts


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class Binance(Exchange):
# REMOVED_UNUSED_CODE:     _ft_has: FtHas = {
# REMOVED_UNUSED_CODE:         "stoploss_on_exchange": True,
# REMOVED_UNUSED_CODE:         "stop_price_param": "stopPrice",
# REMOVED_UNUSED_CODE:         "stop_price_prop": "stopPrice",
# REMOVED_UNUSED_CODE:         "stoploss_order_types": {"limit": "stop_loss_limit"},
# REMOVED_UNUSED_CODE:         "order_time_in_force": ["GTC", "FOK", "IOC", "PO"],
# REMOVED_UNUSED_CODE:         "trades_pagination": "id",
# REMOVED_UNUSED_CODE:         "trades_pagination_arg": "fromId",
# REMOVED_UNUSED_CODE:         "trades_has_history": True,
# REMOVED_UNUSED_CODE:         "l2_limit_range": [5, 10, 20, 50, 100, 500, 1000],
# REMOVED_UNUSED_CODE:         "ws_enabled": True,
# REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE:     _ft_has_futures: FtHas = {
# REMOVED_UNUSED_CODE:         "funding_fee_candle_limit": 1000,
# REMOVED_UNUSED_CODE:         "stoploss_order_types": {"limit": "stop", "market": "stop_market"},
# REMOVED_UNUSED_CODE:         "order_time_in_force": ["GTC", "FOK", "IOC"],
# REMOVED_UNUSED_CODE:         "tickers_have_price": False,
# REMOVED_UNUSED_CODE:         "floor_leverage": True,
# REMOVED_UNUSED_CODE:         "stop_price_type_field": "workingType",
# REMOVED_UNUSED_CODE:         "order_props_in_contracts": ["amount", "cost", "filled", "remaining"],
# REMOVED_UNUSED_CODE:         "stop_price_type_value_mapping": {
# REMOVED_UNUSED_CODE:             PriceType.LAST: "CONTRACT_PRICE",
# REMOVED_UNUSED_CODE:             PriceType.MARK: "MARK_PRICE",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "ws_enabled": False,
# REMOVED_UNUSED_CODE:         "proxy_coin_mapping": {
# REMOVED_UNUSED_CODE:             "BNFCR": "USDC",
# REMOVED_UNUSED_CODE:             "BFUSD": "USDT",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     _supported_trading_mode_margin_pairs: list[tuple[TradingMode, MarginMode]] = [
# REMOVED_UNUSED_CODE:         # TradingMode.SPOT always supported and not required in this list
# REMOVED_UNUSED_CODE:         # (TradingMode.MARGIN, MarginMode.CROSS),
# REMOVED_UNUSED_CODE:         (TradingMode.FUTURES, MarginMode.CROSS),
# REMOVED_UNUSED_CODE:         (TradingMode.FUTURES, MarginMode.ISOLATED),
# REMOVED_UNUSED_CODE:     ]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_proxy_coin(self) -> str:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Get the proxy coin for the given coin
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Falls back to the stake currency if no proxy coin is found
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: Proxy coin or stake currency
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.margin_mode == MarginMode.CROSS:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return self._config.get("proxy_coin", self._config["stake_currency"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._config["stake_currency"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def get_tickers(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         symbols: list[str] | None = None,
# REMOVED_UNUSED_CODE:         *,
# REMOVED_UNUSED_CODE:         cached: bool = False,
# REMOVED_UNUSED_CODE:         market_type: TradingMode | None = None,
# REMOVED_UNUSED_CODE:     ) -> Tickers:
# REMOVED_UNUSED_CODE:         tickers = super().get_tickers(symbols=symbols, cached=cached, market_type=market_type)
# REMOVED_UNUSED_CODE:         if self.trading_mode == TradingMode.FUTURES:
# REMOVED_UNUSED_CODE:             # Binance's future result has no bid/ask values.
# REMOVED_UNUSED_CODE:             # Therefore we must fetch that from fetch_bids_asks and combine the two results.
# REMOVED_UNUSED_CODE:             bidsasks = self.fetch_bids_asks(symbols, cached=cached)
# REMOVED_UNUSED_CODE:             tickers = deep_merge_dicts(bidsasks, tickers, allow_null_overrides=False)
# REMOVED_UNUSED_CODE:         return tickers
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
# REMOVED_UNUSED_CODE:                 position_side = self._api.fapiPrivateGetPositionSideDual()
# REMOVED_UNUSED_CODE:                 self._log_exchange_response("position_side_setting", position_side)
# REMOVED_UNUSED_CODE:                 assets_margin = self._api.fapiPrivateGetMultiAssetsMargin()
# REMOVED_UNUSED_CODE:                 self._log_exchange_response("multi_asset_margin", assets_margin)
# REMOVED_UNUSED_CODE:                 msg = ""
# REMOVED_UNUSED_CODE:                 if position_side.get("dualSidePosition") is True:
# REMOVED_UNUSED_CODE:                     msg += (
# REMOVED_UNUSED_CODE:                         "\nHedge Mode is not supported by freqtrade. "
# REMOVED_UNUSED_CODE:                         "Please change 'Position Mode' on your binance futures account."
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                 if (
# REMOVED_UNUSED_CODE:                     assets_margin.get("multiAssetsMargin") is True
# REMOVED_UNUSED_CODE:                     and self.margin_mode != MarginMode.CROSS
# REMOVED_UNUSED_CODE:                 ):
# REMOVED_UNUSED_CODE:                     msg += (
# REMOVED_UNUSED_CODE:                         "\nMulti-Asset Mode is not supported by freqtrade. "
# REMOVED_UNUSED_CODE:                         "Please change 'Asset Mode' on your binance futures account."
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                 if msg:
# REMOVED_UNUSED_CODE:                     raise OperationalException(msg)
# REMOVED_UNUSED_CODE:         except ccxt.DDoSProtection as e:
# REMOVED_UNUSED_CODE:             raise DDosProtection(e) from e
# REMOVED_UNUSED_CODE:         except (ccxt.OperationFailed, ccxt.ExchangeError) as e:
# REMOVED_UNUSED_CODE:             raise TemporaryError(
# REMOVED_UNUSED_CODE:                 f"Error in additional_exchange_init due to {e.__class__.__name__}. Message: {e}"
# REMOVED_UNUSED_CODE:             ) from e
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         except ccxt.BaseError as e:
# REMOVED_UNUSED_CODE:             raise OperationalException(e) from e
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def get_historic_ohlcv(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE:         timeframe: str,
# REMOVED_UNUSED_CODE:         since_ms: int,
# REMOVED_UNUSED_CODE:         candle_type: CandleType,
# REMOVED_UNUSED_CODE:         is_new_pair: bool = False,
# REMOVED_UNUSED_CODE:         until_ms: int | None = None,
# REMOVED_UNUSED_CODE:     ) -> DataFrame:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Overwrite to introduce "fast new pair" functionality by detecting the pair's listing date
# REMOVED_UNUSED_CODE:         Does not work for other exchanges, which don't return the earliest data when called with "0"
# REMOVED_UNUSED_CODE:         :param candle_type: Any of the enum CandleType (must match trading mode!)
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if is_new_pair:
# REMOVED_UNUSED_CODE:             with self._loop_lock:
# REMOVED_UNUSED_CODE:                 x = self.loop.run_until_complete(
# REMOVED_UNUSED_CODE:                     self._async_get_candle_history(pair, timeframe, candle_type, 0)
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             if x and x[3] and x[3][0] and x[3][0][0] > since_ms:
# REMOVED_UNUSED_CODE:                 # Set starting date to first available candle.
# REMOVED_UNUSED_CODE:                 since_ms = x[3][0][0]
# REMOVED_UNUSED_CODE:                 logger.info(
# REMOVED_UNUSED_CODE:                     f"Candle-data for {pair} available starting with "
# REMOVED_UNUSED_CODE:                     f"{datetime.fromtimestamp(since_ms // 1000, tz=timezone.utc).isoformat()}."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 if until_ms and since_ms >= until_ms:
# REMOVED_UNUSED_CODE:                     logger.warning(
# REMOVED_UNUSED_CODE:                         f"No available candle-data for {pair} before "
# REMOVED_UNUSED_CODE:                         f"{dt_from_ts(until_ms).isoformat()}"
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                     return DataFrame(columns=DEFAULT_DATAFRAME_COLUMNS)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if (
# REMOVED_UNUSED_CODE:             self._config["exchange"].get("only_from_ccxt", False)
# REMOVED_UNUSED_CODE:             or
# REMOVED_UNUSED_CODE:             # only download timeframes with significant improvements,
# REMOVED_UNUSED_CODE:             # otherwise fall back to rest API
# REMOVED_UNUSED_CODE:             not (
# REMOVED_UNUSED_CODE:                 (candle_type == CandleType.SPOT and timeframe in ["1s", "1m", "3m", "5m"])
# REMOVED_UNUSED_CODE:                 or (
# REMOVED_UNUSED_CODE:                     candle_type == CandleType.FUTURES
# REMOVED_UNUSED_CODE:                     and timeframe in ["1m", "3m", "5m", "15m", "30m"]
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             return super().get_historic_ohlcv(
# REMOVED_UNUSED_CODE:                 pair=pair,
# REMOVED_UNUSED_CODE:                 timeframe=timeframe,
# REMOVED_UNUSED_CODE:                 since_ms=since_ms,
# REMOVED_UNUSED_CODE:                 candle_type=candle_type,
# REMOVED_UNUSED_CODE:                 is_new_pair=is_new_pair,
# REMOVED_UNUSED_CODE:                 until_ms=until_ms,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             # Download from data.binance.vision
# REMOVED_UNUSED_CODE:             return self.get_historic_ohlcv_fast(
# REMOVED_UNUSED_CODE:                 pair=pair,
# REMOVED_UNUSED_CODE:                 timeframe=timeframe,
# REMOVED_UNUSED_CODE:                 since_ms=since_ms,
# REMOVED_UNUSED_CODE:                 candle_type=candle_type,
# REMOVED_UNUSED_CODE:                 is_new_pair=is_new_pair,
# REMOVED_UNUSED_CODE:                 until_ms=until_ms,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def get_historic_ohlcv_fast(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE:         timeframe: str,
# REMOVED_UNUSED_CODE:         since_ms: int,
# REMOVED_UNUSED_CODE:         candle_type: CandleType,
# REMOVED_UNUSED_CODE:         is_new_pair: bool = False,
# REMOVED_UNUSED_CODE:         until_ms: int | None = None,
# REMOVED_UNUSED_CODE:     ) -> DataFrame:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Fastly fetch OHLCV data by leveraging https://data.binance.vision.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         with self._loop_lock:
# REMOVED_UNUSED_CODE:             df = self.loop.run_until_complete(
# REMOVED_UNUSED_CODE:                 download_archive_ohlcv(
# REMOVED_UNUSED_CODE:                     candle_type=candle_type,
# REMOVED_UNUSED_CODE:                     pair=pair,
# REMOVED_UNUSED_CODE:                     timeframe=timeframe,
# REMOVED_UNUSED_CODE:                     since_ms=since_ms,
# REMOVED_UNUSED_CODE:                     until_ms=until_ms,
# REMOVED_UNUSED_CODE:                     markets=self.markets,
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # download the remaining data from rest API
# REMOVED_UNUSED_CODE:         if df.empty:
# REMOVED_UNUSED_CODE:             rest_since_ms = since_ms
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             rest_since_ms = dt_ts(df.iloc[-1].date) + timeframe_to_msecs(timeframe)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # make sure since <= until
# REMOVED_UNUSED_CODE:         if until_ms and rest_since_ms > until_ms:
# REMOVED_UNUSED_CODE:             rest_df = DataFrame()
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             rest_df = super().get_historic_ohlcv(
# REMOVED_UNUSED_CODE:                 pair=pair,
# REMOVED_UNUSED_CODE:                 timeframe=timeframe,
# REMOVED_UNUSED_CODE:                 since_ms=rest_since_ms,
# REMOVED_UNUSED_CODE:                 candle_type=candle_type,
# REMOVED_UNUSED_CODE:                 is_new_pair=is_new_pair,
# REMOVED_UNUSED_CODE:                 until_ms=until_ms,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         all_df = concat_safe([df, rest_df])
# REMOVED_UNUSED_CODE:         return all_df
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def funding_fee_cutoff(self, open_date: datetime):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Funding fees are only charged at full hours (usually every 4-8h).
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Therefore a trade opening at 10:00:01 will not be charged a funding fee until the next hour.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         On binance, this cutoff is 15s.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         https://github.com/freqtrade/freqtrade/pull/5779#discussion_r740175931
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param open_date: The open date for a trade
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: True if the date falls on a full hour, False otherwise
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return open_date.minute == 0 and open_date.second < 15
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def fetch_funding_rates(self, symbols: list[str] | None = None) -> dict[str, dict[str, float]]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Fetch funding rates for the given symbols.
# REMOVED_UNUSED_CODE:         :param symbols: List of symbols to fetch funding rates for
# REMOVED_UNUSED_CODE:         :return: Dict of funding rates for the given symbols
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             if self.trading_mode == TradingMode.FUTURES:
# REMOVED_UNUSED_CODE:                 rates = self._api.fetch_funding_rates(symbols)
# REMOVED_UNUSED_CODE:                 return rates
# REMOVED_UNUSED_CODE:             return {}
# REMOVED_UNUSED_CODE:         except ccxt.DDoSProtection as e:
# REMOVED_UNUSED_CODE:             raise DDosProtection(e) from e
# REMOVED_UNUSED_CODE:         except (ccxt.OperationFailed, ccxt.ExchangeError) as e:
# REMOVED_UNUSED_CODE:             raise TemporaryError(
# REMOVED_UNUSED_CODE:                 f"Error in additional_exchange_init due to {e.__class__.__name__}. Message: {e}"
# REMOVED_UNUSED_CODE:             ) from e
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         except ccxt.BaseError as e:
# REMOVED_UNUSED_CODE:             raise OperationalException(e) from e
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def dry_run_liquidation_price(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         open_rate: float,  # Entry price of position
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         is_short: bool,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         amount: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         stake_amount: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         leverage: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         wallet_balance: float,  # Or margin balance
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         open_trades: list,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> float | None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Important: Must be fetching data from cached values as this is used by backtesting!
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         MARGIN: https://www.binance.com/en/support/faq/f6b010588e55413aa58b7d63ee0125ed
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         PERPETUAL: https://www.binance.com/en/support/faq/b3c689c1f50a44cabb3a84e663b81d93
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
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param open_trades: List of open trades in the same wallet
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # * Only required for Cross
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param mm_ex_1: (TMM)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             Cross-Margin Mode: Maintenance Margin of all other contracts, excluding Contract 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             Isolated-Margin Mode: 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param upnl_ex_1: (UPNL)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             Cross-Margin Mode: Unrealized PNL of all other contracts, excluding Contract 1.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             Isolated-Margin Mode: 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param other
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         cross_vars: float = 0.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # mm_ratio: Binance's formula specifies maintenance margin rate which is mm_ratio * 100%
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # maintenance_amt: (CUM) Maintenance Amount of position
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         mm_ratio, maintenance_amt = self.get_maintenance_ratio_and_amt(pair, stake_amount)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.margin_mode == MarginMode.CROSS:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             mm_ex_1: float = 0.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             upnl_ex_1: float = 0.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             pairs = [trade.pair for trade in open_trades]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if self._config["runmode"] in ("live", "dry_run"):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 funding_rates = self.fetch_funding_rates(pairs)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for trade in open_trades:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if trade.pair == pair:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     # Only "other" trades are considered
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     continue
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if self._config["runmode"] in ("live", "dry_run"):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     mark_price = funding_rates[trade.pair]["markPrice"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     # Fall back to open rate for backtesting
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     mark_price = trade.open_rate
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 mm_ratio1, maint_amnt1 = self.get_maintenance_ratio_and_amt(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     trade.pair, trade.stake_amount
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 maint_margin = trade.amount * mark_price * mm_ratio1 - maint_amnt1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 mm_ex_1 += maint_margin
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 upnl_ex_1 += trade.amount * mark_price - trade.amount * trade.open_rate
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             cross_vars = upnl_ex_1 - mm_ex_1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         side_1 = -1 if is_short else 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if maintenance_amt is None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "Parameter maintenance_amt is required by Binance.liquidation_price"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"for {self.trading_mode}"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.trading_mode == TradingMode.FUTURES:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 (wallet_balance + cross_vars + maintenance_amt) - (side_1 * amount * open_rate)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ) / ((amount * mm_ratio) - (side_1 * amount))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "Freqtrade only supports isolated futures for leverage trading"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def load_leverage_tiers(self) -> dict[str, list[dict]]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.trading_mode == TradingMode.FUTURES:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if self._config["dry_run"]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 leverage_tiers_path = Path(__file__).parent / "binance_leverage_tiers.json"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 with leverage_tiers_path.open() as json_file:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     return json_load(json_file)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return self.get_leverage_tiers()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return {}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     async def _async_get_trade_history_id_startup(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, pair: str, since: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> tuple[list[list], str]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         override for initial call
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Binance only provides a limited set of historic trades data.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Using from_id=0, we can get the earliest available trades.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         So if we don't get any data with the provided "since", we can assume to
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         download all available data.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         t, from_id = await self._async_fetch_trades(pair, since=since)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not t:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return [], "0"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return t, from_id
