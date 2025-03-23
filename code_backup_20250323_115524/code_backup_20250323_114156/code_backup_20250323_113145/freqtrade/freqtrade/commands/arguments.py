"""
This module contains the argument manager class
"""

from argparse import ArgumentParser, Namespace, _ArgumentGroup
from functools import partial
from pathlib import Path
from typing import Any

from freqtrade.commands.cli_options import AVAILABLE_CLI_OPTIONS
from freqtrade.constants import DEFAULT_CONFIG


ARGS_COMMON = [
    "verbosity",
    "print_colorized",
    "logfile",
    "version",
    "config",
    "datadir",
    "user_data_dir",
]

ARGS_STRATEGY = [
    "strategy",
    "strategy_path",
    "recursive_strategy_search",
    "freqaimodel",
    "freqaimodel_path",
]

ARGS_TRADE = ["db_url", "sd_notify", "dry_run", "dry_run_wallet", "fee"]

ARGS_WEBSERVER: list[str] = []

ARGS_COMMON_OPTIMIZE = [
    "timeframe",
    "timerange",
    "dataformat_ohlcv",
    "max_open_trades",
    "stake_amount",
    "fee",
    "pairs",
]

ARGS_BACKTEST = ARGS_COMMON_OPTIMIZE + [
    "position_stacking",
    "enable_protections",
    "dry_run_wallet",
    "timeframe_detail",
    "strategy_list",
    "export",
    "exportfilename",
    "backtest_breakdown",
    "backtest_cache",
    "freqai_backtest_live_models",
]

ARGS_HYPEROPT = ARGS_COMMON_OPTIMIZE + [
    "hyperopt",
    "hyperopt_path",
    "position_stacking",
    "enable_protections",
    "dry_run_wallet",
    "timeframe_detail",
    "epochs",
    "spaces",
    "print_all",
    "print_json",
    "hyperopt_jobs",
    "hyperopt_random_state",
    "hyperopt_min_trades",
    "hyperopt_loss",
    "disableparamexport",
    "hyperopt_ignore_missing_space",
    "analyze_per_epoch",
]

ARGS_EDGE = ARGS_COMMON_OPTIMIZE + ["stoploss_range"]

ARGS_LIST_STRATEGIES = [
    "strategy_path",
    "print_one_column",
    "recursive_strategy_search",
]

ARGS_LIST_FREQAIMODELS = ["freqaimodel_path", "print_one_column"]

ARGS_LIST_HYPEROPTS = ["hyperopt_path", "print_one_column"]

ARGS_BACKTEST_SHOW = ["exportfilename", "backtest_show_pair_list", "backtest_breakdown"]

ARGS_LIST_EXCHANGES = ["print_one_column", "list_exchanges_all"]

ARGS_LIST_TIMEFRAMES = ["exchange", "print_one_column"]

ARGS_LIST_PAIRS = [
    "exchange",
    "print_list",
    "list_pairs_print_json",
    "print_one_column",
    "print_csv",
    "base_currencies",
    "quote_currencies",
    "list_pairs_all",
    "trading_mode",
]

ARGS_TEST_PAIRLIST = [
    "user_data_dir",
    "verbosity",
    "config",
    "quote_currencies",
    "print_one_column",
    "list_pairs_print_json",
    "exchange",
]

ARGS_CREATE_USERDIR = ["user_data_dir", "reset"]

ARGS_BUILD_CONFIG = ["config"]
ARGS_SHOW_CONFIG = ["user_data_dir", "config", "show_sensitive"]

ARGS_BUILD_STRATEGY = ["user_data_dir", "strategy", "strategy_path", "template"]

ARGS_CONVERT_DATA_TRADES = ["pairs", "format_from_trades", "format_to", "erase", "exchange"]
ARGS_CONVERT_DATA = ["pairs", "format_from", "format_to", "erase", "exchange"]
ARGS_CONVERT_DATA_OHLCV = ARGS_CONVERT_DATA + ["timeframes", "trading_mode", "candle_types"]

ARGS_CONVERT_TRADES = [
    "pairs",
    "timeframes",
    "exchange",
    "dataformat_ohlcv",
    "dataformat_trades",
    "trading_mode",
]

ARGS_LIST_DATA = [
    "exchange",
    "dataformat_ohlcv",
    "dataformat_trades",
    "trades",
    "pairs",
    "trading_mode",
    "show_timerange",
]

