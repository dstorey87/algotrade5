import logging
# REMOVED_UNUSED_CODE: from collections import Counter
# REMOVED_UNUSED_CODE: from copy import deepcopy
from typing import Any

from jsonschema import Draft4Validator, validators
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from jsonschema.exceptions import ValidationError, best_match

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.configuration.config_schema import (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     CONF_SCHEMA,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     SCHEMA_BACKTEST_REQUIRED,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     SCHEMA_BACKTEST_REQUIRED_FINAL,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     SCHEMA_MINIMAL_REQUIRED,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     SCHEMA_MINIMAL_WEBSERVER,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     SCHEMA_TRADE_REQUIRED,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: )
from freqtrade.configuration.deprecated_settings import process_deprecated_setting
# REMOVED_UNUSED_CODE: from freqtrade.constants import UNLIMITED_STAKE_AMOUNT
# REMOVED_UNUSED_CODE: from freqtrade.enums import RunMode, TradingMode
from freqtrade.exceptions import ConfigurationError


logger = logging.getLogger(__name__)


def _extend_validator(validator_class):
    """
    Extended validator for the Freqtrade configuration JSON Schema.
    Currently it only handles defaults for subschemas.
    """
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for prop, subschema in properties.items():
            if "default" in subschema:
                instance.setdefault(prop, subschema["default"])

        yield from validate_properties(validator, properties, instance, schema)

    return validators.extend(validator_class, {"properties": set_defaults})


# REMOVED_UNUSED_CODE: FreqtradeValidator = _extend_validator(Draft4Validator)


# REMOVED_UNUSED_CODE: def validate_config_schema(conf: dict[str, Any], preliminary: bool = False) -> dict[str, Any]:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Validate the configuration follow the Config Schema
# REMOVED_UNUSED_CODE:     :param conf: Config in JSON format
# REMOVED_UNUSED_CODE:     :return: Returns the config if valid, otherwise throw an exception
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     conf_schema = deepcopy(CONF_SCHEMA)
# REMOVED_UNUSED_CODE:     if conf.get("runmode", RunMode.OTHER) in (RunMode.DRY_RUN, RunMode.LIVE):
# REMOVED_UNUSED_CODE:         conf_schema["required"] = SCHEMA_TRADE_REQUIRED
# REMOVED_UNUSED_CODE:     elif conf.get("runmode", RunMode.OTHER) in (RunMode.BACKTEST, RunMode.HYPEROPT):
# REMOVED_UNUSED_CODE:         if preliminary:
# REMOVED_UNUSED_CODE:             conf_schema["required"] = SCHEMA_BACKTEST_REQUIRED
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             conf_schema["required"] = SCHEMA_BACKTEST_REQUIRED_FINAL
# REMOVED_UNUSED_CODE:     elif conf.get("runmode", RunMode.OTHER) == RunMode.WEBSERVER:
# REMOVED_UNUSED_CODE:         conf_schema["required"] = SCHEMA_MINIMAL_WEBSERVER
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         conf_schema["required"] = SCHEMA_MINIMAL_REQUIRED
# REMOVED_UNUSED_CODE:     try:
# REMOVED_UNUSED_CODE:         FreqtradeValidator(conf_schema).validate(conf)
# REMOVED_UNUSED_CODE:         return conf
# REMOVED_UNUSED_CODE:     except ValidationError as e:
# REMOVED_UNUSED_CODE:         logger.critical(f"Invalid configuration. Reason: {e}")
# REMOVED_UNUSED_CODE:         raise ValidationError(best_match(Draft4Validator(conf_schema).iter_errors(conf)).message)


