# pragma pylint: disable=too-few-public-methods

"""
bot constants
"""

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from typing import Any, Literal

# REMOVED_UNUSED_CODE: from freqtrade.enums import CandleType, PriceType


# REMOVED_UNUSED_CODE: DOCS_LINK = "https://www.freqtrade.io/en/stable"
# REMOVED_UNUSED_CODE: DEFAULT_CONFIG = "config.json"
# REMOVED_UNUSED_CODE: PROCESS_THROTTLE_SECS = 5  # sec
# REMOVED_UNUSED_CODE: HYPEROPT_EPOCH = 100  # epochs
# REMOVED_UNUSED_CODE: RETRY_TIMEOUT = 30  # sec
# REMOVED_UNUSED_CODE: TIMEOUT_UNITS = ["minutes", "seconds"]
# REMOVED_UNUSED_CODE: EXPORT_OPTIONS = ["none", "trades", "signals"]
# REMOVED_UNUSED_CODE: DEFAULT_DB_PROD_URL = "sqlite:///tradesv3.sqlite"
# REMOVED_UNUSED_CODE: DEFAULT_DB_DRYRUN_URL = "sqlite:///tradesv3.dryrun.sqlite"
# REMOVED_UNUSED_CODE: UNLIMITED_STAKE_AMOUNT = "unlimited"
# REMOVED_UNUSED_CODE: DEFAULT_AMOUNT_RESERVE_PERCENT = 0.05
# REMOVED_UNUSED_CODE: REQUIRED_ORDERTIF = ["entry", "exit"]
# REMOVED_UNUSED_CODE: REQUIRED_ORDERTYPES = ["entry", "exit", "stoploss", "stoploss_on_exchange"]
# REMOVED_UNUSED_CODE: PRICING_SIDES = ["ask", "bid", "same", "other"]
# REMOVED_UNUSED_CODE: ORDERTYPE_POSSIBILITIES = ["limit", "market"]
_ORDERTIF_POSSIBILITIES = ["GTC", "FOK", "IOC", "PO"]
# REMOVED_UNUSED_CODE: ORDERTIF_POSSIBILITIES = _ORDERTIF_POSSIBILITIES + [t.lower() for t in _ORDERTIF_POSSIBILITIES]
# REMOVED_UNUSED_CODE: STOPLOSS_PRICE_TYPES = [p for p in PriceType]
# REMOVED_UNUSED_CODE: HYPEROPT_LOSS_BUILTIN = [
# REMOVED_UNUSED_CODE:     "ShortTradeDurHyperOptLoss",
# REMOVED_UNUSED_CODE:     "OnlyProfitHyperOptLoss",
# REMOVED_UNUSED_CODE:     "SharpeHyperOptLoss",
# REMOVED_UNUSED_CODE:     "SharpeHyperOptLossDaily",
# REMOVED_UNUSED_CODE:     "SortinoHyperOptLoss",
# REMOVED_UNUSED_CODE:     "SortinoHyperOptLossDaily",
# REMOVED_UNUSED_CODE:     "CalmarHyperOptLoss",
# REMOVED_UNUSED_CODE:     "MaxDrawDownHyperOptLoss",
# REMOVED_UNUSED_CODE:     "MaxDrawDownRelativeHyperOptLoss",
# REMOVED_UNUSED_CODE:     "ProfitDrawDownHyperOptLoss",
# REMOVED_UNUSED_CODE:     "MultiMetricHyperOptLoss",
# REMOVED_UNUSED_CODE: ]
# REMOVED_UNUSED_CODE: AVAILABLE_PAIRLISTS = [
# REMOVED_UNUSED_CODE:     "StaticPairList",
# REMOVED_UNUSED_CODE:     "VolumePairList",
# REMOVED_UNUSED_CODE:     "PercentChangePairList",
# REMOVED_UNUSED_CODE:     "ProducerPairList",
# REMOVED_UNUSED_CODE:     "RemotePairList",
# REMOVED_UNUSED_CODE:     "MarketCapPairList",
# REMOVED_UNUSED_CODE:     "AgeFilter",
# REMOVED_UNUSED_CODE:     "FullTradesFilter",
# REMOVED_UNUSED_CODE:     "OffsetFilter",
# REMOVED_UNUSED_CODE:     "PerformanceFilter",
# REMOVED_UNUSED_CODE:     "PrecisionFilter",
# REMOVED_UNUSED_CODE:     "PriceFilter",
# REMOVED_UNUSED_CODE:     "RangeStabilityFilter",
# REMOVED_UNUSED_CODE:     "ShuffleFilter",
# REMOVED_UNUSED_CODE:     "SpreadFilter",
# REMOVED_UNUSED_CODE:     "VolatilityFilter",
# REMOVED_UNUSED_CODE: ]
# REMOVED_UNUSED_CODE: AVAILABLE_DATAHANDLERS = ["json", "jsongz", "feather", "parquet"]
BACKTEST_BREAKDOWNS = ["day", "week", "month"]
BACKTEST_CACHE_AGE = ["none", "day", "week", "month"]
BACKTEST_CACHE_DEFAULT = "day"
# REMOVED_UNUSED_CODE: DRY_RUN_WALLET = 1000
# REMOVED_UNUSED_CODE: DATETIME_PRINT_FORMAT = "%Y-%m-%d %H:%M:%S"
# REMOVED_UNUSED_CODE: MATH_CLOSE_PREC = 1e-14  # Precision used for float comparisons
# REMOVED_UNUSED_CODE: DEFAULT_DATAFRAME_COLUMNS = ["date", "open", "high", "low", "close", "volume"]
# Don't modify sequence of DEFAULT_TRADES_COLUMNS
# it has wide consequences for stored trades files
# REMOVED_UNUSED_CODE: DEFAULT_TRADES_COLUMNS = ["timestamp", "id", "type", "side", "price", "amount", "cost"]
# REMOVED_UNUSED_CODE: DEFAULT_ORDERFLOW_COLUMNS = ["level", "bid", "ask", "delta"]
# REMOVED_UNUSED_CODE: TRADES_DTYPES = {
# REMOVED_UNUSED_CODE:     "timestamp": "int64",
# REMOVED_UNUSED_CODE:     "id": "str",
# REMOVED_UNUSED_CODE:     "type": "str",
# REMOVED_UNUSED_CODE:     "side": "str",
# REMOVED_UNUSED_CODE:     "price": "float64",
# REMOVED_UNUSED_CODE:     "amount": "float64",
# REMOVED_UNUSED_CODE:     "cost": "float64",
# REMOVED_UNUSED_CODE: }
# REMOVED_UNUSED_CODE: TRADING_MODES = ["spot", "margin", "futures"]
# REMOVED_UNUSED_CODE: MARGIN_MODES = ["cross", "isolated", ""]

