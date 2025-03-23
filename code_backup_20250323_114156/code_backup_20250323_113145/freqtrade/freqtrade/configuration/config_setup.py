import logging
# REMOVED_UNUSED_CODE: from typing import Any

# REMOVED_UNUSED_CODE: from freqtrade.enums import RunMode

# REMOVED_UNUSED_CODE: from .config_validation import validate_config_consistency
# REMOVED_UNUSED_CODE: from .configuration import Configuration


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: def setup_utils_configuration(
# REMOVED_UNUSED_CODE:     args: dict[str, Any], method: RunMode, *, set_dry: bool = True
# REMOVED_UNUSED_CODE: ) -> dict[str, Any]:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Prepare the configuration for utils subcommands
# REMOVED_UNUSED_CODE:     :param args: Cli args from Arguments()
# REMOVED_UNUSED_CODE:     :param method: Bot running mode
# REMOVED_UNUSED_CODE:     :return: Configuration
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     configuration = Configuration(args, method)
# REMOVED_UNUSED_CODE:     config = configuration.get_config()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Ensure these modes are using Dry-run
# REMOVED_UNUSED_CODE:     if set_dry:
# REMOVED_UNUSED_CODE:         config["dry_run"] = True
# REMOVED_UNUSED_CODE:     validate_config_consistency(config, preliminary=True)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return config
