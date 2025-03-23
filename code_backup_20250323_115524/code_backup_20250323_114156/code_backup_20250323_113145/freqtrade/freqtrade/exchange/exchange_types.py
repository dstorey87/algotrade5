from typing import Any, Literal, TypedDict

from freqtrade.enums import CandleType


# REMOVED_UNUSED_CODE: class FtHas(TypedDict, total=False):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     order_time_in_force: list[str]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     exchange_has_overrides: dict[str, bool]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     marketOrderRequiresPrice: bool
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Stoploss on exchange
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     stoploss_on_exchange: bool
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     stop_price_param: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     stop_price_prop: Literal["stopPrice", "stopLossPrice"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     stop_price_type_field: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     stop_price_type_value_mapping: dict
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     stoploss_order_types: dict[str, str]
# REMOVED_UNUSED_CODE:     # ohlcv
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ohlcv_params: dict
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ohlcv_candle_limit: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ohlcv_has_history: bool
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ohlcv_partial_candle: bool
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ohlcv_require_since: bool
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ohlcv_volume_currency: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ohlcv_candle_limit_per_timeframe: dict[str, int]
# REMOVED_UNUSED_CODE:     # Tickers
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     tickers_have_quoteVolume: bool
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     tickers_have_percentage: bool
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     tickers_have_bid_ask: bool
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     tickers_have_price: bool
# REMOVED_UNUSED_CODE:     # Trades
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     trades_limit: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     trades_pagination: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     trades_pagination_arg: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     trades_has_history: bool
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     trades_pagination_overlap: bool
# REMOVED_UNUSED_CODE:     # Orderbook
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     l2_limit_range: list[int] | None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     l2_limit_range_required: bool
# REMOVED_UNUSED_CODE:     # Futures
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ccxt_futures_name: str  # usually swap
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     mark_ohlcv_price: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     mark_ohlcv_timeframe: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     funding_fee_timeframe: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     funding_fee_candle_limit: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     floor_leverage: bool
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     needs_trading_fees: bool
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     order_props_in_contracts: list[Literal["amount", "cost", "filled", "remaining"]]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     proxy_coin_mapping: dict[str, str]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Websocket control
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ws_enabled: bool


class Ticker(TypedDict):
# REMOVED_UNUSED_CODE:     symbol: str
# REMOVED_UNUSED_CODE:     ask: float | None
# REMOVED_UNUSED_CODE:     askVolume: float | None
# REMOVED_UNUSED_CODE:     bid: float | None
# REMOVED_UNUSED_CODE:     bidVolume: float | None
# REMOVED_UNUSED_CODE:     last: float | None
# REMOVED_UNUSED_CODE:     quoteVolume: float | None
# REMOVED_UNUSED_CODE:     baseVolume: float | None
# REMOVED_UNUSED_CODE:     percentage: float | None
    # Several more - only listing required.


# REMOVED_UNUSED_CODE: Tickers = dict[str, Ticker]


# REMOVED_UNUSED_CODE: class OrderBook(TypedDict):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     symbol: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     bids: list[tuple[float, float]]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     asks: list[tuple[float, float]]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     timestamp: int | None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     datetime: str | None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     nonce: int | None


class CcxtBalance(TypedDict):
# REMOVED_UNUSED_CODE:     free: float
# REMOVED_UNUSED_CODE:     used: float
# REMOVED_UNUSED_CODE:     total: float


# REMOVED_UNUSED_CODE: CcxtBalances = dict[str, CcxtBalance]


# REMOVED_UNUSED_CODE: class CcxtPosition(TypedDict):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     symbol: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     side: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     contracts: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     leverage: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     collateral: float | None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     initialMargin: float | None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     liquidationPrice: float | None


# REMOVED_UNUSED_CODE: CcxtOrder = dict[str, Any]

# pair, timeframe, candleType, OHLCV, drop last?,
# REMOVED_UNUSED_CODE: OHLCVResponse = tuple[str, str, CandleType, list, bool]
