from datetime import date, datetime
from typing import Any

from pydantic import AwareDatetime, BaseModel, RootModel, SerializeAsAny, model_validator

from freqtrade.constants import DL_DATA_TIMEFRAMES, IntOrInf
from freqtrade.enums import MarginMode, OrderTypeValues, SignalDirection, TradingMode
from freqtrade.ft_types import ValidExchangesType
from freqtrade.rpc.api_server.webserver_bgwork import ProgressTask


class ExchangeModePayloadMixin(BaseModel):
# REMOVED_UNUSED_CODE:     trading_mode: TradingMode | None = None
# REMOVED_UNUSED_CODE:     margin_mode: MarginMode | None = None
# REMOVED_UNUSED_CODE:     exchange: str | None = None


# REMOVED_UNUSED_CODE: class Ping(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     status: str


class AccessToken(BaseModel):
# REMOVED_UNUSED_CODE:     access_token: str


# REMOVED_UNUSED_CODE: class AccessAndRefreshToken(AccessToken):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     refresh_token: str


# REMOVED_UNUSED_CODE: class Version(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     version: str


class StatusMsg(BaseModel):
# REMOVED_UNUSED_CODE:     status: str


# REMOVED_UNUSED_CODE: class BgJobStarted(StatusMsg):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     job_id: str


# REMOVED_UNUSED_CODE: class BackgroundTaskStatus(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     job_id: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     job_category: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     status: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     running: bool
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     progress: float | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     progress_tasks: dict[str, ProgressTask] | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     error: str | None = None


class BackgroundTaskResult(BaseModel):
# REMOVED_UNUSED_CODE:     error: str | None = None
# REMOVED_UNUSED_CODE:     status: str


# REMOVED_UNUSED_CODE: class ResultMsg(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     result: str


class Balance(BaseModel):
# REMOVED_UNUSED_CODE:     currency: str
# REMOVED_UNUSED_CODE:     free: float
# REMOVED_UNUSED_CODE:     balance: float
# REMOVED_UNUSED_CODE:     used: float
# REMOVED_UNUSED_CODE:     bot_owned: float | None = None
# REMOVED_UNUSED_CODE:     est_stake: float
# REMOVED_UNUSED_CODE:     est_stake_bot: float | None = None
# REMOVED_UNUSED_CODE:     stake: str
    # Starting with 2.x
# REMOVED_UNUSED_CODE:     side: str
# REMOVED_UNUSED_CODE:     is_position: bool
# REMOVED_UNUSED_CODE:     position: float
# REMOVED_UNUSED_CODE:     is_bot_managed: bool


# REMOVED_UNUSED_CODE: class Balances(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     currencies: list[Balance]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     total: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     total_bot: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     symbol: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     value: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     value_bot: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     stake: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     note: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     starting_capital: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     starting_capital_ratio: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     starting_capital_pct: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     starting_capital_fiat: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     starting_capital_fiat_ratio: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     starting_capital_fiat_pct: float


# REMOVED_UNUSED_CODE: class Count(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     current: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     max: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     total_stake: float


class __BaseStatsModel(BaseModel):
# REMOVED_UNUSED_CODE:     profit_ratio: float
# REMOVED_UNUSED_CODE:     profit_pct: float
# REMOVED_UNUSED_CODE:     profit_abs: float
# REMOVED_UNUSED_CODE:     count: int


# REMOVED_UNUSED_CODE: class Entry(__BaseStatsModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     enter_tag: str


# REMOVED_UNUSED_CODE: class Exit(__BaseStatsModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     exit_reason: str


# REMOVED_UNUSED_CODE: class MixTag(__BaseStatsModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     mix_tag: str


# REMOVED_UNUSED_CODE: class PerformanceEntry(__BaseStatsModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     pair: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     profit: float


# REMOVED_UNUSED_CODE: class Profit(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     profit_closed_coin: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     profit_closed_percent_mean: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     profit_closed_ratio_mean: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     profit_closed_percent_sum: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     profit_closed_ratio_sum: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     profit_closed_percent: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     profit_closed_ratio: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     profit_closed_fiat: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     profit_all_coin: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     profit_all_percent_mean: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     profit_all_ratio_mean: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     profit_all_percent_sum: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     profit_all_ratio_sum: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     profit_all_percent: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     profit_all_ratio: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     profit_all_fiat: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     trade_count: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     closed_trade_count: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     first_trade_date: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     first_trade_humanized: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     first_trade_timestamp: int
# REMOVED_UNUSED_CODE:     latest_trade_date: str
# REMOVED_UNUSED_CODE:     latest_trade_humanized: str
# REMOVED_UNUSED_CODE:     latest_trade_timestamp: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     avg_duration: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     best_pair: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     best_rate: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     best_pair_profit_ratio: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     best_pair_profit_abs: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     winning_trades: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     losing_trades: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     profit_factor: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     winrate: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     expectancy: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     expectancy_ratio: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     max_drawdown: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     max_drawdown_abs: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     max_drawdown_start: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     max_drawdown_start_timestamp: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     max_drawdown_end: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     max_drawdown_end_timestamp: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     trading_volume: float | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     bot_start_timestamp: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     bot_start_date: str


