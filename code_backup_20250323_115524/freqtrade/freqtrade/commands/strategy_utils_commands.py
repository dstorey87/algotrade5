import logging
# REMOVED_UNUSED_CODE: import time
# REMOVED_UNUSED_CODE: from pathlib import Path
# REMOVED_UNUSED_CODE: from typing import Any

# REMOVED_UNUSED_CODE: from freqtrade.enums import RunMode


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: def start_strategy_update(args: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Start the strategy updating script
# REMOVED_UNUSED_CODE:     :param args: Cli args from Arguments()
# REMOVED_UNUSED_CODE:     :return: None
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     from freqtrade.configuration import setup_utils_configuration
# REMOVED_UNUSED_CODE:     from freqtrade.resolvers import StrategyResolver
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     config = setup_utils_configuration(args, RunMode.UTIL_NO_EXCHANGE)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     strategy_objs = StrategyResolver.search_all_objects(
# REMOVED_UNUSED_CODE:         config, enum_failed=False, recursive=config.get("recursive_strategy_search", False)
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     filtered_strategy_objs = []
# REMOVED_UNUSED_CODE:     if args["strategy_list"]:
# REMOVED_UNUSED_CODE:         filtered_strategy_objs = [
# REMOVED_UNUSED_CODE:             strategy_obj
# REMOVED_UNUSED_CODE:             for strategy_obj in strategy_objs
# REMOVED_UNUSED_CODE:             if strategy_obj["name"] in args["strategy_list"]
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         # Use all available entries.
# REMOVED_UNUSED_CODE:         filtered_strategy_objs = strategy_objs
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     processed_locations = set()
# REMOVED_UNUSED_CODE:     for strategy_obj in filtered_strategy_objs:
# REMOVED_UNUSED_CODE:         if strategy_obj["location"] not in processed_locations:
# REMOVED_UNUSED_CODE:             processed_locations.add(strategy_obj["location"])
# REMOVED_UNUSED_CODE:             start_conversion(strategy_obj, config)


# REMOVED_UNUSED_CODE: def start_conversion(strategy_obj, config):
# REMOVED_UNUSED_CODE:     from freqtrade.strategy.strategyupdater import StrategyUpdater
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     print(f"Conversion of {Path(strategy_obj['location']).name} started.")
# REMOVED_UNUSED_CODE:     instance_strategy_updater = StrategyUpdater()
# REMOVED_UNUSED_CODE:     start = time.perf_counter()
# REMOVED_UNUSED_CODE:     instance_strategy_updater.start(config, strategy_obj)
# REMOVED_UNUSED_CODE:     elapsed = time.perf_counter() - start
# REMOVED_UNUSED_CODE:     print(f"Conversion of {Path(strategy_obj['location']).name} took {elapsed:.1f} seconds.")
