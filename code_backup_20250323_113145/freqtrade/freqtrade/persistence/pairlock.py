# REMOVED_UNUSED_CODE: from datetime import datetime, timezone
# REMOVED_UNUSED_CODE: from typing import Any, ClassVar

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from sqlalchemy import ScalarResult, String, or_, select
from sqlalchemy.orm import Mapped, mapped_column

from freqtrade.constants import DATETIME_PRINT_FORMAT
from freqtrade.persistence.base import ModelBase, SessionType


# REMOVED_UNUSED_CODE: class PairLock(ModelBase):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Pair Locks database model.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     __tablename__ = "pairlocks"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     session: ClassVar[SessionType]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     id: Mapped[int] = mapped_column(primary_key=True)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     pair: Mapped[str] = mapped_column(String(25), nullable=False, index=True)
# REMOVED_UNUSED_CODE:     # lock direction - long, short or * (for both)
# REMOVED_UNUSED_CODE:     side: Mapped[str] = mapped_column(String(25), nullable=False, default="*")
# REMOVED_UNUSED_CODE:     reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
# REMOVED_UNUSED_CODE:     # Time the pair was locked (start time)
# REMOVED_UNUSED_CODE:     lock_time: Mapped[datetime] = mapped_column(nullable=False)
# REMOVED_UNUSED_CODE:     # Time until the pair is locked (end time)
# REMOVED_UNUSED_CODE:     lock_end_time: Mapped[datetime] = mapped_column(nullable=False, index=True)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     active: Mapped[bool] = mapped_column(nullable=False, default=True, index=True)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __repr__(self) -> str:
# REMOVED_UNUSED_CODE:         lock_time = self.lock_time.strftime(DATETIME_PRINT_FORMAT)
# REMOVED_UNUSED_CODE:         lock_end_time = self.lock_end_time.strftime(DATETIME_PRINT_FORMAT)
# REMOVED_UNUSED_CODE:         return (
# REMOVED_UNUSED_CODE:             f"PairLock(id={self.id}, pair={self.pair}, side={self.side}, lock_time={lock_time}, "
# REMOVED_UNUSED_CODE:             f"lock_end_time={lock_end_time}, reason={self.reason}, active={self.active})"
# REMOVED_UNUSED_CODE:         )

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def query_pair_locks(
# REMOVED_UNUSED_CODE:         pair: str | None, now: datetime, side: str | None = None
# REMOVED_UNUSED_CODE:     ) -> ScalarResult["PairLock"]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Get all currently active locks for this pair
# REMOVED_UNUSED_CODE:         :param pair: Pair to check for. Returns all current locks if pair is empty
# REMOVED_UNUSED_CODE:         :param now: Datetime object (generated via datetime.now(timezone.utc)).
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         filters = [
# REMOVED_UNUSED_CODE:             PairLock.lock_end_time > now,
# REMOVED_UNUSED_CODE:             # Only active locks
# REMOVED_UNUSED_CODE:             PairLock.active.is_(True),
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE:         if pair:
# REMOVED_UNUSED_CODE:             filters.append(PairLock.pair == pair)
# REMOVED_UNUSED_CODE:         if side is not None and side != "*":
# REMOVED_UNUSED_CODE:             filters.append(or_(PairLock.side == side, PairLock.side == "*"))
# REMOVED_UNUSED_CODE:         elif side is not None:
# REMOVED_UNUSED_CODE:             filters.append(PairLock.side == "*")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return PairLock.session.scalars(select(PairLock).filter(*filters))

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def get_all_locks() -> ScalarResult["PairLock"]:
# REMOVED_UNUSED_CODE:         return PairLock.session.scalars(select(PairLock))

# REMOVED_UNUSED_CODE:     def to_json(self) -> dict[str, Any]:
# REMOVED_UNUSED_CODE:         return {
# REMOVED_UNUSED_CODE:             "id": self.id,
# REMOVED_UNUSED_CODE:             "pair": self.pair,
# REMOVED_UNUSED_CODE:             "lock_time": self.lock_time.strftime(DATETIME_PRINT_FORMAT),
# REMOVED_UNUSED_CODE:             "lock_timestamp": int(self.lock_time.replace(tzinfo=timezone.utc).timestamp() * 1000),
# REMOVED_UNUSED_CODE:             "lock_end_time": self.lock_end_time.strftime(DATETIME_PRINT_FORMAT),
# REMOVED_UNUSED_CODE:             "lock_end_timestamp": int(
# REMOVED_UNUSED_CODE:                 self.lock_end_time.replace(tzinfo=timezone.utc).timestamp() * 1000
# REMOVED_UNUSED_CODE:             ),
# REMOVED_UNUSED_CODE:             "reason": self.reason,
# REMOVED_UNUSED_CODE:             "side": self.side,
# REMOVED_UNUSED_CODE:             "active": self.active,
# REMOVED_UNUSED_CODE:         }