# REMOVED_UNUSED_CODE: LAST_BT_RESULT_FN = ".last_result.json"
# REMOVED_UNUSED_CODE: FTHYPT_FILEVERSION = "fthypt_fileversion"

# REMOVED_UNUSED_CODE: USERPATH_HYPEROPTS = "hyperopts"
# REMOVED_UNUSED_CODE: USERPATH_STRATEGIES = "strategies"
# REMOVED_UNUSED_CODE: USERPATH_NOTEBOOKS = "notebooks"
# REMOVED_UNUSED_CODE: USERPATH_FREQAIMODELS = "freqaimodels"

# REMOVED_UNUSED_CODE: TELEGRAM_SETTING_OPTIONS = ["on", "off", "silent"]
# REMOVED_UNUSED_CODE: WEBHOOK_FORMAT_OPTIONS = ["form", "json", "raw"]
# REMOVED_UNUSED_CODE: FULL_DATAFRAME_THRESHOLD = 100
# REMOVED_UNUSED_CODE: CUSTOM_TAG_MAX_LENGTH = 255
# REMOVED_UNUSED_CODE: DL_DATA_TIMEFRAMES = ["1m", "5m"]

# REMOVED_UNUSED_CODE: ENV_VAR_PREFIX = "FREQTRADE__"

