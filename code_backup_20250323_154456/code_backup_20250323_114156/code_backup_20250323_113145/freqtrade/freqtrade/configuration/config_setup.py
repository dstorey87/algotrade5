import logging
from typing import Any

from freqtrade.enums import RunMode

from .config_validation import validate_config_consistency
from .configuration import Configuration


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
