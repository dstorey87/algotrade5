"""
Functions to handle deprecated settings
"""

import logging

from freqtrade.constants import Config
# REMOVED_UNUSED_CODE: from freqtrade.exceptions import ConfigurationError, OperationalException


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: def check_conflicting_settings(
# REMOVED_UNUSED_CODE:     config: Config,
# REMOVED_UNUSED_CODE:     section_old: str | None,
# REMOVED_UNUSED_CODE:     name_old: str,
# REMOVED_UNUSED_CODE:     section_new: str | None,
# REMOVED_UNUSED_CODE:     name_new: str,
# REMOVED_UNUSED_CODE: ) -> None:
# REMOVED_UNUSED_CODE:     section_new_config = config.get(section_new, {}) if section_new else config
# REMOVED_UNUSED_CODE:     section_old_config = config.get(section_old, {}) if section_old else config
# REMOVED_UNUSED_CODE:     if name_new in section_new_config and name_old in section_old_config:
# REMOVED_UNUSED_CODE:         new_name = f"{section_new}.{name_new}" if section_new else f"{name_new}"
# REMOVED_UNUSED_CODE:         old_name = f"{section_old}.{name_old}" if section_old else f"{name_old}"
# REMOVED_UNUSED_CODE:         raise OperationalException(
# REMOVED_UNUSED_CODE:             f"Conflicting settings `{new_name}` and `{old_name}` "
# REMOVED_UNUSED_CODE:             "(DEPRECATED) detected in the configuration file. "
# REMOVED_UNUSED_CODE:             "This deprecated setting will be removed in the next versions of Freqtrade. "
# REMOVED_UNUSED_CODE:             f"Please delete it from your configuration and use the `{new_name}` "
# REMOVED_UNUSED_CODE:             "setting instead."
# REMOVED_UNUSED_CODE:         )


# REMOVED_UNUSED_CODE: def process_removed_setting(
# REMOVED_UNUSED_CODE:     config: Config, section1: str, name1: str, section2: str | None, name2: str
# REMOVED_UNUSED_CODE: ) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     :param section1: Removed section
# REMOVED_UNUSED_CODE:     :param name1: Removed setting name
# REMOVED_UNUSED_CODE:     :param section2: new section for this key
# REMOVED_UNUSED_CODE:     :param name2: new setting name
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     section1_config = config.get(section1, {})
# REMOVED_UNUSED_CODE:     if name1 in section1_config:
# REMOVED_UNUSED_CODE:         section_2 = f"{section2}.{name2}" if section2 else f"{name2}"
# REMOVED_UNUSED_CODE:         raise ConfigurationError(
# REMOVED_UNUSED_CODE:             f"Setting `{section1}.{name1}` has been moved to `{section_2}. "
# REMOVED_UNUSED_CODE:             f"Please delete it from your configuration and use the `{section_2}` "
# REMOVED_UNUSED_CODE:             "setting instead."
# REMOVED_UNUSED_CODE:         )


# REMOVED_UNUSED_CODE: def process_deprecated_setting(
# REMOVED_UNUSED_CODE:     config: Config,
# REMOVED_UNUSED_CODE:     section_old: str | None,
# REMOVED_UNUSED_CODE:     name_old: str,
# REMOVED_UNUSED_CODE:     section_new: str | None,
# REMOVED_UNUSED_CODE:     name_new: str,
# REMOVED_UNUSED_CODE: ) -> None:
# REMOVED_UNUSED_CODE:     check_conflicting_settings(config, section_old, name_old, section_new, name_new)
# REMOVED_UNUSED_CODE:     section_old_config = config.get(section_old, {}) if section_old else config
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if name_old in section_old_config:
# REMOVED_UNUSED_CODE:         section_1 = f"{section_old}.{name_old}" if section_old else f"{name_old}"
# REMOVED_UNUSED_CODE:         section_2 = f"{section_new}.{name_new}" if section_new else f"{name_new}"
# REMOVED_UNUSED_CODE:         logger.warning(
# REMOVED_UNUSED_CODE:             "DEPRECATED: "
# REMOVED_UNUSED_CODE:             f"The `{section_1}` setting is deprecated and "
# REMOVED_UNUSED_CODE:             "will be removed in the next versions of Freqtrade. "
# REMOVED_UNUSED_CODE:             f"Please use the `{section_2}` setting in your configuration instead."
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         section_new_config = config.get(section_new, {}) if section_new else config
# REMOVED_UNUSED_CODE:         section_new_config[name_new] = section_old_config[name_old]
# REMOVED_UNUSED_CODE:         del section_old_config[name_old]


# REMOVED_UNUSED_CODE: def process_temporary_deprecated_settings(config: Config) -> None:
# REMOVED_UNUSED_CODE:     # Kept for future deprecated / moved settings
# REMOVED_UNUSED_CODE:     # check_conflicting_settings(config, 'ask_strategy', 'use_sell_signal',
# REMOVED_UNUSED_CODE:     #                            'experimental', 'use_sell_signal')
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     process_deprecated_setting(
# REMOVED_UNUSED_CODE:         config,
# REMOVED_UNUSED_CODE:         "ask_strategy",
# REMOVED_UNUSED_CODE:         "ignore_buying_expired_candle_after",
# REMOVED_UNUSED_CODE:         None,
# REMOVED_UNUSED_CODE:         "ignore_buying_expired_candle_after",
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     process_deprecated_setting(config, None, "forcebuy_enable", None, "force_entry_enable")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # New settings
# REMOVED_UNUSED_CODE:     if config.get("telegram"):
# REMOVED_UNUSED_CODE:         process_deprecated_setting(
# REMOVED_UNUSED_CODE:             config["telegram"], "notification_settings", "sell", "notification_settings", "exit"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         process_deprecated_setting(
# REMOVED_UNUSED_CODE:             config["telegram"],
# REMOVED_UNUSED_CODE:             "notification_settings",
# REMOVED_UNUSED_CODE:             "sell_fill",
# REMOVED_UNUSED_CODE:             "notification_settings",
# REMOVED_UNUSED_CODE:             "exit_fill",
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         process_deprecated_setting(
# REMOVED_UNUSED_CODE:             config["telegram"],
# REMOVED_UNUSED_CODE:             "notification_settings",
# REMOVED_UNUSED_CODE:             "sell_cancel",
# REMOVED_UNUSED_CODE:             "notification_settings",
# REMOVED_UNUSED_CODE:             "exit_cancel",
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         process_deprecated_setting(
# REMOVED_UNUSED_CODE:             config["telegram"], "notification_settings", "buy", "notification_settings", "entry"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         process_deprecated_setting(
# REMOVED_UNUSED_CODE:             config["telegram"],
# REMOVED_UNUSED_CODE:             "notification_settings",
# REMOVED_UNUSED_CODE:             "buy_fill",
# REMOVED_UNUSED_CODE:             "notification_settings",
# REMOVED_UNUSED_CODE:             "entry_fill",
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         process_deprecated_setting(
# REMOVED_UNUSED_CODE:             config["telegram"],
# REMOVED_UNUSED_CODE:             "notification_settings",
# REMOVED_UNUSED_CODE:             "buy_cancel",
# REMOVED_UNUSED_CODE:             "notification_settings",
# REMOVED_UNUSED_CODE:             "entry_cancel",
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:     if config.get("webhook"):
# REMOVED_UNUSED_CODE:         process_deprecated_setting(config, "webhook", "webhookbuy", "webhook", "webhookentry")
# REMOVED_UNUSED_CODE:         process_deprecated_setting(
# REMOVED_UNUSED_CODE:             config, "webhook", "webhookbuycancel", "webhook", "webhookentrycancel"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         process_deprecated_setting(
# REMOVED_UNUSED_CODE:             config, "webhook", "webhookbuyfill", "webhook", "webhookentryfill"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         process_deprecated_setting(config, "webhook", "webhooksell", "webhook", "webhookexit")
# REMOVED_UNUSED_CODE:         process_deprecated_setting(
# REMOVED_UNUSED_CODE:             config, "webhook", "webhooksellcancel", "webhook", "webhookexitcancel"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         process_deprecated_setting(
# REMOVED_UNUSED_CODE:             config, "webhook", "webhooksellfill", "webhook", "webhookexitfill"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Legacy way - having them in experimental ...
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     process_removed_setting(config, "experimental", "use_sell_signal", None, "use_exit_signal")
# REMOVED_UNUSED_CODE:     process_removed_setting(config, "experimental", "sell_profit_only", None, "exit_profit_only")
# REMOVED_UNUSED_CODE:     process_removed_setting(
# REMOVED_UNUSED_CODE:         config, "experimental", "ignore_roi_if_buy_signal", None, "ignore_roi_if_entry_signal"
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     process_removed_setting(config, "ask_strategy", "use_sell_signal", None, "use_exit_signal")
# REMOVED_UNUSED_CODE:     process_removed_setting(config, "ask_strategy", "sell_profit_only", None, "exit_profit_only")
# REMOVED_UNUSED_CODE:     process_removed_setting(
# REMOVED_UNUSED_CODE:         config, "ask_strategy", "sell_profit_offset", None, "exit_profit_offset"
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     process_removed_setting(
# REMOVED_UNUSED_CODE:         config, "ask_strategy", "ignore_roi_if_buy_signal", None, "ignore_roi_if_entry_signal"
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     if config.get("edge", {}).get(
# REMOVED_UNUSED_CODE:         "enabled", False
# REMOVED_UNUSED_CODE:     ) and "capital_available_percentage" in config.get("edge", {}):
# REMOVED_UNUSED_CODE:         raise ConfigurationError(
# REMOVED_UNUSED_CODE:             "DEPRECATED: "
# REMOVED_UNUSED_CODE:             "Using 'edge.capital_available_percentage' has been deprecated in favor of "
# REMOVED_UNUSED_CODE:             "'tradable_balance_ratio'. Please migrate your configuration to "
# REMOVED_UNUSED_CODE:             "'tradable_balance_ratio' and remove 'capital_available_percentage' "
# REMOVED_UNUSED_CODE:             "from the edge configuration."
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:     if "ticker_interval" in config:
# REMOVED_UNUSED_CODE:         raise ConfigurationError(
# REMOVED_UNUSED_CODE:             "DEPRECATED: 'ticker_interval' detected. "
# REMOVED_UNUSED_CODE:             "Please use 'timeframe' instead of 'ticker_interval."
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if "protections" in config:
# REMOVED_UNUSED_CODE:         raise ConfigurationError(
# REMOVED_UNUSED_CODE:             "DEPRECATED: Setting 'protections' in the configuration is deprecated."
# REMOVED_UNUSED_CODE:         )
