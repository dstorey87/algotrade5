import logging
import sys
from collections import defaultdict
from typing import Any

from freqtrade.constants import DATETIME_PRINT_FORMAT, DL_DATA_TIMEFRAMES, Config
from freqtrade.enums import CandleType, RunMode, TradingMode
from freqtrade.exceptions import ConfigurationError
from freqtrade.plugins.pairlist.pairlist_helpers import dynamic_expand_pairlist


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


def _check_data_config_download_sanity(config: Config) -> None:
    if "days" in config and "timerange" in config:
        raise ConfigurationError(
            "--days and --timerange are mutually exclusive. You can only specify one or the other."
        )

    if "pairs" not in config:
        raise ConfigurationError(
            "Downloading data requires a list of pairs. "
            "Please check the documentation on how to configure this."
        )


# REMOVED_UNUSED_CODE: def start_download_data(args: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Download data (former download_backtest_data.py script)
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     from freqtrade.configuration import setup_utils_configuration
# REMOVED_UNUSED_CODE:     from freqtrade.data.history import download_data_main
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     config = setup_utils_configuration(args, RunMode.UTIL_EXCHANGE)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     _check_data_config_download_sanity(config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     try:
# REMOVED_UNUSED_CODE:         download_data_main(config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     except KeyboardInterrupt:
# REMOVED_UNUSED_CODE:         sys.exit("SIGINT received, aborting ...")


# REMOVED_UNUSED_CODE: def start_convert_trades(args: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     from freqtrade.configuration import TimeRange, setup_utils_configuration
# REMOVED_UNUSED_CODE:     from freqtrade.data.converter import convert_trades_to_ohlcv
# REMOVED_UNUSED_CODE:     from freqtrade.resolvers import ExchangeResolver
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     config = setup_utils_configuration(args, RunMode.UTIL_EXCHANGE)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     timerange = TimeRange()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Remove stake-currency to skip checks which are not relevant for datadownload
# REMOVED_UNUSED_CODE:     config["stake_currency"] = ""
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if "timeframes" not in config:
# REMOVED_UNUSED_CODE:         config["timeframes"] = DL_DATA_TIMEFRAMES
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Init exchange
# REMOVED_UNUSED_CODE:     exchange = ExchangeResolver.load_exchange(config, validate=False)
# REMOVED_UNUSED_CODE:     # Manual validations of relevant settings
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     for timeframe in config["timeframes"]:
# REMOVED_UNUSED_CODE:         exchange.validate_timeframes(timeframe)
# REMOVED_UNUSED_CODE:     available_pairs = [
# REMOVED_UNUSED_CODE:         p
# REMOVED_UNUSED_CODE:         for p in exchange.get_markets(
# REMOVED_UNUSED_CODE:             tradable_only=True, active_only=not config.get("include_inactive")
# REMOVED_UNUSED_CODE:         ).keys()
# REMOVED_UNUSED_CODE:     ]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     expanded_pairs = dynamic_expand_pairlist(config, available_pairs)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Convert downloaded trade data to different timeframes
# REMOVED_UNUSED_CODE:     convert_trades_to_ohlcv(
# REMOVED_UNUSED_CODE:         pairs=expanded_pairs,
# REMOVED_UNUSED_CODE:         timeframes=config["timeframes"],
# REMOVED_UNUSED_CODE:         datadir=config["datadir"],
# REMOVED_UNUSED_CODE:         timerange=timerange,
# REMOVED_UNUSED_CODE:         erase=bool(config.get("erase")),
# REMOVED_UNUSED_CODE:         data_format_ohlcv=config["dataformat_ohlcv"],
# REMOVED_UNUSED_CODE:         data_format_trades=config["dataformat_trades"],
# REMOVED_UNUSED_CODE:         candle_type=config.get("candle_type_def", CandleType.SPOT),
# REMOVED_UNUSED_CODE:     )


# REMOVED_UNUSED_CODE: def start_convert_data(args: dict[str, Any], ohlcv: bool = True) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Convert data from one format to another
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     from freqtrade.configuration import setup_utils_configuration
# REMOVED_UNUSED_CODE:     from freqtrade.data.converter import convert_ohlcv_format, convert_trades_format
# REMOVED_UNUSED_CODE:     from freqtrade.util.migrations import migrate_data
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     config = setup_utils_configuration(args, RunMode.UTIL_NO_EXCHANGE)
# REMOVED_UNUSED_CODE:     if ohlcv:
# REMOVED_UNUSED_CODE:         migrate_data(config)
# REMOVED_UNUSED_CODE:         convert_ohlcv_format(
# REMOVED_UNUSED_CODE:             config,
# REMOVED_UNUSED_CODE:             convert_from=args["format_from"],
# REMOVED_UNUSED_CODE:             convert_to=args["format_to"],
# REMOVED_UNUSED_CODE:             erase=args["erase"],
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         convert_trades_format(
# REMOVED_UNUSED_CODE:             config,
# REMOVED_UNUSED_CODE:             convert_from=args["format_from_trades"],
# REMOVED_UNUSED_CODE:             convert_to=args["format_to"],
# REMOVED_UNUSED_CODE:             erase=args["erase"],
# REMOVED_UNUSED_CODE:         )


# REMOVED_UNUSED_CODE: def start_list_data(args: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     List available OHLCV data
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     from freqtrade.configuration import setup_utils_configuration
# REMOVED_UNUSED_CODE:     from freqtrade.exchange import timeframe_to_minutes
# REMOVED_UNUSED_CODE:     from freqtrade.util import print_rich_table
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if args["trades"]:
# REMOVED_UNUSED_CODE:         start_list_trades_data(args)
# REMOVED_UNUSED_CODE:         return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     config = setup_utils_configuration(args, RunMode.UTIL_NO_EXCHANGE)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     from freqtrade.data.history import get_datahandler
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     dhc = get_datahandler(config["datadir"], config["dataformat_ohlcv"])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     paircombs = dhc.ohlcv_get_available_data(
# REMOVED_UNUSED_CODE:         config["datadir"], config.get("trading_mode", TradingMode.SPOT)
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     if args["pairs"]:
# REMOVED_UNUSED_CODE:         paircombs = [comb for comb in paircombs if comb[0] in args["pairs"]]
# REMOVED_UNUSED_CODE:     title = f"Found {len(paircombs)} pair / timeframe combinations."
# REMOVED_UNUSED_CODE:     if not config.get("show_timerange"):
# REMOVED_UNUSED_CODE:         groupedpair = defaultdict(list)
# REMOVED_UNUSED_CODE:         for pair, timeframe, candle_type in sorted(
# REMOVED_UNUSED_CODE:             paircombs, key=lambda x: (x[0], timeframe_to_minutes(x[1]), x[2])
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             groupedpair[(pair, candle_type)].append(timeframe)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if groupedpair:
# REMOVED_UNUSED_CODE:             print_rich_table(
# REMOVED_UNUSED_CODE:                 [
# REMOVED_UNUSED_CODE:                     (pair, ", ".join(timeframes), candle_type)
# REMOVED_UNUSED_CODE:                     for (pair, candle_type), timeframes in groupedpair.items()
# REMOVED_UNUSED_CODE:                 ],
# REMOVED_UNUSED_CODE:                 ("Pair", "Timeframe", "Type"),
# REMOVED_UNUSED_CODE:                 title,
# REMOVED_UNUSED_CODE:                 table_kwargs={"min_width": 50},
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         paircombs1 = [
# REMOVED_UNUSED_CODE:             (pair, timeframe, candle_type, *dhc.ohlcv_data_min_max(pair, timeframe, candle_type))
# REMOVED_UNUSED_CODE:             for pair, timeframe, candle_type in paircombs
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE:         print_rich_table(
# REMOVED_UNUSED_CODE:             [
# REMOVED_UNUSED_CODE:                 (
# REMOVED_UNUSED_CODE:                     pair,
# REMOVED_UNUSED_CODE:                     timeframe,
# REMOVED_UNUSED_CODE:                     candle_type,
# REMOVED_UNUSED_CODE:                     start.strftime(DATETIME_PRINT_FORMAT),
# REMOVED_UNUSED_CODE:                     end.strftime(DATETIME_PRINT_FORMAT),
# REMOVED_UNUSED_CODE:                     str(length),
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 for pair, timeframe, candle_type, start, end, length in sorted(
# REMOVED_UNUSED_CODE:                     paircombs1, key=lambda x: (x[0], timeframe_to_minutes(x[1]), x[2])
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             ],
# REMOVED_UNUSED_CODE:             ("Pair", "Timeframe", "Type", "From", "To", "Candles"),
# REMOVED_UNUSED_CODE:             summary=title,
# REMOVED_UNUSED_CODE:             table_kwargs={"min_width": 50},
# REMOVED_UNUSED_CODE:         )


def start_list_trades_data(args: dict[str, Any]) -> None:
    """
    List available Trades data
    """
    from freqtrade.configuration import setup_utils_configuration
    from freqtrade.misc import plural
    from freqtrade.util import print_rich_table

    config = setup_utils_configuration(args, RunMode.UTIL_NO_EXCHANGE)

    from freqtrade.data.history import get_datahandler

    dhc = get_datahandler(config["datadir"], config["dataformat_trades"])

    paircombs = dhc.trades_get_available_data(
        config["datadir"], config.get("trading_mode", TradingMode.SPOT)
    )

    if args["pairs"]:
        paircombs = [comb for comb in paircombs if comb in args["pairs"]]

    title = f"Found trades data for {len(paircombs)} {plural(len(paircombs), 'pair')}."
    if not config.get("show_timerange"):
        print_rich_table(
            [(pair, config.get("candle_type_def", CandleType.SPOT)) for pair in sorted(paircombs)],
            ("Pair", "Type"),
            title,
            table_kwargs={"min_width": 50},
        )
    else:
        paircombs1 = [
            (pair, *dhc.trades_data_min_max(pair, config.get("trading_mode", TradingMode.SPOT)))
            for pair in paircombs
        ]
        print_rich_table(
            [
                (
                    pair,
                    config.get("candle_type_def", CandleType.SPOT),
                    start.strftime(DATETIME_PRINT_FORMAT),
                    end.strftime(DATETIME_PRINT_FORMAT),
                    str(length),
                )
                for pair, start, end, length in sorted(paircombs1, key=lambda x: (x[0]))
            ],
            ("Pair", "Type", "From", "To", "Trades"),
            summary=title,
            table_kwargs={"min_width": 50},
        )
