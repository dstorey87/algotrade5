import json
import logging
from collections.abc import Sequence
from datetime import datetime
from typing import Any, ClassVar

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, select
# REMOVED_UNUSED_CODE: from sqlalchemy.orm import Mapped, mapped_column, relationship

from freqtrade.constants import DATETIME_PRINT_FORMAT
from freqtrade.persistence.base import ModelBase, SessionType
from freqtrade.util import dt_now


logger = logging.getLogger(__name__)


class _CustomData(ModelBase):
    """
    CustomData database model
    Keeps records of metadata as key/value store
    for trades or global persistent values
    One to many relationship with Trades:
      - One trade can have many metadata entries
      - One metadata entry can only be associated with one Trade
    """

    __tablename__ = "trade_custom_data"
    __allow_unmapped__ = True
    session: ClassVar[SessionType]

    # Uniqueness should be ensured over pair, order_id
    # its likely that order_id is unique per Pair on some exchanges.
    __table_args__ = (UniqueConstraint("ft_trade_id", "cd_key", name="_trade_id_cd_key"),)

    id = mapped_column(Integer, primary_key=True)
    ft_trade_id = mapped_column(Integer, ForeignKey("trades.id"), index=True)

# REMOVED_UNUSED_CODE:     trade = relationship("Trade", back_populates="custom_data")

    cd_key: Mapped[str] = mapped_column(String(255), nullable=False)
    cd_type: Mapped[str] = mapped_column(String(25), nullable=False)
    cd_value: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=dt_now)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Empty container value - not persisted, but filled with cd_value on query
    value: Any = None

    def __repr__(self):
        create_time = (
            self.created_at.strftime(DATETIME_PRINT_FORMAT) if self.created_at is not None else None
        )
        update_time = (
            self.updated_at.strftime(DATETIME_PRINT_FORMAT) if self.updated_at is not None else None
        )
        return (
            f"CustomData(id={self.id}, key={self.cd_key}, type={self.cd_type}, "
            + f"value={self.cd_value}, trade_id={self.ft_trade_id}, created={create_time}, "
            + f"updated={update_time})"
        )

# REMOVED_UNUSED_CODE:     @classmethod
# REMOVED_UNUSED_CODE:     def query_cd(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         cls, key: str | None = None, trade_id: int | None = None
# REMOVED_UNUSED_CODE:     ) -> Sequence["_CustomData"]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Get all CustomData, if trade_id is not specified
# REMOVED_UNUSED_CODE:         return will be for generic values not tied to a trade
# REMOVED_UNUSED_CODE:         :param trade_id: id of the Trade
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         filters = []
# REMOVED_UNUSED_CODE:         if trade_id is not None:
# REMOVED_UNUSED_CODE:             filters.append(_CustomData.ft_trade_id == trade_id)
# REMOVED_UNUSED_CODE:         if key is not None:
# REMOVED_UNUSED_CODE:             filters.append(_CustomData.cd_key.ilike(key))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return _CustomData.session.scalars(select(_CustomData).filter(*filters)).all()


class CustomDataWrapper:
    """
    CustomData middleware class
    Abstracts the database layer away so it becomes optional - which will be necessary to support
    backtesting and hyperopt in the future.
    """

    use_db = True
    custom_data: list[_CustomData] = []
    unserialized_types = ["bool", "float", "int", "str"]

    @staticmethod
    def _convert_custom_data(data: _CustomData) -> _CustomData:
        if data.cd_type in CustomDataWrapper.unserialized_types:
            data.value = data.cd_value
            if data.cd_type == "bool":
                data.value = data.cd_value.lower() == "true"
            elif data.cd_type == "int":
                data.value = int(data.cd_value)
            elif data.cd_type == "float":
                data.value = float(data.cd_value)
        else:
            data.value = json.loads(data.cd_value)
        return data

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def reset_custom_data() -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Resets all key-value pairs. Only active for backtesting mode.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if not CustomDataWrapper.use_db:
# REMOVED_UNUSED_CODE:             CustomDataWrapper.custom_data = []

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def delete_custom_data(trade_id: int) -> None:
# REMOVED_UNUSED_CODE:         _CustomData.session.query(_CustomData).filter(_CustomData.ft_trade_id == trade_id).delete()
# REMOVED_UNUSED_CODE:         _CustomData.session.commit()

    @staticmethod
    def get_custom_data(*, trade_id: int, key: str | None = None) -> list[_CustomData]:
        if CustomDataWrapper.use_db:
            filters = [
                _CustomData.ft_trade_id == trade_id,
            ]
            if key is not None:
                filters.append(_CustomData.cd_key.ilike(key))
            filtered_custom_data = _CustomData.session.scalars(
                select(_CustomData).filter(*filters)
            ).all()

        else:
            filtered_custom_data = [
                data_entry
                for data_entry in CustomDataWrapper.custom_data
                if (data_entry.ft_trade_id == trade_id)
            ]
            if key is not None:
                filtered_custom_data = [
                    data_entry
                    for data_entry in filtered_custom_data
                    if (data_entry.cd_key.casefold() == key.casefold())
                ]
        return [CustomDataWrapper._convert_custom_data(d) for d in filtered_custom_data]

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def set_custom_data(trade_id: int, key: str, value: Any) -> None:
# REMOVED_UNUSED_CODE:         value_type = type(value).__name__
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if value_type not in CustomDataWrapper.unserialized_types:
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 value_db = json.dumps(value)
# REMOVED_UNUSED_CODE:             except TypeError as e:
# REMOVED_UNUSED_CODE:                 logger.warning(f"could not serialize {key} value due to {e}")
# REMOVED_UNUSED_CODE:                 return
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             value_db = str(value)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if trade_id is None:
# REMOVED_UNUSED_CODE:             trade_id = 0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         custom_data = CustomDataWrapper.get_custom_data(trade_id=trade_id, key=key)
# REMOVED_UNUSED_CODE:         if custom_data:
# REMOVED_UNUSED_CODE:             data_entry = custom_data[0]
# REMOVED_UNUSED_CODE:             data_entry.cd_value = value_db
# REMOVED_UNUSED_CODE:             data_entry.updated_at = dt_now()
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             data_entry = _CustomData(
# REMOVED_UNUSED_CODE:                 ft_trade_id=trade_id,
# REMOVED_UNUSED_CODE:                 cd_key=key,
# REMOVED_UNUSED_CODE:                 cd_type=value_type,
# REMOVED_UNUSED_CODE:                 cd_value=value_db,
# REMOVED_UNUSED_CODE:                 created_at=dt_now(),
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         data_entry.value = value
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if CustomDataWrapper.use_db and value_db is not None:
# REMOVED_UNUSED_CODE:             _CustomData.session.add(data_entry)
# REMOVED_UNUSED_CODE:             _CustomData.session.commit()
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             if not custom_data:
# REMOVED_UNUSED_CODE:                 CustomDataWrapper.custom_data.append(data_entry)
            # Existing data will have updated interactively.
