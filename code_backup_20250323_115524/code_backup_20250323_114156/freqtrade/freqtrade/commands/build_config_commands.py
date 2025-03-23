import logging
# REMOVED_UNUSED_CODE: from pathlib import Path
# REMOVED_UNUSED_CODE: from typing import Any

# REMOVED_UNUSED_CODE: from freqtrade.enums import RunMode
# REMOVED_UNUSED_CODE: from freqtrade.exceptions import OperationalException


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: def start_new_config(args: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Create a new strategy from a template
# REMOVED_UNUSED_CODE:     Asking the user questions to fill out the template accordingly.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     from freqtrade.configuration.deploy_config import (
# REMOVED_UNUSED_CODE:         ask_user_config,
# REMOVED_UNUSED_CODE:         ask_user_overwrite,
# REMOVED_UNUSED_CODE:         deploy_new_config,
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     from freqtrade.configuration.directory_operations import chown_user_directory
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     config_path = Path(args["config"][0])
# REMOVED_UNUSED_CODE:     chown_user_directory(config_path.parent)
# REMOVED_UNUSED_CODE:     if config_path.exists():
# REMOVED_UNUSED_CODE:         overwrite = ask_user_overwrite(config_path)
# REMOVED_UNUSED_CODE:         if overwrite:
# REMOVED_UNUSED_CODE:             config_path.unlink()
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 f"Configuration file `{config_path}` already exists. "
# REMOVED_UNUSED_CODE:                 "Please delete it or use a different configuration file name."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:     selections = ask_user_config()
# REMOVED_UNUSED_CODE:     deploy_new_config(config_path, selections)


# REMOVED_UNUSED_CODE: def start_show_config(args: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     from freqtrade.configuration import sanitize_config
# REMOVED_UNUSED_CODE:     from freqtrade.configuration.config_setup import setup_utils_configuration
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     config = setup_utils_configuration(args, RunMode.UTIL_EXCHANGE, set_dry=False)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     print("Your combined configuration is:")
# REMOVED_UNUSED_CODE:     config_sanitized = sanitize_config(
# REMOVED_UNUSED_CODE:         config["original_config"], show_sensitive=args.get("show_sensitive", False)
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     from rich import print_json
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     print_json(data=config_sanitized)
