"""
This module contains the configuration class
"""

import ast
import logging
import warnings
from collections.abc import Callable
from copy import deepcopy
from pathlib import Path
from typing import Any

from freqtrade import constants
from freqtrade.configuration.deprecated_settings import process_temporary_deprecated_settings
from freqtrade.configuration.directory_operations import create_datadir, create_userdata_dir
from freqtrade.configuration.environment_vars import enironment_vars_to_dict
from freqtrade.configuration.load_config import load_file, load_from_files
from freqtrade.constants import Config
from freqtrade.enums import (
    NON_UTIL_MODES,
    TRADE_MODES,
    CandleType,
    MarginMode,
    RunMode,
    TradingMode,
)
from freqtrade.exceptions import OperationalException
from freqtrade.loggers import setup_logging
from freqtrade.misc import deep_merge_dicts, parse_db_uri_for_logging, safe_value_fallback


logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class Configuration:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Class to read and init the bot configuration
# REMOVED_UNUSED_CODE:     Reuse this class for the bot, backtesting, hyperopt and every script that required configuration
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, args: dict[str, Any], runmode: RunMode | None = None) -> None:
# REMOVED_UNUSED_CODE:         self.args = args
# REMOVED_UNUSED_CODE:         self.config: Config | None = None
# REMOVED_UNUSED_CODE:         self.runmode = runmode
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_config(self) -> Config:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Return the config. Use this method to get the bot config
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: Dict: Bot config
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.config is None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.config = self.load_config()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self.config
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def from_files(files: list[str]) -> dict[str, Any]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Iterate through the config files passed in, loading all of them
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         and merging their contents.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Files are loaded in sequence, parameters in later configuration files
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         override the same parameter from an earlier file (last definition wins).
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Runs through the whole Configuration initialization, so all expected config entries
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         are available to interactive environments.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param files: List of file paths
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: configuration dictionary
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Keep this method as staticmethod, so it can be used from interactive environments
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         c = Configuration({"config": files}, RunMode.OTHER)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return c.get_config()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def load_config(self) -> dict[str, Any]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Extract information for sys.argv and load the bot configuration
# REMOVED_UNUSED_CODE:         :return: Configuration dictionary
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         # Load all configs
# REMOVED_UNUSED_CODE:         config: Config = load_from_files(self.args.get("config", []))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Load environment variables
# REMOVED_UNUSED_CODE:         from freqtrade.commands.arguments import NO_CONF_ALLOWED
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.args.get("command") not in NO_CONF_ALLOWED:
# REMOVED_UNUSED_CODE:             env_data = enironment_vars_to_dict()
# REMOVED_UNUSED_CODE:             config = deep_merge_dicts(env_data, config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Normalize config
# REMOVED_UNUSED_CODE:         if "internals" not in config:
# REMOVED_UNUSED_CODE:             config["internals"] = {}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if "pairlists" not in config:
# REMOVED_UNUSED_CODE:             config["pairlists"] = []
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Keep a copy of the original configuration file
# REMOVED_UNUSED_CODE:         config["original_config"] = deepcopy(config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._process_logging_options(config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._process_runmode(config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._process_common_options(config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._process_trading_options(config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._process_optimize_options(config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._process_plot_options(config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._process_data_options(config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._process_analyze_options(config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._process_freqai_options(config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Import check_exchange here to avoid import cycle problems
# REMOVED_UNUSED_CODE:         from freqtrade.exchange.check_exchange import check_exchange
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Check if the exchange set by the user is supported
# REMOVED_UNUSED_CODE:         check_exchange(config, config.get("experimental", {}).get("block_bad_exchanges", True))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._resolve_pairs_list(config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         process_temporary_deprecated_settings(config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return config
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _process_logging_options(self, config: Config) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Extract information for sys.argv and load logging configuration:
# REMOVED_UNUSED_CODE:         the -v/--verbose, --logfile options
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         # Log level
# REMOVED_UNUSED_CODE:         if "verbosity" not in config or self.args.get("verbosity") is not None:
# REMOVED_UNUSED_CODE:             config.update(
# REMOVED_UNUSED_CODE:                 {"verbosity": safe_value_fallback(self.args, "verbosity", default_value=0)}
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if "logfile" in self.args and self.args["logfile"]:
# REMOVED_UNUSED_CODE:             config.update({"logfile": self.args["logfile"]})
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if "print_colorized" in self.args and not self.args["print_colorized"]:
# REMOVED_UNUSED_CODE:             logger.info("Parameter --no-color detected ...")
# REMOVED_UNUSED_CODE:             config.update({"print_colorized": False})
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             config.update({"print_colorized": True})
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         setup_logging(config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _process_trading_options(self, config: Config) -> None:
# REMOVED_UNUSED_CODE:         if config["runmode"] not in TRADE_MODES:
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if config.get("dry_run", False):
# REMOVED_UNUSED_CODE:             logger.info("Dry run is enabled")
# REMOVED_UNUSED_CODE:             if config.get("db_url") in [None, constants.DEFAULT_DB_PROD_URL]:
# REMOVED_UNUSED_CODE:                 # Default to in-memory db for dry_run if not specified
# REMOVED_UNUSED_CODE:                 config["db_url"] = constants.DEFAULT_DB_DRYRUN_URL
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             if not config.get("db_url"):
# REMOVED_UNUSED_CODE:                 config["db_url"] = constants.DEFAULT_DB_PROD_URL
# REMOVED_UNUSED_CODE:             logger.info("Dry run is disabled")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         logger.info(f'Using DB: "{parse_db_uri_for_logging(config["db_url"])}"')
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _process_common_options(self, config: Config) -> None:
# REMOVED_UNUSED_CODE:         # Set strategy if not specified in config and or if it's non default
# REMOVED_UNUSED_CODE:         if self.args.get("strategy") or not config.get("strategy"):
# REMOVED_UNUSED_CODE:             config.update({"strategy": self.args.get("strategy")})
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._args_to_config(
# REMOVED_UNUSED_CODE:             config, argname="strategy_path", logstring="Using additional Strategy lookup path: {}"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if (
# REMOVED_UNUSED_CODE:             "db_url" in self.args
# REMOVED_UNUSED_CODE:             and self.args["db_url"]
# REMOVED_UNUSED_CODE:             and self.args["db_url"] != constants.DEFAULT_DB_PROD_URL
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             config.update({"db_url": self.args["db_url"]})
# REMOVED_UNUSED_CODE:             logger.info("Parameter --db-url detected ...")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._args_to_config(
# REMOVED_UNUSED_CODE:             config, argname="db_url_from", logstring="Parameter --db-url-from detected ..."
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if config.get("force_entry_enable", False):
# REMOVED_UNUSED_CODE:             logger.warning("`force_entry_enable` RPC message enabled.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Support for sd_notify
# REMOVED_UNUSED_CODE:         if "sd_notify" in self.args and self.args["sd_notify"]:
# REMOVED_UNUSED_CODE:             config["internals"].update({"sd_notify": True})
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _process_datadir_options(self, config: Config) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Extract information for sys.argv and load directory configurations
# REMOVED_UNUSED_CODE:         --user-data, --datadir
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         # Check exchange parameter here - otherwise `datadir` might be wrong.
# REMOVED_UNUSED_CODE:         if "exchange" in self.args and self.args["exchange"]:
# REMOVED_UNUSED_CODE:             config["exchange"]["name"] = self.args["exchange"]
# REMOVED_UNUSED_CODE:             logger.info(f"Using exchange {config['exchange']['name']}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if "pair_whitelist" not in config["exchange"]:
# REMOVED_UNUSED_CODE:             config["exchange"]["pair_whitelist"] = []
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if "user_data_dir" in self.args and self.args["user_data_dir"]:
# REMOVED_UNUSED_CODE:             config.update({"user_data_dir": self.args["user_data_dir"]})
# REMOVED_UNUSED_CODE:         elif "user_data_dir" not in config:
# REMOVED_UNUSED_CODE:             # Default to cwd/user_data (legacy option ...)
# REMOVED_UNUSED_CODE:             config.update({"user_data_dir": str(Path.cwd() / "user_data")})
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # reset to user_data_dir so this contains the absolute path.
# REMOVED_UNUSED_CODE:         config["user_data_dir"] = create_userdata_dir(config["user_data_dir"], create_dir=False)
# REMOVED_UNUSED_CODE:         logger.info("Using user-data directory: %s ...", config["user_data_dir"])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         config.update({"datadir": create_datadir(config, self.args.get("datadir"))})
# REMOVED_UNUSED_CODE:         logger.info("Using data directory: %s ...", config.get("datadir"))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.args.get("exportfilename"):
# REMOVED_UNUSED_CODE:             self._args_to_config(
# REMOVED_UNUSED_CODE:                 config, argname="exportfilename", logstring="Storing backtest results to {} ..."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             config["exportfilename"] = Path(config["exportfilename"])
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             config["exportfilename"] = config["user_data_dir"] / "backtest_results"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.args.get("show_sensitive"):
# REMOVED_UNUSED_CODE:             logger.warning(
# REMOVED_UNUSED_CODE:                 "Sensitive information will be shown in the upcoming output. "
# REMOVED_UNUSED_CODE:                 "Please make sure to never share this output without redacting "
# REMOVED_UNUSED_CODE:                 "the information yourself."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _process_optimize_options(self, config: Config) -> None:
# REMOVED_UNUSED_CODE:         # This will override the strategy configuration
# REMOVED_UNUSED_CODE:         self._args_to_config(
# REMOVED_UNUSED_CODE:             config,
# REMOVED_UNUSED_CODE:             argname="timeframe",
# REMOVED_UNUSED_CODE:             logstring="Parameter -i/--timeframe detected ... Using timeframe: {} ...",
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._args_to_config(
# REMOVED_UNUSED_CODE:             config,
# REMOVED_UNUSED_CODE:             argname="position_stacking",
# REMOVED_UNUSED_CODE:             logstring="Parameter --enable-position-stacking detected ...",
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._args_to_config(
# REMOVED_UNUSED_CODE:             config,
# REMOVED_UNUSED_CODE:             argname="enable_protections",
# REMOVED_UNUSED_CODE:             logstring="Parameter --enable-protections detected, enabling Protections. ...",
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if "max_open_trades" in self.args and self.args["max_open_trades"]:
# REMOVED_UNUSED_CODE:             config.update({"max_open_trades": self.args["max_open_trades"]})
# REMOVED_UNUSED_CODE:             logger.info(
# REMOVED_UNUSED_CODE:                 "Parameter --max-open-trades detected, overriding max_open_trades to: %s ...",
# REMOVED_UNUSED_CODE:                 config.get("max_open_trades"),
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         elif config["runmode"] in NON_UTIL_MODES:
# REMOVED_UNUSED_CODE:             logger.info("Using max_open_trades: %s ...", config.get("max_open_trades"))
# REMOVED_UNUSED_CODE:         # Setting max_open_trades to infinite if -1
# REMOVED_UNUSED_CODE:         if config.get("max_open_trades") == -1:
# REMOVED_UNUSED_CODE:             config["max_open_trades"] = float("inf")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.args.get("stake_amount"):
# REMOVED_UNUSED_CODE:             # Convert explicitly to float to support CLI argument for both unlimited and value
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 self.args["stake_amount"] = float(self.args["stake_amount"])
# REMOVED_UNUSED_CODE:             except ValueError:
# REMOVED_UNUSED_CODE:                 pass
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         configurations = [
# REMOVED_UNUSED_CODE:             (
# REMOVED_UNUSED_CODE:                 "timeframe_detail",
# REMOVED_UNUSED_CODE:                 "Parameter --timeframe-detail detected, using {} for intra-candle backtesting ...",
# REMOVED_UNUSED_CODE:             ),
# REMOVED_UNUSED_CODE:             ("backtest_show_pair_list", "Parameter --show-pair-list detected."),
# REMOVED_UNUSED_CODE:             (
# REMOVED_UNUSED_CODE:                 "stake_amount",
# REMOVED_UNUSED_CODE:                 "Parameter --stake-amount detected, overriding stake_amount to: {} ...",
# REMOVED_UNUSED_CODE:             ),
# REMOVED_UNUSED_CODE:             (
# REMOVED_UNUSED_CODE:                 "dry_run_wallet",
# REMOVED_UNUSED_CODE:                 "Parameter --dry-run-wallet detected, overriding dry_run_wallet to: {} ...",
# REMOVED_UNUSED_CODE:             ),
# REMOVED_UNUSED_CODE:             ("fee", "Parameter --fee detected, setting fee to: {} ..."),
# REMOVED_UNUSED_CODE:             ("timerange", "Parameter --timerange detected: {} ..."),
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._args_to_config_loop(config, configurations)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._process_datadir_options(config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._args_to_config(
# REMOVED_UNUSED_CODE:             config,
# REMOVED_UNUSED_CODE:             argname="strategy_list",
# REMOVED_UNUSED_CODE:             logstring="Using strategy list of {} strategies",
# REMOVED_UNUSED_CODE:             logfun=len,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         configurations = [
# REMOVED_UNUSED_CODE:             (
# REMOVED_UNUSED_CODE:                 "recursive_strategy_search",
# REMOVED_UNUSED_CODE:                 "Recursively searching for a strategy in the strategies folder.",
# REMOVED_UNUSED_CODE:             ),
# REMOVED_UNUSED_CODE:             ("timeframe", "Overriding timeframe with Command line argument"),
# REMOVED_UNUSED_CODE:             ("export", "Parameter --export detected: {} ..."),
# REMOVED_UNUSED_CODE:             ("backtest_breakdown", "Parameter --breakdown detected ..."),
# REMOVED_UNUSED_CODE:             ("backtest_cache", "Parameter --cache={} detected ..."),
# REMOVED_UNUSED_CODE:             ("disableparamexport", "Parameter --disableparamexport detected: {} ..."),
# REMOVED_UNUSED_CODE:             ("freqai_backtest_live_models", "Parameter --freqai-backtest-live-models detected ..."),
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE:         self._args_to_config_loop(config, configurations)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Edge section:
# REMOVED_UNUSED_CODE:         if "stoploss_range" in self.args and self.args["stoploss_range"]:
# REMOVED_UNUSED_CODE:             txt_range = ast.literal_eval(self.args["stoploss_range"])
# REMOVED_UNUSED_CODE:             config["edge"].update({"stoploss_range_min": txt_range[0]})
# REMOVED_UNUSED_CODE:             config["edge"].update({"stoploss_range_max": txt_range[1]})
# REMOVED_UNUSED_CODE:             config["edge"].update({"stoploss_range_step": txt_range[2]})
# REMOVED_UNUSED_CODE:             logger.info("Parameter --stoplosses detected: %s ...", self.args["stoploss_range"])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Hyperopt section
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         configurations = [
# REMOVED_UNUSED_CODE:             ("hyperopt", "Using Hyperopt class name: {}"),
# REMOVED_UNUSED_CODE:             ("hyperopt_path", "Using additional Hyperopt lookup path: {}"),
# REMOVED_UNUSED_CODE:             ("hyperoptexportfilename", "Using hyperopt file: {}"),
# REMOVED_UNUSED_CODE:             ("lookahead_analysis_exportfilename", "Saving lookahead analysis results into {} ..."),
# REMOVED_UNUSED_CODE:             ("epochs", "Parameter --epochs detected ... Will run Hyperopt with for {} epochs ..."),
# REMOVED_UNUSED_CODE:             ("spaces", "Parameter -s/--spaces detected: {}"),
# REMOVED_UNUSED_CODE:             ("analyze_per_epoch", "Parameter --analyze-per-epoch detected."),
# REMOVED_UNUSED_CODE:             ("print_all", "Parameter --print-all detected ..."),
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE:         self._args_to_config_loop(config, configurations)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         configurations = [
# REMOVED_UNUSED_CODE:             ("print_json", "Parameter --print-json detected ..."),
# REMOVED_UNUSED_CODE:             ("export_csv", "Parameter --export-csv detected: {}"),
# REMOVED_UNUSED_CODE:             ("hyperopt_jobs", "Parameter -j/--job-workers detected: {}"),
# REMOVED_UNUSED_CODE:             ("hyperopt_random_state", "Parameter --random-state detected: {}"),
# REMOVED_UNUSED_CODE:             ("hyperopt_min_trades", "Parameter --min-trades detected: {}"),
# REMOVED_UNUSED_CODE:             ("hyperopt_loss", "Using Hyperopt loss class name: {}"),
# REMOVED_UNUSED_CODE:             ("hyperopt_show_index", "Parameter -n/--index detected: {}"),
# REMOVED_UNUSED_CODE:             ("hyperopt_list_best", "Parameter --best detected: {}"),
# REMOVED_UNUSED_CODE:             ("hyperopt_list_profitable", "Parameter --profitable detected: {}"),
# REMOVED_UNUSED_CODE:             ("hyperopt_list_min_trades", "Parameter --min-trades detected: {}"),
# REMOVED_UNUSED_CODE:             ("hyperopt_list_max_trades", "Parameter --max-trades detected: {}"),
# REMOVED_UNUSED_CODE:             ("hyperopt_list_min_avg_time", "Parameter --min-avg-time detected: {}"),
# REMOVED_UNUSED_CODE:             ("hyperopt_list_max_avg_time", "Parameter --max-avg-time detected: {}"),
# REMOVED_UNUSED_CODE:             ("hyperopt_list_min_avg_profit", "Parameter --min-avg-profit detected: {}"),
# REMOVED_UNUSED_CODE:             ("hyperopt_list_max_avg_profit", "Parameter --max-avg-profit detected: {}"),
# REMOVED_UNUSED_CODE:             ("hyperopt_list_min_total_profit", "Parameter --min-total-profit detected: {}"),
# REMOVED_UNUSED_CODE:             ("hyperopt_list_max_total_profit", "Parameter --max-total-profit detected: {}"),
# REMOVED_UNUSED_CODE:             ("hyperopt_list_min_objective", "Parameter --min-objective detected: {}"),
# REMOVED_UNUSED_CODE:             ("hyperopt_list_max_objective", "Parameter --max-objective detected: {}"),
# REMOVED_UNUSED_CODE:             ("hyperopt_list_no_details", "Parameter --no-details detected: {}"),
# REMOVED_UNUSED_CODE:             ("hyperopt_show_no_header", "Parameter --no-header detected: {}"),
# REMOVED_UNUSED_CODE:             ("hyperopt_ignore_missing_space", "Parameter --ignore-missing-space detected: {}"),
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._args_to_config_loop(config, configurations)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _process_plot_options(self, config: Config) -> None:
# REMOVED_UNUSED_CODE:         configurations = [
# REMOVED_UNUSED_CODE:             ("pairs", "Using pairs {}"),
# REMOVED_UNUSED_CODE:             ("indicators1", "Using indicators1: {}"),
# REMOVED_UNUSED_CODE:             ("indicators2", "Using indicators2: {}"),
# REMOVED_UNUSED_CODE:             ("trade_ids", "Filtering on trade_ids: {}"),
# REMOVED_UNUSED_CODE:             ("plot_limit", "Limiting plot to: {}"),
# REMOVED_UNUSED_CODE:             ("plot_auto_open", "Parameter --auto-open detected."),
# REMOVED_UNUSED_CODE:             ("trade_source", "Using trades from: {}"),
# REMOVED_UNUSED_CODE:             ("prepend_data", "Prepend detected. Allowing data prepending."),
# REMOVED_UNUSED_CODE:             ("erase", "Erase detected. Deleting existing data."),
# REMOVED_UNUSED_CODE:             ("no_trades", "Parameter --no-trades detected."),
# REMOVED_UNUSED_CODE:             ("timeframes", "timeframes --timeframes: {}"),
# REMOVED_UNUSED_CODE:             ("days", "Detected --days: {}"),
# REMOVED_UNUSED_CODE:             ("include_inactive", "Detected --include-inactive-pairs: {}"),
# REMOVED_UNUSED_CODE:             ("download_trades", "Detected --dl-trades: {}"),
# REMOVED_UNUSED_CODE:             ("convert_trades", "Detected --convert: {} - Converting Trade data to OHCV {}"),
# REMOVED_UNUSED_CODE:             ("dataformat_ohlcv", 'Using "{}" to store OHLCV data.'),
# REMOVED_UNUSED_CODE:             ("dataformat_trades", 'Using "{}" to store trades data.'),
# REMOVED_UNUSED_CODE:             ("show_timerange", "Detected --show-timerange"),
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE:         self._args_to_config_loop(config, configurations)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _process_data_options(self, config: Config) -> None:
# REMOVED_UNUSED_CODE:         self._args_to_config(
# REMOVED_UNUSED_CODE:             config, argname="new_pairs_days", logstring="Detected --new-pairs-days: {}"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         self._args_to_config(
# REMOVED_UNUSED_CODE:             config, argname="trading_mode", logstring="Detected --trading-mode: {}"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         config["candle_type_def"] = CandleType.get_default(
# REMOVED_UNUSED_CODE:             config.get("trading_mode", "spot") or "spot"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         config["trading_mode"] = TradingMode(config.get("trading_mode", "spot") or "spot")
# REMOVED_UNUSED_CODE:         config["margin_mode"] = MarginMode(config.get("margin_mode", "") or "")
# REMOVED_UNUSED_CODE:         self._args_to_config(
# REMOVED_UNUSED_CODE:             config, argname="candle_types", logstring="Detected --candle-types: {}"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _process_analyze_options(self, config: Config) -> None:
# REMOVED_UNUSED_CODE:         configurations = [
# REMOVED_UNUSED_CODE:             ("analysis_groups", "Analysis reason groups: {}"),
# REMOVED_UNUSED_CODE:             ("enter_reason_list", "Analysis enter tag list: {}"),
# REMOVED_UNUSED_CODE:             ("exit_reason_list", "Analysis exit tag list: {}"),
# REMOVED_UNUSED_CODE:             ("indicator_list", "Analysis indicator list: {}"),
# REMOVED_UNUSED_CODE:             ("entry_only", "Only analyze entry signals: {}"),
# REMOVED_UNUSED_CODE:             ("exit_only", "Only analyze exit signals: {}"),
# REMOVED_UNUSED_CODE:             ("timerange", "Filter trades by timerange: {}"),
# REMOVED_UNUSED_CODE:             ("analysis_rejected", "Analyse rejected signals: {}"),
# REMOVED_UNUSED_CODE:             ("analysis_to_csv", "Store analysis tables to CSV: {}"),
# REMOVED_UNUSED_CODE:             ("analysis_csv_path", "Path to store analysis CSVs: {}"),
# REMOVED_UNUSED_CODE:             # Lookahead analysis results
# REMOVED_UNUSED_CODE:             ("targeted_trade_amount", "Targeted Trade amount: {}"),
# REMOVED_UNUSED_CODE:             ("minimum_trade_amount", "Minimum Trade amount: {}"),
# REMOVED_UNUSED_CODE:             ("lookahead_analysis_exportfilename", "Path to store lookahead-analysis-results: {}"),
# REMOVED_UNUSED_CODE:             ("startup_candle", "Startup candle to be used on recursive analysis: {}"),
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE:         self._args_to_config_loop(config, configurations)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _args_to_config_loop(self, config, configurations: list[tuple[str, str]]) -> None:
# REMOVED_UNUSED_CODE:         for argname, logstring in configurations:
# REMOVED_UNUSED_CODE:             self._args_to_config(config, argname=argname, logstring=logstring)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _process_runmode(self, config: Config) -> None:
# REMOVED_UNUSED_CODE:         self._args_to_config(
# REMOVED_UNUSED_CODE:             config,
# REMOVED_UNUSED_CODE:             argname="dry_run",
# REMOVED_UNUSED_CODE:             logstring="Parameter --dry-run detected, overriding dry_run to: {} ...",
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not self.runmode:
# REMOVED_UNUSED_CODE:             # Handle real mode, infer dry/live from config
# REMOVED_UNUSED_CODE:             self.runmode = RunMode.DRY_RUN if config.get("dry_run", True) else RunMode.LIVE
# REMOVED_UNUSED_CODE:             logger.info(f"Runmode set to {self.runmode.value}.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         config.update({"runmode": self.runmode})
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _process_freqai_options(self, config: Config) -> None:
# REMOVED_UNUSED_CODE:         self._args_to_config(
# REMOVED_UNUSED_CODE:             config, argname="freqaimodel", logstring="Using freqaimodel class name: {}"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._args_to_config(
# REMOVED_UNUSED_CODE:             config, argname="freqaimodel_path", logstring="Using freqaimodel path: {}"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _args_to_config(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         config: Config,
# REMOVED_UNUSED_CODE:         argname: str,
# REMOVED_UNUSED_CODE:         logstring: str,
# REMOVED_UNUSED_CODE:         logfun: Callable | None = None,
# REMOVED_UNUSED_CODE:         deprecated_msg: str | None = None,
# REMOVED_UNUSED_CODE:     ) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         :param config: Configuration dictionary
# REMOVED_UNUSED_CODE:         :param argname: Argumentname in self.args - will be copied to config dict.
# REMOVED_UNUSED_CODE:         :param logstring: Logging String
# REMOVED_UNUSED_CODE:         :param logfun: logfun is applied to the configuration entry before passing
# REMOVED_UNUSED_CODE:                         that entry to the log string using .format().
# REMOVED_UNUSED_CODE:                         sample: logfun=len (prints the length of the found
# REMOVED_UNUSED_CODE:                         configuration instead of the content)
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if (
# REMOVED_UNUSED_CODE:             argname in self.args
# REMOVED_UNUSED_CODE:             and self.args[argname] is not None
# REMOVED_UNUSED_CODE:             and self.args[argname] is not False
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             config.update({argname: self.args[argname]})
# REMOVED_UNUSED_CODE:             if logfun:
# REMOVED_UNUSED_CODE:                 logger.info(logstring.format(logfun(config[argname])))
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 logger.info(logstring.format(config[argname]))
# REMOVED_UNUSED_CODE:             if deprecated_msg:
# REMOVED_UNUSED_CODE:                 warnings.warn(f"DEPRECATED: {deprecated_msg}", DeprecationWarning, stacklevel=1)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _resolve_pairs_list(self, config: Config) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Helper for download script.
# REMOVED_UNUSED_CODE:         Takes first found:
# REMOVED_UNUSED_CODE:         * -p (pairs argument)
# REMOVED_UNUSED_CODE:         * --pairs-file
# REMOVED_UNUSED_CODE:         * whitelist from config
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if "pairs" in config:
# REMOVED_UNUSED_CODE:             config["exchange"]["pair_whitelist"] = config["pairs"]
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if "pairs_file" in self.args and self.args["pairs_file"]:
# REMOVED_UNUSED_CODE:             pairs_file = Path(self.args["pairs_file"])
# REMOVED_UNUSED_CODE:             logger.info(f'Reading pairs file "{pairs_file}".')
# REMOVED_UNUSED_CODE:             # Download pairs from the pairs file if no config is specified
# REMOVED_UNUSED_CODE:             # or if pairs file is specified explicitly
# REMOVED_UNUSED_CODE:             if not pairs_file.exists():
# REMOVED_UNUSED_CODE:                 raise OperationalException(f'No pairs file found with path "{pairs_file}".')
# REMOVED_UNUSED_CODE:             config["pairs"] = load_file(pairs_file)
# REMOVED_UNUSED_CODE:             if isinstance(config["pairs"], list):
# REMOVED_UNUSED_CODE:                 config["pairs"].sort()
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if "config" in self.args and self.args["config"]:
# REMOVED_UNUSED_CODE:             logger.info("Using pairlist from configuration.")
# REMOVED_UNUSED_CODE:             config["pairs"] = config.get("exchange", {}).get("pair_whitelist")
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             # Fall back to /dl_path/pairs.json
# REMOVED_UNUSED_CODE:             pairs_file = config["datadir"] / "pairs.json"
# REMOVED_UNUSED_CODE:             if pairs_file.exists():
# REMOVED_UNUSED_CODE:                 logger.info(f'Reading pairs file "{pairs_file}".')
# REMOVED_UNUSED_CODE:                 config["pairs"] = load_file(pairs_file)
# REMOVED_UNUSED_CODE:                 if "pairs" in config and isinstance(config["pairs"], list):
# REMOVED_UNUSED_CODE:                     config["pairs"].sort()
