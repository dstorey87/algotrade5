import hashlib
from copy import deepcopy
from pathlib import Path

import rapidjson


# REMOVED_UNUSED_CODE: def get_strategy_run_id(strategy) -> str:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Generate unique identification hash for a backtest run. Identical config and strategy file will
# REMOVED_UNUSED_CODE:     always return an identical hash.
# REMOVED_UNUSED_CODE:     :param strategy: strategy object.
# REMOVED_UNUSED_CODE:     :return: hex string id.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     digest = hashlib.sha1()  # noqa: S324
# REMOVED_UNUSED_CODE:     config = deepcopy(strategy.config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Options that have no impact on results of individual backtest.
# REMOVED_UNUSED_CODE:     not_important_keys = ("strategy_list", "original_config", "telegram", "api_server")
# REMOVED_UNUSED_CODE:     for k in not_important_keys:
# REMOVED_UNUSED_CODE:         if k in config:
# REMOVED_UNUSED_CODE:             del config[k]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Explicitly allow NaN values (e.g. max_open_trades).
# REMOVED_UNUSED_CODE:     # as it does not matter for getting the hash.
# REMOVED_UNUSED_CODE:     digest.update(
# REMOVED_UNUSED_CODE:         rapidjson.dumps(config, default=str, number_mode=rapidjson.NM_NAN).encode("utf-8")
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     # Include _ft_params_from_file - so changing parameter files cause cache eviction
# REMOVED_UNUSED_CODE:     digest.update(
# REMOVED_UNUSED_CODE:         rapidjson.dumps(
# REMOVED_UNUSED_CODE:             strategy._ft_params_from_file, default=str, number_mode=rapidjson.NM_NAN
# REMOVED_UNUSED_CODE:         ).encode("utf-8")
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     with Path(strategy.__file__).open("rb") as fp:
# REMOVED_UNUSED_CODE:         digest.update(fp.read())
# REMOVED_UNUSED_CODE:     return digest.hexdigest().lower()


def get_backtest_metadata_filename(filename: Path | str) -> Path:
    """Return metadata filename for specified backtest results file."""
    filename = Path(filename)
    return filename.parent / Path(f"{filename.stem}.meta.json")