class SellReason(BaseModel):
# REMOVED_UNUSED_CODE:     wins: int
# REMOVED_UNUSED_CODE:     losses: int
# REMOVED_UNUSED_CODE:     draws: int


# REMOVED_UNUSED_CODE: class Stats(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     exit_reasons: dict[str, SellReason]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     durations: dict[str, float | None]


class DailyWeeklyMonthlyRecord(BaseModel):
    date: date
# REMOVED_UNUSED_CODE:     abs_profit: float
# REMOVED_UNUSED_CODE:     rel_profit: float
# REMOVED_UNUSED_CODE:     starting_balance: float
# REMOVED_UNUSED_CODE:     fiat_value: float
# REMOVED_UNUSED_CODE:     trade_count: int


# REMOVED_UNUSED_CODE: class DailyWeeklyMonthly(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     data: list[DailyWeeklyMonthlyRecord]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     fiat_display_currency: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     stake_currency: str


class UnfilledTimeout(BaseModel):
# REMOVED_UNUSED_CODE:     entry: int | None = None
# REMOVED_UNUSED_CODE:     exit: int | None = None
# REMOVED_UNUSED_CODE:     unit: str | None = None
# REMOVED_UNUSED_CODE:     exit_timeout_count: int | None = None


class OrderTypes(BaseModel):
# REMOVED_UNUSED_CODE:     entry: OrderTypeValues
# REMOVED_UNUSED_CODE:     exit: OrderTypeValues
# REMOVED_UNUSED_CODE:     emergency_exit: OrderTypeValues | None = None
# REMOVED_UNUSED_CODE:     force_exit: OrderTypeValues | None = None
# REMOVED_UNUSED_CODE:     force_entry: OrderTypeValues | None = None
# REMOVED_UNUSED_CODE:     stoploss: OrderTypeValues
# REMOVED_UNUSED_CODE:     stoploss_on_exchange: bool
# REMOVED_UNUSED_CODE:     stoploss_on_exchange_interval: int | None = None


# REMOVED_UNUSED_CODE: class ShowConfig(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     version: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     strategy_version: str | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     api_version: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     dry_run: bool
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     trading_mode: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     short_allowed: bool
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     stake_currency: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     stake_amount: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     available_capital: float | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     stake_currency_decimals: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     max_open_trades: IntOrInf
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     minimal_roi: dict[str, Any]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     stoploss: float | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     stoploss_on_exchange: bool
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     trailing_stop: bool | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     trailing_stop_positive: float | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     trailing_stop_positive_offset: float | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     trailing_only_offset_is_reached: bool | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     unfilledtimeout: UnfilledTimeout | None = None  # Empty in webserver mode
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     order_types: OrderTypes | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     use_custom_stoploss: bool | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     timeframe: str | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     timeframe_ms: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     timeframe_min: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     exchange: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     strategy: str | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     force_entry_enable: bool
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     exit_pricing: dict[str, Any]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     entry_pricing: dict[str, Any]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     bot_name: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     state: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     runmode: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     position_adjustment_enable: bool
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     max_entry_position_adjustment: int


class OrderSchema(BaseModel):
# REMOVED_UNUSED_CODE:     pair: str
# REMOVED_UNUSED_CODE:     order_id: str
# REMOVED_UNUSED_CODE:     status: str
# REMOVED_UNUSED_CODE:     remaining: float | None = None
# REMOVED_UNUSED_CODE:     amount: float
# REMOVED_UNUSED_CODE:     safe_price: float
# REMOVED_UNUSED_CODE:     cost: float
# REMOVED_UNUSED_CODE:     filled: float | None = None
# REMOVED_UNUSED_CODE:     ft_order_side: str
# REMOVED_UNUSED_CODE:     order_type: str
# REMOVED_UNUSED_CODE:     is_open: bool
# REMOVED_UNUSED_CODE:     order_timestamp: int | None = None
# REMOVED_UNUSED_CODE:     order_filled_timestamp: int | None = None
# REMOVED_UNUSED_CODE:     ft_fee_base: float | None = None
# REMOVED_UNUSED_CODE:     ft_order_tag: str | None = None