# REMOVED_UNUSED_CODE: def validate_config_consistency(conf: dict[str, Any], *, preliminary: bool = False) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Validate the configuration consistency.
# REMOVED_UNUSED_CODE:     Should be ran after loading both configuration and strategy,
# REMOVED_UNUSED_CODE:     since strategies can set certain configuration settings too.
# REMOVED_UNUSED_CODE:     :param conf: Config in JSON format
# REMOVED_UNUSED_CODE:     :return: Returns None if everything is ok, otherwise throw an ConfigurationError
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # validating trailing stoploss
# REMOVED_UNUSED_CODE:     _validate_trailing_stoploss(conf)
# REMOVED_UNUSED_CODE:     _validate_price_config(conf)
# REMOVED_UNUSED_CODE:     _validate_edge(conf)
# REMOVED_UNUSED_CODE:     _validate_whitelist(conf)
# REMOVED_UNUSED_CODE:     _validate_unlimited_amount(conf)
# REMOVED_UNUSED_CODE:     _validate_ask_orderbook(conf)
# REMOVED_UNUSED_CODE:     _validate_freqai_hyperopt(conf)
# REMOVED_UNUSED_CODE:     _validate_freqai_backtest(conf)
# REMOVED_UNUSED_CODE:     _validate_freqai_include_timeframes(conf, preliminary=preliminary)
# REMOVED_UNUSED_CODE:     _validate_consumers(conf)
# REMOVED_UNUSED_CODE:     validate_migrated_strategy_settings(conf)
# REMOVED_UNUSED_CODE:     _validate_orderflow(conf)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # validate configuration before returning
# REMOVED_UNUSED_CODE:     logger.info("Validating configuration ...")
# REMOVED_UNUSED_CODE:     validate_config_schema(conf, preliminary=preliminary)


