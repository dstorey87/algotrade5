import logging
import sys
# REMOVED_UNUSED_CODE: from pathlib import Path
# REMOVED_UNUSED_CODE: from typing import Any

# REMOVED_UNUSED_CODE: from freqtrade.constants import USERPATH_STRATEGIES
# REMOVED_UNUSED_CODE: from freqtrade.enums import RunMode
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.exceptions import ConfigurationError, OperationalException


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# Timeout for requests
# REMOVED_UNUSED_CODE: req_timeout = 30


# REMOVED_UNUSED_CODE: def start_create_userdir(args: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Create "user_data" directory to contain user data strategies, hyperopt, ...)
# REMOVED_UNUSED_CODE:     :param args: Cli args from Arguments()
# REMOVED_UNUSED_CODE:     :return: None
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     from freqtrade.configuration.directory_operations import copy_sample_files, create_userdata_dir
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if "user_data_dir" in args and args["user_data_dir"]:
# REMOVED_UNUSED_CODE:         userdir = create_userdata_dir(args["user_data_dir"], create_dir=True)
# REMOVED_UNUSED_CODE:         copy_sample_files(userdir, overwrite=args["reset"])
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         logger.warning("`create-userdir` requires --userdir to be set.")
# REMOVED_UNUSED_CODE:         sys.exit(1)


# REMOVED_UNUSED_CODE: def deploy_new_strategy(strategy_name: str, strategy_path: Path, subtemplate: str) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Deploy new strategy from template to strategy_path
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     from freqtrade.util import render_template, render_template_with_fallback
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     fallback = "full"
# REMOVED_UNUSED_CODE:     attributes = render_template_with_fallback(
# REMOVED_UNUSED_CODE:         templatefile=f"strategy_subtemplates/strategy_attributes_{subtemplate}.j2",
# REMOVED_UNUSED_CODE:         templatefallbackfile=f"strategy_subtemplates/strategy_attributes_{fallback}.j2",
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     indicators = render_template_with_fallback(
# REMOVED_UNUSED_CODE:         templatefile=f"strategy_subtemplates/indicators_{subtemplate}.j2",
# REMOVED_UNUSED_CODE:         templatefallbackfile=f"strategy_subtemplates/indicators_{fallback}.j2",
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     buy_trend = render_template_with_fallback(
# REMOVED_UNUSED_CODE:         templatefile=f"strategy_subtemplates/buy_trend_{subtemplate}.j2",
# REMOVED_UNUSED_CODE:         templatefallbackfile=f"strategy_subtemplates/buy_trend_{fallback}.j2",
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     sell_trend = render_template_with_fallback(
# REMOVED_UNUSED_CODE:         templatefile=f"strategy_subtemplates/sell_trend_{subtemplate}.j2",
# REMOVED_UNUSED_CODE:         templatefallbackfile=f"strategy_subtemplates/sell_trend_{fallback}.j2",
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     plot_config = render_template_with_fallback(
# REMOVED_UNUSED_CODE:         templatefile=f"strategy_subtemplates/plot_config_{subtemplate}.j2",
# REMOVED_UNUSED_CODE:         templatefallbackfile=f"strategy_subtemplates/plot_config_{fallback}.j2",
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     additional_methods = render_template_with_fallback(
# REMOVED_UNUSED_CODE:         templatefile=f"strategy_subtemplates/strategy_methods_{subtemplate}.j2",
# REMOVED_UNUSED_CODE:         templatefallbackfile="strategy_subtemplates/strategy_methods_empty.j2",
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     strategy_text = render_template(
# REMOVED_UNUSED_CODE:         templatefile="base_strategy.py.j2",
# REMOVED_UNUSED_CODE:         arguments={
# REMOVED_UNUSED_CODE:             "strategy": strategy_name,
# REMOVED_UNUSED_CODE:             "attributes": attributes,
# REMOVED_UNUSED_CODE:             "indicators": indicators,
# REMOVED_UNUSED_CODE:             "buy_trend": buy_trend,
# REMOVED_UNUSED_CODE:             "sell_trend": sell_trend,
# REMOVED_UNUSED_CODE:             "plot_config": plot_config,
# REMOVED_UNUSED_CODE:             "additional_methods": additional_methods,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     logger.info(f"Writing strategy to `{strategy_path}`.")
# REMOVED_UNUSED_CODE:     strategy_path.write_text(strategy_text)


# REMOVED_UNUSED_CODE: def start_new_strategy(args: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     from freqtrade.configuration import setup_utils_configuration
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     config = setup_utils_configuration(args, RunMode.UTIL_NO_EXCHANGE)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if "strategy" in args and args["strategy"]:
# REMOVED_UNUSED_CODE:         if "strategy_path" in args and args["strategy_path"]:
# REMOVED_UNUSED_CODE:             strategy_dir = Path(args["strategy_path"])
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             strategy_dir = config["user_data_dir"] / USERPATH_STRATEGIES
# REMOVED_UNUSED_CODE:         if not strategy_dir.is_dir():
# REMOVED_UNUSED_CODE:             logger.info(f"Creating strategy directory {strategy_dir}")
# REMOVED_UNUSED_CODE:             strategy_dir.mkdir(parents=True)
# REMOVED_UNUSED_CODE:         new_path = strategy_dir / (args["strategy"] + ".py")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if new_path.exists():
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 f"`{new_path}` already exists. Please choose another Strategy Name."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         deploy_new_strategy(args["strategy"], new_path, args["template"])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         raise ConfigurationError("`new-strategy` requires --strategy to be set.")


# REMOVED_UNUSED_CODE: def start_install_ui(args: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     from freqtrade.commands.deploy_ui import (
# REMOVED_UNUSED_CODE:         clean_ui_subdir,
# REMOVED_UNUSED_CODE:         download_and_install_ui,
# REMOVED_UNUSED_CODE:         get_ui_download_url,
# REMOVED_UNUSED_CODE:         read_ui_version,
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     dest_folder = Path(__file__).parents[1] / "rpc/api_server/ui/installed/"
# REMOVED_UNUSED_CODE:     # First make sure the assets are removed.
# REMOVED_UNUSED_CODE:     dl_url, latest_version = get_ui_download_url(args.get("ui_version"))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     curr_version = read_ui_version(dest_folder)
# REMOVED_UNUSED_CODE:     if curr_version == latest_version and not args.get("erase_ui_only"):
# REMOVED_UNUSED_CODE:         logger.info(f"UI already up-to-date, FreqUI Version {curr_version}.")
# REMOVED_UNUSED_CODE:         return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     clean_ui_subdir(dest_folder)
# REMOVED_UNUSED_CODE:     if args.get("erase_ui_only"):
# REMOVED_UNUSED_CODE:         logger.info("Erased UI directory content. Not downloading new version.")
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         # Download a new version
# REMOVED_UNUSED_CODE:         download_and_install_ui(dest_folder, dl_url, latest_version)
