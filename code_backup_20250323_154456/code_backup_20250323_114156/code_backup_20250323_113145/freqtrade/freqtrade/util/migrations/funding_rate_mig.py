import logging

from freqtrade.constants import Config
from freqtrade.enums import TradingMode
from freqtrade.exchange import Exchange


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: def migrate_funding_fee_timeframe(config: Config, exchange: Exchange | None):
# REMOVED_UNUSED_CODE:     from freqtrade.data.history import get_datahandler
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if config.get("trading_mode", TradingMode.SPOT) != TradingMode.FUTURES:
# REMOVED_UNUSED_CODE:         # only act on futures
# REMOVED_UNUSED_CODE:         return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if not exchange:
# REMOVED_UNUSED_CODE:         from freqtrade.resolvers import ExchangeResolver
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         exchange = ExchangeResolver.load_exchange(config, validate=False)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     ff_timeframe = exchange.get_option("funding_fee_timeframe")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     dhc = get_datahandler(config["datadir"], config["dataformat_ohlcv"])
# REMOVED_UNUSED_CODE:     dhc.fix_funding_fee_timeframe(ff_timeframe)