ARGS_DOWNLOAD_DATA = [
    "pairs",
    "pairs_file",
    "days",
    "new_pairs_days",
    "include_inactive",
    "timerange",
    "download_trades",
    "convert_trades",
    "exchange",
    "timeframes",
    "erase",
    "dataformat_ohlcv",
    "dataformat_trades",
    "trading_mode",
    "prepend_data",
]

ARGS_PLOT_DATAFRAME = [
    "pairs",
    "indicators1",
    "indicators2",
    "plot_limit",
    "db_url",
    "trade_source",
    "export",
    "exportfilename",
    "timerange",
    "timeframe",
    "no_trades",
]

ARGS_PLOT_PROFIT = [
    "pairs",
    "timerange",
    "export",
    "exportfilename",
    "db_url",
    "trade_source",
    "timeframe",
    "plot_auto_open",
]

ARGS_CONVERT_DB = ["db_url", "db_url_from"]

ARGS_INSTALL_UI = ["erase_ui_only", "ui_version"]

ARGS_SHOW_TRADES = ["db_url", "trade_ids", "print_json"]

ARGS_HYPEROPT_LIST = [
    "hyperopt_list_best",
    "hyperopt_list_profitable",
    "hyperopt_list_min_trades",
    "hyperopt_list_max_trades",
    "hyperopt_list_min_avg_time",
    "hyperopt_list_max_avg_time",
    "hyperopt_list_min_avg_profit",
    "hyperopt_list_max_avg_profit",
    "hyperopt_list_min_total_profit",
    "hyperopt_list_max_total_profit",
    "hyperopt_list_min_objective",
    "hyperopt_list_max_objective",
    "print_json",
    "hyperopt_list_no_details",
    "hyperoptexportfilename",
    "export_csv",
]

ARGS_HYPEROPT_SHOW = [
    "hyperopt_list_best",
    "hyperopt_list_profitable",
    "hyperopt_show_index",
    "print_json",
    "hyperoptexportfilename",
    "hyperopt_show_no_header",
    "disableparamexport",
    "backtest_breakdown",
]

ARGS_ANALYZE_ENTRIES_EXITS = [
    "exportfilename",
    "analysis_groups",
    "enter_reason_list",
    "exit_reason_list",
    "indicator_list",
    "entry_only",
    "exit_only",
    "timerange",
    "analysis_rejected",
    "analysis_to_csv",
    "analysis_csv_path",
]


ARGS_STRATEGY_UPDATER = ["strategy_list", "strategy_path", "recursive_strategy_search"]

ARGS_LOOKAHEAD_ANALYSIS = [
    a
    for a in ARGS_BACKTEST
    if a not in ("position_stacking", "backtest_cache", "backtest_breakdown")
] + ["minimum_trade_amount", "targeted_trade_amount", "lookahead_analysis_exportfilename"]

ARGS_RECURSIVE_ANALYSIS = ["timeframe", "timerange", "dataformat_ohlcv", "pairs", "startup_candle"]

# Command level configs - keep at the bottom of the above definitions
NO_CONF_REQURIED = [
    "convert-data",
    "convert-trade-data",
    "download-data",
    "list-timeframes",
    "list-markets",
    "list-pairs",
    "list-strategies",
    "list-freqaimodels",
    "list-hyperoptloss",
    "list-data",
    "hyperopt-list",
    "hyperopt-show",
    "backtest-filter",
    "plot-dataframe",
    "plot-profit",
    "show-trades",
    "trades-to-ohlcv",
    "strategy-updater",
]

# REMOVED_UNUSED_CODE: NO_CONF_ALLOWED = ["create-userdir", "list-exchanges", "new-strategy"]


