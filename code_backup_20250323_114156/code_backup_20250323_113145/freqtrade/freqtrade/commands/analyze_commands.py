import logging
# REMOVED_UNUSED_CODE: from typing import Any

# REMOVED_UNUSED_CODE: from freqtrade.enums import RunMode


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: def start_analysis_entries_exits(args: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Start analysis script
# REMOVED_UNUSED_CODE:     :param args: Cli args from Arguments()
# REMOVED_UNUSED_CODE:     :return: None
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     from freqtrade.configuration import setup_utils_configuration
# REMOVED_UNUSED_CODE:     from freqtrade.data.entryexitanalysis import process_entry_exit_reasons
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Initialize configuration
# REMOVED_UNUSED_CODE:     config = setup_utils_configuration(args, RunMode.BACKTEST)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     logger.info("Starting freqtrade in analysis mode")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     process_entry_exit_reasons(config)