# REMOVED_UNUSED_CODE: CANCELED_EXCHANGE_STATES = ("cancelled", "canceled", "expired", "rejected")
# REMOVED_UNUSED_CODE: NON_OPEN_EXCHANGE_STATES = CANCELED_EXCHANGE_STATES + ("closed",)

# Define decimals per coin for outputs
# Only used for outputs.
# REMOVED_UNUSED_CODE: DECIMAL_PER_COIN_FALLBACK = 3  # Should be low to avoid listing all possible FIAT's
# REMOVED_UNUSED_CODE: DECIMALS_PER_COIN = {
# REMOVED_UNUSED_CODE:     "BTC": 8,
# REMOVED_UNUSED_CODE:     "ETH": 5,
# REMOVED_UNUSED_CODE: }

# REMOVED_UNUSED_CODE: DUST_PER_COIN = {"BTC": 0.0001, "ETH": 0.01}

# Source files with destination directories within user-directory
# REMOVED_UNUSED_CODE: USER_DATA_FILES = {
# REMOVED_UNUSED_CODE:     "sample_strategy.py": USERPATH_STRATEGIES,
# REMOVED_UNUSED_CODE:     "sample_hyperopt_loss.py": USERPATH_HYPEROPTS,
# REMOVED_UNUSED_CODE:     "strategy_analysis_example.ipynb": USERPATH_NOTEBOOKS,
# REMOVED_UNUSED_CODE: }

# REMOVED_UNUSED_CODE: SUPPORTED_FIAT = [
# REMOVED_UNUSED_CODE:     "AUD",
# REMOVED_UNUSED_CODE:     "BRL",
# REMOVED_UNUSED_CODE:     "CAD",
# REMOVED_UNUSED_CODE:     "CHF",
# REMOVED_UNUSED_CODE:     "CLP",
# REMOVED_UNUSED_CODE:     "CNY",
# REMOVED_UNUSED_CODE:     "CZK",
# REMOVED_UNUSED_CODE:     "DKK",
# REMOVED_UNUSED_CODE:     "EUR",
# REMOVED_UNUSED_CODE:     "GBP",
# REMOVED_UNUSED_CODE:     "HKD",
# REMOVED_UNUSED_CODE:     "HUF",
# REMOVED_UNUSED_CODE:     "IDR",
# REMOVED_UNUSED_CODE:     "ILS",
# REMOVED_UNUSED_CODE:     "INR",
# REMOVED_UNUSED_CODE:     "JPY",
# REMOVED_UNUSED_CODE:     "KRW",
# REMOVED_UNUSED_CODE:     "MXN",
# REMOVED_UNUSED_CODE:     "MYR",
# REMOVED_UNUSED_CODE:     "NOK",
# REMOVED_UNUSED_CODE:     "NZD",
# REMOVED_UNUSED_CODE:     "PHP",
# REMOVED_UNUSED_CODE:     "PKR",
# REMOVED_UNUSED_CODE:     "PLN",
# REMOVED_UNUSED_CODE:     "RUB",
# REMOVED_UNUSED_CODE:     "UAH",
# REMOVED_UNUSED_CODE:     "SEK",
# REMOVED_UNUSED_CODE:     "SGD",
# REMOVED_UNUSED_CODE:     "THB",
# REMOVED_UNUSED_CODE:     "TRY",
# REMOVED_UNUSED_CODE:     "TWD",
# REMOVED_UNUSED_CODE:     "ZAR",
# REMOVED_UNUSED_CODE:     "USD",
# REMOVED_UNUSED_CODE:     "BTC",
# REMOVED_UNUSED_CODE:     "ETH",
# REMOVED_UNUSED_CODE:     "XRP",
# REMOVED_UNUSED_CODE:     "LTC",
# REMOVED_UNUSED_CODE:     "BCH",
# REMOVED_UNUSED_CODE:     "BNB",
# REMOVED_UNUSED_CODE:     "",  # Allow empty field in config.
# REMOVED_UNUSED_CODE: ]