# REMOVED_UNUSED_CODE: def _validate_unlimited_amount(conf: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     If edge is disabled, either max_open_trades or stake_amount need to be set.
# REMOVED_UNUSED_CODE:     :raise: ConfigurationError if config validation failed
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     if (
# REMOVED_UNUSED_CODE:         not conf.get("edge", {}).get("enabled")
# REMOVED_UNUSED_CODE:         and conf.get("max_open_trades") == float("inf")
# REMOVED_UNUSED_CODE:         and conf.get("stake_amount") == UNLIMITED_STAKE_AMOUNT
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         raise ConfigurationError("`max_open_trades` and `stake_amount` cannot both be unlimited.")


# REMOVED_UNUSED_CODE: def _validate_price_config(conf: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     When using market orders, price sides must be using the "other" side of the price
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     # TODO: The below could be an enforced setting when using market orders
# REMOVED_UNUSED_CODE:     if conf.get("order_types", {}).get("entry") == "market" and conf.get("entry_pricing", {}).get(
# REMOVED_UNUSED_CODE:         "price_side"
# REMOVED_UNUSED_CODE:     ) not in ("ask", "other"):
# REMOVED_UNUSED_CODE:         raise ConfigurationError('Market entry orders require entry_pricing.price_side = "other".')
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if conf.get("order_types", {}).get("exit") == "market" and conf.get("exit_pricing", {}).get(
# REMOVED_UNUSED_CODE:         "price_side"
# REMOVED_UNUSED_CODE:     ) not in ("bid", "other"):
# REMOVED_UNUSED_CODE:         raise ConfigurationError('Market exit orders require exit_pricing.price_side = "other".')


# REMOVED_UNUSED_CODE: def _validate_trailing_stoploss(conf: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     if conf.get("stoploss") == 0.0:
# REMOVED_UNUSED_CODE:         raise ConfigurationError(
# REMOVED_UNUSED_CODE:             "The config stoploss needs to be different from 0 to avoid problems with sell orders."
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:     # Skip if trailing stoploss is not activated
# REMOVED_UNUSED_CODE:     if not conf.get("trailing_stop", False):
# REMOVED_UNUSED_CODE:         return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     tsl_positive = float(conf.get("trailing_stop_positive", 0))
# REMOVED_UNUSED_CODE:     tsl_offset = float(conf.get("trailing_stop_positive_offset", 0))
# REMOVED_UNUSED_CODE:     tsl_only_offset = conf.get("trailing_only_offset_is_reached", False)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if tsl_only_offset:
# REMOVED_UNUSED_CODE:         if tsl_positive == 0.0:
# REMOVED_UNUSED_CODE:             raise ConfigurationError(
# REMOVED_UNUSED_CODE:                 "The config trailing_only_offset_is_reached needs "
# REMOVED_UNUSED_CODE:                 "trailing_stop_positive_offset to be more than 0 in your config."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:     if tsl_positive > 0 and 0 < tsl_offset <= tsl_positive:
# REMOVED_UNUSED_CODE:         raise ConfigurationError(
# REMOVED_UNUSED_CODE:             "The config trailing_stop_positive_offset needs "
# REMOVED_UNUSED_CODE:             "to be greater than trailing_stop_positive in your config."
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Fetch again without default
# REMOVED_UNUSED_CODE:     if "trailing_stop_positive" in conf and float(conf["trailing_stop_positive"]) == 0.0:
# REMOVED_UNUSED_CODE:         raise ConfigurationError(
# REMOVED_UNUSED_CODE:             "The config trailing_stop_positive needs to be different from 0 "
# REMOVED_UNUSED_CODE:             "to avoid problems with sell orders."
# REMOVED_UNUSED_CODE:         )


# REMOVED_UNUSED_CODE: def _validate_edge(conf: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Edge and Dynamic whitelist should not both be enabled, since edge overrides dynamic whitelists.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if not conf.get("edge", {}).get("enabled"):
# REMOVED_UNUSED_CODE:         return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if not conf.get("use_exit_signal", True):
# REMOVED_UNUSED_CODE:         raise ConfigurationError(
# REMOVED_UNUSED_CODE:             "Edge requires `use_exit_signal` to be True, otherwise no sells will happen."
# REMOVED_UNUSED_CODE:         )


# REMOVED_UNUSED_CODE: def _validate_whitelist(conf: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Dynamic whitelist does not require pair_whitelist to be set - however StaticWhitelist does.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     if conf.get("runmode", RunMode.OTHER) in [
# REMOVED_UNUSED_CODE:         RunMode.OTHER,
# REMOVED_UNUSED_CODE:         RunMode.PLOT,
# REMOVED_UNUSED_CODE:         RunMode.UTIL_NO_EXCHANGE,
# REMOVED_UNUSED_CODE:         RunMode.UTIL_EXCHANGE,
# REMOVED_UNUSED_CODE:     ]:
# REMOVED_UNUSED_CODE:         return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     for pl in conf.get("pairlists", [{"method": "StaticPairList"}]):
# REMOVED_UNUSED_CODE:         if (
# REMOVED_UNUSED_CODE:             isinstance(pl, dict)
# REMOVED_UNUSED_CODE:             and pl.get("method") == "StaticPairList"
# REMOVED_UNUSED_CODE:             and not conf.get("exchange", {}).get("pair_whitelist")
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             raise ConfigurationError("StaticPairList requires pair_whitelist to be set.")


# REMOVED_UNUSED_CODE: def _validate_ask_orderbook(conf: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     ask_strategy = conf.get("exit_pricing", {})
# REMOVED_UNUSED_CODE:     ob_min = ask_strategy.get("order_book_min")
# REMOVED_UNUSED_CODE:     ob_max = ask_strategy.get("order_book_max")
# REMOVED_UNUSED_CODE:     if ob_min is not None and ob_max is not None and ask_strategy.get("use_order_book"):
# REMOVED_UNUSED_CODE:         if ob_min != ob_max:
# REMOVED_UNUSED_CODE:             raise ConfigurationError(
# REMOVED_UNUSED_CODE:                 "Using order_book_max != order_book_min in exit_pricing is no longer supported."
# REMOVED_UNUSED_CODE:                 "Please pick one value and use `order_book_top` in the future."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             # Move value to order_book_top
# REMOVED_UNUSED_CODE:             ask_strategy["order_book_top"] = ob_min
# REMOVED_UNUSED_CODE:             logger.warning(
# REMOVED_UNUSED_CODE:                 "DEPRECATED: "
# REMOVED_UNUSED_CODE:                 "Please use `order_book_top` instead of `order_book_min` and `order_book_max` "
# REMOVED_UNUSED_CODE:                 "for your `exit_pricing` configuration."
# REMOVED_UNUSED_CODE:             )


# REMOVED_UNUSED_CODE: def validate_migrated_strategy_settings(conf: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     _validate_time_in_force(conf)
# REMOVED_UNUSED_CODE:     _validate_order_types(conf)
# REMOVED_UNUSED_CODE:     _validate_unfilledtimeout(conf)
# REMOVED_UNUSED_CODE:     _validate_pricing_rules(conf)
# REMOVED_UNUSED_CODE:     _strategy_settings(conf)


# REMOVED_UNUSED_CODE: def _validate_time_in_force(conf: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     time_in_force = conf.get("order_time_in_force", {})
# REMOVED_UNUSED_CODE:     if "buy" in time_in_force or "sell" in time_in_force:
# REMOVED_UNUSED_CODE:         if conf.get("trading_mode", TradingMode.SPOT) != TradingMode.SPOT:
# REMOVED_UNUSED_CODE:             raise ConfigurationError(
# REMOVED_UNUSED_CODE:                 "Please migrate your time_in_force settings to use 'entry' and 'exit'."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             logger.warning(
# REMOVED_UNUSED_CODE:                 "DEPRECATED: Using 'buy' and 'sell' for time_in_force is deprecated."
# REMOVED_UNUSED_CODE:                 "Please migrate your time_in_force settings to use 'entry' and 'exit'."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             process_deprecated_setting(
# REMOVED_UNUSED_CODE:                 conf, "order_time_in_force", "buy", "order_time_in_force", "entry"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             process_deprecated_setting(
# REMOVED_UNUSED_CODE:                 conf, "order_time_in_force", "sell", "order_time_in_force", "exit"
# REMOVED_UNUSED_CODE:             )


# REMOVED_UNUSED_CODE: def _validate_order_types(conf: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     order_types = conf.get("order_types", {})
# REMOVED_UNUSED_CODE:     old_order_types = [
# REMOVED_UNUSED_CODE:         "buy",
# REMOVED_UNUSED_CODE:         "sell",
# REMOVED_UNUSED_CODE:         "emergencysell",
# REMOVED_UNUSED_CODE:         "forcebuy",
# REMOVED_UNUSED_CODE:         "forcesell",
# REMOVED_UNUSED_CODE:         "emergencyexit",
# REMOVED_UNUSED_CODE:         "forceexit",
# REMOVED_UNUSED_CODE:         "forceentry",
# REMOVED_UNUSED_CODE:     ]
# REMOVED_UNUSED_CODE:     if any(x in order_types for x in old_order_types):
# REMOVED_UNUSED_CODE:         if conf.get("trading_mode", TradingMode.SPOT) != TradingMode.SPOT:
# REMOVED_UNUSED_CODE:             raise ConfigurationError(
# REMOVED_UNUSED_CODE:                 "Please migrate your order_types settings to use the new wording."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             logger.warning(
# REMOVED_UNUSED_CODE:                 "DEPRECATED: Using 'buy' and 'sell' for order_types is deprecated."
# REMOVED_UNUSED_CODE:                 "Please migrate your order_types settings to use 'entry' and 'exit' wording."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             for o, n in [
# REMOVED_UNUSED_CODE:                 ("buy", "entry"),
# REMOVED_UNUSED_CODE:                 ("sell", "exit"),
# REMOVED_UNUSED_CODE:                 ("emergencysell", "emergency_exit"),
# REMOVED_UNUSED_CODE:                 ("forcesell", "force_exit"),
# REMOVED_UNUSED_CODE:                 ("forcebuy", "force_entry"),
# REMOVED_UNUSED_CODE:                 ("emergencyexit", "emergency_exit"),
# REMOVED_UNUSED_CODE:                 ("forceexit", "force_exit"),
# REMOVED_UNUSED_CODE:                 ("forceentry", "force_entry"),
# REMOVED_UNUSED_CODE:             ]:
# REMOVED_UNUSED_CODE:                 process_deprecated_setting(conf, "order_types", o, "order_types", n)


# REMOVED_UNUSED_CODE: def _validate_unfilledtimeout(conf: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     unfilledtimeout = conf.get("unfilledtimeout", {})
# REMOVED_UNUSED_CODE:     if any(x in unfilledtimeout for x in ["buy", "sell"]):
# REMOVED_UNUSED_CODE:         if conf.get("trading_mode", TradingMode.SPOT) != TradingMode.SPOT:
# REMOVED_UNUSED_CODE:             raise ConfigurationError(
# REMOVED_UNUSED_CODE:                 "Please migrate your unfilledtimeout settings to use the new wording."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             logger.warning(
# REMOVED_UNUSED_CODE:                 "DEPRECATED: Using 'buy' and 'sell' for unfilledtimeout is deprecated."
# REMOVED_UNUSED_CODE:                 "Please migrate your unfilledtimeout settings to use 'entry' and 'exit' wording."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             for o, n in [
# REMOVED_UNUSED_CODE:                 ("buy", "entry"),
# REMOVED_UNUSED_CODE:                 ("sell", "exit"),
# REMOVED_UNUSED_CODE:             ]:
# REMOVED_UNUSED_CODE:                 process_deprecated_setting(conf, "unfilledtimeout", o, "unfilledtimeout", n)


# REMOVED_UNUSED_CODE: def _validate_pricing_rules(conf: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     if conf.get("ask_strategy") or conf.get("bid_strategy"):
# REMOVED_UNUSED_CODE:         if conf.get("trading_mode", TradingMode.SPOT) != TradingMode.SPOT:
# REMOVED_UNUSED_CODE:             raise ConfigurationError("Please migrate your pricing settings to use the new wording.")
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             logger.warning(
# REMOVED_UNUSED_CODE:                 "DEPRECATED: Using 'ask_strategy' and 'bid_strategy' is deprecated."
# REMOVED_UNUSED_CODE:                 "Please migrate your settings to use 'entry_pricing' and 'exit_pricing'."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             conf["entry_pricing"] = {}
# REMOVED_UNUSED_CODE:             for obj in list(conf.get("bid_strategy", {}).keys()):
# REMOVED_UNUSED_CODE:                 if obj == "ask_last_balance":
# REMOVED_UNUSED_CODE:                     process_deprecated_setting(
# REMOVED_UNUSED_CODE:                         conf, "bid_strategy", obj, "entry_pricing", "price_last_balance"
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE:                     process_deprecated_setting(conf, "bid_strategy", obj, "entry_pricing", obj)
# REMOVED_UNUSED_CODE:             del conf["bid_strategy"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             conf["exit_pricing"] = {}
# REMOVED_UNUSED_CODE:             for obj in list(conf.get("ask_strategy", {}).keys()):
# REMOVED_UNUSED_CODE:                 if obj == "bid_last_balance":
# REMOVED_UNUSED_CODE:                     process_deprecated_setting(
# REMOVED_UNUSED_CODE:                         conf, "ask_strategy", obj, "exit_pricing", "price_last_balance"
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE:                     process_deprecated_setting(conf, "ask_strategy", obj, "exit_pricing", obj)
# REMOVED_UNUSED_CODE:             del conf["ask_strategy"]


# REMOVED_UNUSED_CODE: def _validate_freqai_hyperopt(conf: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     freqai_enabled = conf.get("freqai", {}).get("enabled", False)
# REMOVED_UNUSED_CODE:     analyze_per_epoch = conf.get("analyze_per_epoch", False)
# REMOVED_UNUSED_CODE:     if analyze_per_epoch and freqai_enabled:
# REMOVED_UNUSED_CODE:         raise ConfigurationError(
# REMOVED_UNUSED_CODE:             "Using analyze-per-epoch parameter is not supported with a FreqAI strategy."
# REMOVED_UNUSED_CODE:         )


# REMOVED_UNUSED_CODE: def _validate_freqai_include_timeframes(conf: dict[str, Any], preliminary: bool) -> None:
# REMOVED_UNUSED_CODE:     freqai_enabled = conf.get("freqai", {}).get("enabled", False)
# REMOVED_UNUSED_CODE:     if freqai_enabled:
# REMOVED_UNUSED_CODE:         main_tf = conf.get("timeframe", "5m")
# REMOVED_UNUSED_CODE:         freqai_include_timeframes = (
# REMOVED_UNUSED_CODE:             conf.get("freqai", {}).get("feature_parameters", {}).get("include_timeframes", [])
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         from freqtrade.exchange import timeframe_to_seconds
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         main_tf_s = timeframe_to_seconds(main_tf)
# REMOVED_UNUSED_CODE:         offending_lines = []
# REMOVED_UNUSED_CODE:         for tf in freqai_include_timeframes:
# REMOVED_UNUSED_CODE:             tf_s = timeframe_to_seconds(tf)
# REMOVED_UNUSED_CODE:             if tf_s < main_tf_s:
# REMOVED_UNUSED_CODE:                 offending_lines.append(tf)
# REMOVED_UNUSED_CODE:         if offending_lines:
# REMOVED_UNUSED_CODE:             raise ConfigurationError(
# REMOVED_UNUSED_CODE:                 f"Main timeframe of {main_tf} must be smaller or equal to FreqAI "
# REMOVED_UNUSED_CODE:                 f"`include_timeframes`.Offending include-timeframes: {', '.join(offending_lines)}"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Ensure that the base timeframe is included in the include_timeframes list
# REMOVED_UNUSED_CODE:         if not preliminary and main_tf not in freqai_include_timeframes:
# REMOVED_UNUSED_CODE:             feature_parameters = conf.get("freqai", {}).get("feature_parameters", {})
# REMOVED_UNUSED_CODE:             include_timeframes = [main_tf] + freqai_include_timeframes
# REMOVED_UNUSED_CODE:             conf.get("freqai", {}).get("feature_parameters", {}).update(
# REMOVED_UNUSED_CODE:                 {**feature_parameters, "include_timeframes": include_timeframes}
# REMOVED_UNUSED_CODE:             )


# REMOVED_UNUSED_CODE: def _validate_freqai_backtest(conf: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     if conf.get("runmode", RunMode.OTHER) == RunMode.BACKTEST:
# REMOVED_UNUSED_CODE:         freqai_enabled = conf.get("freqai", {}).get("enabled", False)
# REMOVED_UNUSED_CODE:         timerange = conf.get("timerange")
# REMOVED_UNUSED_CODE:         freqai_backtest_live_models = conf.get("freqai_backtest_live_models", False)
# REMOVED_UNUSED_CODE:         if freqai_backtest_live_models and freqai_enabled and timerange:
# REMOVED_UNUSED_CODE:             raise ConfigurationError(
# REMOVED_UNUSED_CODE:                 "Using timerange parameter is not supported with "
# REMOVED_UNUSED_CODE:                 "--freqai-backtest-live-models parameter."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if freqai_backtest_live_models and not freqai_enabled:
# REMOVED_UNUSED_CODE:             raise ConfigurationError(
# REMOVED_UNUSED_CODE:                 "Using --freqai-backtest-live-models parameter is only "
# REMOVED_UNUSED_CODE:                 "supported with a FreqAI strategy."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if freqai_enabled and not freqai_backtest_live_models and not timerange:
# REMOVED_UNUSED_CODE:             raise ConfigurationError(
# REMOVED_UNUSED_CODE:                 "Please pass --timerange if you intend to use FreqAI for backtesting."
# REMOVED_UNUSED_CODE:             )


# REMOVED_UNUSED_CODE: def _validate_consumers(conf: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     emc_conf = conf.get("external_message_consumer", {})
# REMOVED_UNUSED_CODE:     if emc_conf.get("enabled", False):
# REMOVED_UNUSED_CODE:         if len(emc_conf.get("producers", [])) < 1:
# REMOVED_UNUSED_CODE:             raise ConfigurationError("You must specify at least 1 Producer to connect to.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         producer_names = [p["name"] for p in emc_conf.get("producers", [])]
# REMOVED_UNUSED_CODE:         duplicates = [item for item, count in Counter(producer_names).items() if count > 1]
# REMOVED_UNUSED_CODE:         if duplicates:
# REMOVED_UNUSED_CODE:             raise ConfigurationError(
# REMOVED_UNUSED_CODE:                 f"Producer names must be unique. Duplicate: {', '.join(duplicates)}"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         if conf.get("process_only_new_candles", True):
# REMOVED_UNUSED_CODE:             # Warning here or require it?
# REMOVED_UNUSED_CODE:             logger.warning(
# REMOVED_UNUSED_CODE:                 "To receive best performance with external data, "
# REMOVED_UNUSED_CODE:                 "please set `process_only_new_candles` to False"
# REMOVED_UNUSED_CODE:             )


# REMOVED_UNUSED_CODE: def _validate_orderflow(conf: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     if conf.get("exchange", {}).get("use_public_trades"):
# REMOVED_UNUSED_CODE:         if "orderflow" not in conf:
# REMOVED_UNUSED_CODE:             raise ConfigurationError(
# REMOVED_UNUSED_CODE:                 "Orderflow is a required configuration key when using public trades."
# REMOVED_UNUSED_CODE:             )


# REMOVED_UNUSED_CODE: def _strategy_settings(conf: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     process_deprecated_setting(conf, None, "use_sell_signal", None, "use_exit_signal")
# REMOVED_UNUSED_CODE:     process_deprecated_setting(conf, None, "sell_profit_only", None, "exit_profit_only")
# REMOVED_UNUSED_CODE:     process_deprecated_setting(conf, None, "sell_profit_offset", None, "exit_profit_offset")
# REMOVED_UNUSED_CODE:     process_deprecated_setting(
# REMOVED_UNUSED_CODE:         conf, None, "ignore_roi_if_buy_signal", None, "ignore_roi_if_entry_signal"
# REMOVED_UNUSED_CODE:     )
