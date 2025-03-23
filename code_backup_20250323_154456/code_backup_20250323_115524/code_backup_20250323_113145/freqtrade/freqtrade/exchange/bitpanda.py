"""Bitpanda exchange subclass"""

import logging
from datetime import datetime, timezone

from freqtrade.exchange import Exchange


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class Bitpanda(Exchange):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Bitpanda exchange class. Contains adjustments needed for Freqtrade to work
# REMOVED_UNUSED_CODE:     with this exchange.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def get_trades_for_order(
# REMOVED_UNUSED_CODE:         self, order_id: str, pair: str, since: datetime, params: dict | None = None
# REMOVED_UNUSED_CODE:     ) -> list:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Fetch Orders using the "fetch_my_trades" endpoint and filter them by order-id.
# REMOVED_UNUSED_CODE:         The "since" argument passed in is coming from the database and is in UTC,
# REMOVED_UNUSED_CODE:         as timezone-native datetime object.
# REMOVED_UNUSED_CODE:         From the python documentation:
# REMOVED_UNUSED_CODE:             > Naive datetime instances are assumed to represent local time
# REMOVED_UNUSED_CODE:         Therefore, calling "since.timestamp()" will get the UTC timestamp, after applying the
# REMOVED_UNUSED_CODE:         transformation from local timezone to UTC.
# REMOVED_UNUSED_CODE:         This works for timezones UTC+ since then the result will contain trades from a few hours
# REMOVED_UNUSED_CODE:         instead of from the last 5 seconds, however fails for UTC- timezones,
# REMOVED_UNUSED_CODE:         since we're then asking for trades with a "since" argument in the future.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         :param order_id order_id: Order-id as given when creating the order
# REMOVED_UNUSED_CODE:         :param pair: Pair the order is for
# REMOVED_UNUSED_CODE:         :param since: datetime object of the order creation time. Assumes object is in UTC.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         params = {"to": int(datetime.now(timezone.utc).timestamp() * 1000)}
# REMOVED_UNUSED_CODE:         return super().get_trades_for_order(order_id, pair, since, params)