# REMOVED_UNUSED_CODE: MINIMAL_CONFIG = {
# REMOVED_UNUSED_CODE:     "stake_currency": "",
# REMOVED_UNUSED_CODE:     "dry_run": True,
# REMOVED_UNUSED_CODE:     "exchange": {
# REMOVED_UNUSED_CODE:         "name": "",
# REMOVED_UNUSED_CODE:         "key": "",
# REMOVED_UNUSED_CODE:         "secret": "",
# REMOVED_UNUSED_CODE:         "pair_whitelist": [],
# REMOVED_UNUSED_CODE:         "ccxt_async_config": {},
# REMOVED_UNUSED_CODE:     },
# REMOVED_UNUSED_CODE: }


# REMOVED_UNUSED_CODE: CANCEL_REASON = {
# REMOVED_UNUSED_CODE:     "TIMEOUT": "cancelled due to timeout",
# REMOVED_UNUSED_CODE:     "PARTIALLY_FILLED_KEEP_OPEN": "partially filled - keeping order open",
# REMOVED_UNUSED_CODE:     "PARTIALLY_FILLED": "partially filled",
# REMOVED_UNUSED_CODE:     "FULLY_CANCELLED": "fully cancelled",
# REMOVED_UNUSED_CODE:     "ALL_CANCELLED": "cancelled (all unfilled and partially filled open orders cancelled)",
# REMOVED_UNUSED_CODE:     "CANCELLED_ON_EXCHANGE": "cancelled on exchange",
# REMOVED_UNUSED_CODE:     "FORCE_EXIT": "forcesold",
# REMOVED_UNUSED_CODE:     "REPLACE": "cancelled to be replaced by new limit order",
# REMOVED_UNUSED_CODE:     "REPLACE_FAILED": "failed to replace order, deleting Trade",
# REMOVED_UNUSED_CODE:     "USER_CANCEL": "user requested order cancel",
# REMOVED_UNUSED_CODE: }

# List of pairs with their timeframes
# REMOVED_UNUSED_CODE: PairWithTimeframe = tuple[str, str, CandleType]
# REMOVED_UNUSED_CODE: ListPairsWithTimeframes = list[PairWithTimeframe]

# Type for trades list
# REMOVED_UNUSED_CODE: TradeList = list[list]
# ticks, pair, timeframe, CandleType
# REMOVED_UNUSED_CODE: TickWithTimeframe = tuple[str, str, CandleType, int | None, int | None]
# REMOVED_UNUSED_CODE: ListTicksWithTimeframes = list[TickWithTimeframe]

# REMOVED_UNUSED_CODE: LongShort = Literal["long", "short"]
# REMOVED_UNUSED_CODE: EntryExit = Literal["entry", "exit"]
# REMOVED_UNUSED_CODE: BuySell = Literal["buy", "sell"]
# REMOVED_UNUSED_CODE: MakerTaker = Literal["maker", "taker"]
# REMOVED_UNUSED_CODE: BidAsk = Literal["bid", "ask"]
# REMOVED_UNUSED_CODE: OBLiteral = Literal["asks", "bids"]

# REMOVED_UNUSED_CODE: Config = dict[str, Any]
# Exchange part of the configuration.
# REMOVED_UNUSED_CODE: ExchangeConfig = dict[str, Any]
# REMOVED_UNUSED_CODE: IntOrInf = float


# REMOVED_UNUSED_CODE: EntryExecuteMode = Literal["initial", "pos_adjust", "replace"]
