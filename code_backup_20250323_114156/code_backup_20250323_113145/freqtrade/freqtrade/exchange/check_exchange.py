import logging

# REMOVED_UNUSED_CODE: from freqtrade.constants import Config
# REMOVED_UNUSED_CODE: from freqtrade.enums import RunMode
# REMOVED_UNUSED_CODE: from freqtrade.exceptions import OperationalException
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.exchange import available_exchanges, is_exchange_known_ccxt, validate_exchange
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.exchange.common import MAP_EXCHANGE_CHILDCLASS, SUPPORTED_EXCHANGES


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: def check_exchange(config: Config, check_for_bad: bool = True) -> bool:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Check if the exchange name in the config file is supported by Freqtrade
# REMOVED_UNUSED_CODE:     :param check_for_bad: if True, check the exchange against the list of known 'bad'
# REMOVED_UNUSED_CODE:                           exchanges
# REMOVED_UNUSED_CODE:     :return: False if exchange is 'bad', i.e. is known to work with the bot with
# REMOVED_UNUSED_CODE:              critical issues or does not work at all, crashes, etc. True otherwise.
# REMOVED_UNUSED_CODE:              raises an exception if the exchange if not supported by ccxt
# REMOVED_UNUSED_CODE:              and thus is not known for the Freqtrade at all.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if config["runmode"] in [
# REMOVED_UNUSED_CODE:         RunMode.PLOT,
# REMOVED_UNUSED_CODE:         RunMode.UTIL_NO_EXCHANGE,
# REMOVED_UNUSED_CODE:         RunMode.OTHER,
# REMOVED_UNUSED_CODE:     ] and not config.get("exchange", {}).get("name"):
# REMOVED_UNUSED_CODE:         # Skip checking exchange in plot mode, since it requires no exchange
# REMOVED_UNUSED_CODE:         return True
# REMOVED_UNUSED_CODE:     logger.info("Checking exchange...")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     exchange = config.get("exchange", {}).get("name", "").lower()
# REMOVED_UNUSED_CODE:     if not exchange:
# REMOVED_UNUSED_CODE:         raise OperationalException(
# REMOVED_UNUSED_CODE:             f"This command requires a configured exchange. You should either use "
# REMOVED_UNUSED_CODE:             f"`--exchange <exchange_name>` or specify a configuration file via `--config`.\n"
# REMOVED_UNUSED_CODE:             f"The following exchanges are available for Freqtrade: "
# REMOVED_UNUSED_CODE:             f"{', '.join(available_exchanges())}"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if not is_exchange_known_ccxt(exchange):
# REMOVED_UNUSED_CODE:         raise OperationalException(
# REMOVED_UNUSED_CODE:             f'Exchange "{exchange}" is not known to the ccxt library '
# REMOVED_UNUSED_CODE:             f"and therefore not available for the bot.\n"
# REMOVED_UNUSED_CODE:             f"The following exchanges are available for Freqtrade: "
# REMOVED_UNUSED_CODE:             f"{', '.join(available_exchanges())}"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     valid, reason, _ = validate_exchange(exchange)
# REMOVED_UNUSED_CODE:     if not valid:
# REMOVED_UNUSED_CODE:         if check_for_bad:
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 f'Exchange "{exchange}"  will not work with Freqtrade. Reason: {reason}'
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             logger.warning(f'Exchange "{exchange}"  will not work with Freqtrade. Reason: {reason}')
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if MAP_EXCHANGE_CHILDCLASS.get(exchange, exchange) in SUPPORTED_EXCHANGES:
# REMOVED_UNUSED_CODE:         logger.info(
# REMOVED_UNUSED_CODE:             f'Exchange "{exchange}" is officially supported by the Freqtrade development team.'
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         logger.warning(
# REMOVED_UNUSED_CODE:             f'Exchange "{exchange}" is known to the ccxt library, '
# REMOVED_UNUSED_CODE:             f"available for the bot, but not officially supported "
# REMOVED_UNUSED_CODE:             f"by the Freqtrade development team. "
# REMOVED_UNUSED_CODE:             f"It may work flawlessly (please report back) or have serious issues. "
# REMOVED_UNUSED_CODE:             f"Use it at your own discretion."
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return True
