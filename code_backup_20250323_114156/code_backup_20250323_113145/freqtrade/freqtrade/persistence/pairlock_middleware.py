import logging
from collections.abc import Sequence
from datetime import datetime, timezone

from sqlalchemy import select

from freqtrade.exchange import timeframe_to_next_date
from freqtrade.persistence.models import PairLock


logger = logging.getLogger(__name__)


class PairLocks:
    """
    Pairlocks middleware class
    Abstracts the database layer away so it becomes optional - which will be necessary to support
    backtesting and hyperopt in the future.
    """

    use_db = True
    locks: list[PairLock] = []

    timeframe: str = ""

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def reset_locks() -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Resets all locks. Only active for backtesting mode.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if not PairLocks.use_db:
# REMOVED_UNUSED_CODE:             PairLocks.locks = []

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def lock_pair(
# REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE:         until: datetime,
# REMOVED_UNUSED_CODE:         reason: str | None = None,
# REMOVED_UNUSED_CODE:         *,
# REMOVED_UNUSED_CODE:         now: datetime | None = None,
# REMOVED_UNUSED_CODE:         side: str = "*",
# REMOVED_UNUSED_CODE:     ) -> PairLock:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Create PairLock from now to "until".
# REMOVED_UNUSED_CODE:         Uses database by default, unless PairLocks.use_db is set to False,
# REMOVED_UNUSED_CODE:         in which case a list is maintained.
# REMOVED_UNUSED_CODE:         :param pair: pair to lock. use '*' to lock all pairs
# REMOVED_UNUSED_CODE:         :param until: End time of the lock. Will be rounded up to the next candle.
# REMOVED_UNUSED_CODE:         :param reason: Reason string that will be shown as reason for the lock
# REMOVED_UNUSED_CODE:         :param now: Current timestamp. Used to determine lock start time.
# REMOVED_UNUSED_CODE:         :param side: Side to lock pair, can be 'long', 'short' or '*'
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         lock = PairLock(
# REMOVED_UNUSED_CODE:             pair=pair,
# REMOVED_UNUSED_CODE:             lock_time=now or datetime.now(timezone.utc),
# REMOVED_UNUSED_CODE:             lock_end_time=timeframe_to_next_date(PairLocks.timeframe, until),
# REMOVED_UNUSED_CODE:             reason=reason,
# REMOVED_UNUSED_CODE:             side=side,
# REMOVED_UNUSED_CODE:             active=True,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         if PairLocks.use_db:
# REMOVED_UNUSED_CODE:             PairLock.session.add(lock)
# REMOVED_UNUSED_CODE:             PairLock.session.commit()
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             PairLocks.locks.append(lock)
# REMOVED_UNUSED_CODE:         return lock

    @staticmethod
    def get_pair_locks(
        pair: str | None, now: datetime | None = None, side: str | None = None
    ) -> Sequence[PairLock]:
        """
        Get all currently active locks for this pair
        :param pair: Pair to check for. Returns all current locks if pair is empty
        :param now: Datetime object (generated via datetime.now(timezone.utc)).
                    defaults to datetime.now(timezone.utc)
        :param side: Side get locks for, can be 'long', 'short', '*' or None
        """
        if not now:
            now = datetime.now(timezone.utc)

        if PairLocks.use_db:
            return PairLock.query_pair_locks(pair, now, side).all()
        else:
            locks = [
                lock
                for lock in PairLocks.locks
                if (
                    lock.lock_end_time >= now
                    and lock.active is True
                    and (pair is None or lock.pair == pair)
                    and (side is None or lock.side == "*" or lock.side == side)
                )
            ]
            return locks

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def get_pair_longest_lock(
# REMOVED_UNUSED_CODE:         pair: str, now: datetime | None = None, side: str = "*"
# REMOVED_UNUSED_CODE:     ) -> PairLock | None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Get the lock that expires the latest for the pair given.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         locks = PairLocks.get_pair_locks(pair, now, side=side)
# REMOVED_UNUSED_CODE:         locks = sorted(locks, key=lambda lock: lock.lock_end_time, reverse=True)
# REMOVED_UNUSED_CODE:         return locks[0] if locks else None

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def unlock_pair(pair: str, now: datetime | None = None, side: str = "*") -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Release all locks for this pair.
# REMOVED_UNUSED_CODE:         :param pair: Pair to unlock
# REMOVED_UNUSED_CODE:         :param now: Datetime object (generated via datetime.now(timezone.utc)).
# REMOVED_UNUSED_CODE:             defaults to datetime.now(timezone.utc)
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if not now:
# REMOVED_UNUSED_CODE:             now = datetime.now(timezone.utc)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         logger.info(f"Releasing all locks for {pair}.")
# REMOVED_UNUSED_CODE:         locks = PairLocks.get_pair_locks(pair, now, side=side)
# REMOVED_UNUSED_CODE:         for lock in locks:
# REMOVED_UNUSED_CODE:             lock.active = False
# REMOVED_UNUSED_CODE:         if PairLocks.use_db:
# REMOVED_UNUSED_CODE:             PairLock.session.commit()

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def unlock_reason(reason: str, now: datetime | None = None) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Release all locks for this reason.
# REMOVED_UNUSED_CODE:         :param reason: Which reason to unlock
# REMOVED_UNUSED_CODE:         :param now: Datetime object (generated via datetime.now(timezone.utc)).
# REMOVED_UNUSED_CODE:             defaults to datetime.now(timezone.utc)
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if not now:
# REMOVED_UNUSED_CODE:             now = datetime.now(timezone.utc)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if PairLocks.use_db:
# REMOVED_UNUSED_CODE:             # used in live modes
# REMOVED_UNUSED_CODE:             logger.info(f"Releasing all locks with reason '{reason}':")
# REMOVED_UNUSED_CODE:             filters = [
# REMOVED_UNUSED_CODE:                 PairLock.lock_end_time > now,
# REMOVED_UNUSED_CODE:                 PairLock.active.is_(True),
# REMOVED_UNUSED_CODE:                 PairLock.reason == reason,
# REMOVED_UNUSED_CODE:             ]
# REMOVED_UNUSED_CODE:             locks = PairLock.session.scalars(select(PairLock).filter(*filters)).all()
# REMOVED_UNUSED_CODE:             for lock in locks:
# REMOVED_UNUSED_CODE:                 logger.info(f"Releasing lock for {lock.pair} with reason '{reason}'.")
# REMOVED_UNUSED_CODE:                 lock.active = False
# REMOVED_UNUSED_CODE:             PairLock.session.commit()
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             # used in backtesting mode; don't show log messages for speed
# REMOVED_UNUSED_CODE:             locksb = PairLocks.get_pair_locks(None)
# REMOVED_UNUSED_CODE:             for lock in locksb:
# REMOVED_UNUSED_CODE:                 if lock.reason == reason:
# REMOVED_UNUSED_CODE:                     lock.active = False

    @staticmethod
    def is_global_lock(now: datetime | None = None, side: str = "*") -> bool:
        """
        :param now: Datetime object (generated via datetime.now(timezone.utc)).
            defaults to datetime.now(timezone.utc)
        """
        if not now:
            now = datetime.now(timezone.utc)

        return len(PairLocks.get_pair_locks("*", now, side)) > 0

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def is_pair_locked(pair: str, now: datetime | None = None, side: str = "*") -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         :param pair: Pair to check for
# REMOVED_UNUSED_CODE:         :param now: Datetime object (generated via datetime.now(timezone.utc)).
# REMOVED_UNUSED_CODE:             defaults to datetime.now(timezone.utc)
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if not now:
# REMOVED_UNUSED_CODE:             now = datetime.now(timezone.utc)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return len(PairLocks.get_pair_locks(pair, now, side)) > 0 or PairLocks.is_global_lock(
# REMOVED_UNUSED_CODE:             now, side
# REMOVED_UNUSED_CODE:         )

    @staticmethod
    def get_all_locks() -> Sequence[PairLock]:
        """
        Return all locks, also locks with expired end date
        """
        if PairLocks.use_db:
            return PairLock.get_all_locks().all()
        else:
            return PairLocks.locks