class TradeSchema(BaseModel):
# REMOVED_UNUSED_CODE:     trade_id: int
# REMOVED_UNUSED_CODE:     pair: str
# REMOVED_UNUSED_CODE:     base_currency: str
# REMOVED_UNUSED_CODE:     quote_currency: str
# REMOVED_UNUSED_CODE:     is_open: bool
# REMOVED_UNUSED_CODE:     is_short: bool
# REMOVED_UNUSED_CODE:     exchange: str
# REMOVED_UNUSED_CODE:     amount: float
# REMOVED_UNUSED_CODE:     amount_requested: float
# REMOVED_UNUSED_CODE:     stake_amount: float
# REMOVED_UNUSED_CODE:     max_stake_amount: float | None = None
# REMOVED_UNUSED_CODE:     strategy: str
# REMOVED_UNUSED_CODE:     enter_tag: str | None = None
# REMOVED_UNUSED_CODE:     timeframe: int
# REMOVED_UNUSED_CODE:     fee_open: float | None = None
# REMOVED_UNUSED_CODE:     fee_open_cost: float | None = None
# REMOVED_UNUSED_CODE:     fee_open_currency: str | None = None
# REMOVED_UNUSED_CODE:     fee_close: float | None = None
# REMOVED_UNUSED_CODE:     fee_close_cost: float | None = None
# REMOVED_UNUSED_CODE:     fee_close_currency: str | None = None

# REMOVED_UNUSED_CODE:     open_date: str
# REMOVED_UNUSED_CODE:     open_timestamp: int
# REMOVED_UNUSED_CODE:     open_fill_date: str | None
# REMOVED_UNUSED_CODE:     open_fill_timestamp: int | None
# REMOVED_UNUSED_CODE:     open_rate: float
# REMOVED_UNUSED_CODE:     open_rate_requested: float | None = None
# REMOVED_UNUSED_CODE:     open_trade_value: float

# REMOVED_UNUSED_CODE:     close_date: str | None = None
# REMOVED_UNUSED_CODE:     close_timestamp: int | None = None
# REMOVED_UNUSED_CODE:     close_rate: float | None = None
# REMOVED_UNUSED_CODE:     close_rate_requested: float | None = None

# REMOVED_UNUSED_CODE:     close_profit: float | None = None
# REMOVED_UNUSED_CODE:     close_profit_pct: float | None = None
# REMOVED_UNUSED_CODE:     close_profit_abs: float | None = None

# REMOVED_UNUSED_CODE:     profit_ratio: float | None = None
# REMOVED_UNUSED_CODE:     profit_pct: float | None = None
# REMOVED_UNUSED_CODE:     profit_abs: float | None = None
# REMOVED_UNUSED_CODE:     profit_fiat: float | None = None

# REMOVED_UNUSED_CODE:     realized_profit: float
# REMOVED_UNUSED_CODE:     realized_profit_ratio: float | None = None

# REMOVED_UNUSED_CODE:     exit_reason: str | None = None
# REMOVED_UNUSED_CODE:     exit_order_status: str | None = None

# REMOVED_UNUSED_CODE:     stop_loss_abs: float | None = None
# REMOVED_UNUSED_CODE:     stop_loss_ratio: float | None = None
# REMOVED_UNUSED_CODE:     stop_loss_pct: float | None = None
# REMOVED_UNUSED_CODE:     stoploss_last_update: str | None = None
# REMOVED_UNUSED_CODE:     stoploss_last_update_timestamp: int | None = None
# REMOVED_UNUSED_CODE:     initial_stop_loss_abs: float | None = None
# REMOVED_UNUSED_CODE:     initial_stop_loss_ratio: float | None = None
# REMOVED_UNUSED_CODE:     initial_stop_loss_pct: float | None = None

# REMOVED_UNUSED_CODE:     min_rate: float | None = None
# REMOVED_UNUSED_CODE:     max_rate: float | None = None
# REMOVED_UNUSED_CODE:     has_open_orders: bool
# REMOVED_UNUSED_CODE:     orders: list[OrderSchema]

# REMOVED_UNUSED_CODE:     leverage: float | None = None
# REMOVED_UNUSED_CODE:     interest_rate: float | None = None
# REMOVED_UNUSED_CODE:     liquidation_price: float | None = None
# REMOVED_UNUSED_CODE:     funding_fees: float | None = None
# REMOVED_UNUSED_CODE:     trading_mode: TradingMode | None = None