# REMOVED_UNUSED_CODE: class Arguments:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Arguments Class. Manage the arguments received by the cli
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, args: list[str] | None) -> None:
# REMOVED_UNUSED_CODE:         self.args = args
# REMOVED_UNUSED_CODE:         self._parsed_arg: Namespace | None = None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_parsed_arg(self) -> dict[str, Any]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Return the list of arguments
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: List[str] List of arguments
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._parsed_arg is None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._build_subcommands()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._parsed_arg = self._parse_args()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return vars(self._parsed_arg)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _parse_args(self) -> Namespace:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Parses given arguments and returns an argparse Namespace instance.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         parsed_arg = self.parser.parse_args(self.args)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Workaround issue in argparse with action='append' and default value
# REMOVED_UNUSED_CODE:         # (see https://bugs.python.org/issue16399)
# REMOVED_UNUSED_CODE:         # Allow no-config for certain commands (like downloading / plotting)
# REMOVED_UNUSED_CODE:         if "config" in parsed_arg and parsed_arg.config is None:
# REMOVED_UNUSED_CODE:             conf_required = "command" in parsed_arg and parsed_arg.command in NO_CONF_REQURIED
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if "user_data_dir" in parsed_arg and parsed_arg.user_data_dir is not None:
# REMOVED_UNUSED_CODE:                 user_dir = parsed_arg.user_data_dir
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 # Default case
# REMOVED_UNUSED_CODE:                 user_dir = "user_data"
# REMOVED_UNUSED_CODE:                 # Try loading from "user_data/config.json"
# REMOVED_UNUSED_CODE:             cfgfile = Path(user_dir) / DEFAULT_CONFIG
# REMOVED_UNUSED_CODE:             if cfgfile.is_file():
# REMOVED_UNUSED_CODE:                 parsed_arg.config = [str(cfgfile)]
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 # Else use "config.json".
# REMOVED_UNUSED_CODE:                 cfgfile = Path.cwd() / DEFAULT_CONFIG
# REMOVED_UNUSED_CODE:                 if cfgfile.is_file() or not conf_required:
# REMOVED_UNUSED_CODE:                     parsed_arg.config = [DEFAULT_CONFIG]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return parsed_arg
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _build_args(self, optionlist: list[str], parser: ArgumentParser | _ArgumentGroup) -> None:
# REMOVED_UNUSED_CODE:         for val in optionlist:
# REMOVED_UNUSED_CODE:             opt = AVAILABLE_CLI_OPTIONS[val]
# REMOVED_UNUSED_CODE:             parser.add_argument(*opt.cli, dest=val, **opt.kwargs)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _build_subcommands(self) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Builds and attaches all subcommands.
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         # Build shared arguments (as group Common Options)
# REMOVED_UNUSED_CODE:         _common_parser = ArgumentParser(add_help=False)
# REMOVED_UNUSED_CODE:         group = _common_parser.add_argument_group("Common arguments")
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_COMMON, parser=group)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         _strategy_parser = ArgumentParser(add_help=False)
# REMOVED_UNUSED_CODE:         strategy_group = _strategy_parser.add_argument_group("Strategy arguments")
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_STRATEGY, parser=strategy_group)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Build main command
# REMOVED_UNUSED_CODE:         self.parser = ArgumentParser(
# REMOVED_UNUSED_CODE:             prog="freqtrade", description="Free, open source crypto trading bot"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=["version_main"], parser=self.parser)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         from freqtrade.commands import (
# REMOVED_UNUSED_CODE:             start_analysis_entries_exits,
# REMOVED_UNUSED_CODE:             start_backtesting,
# REMOVED_UNUSED_CODE:             start_backtesting_show,
# REMOVED_UNUSED_CODE:             start_convert_data,
# REMOVED_UNUSED_CODE:             start_convert_db,
# REMOVED_UNUSED_CODE:             start_convert_trades,
# REMOVED_UNUSED_CODE:             start_create_userdir,
# REMOVED_UNUSED_CODE:             start_download_data,
# REMOVED_UNUSED_CODE:             start_edge,
# REMOVED_UNUSED_CODE:             start_hyperopt,
# REMOVED_UNUSED_CODE:             start_hyperopt_list,
# REMOVED_UNUSED_CODE:             start_hyperopt_show,
# REMOVED_UNUSED_CODE:             start_install_ui,
# REMOVED_UNUSED_CODE:             start_list_data,
# REMOVED_UNUSED_CODE:             start_list_exchanges,
# REMOVED_UNUSED_CODE:             start_list_freqAI_models,
# REMOVED_UNUSED_CODE:             start_list_hyperopt_loss_functions,
# REMOVED_UNUSED_CODE:             start_list_markets,
# REMOVED_UNUSED_CODE:             start_list_strategies,
# REMOVED_UNUSED_CODE:             start_list_timeframes,
# REMOVED_UNUSED_CODE:             start_lookahead_analysis,
# REMOVED_UNUSED_CODE:             start_new_config,
# REMOVED_UNUSED_CODE:             start_new_strategy,
# REMOVED_UNUSED_CODE:             start_plot_dataframe,
# REMOVED_UNUSED_CODE:             start_plot_profit,
# REMOVED_UNUSED_CODE:             start_recursive_analysis,
# REMOVED_UNUSED_CODE:             start_show_config,
# REMOVED_UNUSED_CODE:             start_show_trades,
# REMOVED_UNUSED_CODE:             start_strategy_update,
# REMOVED_UNUSED_CODE:             start_test_pairlist,
# REMOVED_UNUSED_CODE:             start_trading,
# REMOVED_UNUSED_CODE:             start_webserver,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         subparsers = self.parser.add_subparsers(
# REMOVED_UNUSED_CODE:             dest="command",
# REMOVED_UNUSED_CODE:             # Use custom message when no subhandler is added
# REMOVED_UNUSED_CODE:             # shown from `main.py`
# REMOVED_UNUSED_CODE:             # required=True
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add trade subcommand
# REMOVED_UNUSED_CODE:         trade_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "trade", help="Trade module.", parents=[_common_parser, _strategy_parser]
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         trade_cmd.set_defaults(func=start_trading)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_TRADE, parser=trade_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # add create-userdir subcommand
# REMOVED_UNUSED_CODE:         create_userdir_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "create-userdir",
# REMOVED_UNUSED_CODE:             help="Create user-data directory.",
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         create_userdir_cmd.set_defaults(func=start_create_userdir)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_CREATE_USERDIR, parser=create_userdir_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # add new-config subcommand
# REMOVED_UNUSED_CODE:         build_config_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "new-config",
# REMOVED_UNUSED_CODE:             help="Create new config",
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         build_config_cmd.set_defaults(func=start_new_config)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_BUILD_CONFIG, parser=build_config_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # add show-config subcommand
# REMOVED_UNUSED_CODE:         show_config_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "show-config",
# REMOVED_UNUSED_CODE:             help="Show resolved config",
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         show_config_cmd.set_defaults(func=start_show_config)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_SHOW_CONFIG, parser=show_config_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # add new-strategy subcommand
# REMOVED_UNUSED_CODE:         build_strategy_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "new-strategy",
# REMOVED_UNUSED_CODE:             help="Create new strategy",
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         build_strategy_cmd.set_defaults(func=start_new_strategy)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_BUILD_STRATEGY, parser=build_strategy_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add download-data subcommand
# REMOVED_UNUSED_CODE:         download_data_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "download-data",
# REMOVED_UNUSED_CODE:             help="Download backtesting data.",
# REMOVED_UNUSED_CODE:             parents=[_common_parser],
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         download_data_cmd.set_defaults(func=start_download_data)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_DOWNLOAD_DATA, parser=download_data_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add convert-data subcommand
# REMOVED_UNUSED_CODE:         convert_data_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "convert-data",
# REMOVED_UNUSED_CODE:             help="Convert candle (OHLCV) data from one format to another.",
# REMOVED_UNUSED_CODE:             parents=[_common_parser],
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         convert_data_cmd.set_defaults(func=partial(start_convert_data, ohlcv=True))
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_CONVERT_DATA_OHLCV, parser=convert_data_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add convert-trade-data subcommand
# REMOVED_UNUSED_CODE:         convert_trade_data_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "convert-trade-data",
# REMOVED_UNUSED_CODE:             help="Convert trade data from one format to another.",
# REMOVED_UNUSED_CODE:             parents=[_common_parser],
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         convert_trade_data_cmd.set_defaults(func=partial(start_convert_data, ohlcv=False))
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_CONVERT_DATA_TRADES, parser=convert_trade_data_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add trades-to-ohlcv subcommand
# REMOVED_UNUSED_CODE:         convert_trade_data_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "trades-to-ohlcv",
# REMOVED_UNUSED_CODE:             help="Convert trade data to OHLCV data.",
# REMOVED_UNUSED_CODE:             parents=[_common_parser],
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         convert_trade_data_cmd.set_defaults(func=start_convert_trades)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_CONVERT_TRADES, parser=convert_trade_data_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add list-data subcommand
# REMOVED_UNUSED_CODE:         list_data_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "list-data",
# REMOVED_UNUSED_CODE:             help="List downloaded data.",
# REMOVED_UNUSED_CODE:             parents=[_common_parser],
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         list_data_cmd.set_defaults(func=start_list_data)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_LIST_DATA, parser=list_data_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add backtesting subcommand
# REMOVED_UNUSED_CODE:         backtesting_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "backtesting", help="Backtesting module.", parents=[_common_parser, _strategy_parser]
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         backtesting_cmd.set_defaults(func=start_backtesting)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_BACKTEST, parser=backtesting_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add backtesting-show subcommand
# REMOVED_UNUSED_CODE:         backtesting_show_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "backtesting-show",
# REMOVED_UNUSED_CODE:             help="Show past Backtest results",
# REMOVED_UNUSED_CODE:             parents=[_common_parser],
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         backtesting_show_cmd.set_defaults(func=start_backtesting_show)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_BACKTEST_SHOW, parser=backtesting_show_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add backtesting analysis subcommand
# REMOVED_UNUSED_CODE:         analysis_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "backtesting-analysis", help="Backtest Analysis module.", parents=[_common_parser]
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         analysis_cmd.set_defaults(func=start_analysis_entries_exits)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_ANALYZE_ENTRIES_EXITS, parser=analysis_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add edge subcommand
# REMOVED_UNUSED_CODE:         edge_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "edge", help="Edge module.", parents=[_common_parser, _strategy_parser]
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         edge_cmd.set_defaults(func=start_edge)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_EDGE, parser=edge_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add hyperopt subcommand
# REMOVED_UNUSED_CODE:         hyperopt_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "hyperopt",
# REMOVED_UNUSED_CODE:             help="Hyperopt module.",
# REMOVED_UNUSED_CODE:             parents=[_common_parser, _strategy_parser],
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         hyperopt_cmd.set_defaults(func=start_hyperopt)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_HYPEROPT, parser=hyperopt_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add hyperopt-list subcommand
# REMOVED_UNUSED_CODE:         hyperopt_list_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "hyperopt-list",
# REMOVED_UNUSED_CODE:             help="List Hyperopt results",
# REMOVED_UNUSED_CODE:             parents=[_common_parser],
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         hyperopt_list_cmd.set_defaults(func=start_hyperopt_list)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_HYPEROPT_LIST, parser=hyperopt_list_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add hyperopt-show subcommand
# REMOVED_UNUSED_CODE:         hyperopt_show_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "hyperopt-show",
# REMOVED_UNUSED_CODE:             help="Show details of Hyperopt results",
# REMOVED_UNUSED_CODE:             parents=[_common_parser],
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         hyperopt_show_cmd.set_defaults(func=start_hyperopt_show)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_HYPEROPT_SHOW, parser=hyperopt_show_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add list-exchanges subcommand
# REMOVED_UNUSED_CODE:         list_exchanges_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "list-exchanges",
# REMOVED_UNUSED_CODE:             help="Print available exchanges.",
# REMOVED_UNUSED_CODE:             parents=[_common_parser],
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         list_exchanges_cmd.set_defaults(func=start_list_exchanges)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_LIST_EXCHANGES, parser=list_exchanges_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add list-markets subcommand
# REMOVED_UNUSED_CODE:         list_markets_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "list-markets",
# REMOVED_UNUSED_CODE:             help="Print markets on exchange.",
# REMOVED_UNUSED_CODE:             parents=[_common_parser],
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         list_markets_cmd.set_defaults(func=partial(start_list_markets, pairs_only=False))
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_LIST_PAIRS, parser=list_markets_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add list-pairs subcommand
# REMOVED_UNUSED_CODE:         list_pairs_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "list-pairs",
# REMOVED_UNUSED_CODE:             help="Print pairs on exchange.",
# REMOVED_UNUSED_CODE:             parents=[_common_parser],
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         list_pairs_cmd.set_defaults(func=partial(start_list_markets, pairs_only=True))
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_LIST_PAIRS, parser=list_pairs_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add list-strategies subcommand
# REMOVED_UNUSED_CODE:         list_strategies_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "list-strategies",
# REMOVED_UNUSED_CODE:             help="Print available strategies.",
# REMOVED_UNUSED_CODE:             parents=[_common_parser],
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         list_strategies_cmd.set_defaults(func=start_list_strategies)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_LIST_STRATEGIES, parser=list_strategies_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add list-Hyperopt loss subcommand
# REMOVED_UNUSED_CODE:         list_hyperopt_loss_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "list-hyperoptloss",
# REMOVED_UNUSED_CODE:             help="Print available hyperopt loss functions.",
# REMOVED_UNUSED_CODE:             parents=[_common_parser],
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         list_hyperopt_loss_cmd.set_defaults(func=start_list_hyperopt_loss_functions)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_LIST_HYPEROPTS, parser=list_hyperopt_loss_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add list-freqAI Models subcommand
# REMOVED_UNUSED_CODE:         list_freqaimodels_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "list-freqaimodels",
# REMOVED_UNUSED_CODE:             help="Print available freqAI models.",
# REMOVED_UNUSED_CODE:             parents=[_common_parser],
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         list_freqaimodels_cmd.set_defaults(func=start_list_freqAI_models)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_LIST_FREQAIMODELS, parser=list_freqaimodels_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add list-timeframes subcommand
# REMOVED_UNUSED_CODE:         list_timeframes_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "list-timeframes",
# REMOVED_UNUSED_CODE:             help="Print available timeframes for the exchange.",
# REMOVED_UNUSED_CODE:             parents=[_common_parser],
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         list_timeframes_cmd.set_defaults(func=start_list_timeframes)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_LIST_TIMEFRAMES, parser=list_timeframes_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add show-trades subcommand
# REMOVED_UNUSED_CODE:         show_trades = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "show-trades",
# REMOVED_UNUSED_CODE:             help="Show trades.",
# REMOVED_UNUSED_CODE:             parents=[_common_parser],
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         show_trades.set_defaults(func=start_show_trades)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_SHOW_TRADES, parser=show_trades)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add test-pairlist subcommand
# REMOVED_UNUSED_CODE:         test_pairlist_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "test-pairlist",
# REMOVED_UNUSED_CODE:             help="Test your pairlist configuration.",
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         test_pairlist_cmd.set_defaults(func=start_test_pairlist)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_TEST_PAIRLIST, parser=test_pairlist_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add db-convert subcommand
# REMOVED_UNUSED_CODE:         convert_db = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "convert-db",
# REMOVED_UNUSED_CODE:             help="Migrate database to different system",
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         convert_db.set_defaults(func=start_convert_db)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_CONVERT_DB, parser=convert_db)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add install-ui subcommand
# REMOVED_UNUSED_CODE:         install_ui_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "install-ui",
# REMOVED_UNUSED_CODE:             help="Install FreqUI",
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         install_ui_cmd.set_defaults(func=start_install_ui)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_INSTALL_UI, parser=install_ui_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add Plotting subcommand
# REMOVED_UNUSED_CODE:         plot_dataframe_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "plot-dataframe",
# REMOVED_UNUSED_CODE:             help="Plot candles with indicators.",
# REMOVED_UNUSED_CODE:             parents=[_common_parser, _strategy_parser],
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         plot_dataframe_cmd.set_defaults(func=start_plot_dataframe)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_PLOT_DATAFRAME, parser=plot_dataframe_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Plot profit
# REMOVED_UNUSED_CODE:         plot_profit_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "plot-profit",
# REMOVED_UNUSED_CODE:             help="Generate plot showing profits.",
# REMOVED_UNUSED_CODE:             parents=[_common_parser, _strategy_parser],
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         plot_profit_cmd.set_defaults(func=start_plot_profit)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_PLOT_PROFIT, parser=plot_profit_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add webserver subcommand
# REMOVED_UNUSED_CODE:         webserver_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "webserver", help="Webserver module.", parents=[_common_parser]
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         webserver_cmd.set_defaults(func=start_webserver)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_WEBSERVER, parser=webserver_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add strategy_updater subcommand
# REMOVED_UNUSED_CODE:         strategy_updater_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "strategy-updater",
# REMOVED_UNUSED_CODE:             help="updates outdated strategy files to the current version",
# REMOVED_UNUSED_CODE:             parents=[_common_parser],
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         strategy_updater_cmd.set_defaults(func=start_strategy_update)
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_STRATEGY_UPDATER, parser=strategy_updater_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add lookahead_analysis subcommand
# REMOVED_UNUSED_CODE:         lookahead_analayis_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "lookahead-analysis",
# REMOVED_UNUSED_CODE:             help="Check for potential look ahead bias.",
# REMOVED_UNUSED_CODE:             parents=[_common_parser, _strategy_parser],
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         lookahead_analayis_cmd.set_defaults(func=start_lookahead_analysis)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_LOOKAHEAD_ANALYSIS, parser=lookahead_analayis_cmd)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add recursive_analysis subcommand
# REMOVED_UNUSED_CODE:         recursive_analayis_cmd = subparsers.add_parser(
# REMOVED_UNUSED_CODE:             "recursive-analysis",
# REMOVED_UNUSED_CODE:             help="Check for potential recursive formula issue.",
# REMOVED_UNUSED_CODE:             parents=[_common_parser, _strategy_parser],
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         recursive_analayis_cmd.set_defaults(func=start_recursive_analysis)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._build_args(optionlist=ARGS_RECURSIVE_ANALYSIS, parser=recursive_analayis_cmd)
