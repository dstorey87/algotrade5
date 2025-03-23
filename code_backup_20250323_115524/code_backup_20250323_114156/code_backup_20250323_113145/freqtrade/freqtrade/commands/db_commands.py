import logging
from typing import Any

from freqtrade.enums import RunMode


logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: def start_convert_db(args: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     from sqlalchemy import func, select
# REMOVED_UNUSED_CODE:     from sqlalchemy.orm import make_transient
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     from freqtrade.configuration.config_setup import setup_utils_configuration
# REMOVED_UNUSED_CODE:     from freqtrade.persistence import Order, Trade, init_db
# REMOVED_UNUSED_CODE:     from freqtrade.persistence.migrations import set_sequence_ids
# REMOVED_UNUSED_CODE:     from freqtrade.persistence.pairlock import PairLock
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     config = setup_utils_configuration(args, RunMode.UTIL_NO_EXCHANGE)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     init_db(config["db_url"])
# REMOVED_UNUSED_CODE:     session_target = Trade.session
# REMOVED_UNUSED_CODE:     init_db(config["db_url_from"])
# REMOVED_UNUSED_CODE:     logger.info("Starting db migration.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     trade_count = 0
# REMOVED_UNUSED_CODE:     pairlock_count = 0
# REMOVED_UNUSED_CODE:     for trade in Trade.get_trades():
# REMOVED_UNUSED_CODE:         trade_count += 1
# REMOVED_UNUSED_CODE:         make_transient(trade)
# REMOVED_UNUSED_CODE:         for o in trade.orders:
# REMOVED_UNUSED_CODE:             make_transient(o)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         session_target.add(trade)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     session_target.commit()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     for pairlock in PairLock.get_all_locks():
# REMOVED_UNUSED_CODE:         pairlock_count += 1
# REMOVED_UNUSED_CODE:         make_transient(pairlock)
# REMOVED_UNUSED_CODE:         session_target.add(pairlock)
# REMOVED_UNUSED_CODE:     session_target.commit()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Update sequences
# REMOVED_UNUSED_CODE:     max_trade_id = session_target.scalar(select(func.max(Trade.id)))
# REMOVED_UNUSED_CODE:     max_order_id = session_target.scalar(select(func.max(Order.id)))
# REMOVED_UNUSED_CODE:     max_pairlock_id = session_target.scalar(select(func.max(PairLock.id)))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     set_sequence_ids(
# REMOVED_UNUSED_CODE:         session_target.get_bind(),
# REMOVED_UNUSED_CODE:         trade_id=max_trade_id,
# REMOVED_UNUSED_CODE:         order_id=max_order_id,
# REMOVED_UNUSED_CODE:         pairlock_id=max_pairlock_id,
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     logger.info(f"Migrated {trade_count} Trades, and {pairlock_count} Pairlocks.")