# REMOVED_UNUSED_CODE:     amount_precision: float | None = None
# REMOVED_UNUSED_CODE:     price_precision: float | None = None
# REMOVED_UNUSED_CODE:     precision_mode: int | None = None


# REMOVED_UNUSED_CODE: class OpenTradeSchema(TradeSchema):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     stoploss_current_dist: float | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     stoploss_current_dist_pct: float | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     stoploss_current_dist_ratio: float | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     stoploss_entry_dist: float | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     stoploss_entry_dist_ratio: float | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     current_rate: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     total_profit_abs: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     total_profit_fiat: float | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     total_profit_ratio: float | None = None


# REMOVED_UNUSED_CODE: class TradeResponse(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     trades: list[TradeSchema]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     trades_count: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     offset: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     total_trades: int


# REMOVED_UNUSED_CODE: ForceEnterResponse = RootModel[TradeSchema | StatusMsg]


class LockModel(BaseModel):
# REMOVED_UNUSED_CODE:     id: int
# REMOVED_UNUSED_CODE:     active: bool
# REMOVED_UNUSED_CODE:     lock_end_time: str
# REMOVED_UNUSED_CODE:     lock_end_timestamp: int
# REMOVED_UNUSED_CODE:     lock_time: str
# REMOVED_UNUSED_CODE:     lock_timestamp: int
# REMOVED_UNUSED_CODE:     pair: str
# REMOVED_UNUSED_CODE:     side: str
# REMOVED_UNUSED_CODE:     reason: str | None = None


# REMOVED_UNUSED_CODE: class Locks(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     lock_count: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     locks: list[LockModel]


# REMOVED_UNUSED_CODE: class LocksPayload(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     pair: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     side: str = "*"  # Default to both sides
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     until: AwareDatetime
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     reason: str | None = None


# REMOVED_UNUSED_CODE: class DeleteLockRequest(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     pair: str | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     lockid: int | None = None


# REMOVED_UNUSED_CODE: class Logs(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     log_count: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     logs: list[list]


# REMOVED_UNUSED_CODE: class ForceEnterPayload(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     pair: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     side: SignalDirection = SignalDirection.LONG
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     price: float | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ordertype: OrderTypeValues | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     stakeamount: float | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     entry_tag: str | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     leverage: float | None = None


# REMOVED_UNUSED_CODE: class ForceExitPayload(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     tradeid: str | int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ordertype: OrderTypeValues | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     amount: float | None = None


# REMOVED_UNUSED_CODE: class BlacklistPayload(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     blacklist: list[str]


# REMOVED_UNUSED_CODE: class BlacklistResponse(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     blacklist: list[str]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     blacklist_expanded: list[str]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     errors: dict
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     length: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     method: list[str]


class WhitelistResponse(BaseModel):
# REMOVED_UNUSED_CODE:     whitelist: list[str]
# REMOVED_UNUSED_CODE:     length: int
# REMOVED_UNUSED_CODE:     method: list[str]


# REMOVED_UNUSED_CODE: class WhitelistEvaluateResponse(BackgroundTaskResult):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     result: WhitelistResponse | None = None


# REMOVED_UNUSED_CODE: class DeleteTrade(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     cancel_order_count: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     result: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     result_msg: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     trade_id: int


class PlotConfig_(BaseModel):
# REMOVED_UNUSED_CODE:     main_plot: dict[str, Any]
# REMOVED_UNUSED_CODE:     subplots: dict[str, Any]


# REMOVED_UNUSED_CODE: PlotConfig = RootModel[PlotConfig_ | dict]


# REMOVED_UNUSED_CODE: class StrategyListResponse(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     strategies: list[str]


# REMOVED_UNUSED_CODE: class ExchangeListResponse(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     exchanges: list[ValidExchangesType]


class HyperoptLoss(BaseModel):
# REMOVED_UNUSED_CODE:     name: str
# REMOVED_UNUSED_CODE:     description: str


# REMOVED_UNUSED_CODE: class HyperoptLossListResponse(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     loss_functions: list[HyperoptLoss]


class PairListResponse(BaseModel):
# REMOVED_UNUSED_CODE:     name: str
# REMOVED_UNUSED_CODE:     description: str
# REMOVED_UNUSED_CODE:     is_pairlist_generator: bool
# REMOVED_UNUSED_CODE:     params: dict[str, Any]


# REMOVED_UNUSED_CODE: class PairListsResponse(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     pairlists: list[PairListResponse]


# REMOVED_UNUSED_CODE: class PairListsPayload(ExchangeModePayloadMixin, BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     pairlists: list[dict[str, Any]]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     blacklist: list[str]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     stake_currency: str


