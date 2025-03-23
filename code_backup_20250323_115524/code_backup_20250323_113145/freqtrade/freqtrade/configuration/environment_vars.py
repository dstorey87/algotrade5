import logging
# REMOVED_UNUSED_CODE: import os
from typing import Any

import rapidjson

# REMOVED_UNUSED_CODE: from freqtrade.constants import ENV_VAR_PREFIX
from freqtrade.misc import deep_merge_dicts


logger = logging.getLogger(__name__)


def _get_var_typed(val):
    try:
        return int(val)
    except ValueError:
        try:
            return float(val)
        except ValueError:
            if val.lower() in ("t", "true"):
                return True
            elif val.lower() in ("f", "false"):
                return False
            # try to convert from json
            try:
                value = rapidjson.loads(val)
                # Limited to lists for now
                if isinstance(value, list):
                    return value
            except rapidjson.JSONDecodeError:
                pass
    # keep as string
    return val


# REMOVED_UNUSED_CODE: def _flat_vars_to_nested_dict(env_dict: dict[str, Any], prefix: str) -> dict[str, Any]:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Environment variables must be prefixed with FREQTRADE.
# REMOVED_UNUSED_CODE:     FREQTRADE__{section}__{key}
# REMOVED_UNUSED_CODE:     :param env_dict: Dictionary to validate - usually os.environ
# REMOVED_UNUSED_CODE:     :param prefix: Prefix to consider (usually FREQTRADE__)
# REMOVED_UNUSED_CODE:     :return: Nested dict based on available and relevant variables.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     no_convert = ["CHAT_ID", "PASSWORD"]
# REMOVED_UNUSED_CODE:     relevant_vars: dict[str, Any] = {}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     for env_var, val in sorted(env_dict.items()):
# REMOVED_UNUSED_CODE:         if env_var.startswith(prefix):
# REMOVED_UNUSED_CODE:             logger.info(f"Loading variable '{env_var}'")
# REMOVED_UNUSED_CODE:             key = env_var.replace(prefix, "")
# REMOVED_UNUSED_CODE:             for k in reversed(key.split("__")):
# REMOVED_UNUSED_CODE:                 val = {
# REMOVED_UNUSED_CODE:                     k.lower(): (
# REMOVED_UNUSED_CODE:                         _get_var_typed(val)
# REMOVED_UNUSED_CODE:                         if not isinstance(val, dict) and k not in no_convert
# REMOVED_UNUSED_CODE:                         else val
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                 }
# REMOVED_UNUSED_CODE:             relevant_vars = deep_merge_dicts(val, relevant_vars)
# REMOVED_UNUSED_CODE:     return relevant_vars


# REMOVED_UNUSED_CODE: def enironment_vars_to_dict() -> dict[str, Any]:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Read environment variables and return a nested dict for relevant variables
# REMOVED_UNUSED_CODE:     Relevant variables must follow the FREQTRADE__{section}__{key} pattern
# REMOVED_UNUSED_CODE:     :return: Nested dict based on available and relevant variables.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     return _flat_vars_to_nested_dict(os.environ.copy(), ENV_VAR_PREFIX)