# REMOVED_UNUSED_CODE: class DownloadDataPayload(ExchangeModePayloadMixin, BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     pairs: list[str]
# REMOVED_UNUSED_CODE:     timeframes: list[str] | None = DL_DATA_TIMEFRAMES
# REMOVED_UNUSED_CODE:     days: int | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     timerange: str | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     erase: bool = False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     download_trades: bool = False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @model_validator(mode="before")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def check_mutually_exclusive(cls, values):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         timeframes, days = values.get("timerange"), values.get("days")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if timeframes and days:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise ValueError("Only one of timeframes or days can be provided, not both.")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return values


# REMOVED_UNUSED_CODE: class FreqAIModelListResponse(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     freqaimodels: list[str]


# REMOVED_UNUSED_CODE: class StrategyResponse(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     strategy: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     code: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     timeframe: str | None


# REMOVED_UNUSED_CODE: class AvailablePairs(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     length: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     pairs: list[str]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     pair_interval: list[list[str]]


class PairCandlesRequest(BaseModel):
# REMOVED_UNUSED_CODE:     pair: str
# REMOVED_UNUSED_CODE:     timeframe: str
# REMOVED_UNUSED_CODE:     limit: int | None = None
# REMOVED_UNUSED_CODE:     columns: list[str] | None = None


# REMOVED_UNUSED_CODE: class PairHistoryRequest(PairCandlesRequest, ExchangeModePayloadMixin):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     timerange: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     strategy: str | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     freqaimodel: str | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     live_mode: bool = False


# REMOVED_UNUSED_CODE: class PairHistory(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     strategy: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     pair: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     timeframe: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     timeframe_ms: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     columns: list[str]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     all_columns: list[str] = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     data: SerializeAsAny[list[Any]]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     length: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     buy_signals: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     sell_signals: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     enter_long_signals: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     exit_long_signals: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     enter_short_signals: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     exit_short_signals: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     last_analyzed: datetime
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     last_analyzed_ts: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     data_start_ts: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     data_start: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     data_stop: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     data_stop_ts: int


class BacktestFreqAIInputs(BaseModel):
# REMOVED_UNUSED_CODE:     identifier: str


# REMOVED_UNUSED_CODE: class BacktestRequest(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     strategy: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     timeframe: str | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     timeframe_detail: str | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     timerange: str | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     max_open_trades: IntOrInf | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     stake_amount: str | float | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     enable_protections: bool
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     dry_run_wallet: float | None = None
# REMOVED_UNUSED_CODE:     backtest_cache: str | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     freqaimodel: str | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     freqai: BacktestFreqAIInputs | None = None


# REMOVED_UNUSED_CODE: class BacktestResponse(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     status: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     running: bool
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     status_msg: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     step: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     progress: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     trade_count: float | None = None
# REMOVED_UNUSED_CODE:     # TODO: Properly type backtestresult...
# REMOVED_UNUSED_CODE:     backtest_result: dict[str, Any] | None = None


# TODO: This is a copy of BacktestHistoryEntryType
# REMOVED_UNUSED_CODE: class BacktestHistoryEntry(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     filename: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     strategy: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     run_id: str
# REMOVED_UNUSED_CODE:     backtest_start_time: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     notes: str | None = ""
# REMOVED_UNUSED_CODE:     backtest_start_ts: int | None = None
# REMOVED_UNUSED_CODE:     backtest_end_ts: int | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     timeframe: str | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     timeframe_detail: str | None = None


# REMOVED_UNUSED_CODE: class BacktestMetadataUpdate(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     strategy: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     notes: str = ""


# REMOVED_UNUSED_CODE: class BacktestMarketChange(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     columns: list[str]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     length: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     data: list[list[Any]]


# REMOVED_UNUSED_CODE: class MarketRequest(ExchangeModePayloadMixin, BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     base: str | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     quote: str | None = None


class MarketModel(BaseModel):
# REMOVED_UNUSED_CODE:     symbol: str
# REMOVED_UNUSED_CODE:     base: str
# REMOVED_UNUSED_CODE:     quote: str
# REMOVED_UNUSED_CODE:     spot: bool
# REMOVED_UNUSED_CODE:     swap: bool


# REMOVED_UNUSED_CODE: class MarketResponse(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     markets: dict[str, MarketModel]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     exchange_id: str


# REMOVED_UNUSED_CODE: class SysInfo(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     cpu_pct: list[float]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ram_pct: float


# REMOVED_UNUSED_CODE: class Health(BaseModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     last_process: datetime | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     last_process_ts: int | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     bot_start: datetime | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     bot_start_ts: int | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     bot_startup: datetime | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     bot_startup_ts: int | None = None
