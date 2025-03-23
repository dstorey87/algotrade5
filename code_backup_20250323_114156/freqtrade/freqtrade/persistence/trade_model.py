"""
This module contains the class to persist trades into SQLite
"""

import logging
from collections import defaultdict
# REMOVED_UNUSED_CODE: from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
# REMOVED_UNUSED_CODE: from math import isclose
# REMOVED_UNUSED_CODE: from typing import Any, ClassVar, Optional, cast

from sqlalchemy import (
    Enum,
    Float,
    ForeignKey,
    Integer,
    ScalarResult,
    Select,
    String,
    UniqueConstraint,
    case,
    desc,
    func,
    select,
)
# REMOVED_UNUSED_CODE: from sqlalchemy.orm import Mapped, lazyload, mapped_column, relationship, validates
from typing_extensions import Self

# REMOVED_UNUSED_CODE: from freqtrade.constants import (
# REMOVED_UNUSED_CODE:     CANCELED_EXCHANGE_STATES,
# REMOVED_UNUSED_CODE:     CUSTOM_TAG_MAX_LENGTH,
# REMOVED_UNUSED_CODE:     DATETIME_PRINT_FORMAT,
# REMOVED_UNUSED_CODE:     MATH_CLOSE_PREC,
# REMOVED_UNUSED_CODE:     NON_OPEN_EXCHANGE_STATES,
# REMOVED_UNUSED_CODE:     BuySell,
# REMOVED_UNUSED_CODE:     LongShort,
# REMOVED_UNUSED_CODE: )
# REMOVED_UNUSED_CODE: from freqtrade.enums import ExitType, TradingMode
from freqtrade.exceptions import DependencyException, OperationalException
from freqtrade.exchange import (
    ROUND_DOWN,
    ROUND_UP,
    amount_to_contract_precision,
    price_to_precision,
)
from freqtrade.exchange.exchange_types import CcxtOrder
from freqtrade.leverage import interest
from freqtrade.misc import safe_value_fallback
from freqtrade.persistence.base import ModelBase, SessionType
# REMOVED_UNUSED_CODE: from freqtrade.persistence.custom_data import CustomDataWrapper, _CustomData
from freqtrade.util import FtPrecise, dt_from_ts, dt_now, dt_ts, dt_ts_none


logger = logging.getLogger(__name__)


@dataclass
class ProfitStruct:
    profit_abs: float
    profit_ratio: float
# REMOVED_UNUSED_CODE:     total_profit: float
    total_profit_ratio: float


class Order(ModelBase):
    """
    Order database model
    Keeps a record of all orders placed on the exchange

    One to many relationship with Trades:
      - One trade can have many orders
      - One Order can only be associated with one Trade

    Mirrors CCXT Order structure
    """

    __tablename__ = "orders"
    __allow_unmapped__ = True
    session: ClassVar[SessionType]

    # Uniqueness should be ensured over pair, order_id
    # its likely that order_id is unique per Pair on some exchanges.
    __table_args__ = (UniqueConstraint("ft_pair", "order_id", name="_order_pair_order_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ft_trade_id: Mapped[int] = mapped_column(Integer, ForeignKey("trades.id"), index=True)

    _trade_live: Mapped["Trade"] = relationship("Trade", back_populates="orders", lazy="immediate")
    _trade_bt: "LocalTrade" = None  # type: ignore

    # order_side can only be 'buy', 'sell' or 'stoploss'
    ft_order_side: Mapped[str] = mapped_column(String(25), nullable=False)
    ft_pair: Mapped[str] = mapped_column(String(25), nullable=False)
    ft_is_open: Mapped[bool] = mapped_column(nullable=False, default=True, index=True)
    ft_amount: Mapped[float] = mapped_column(Float(), nullable=False)
    ft_price: Mapped[float] = mapped_column(Float(), nullable=False)
# REMOVED_UNUSED_CODE:     ft_cancel_reason: Mapped[str] = mapped_column(String(CUSTOM_TAG_MAX_LENGTH), nullable=True)

    order_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    status: Mapped[str | None] = mapped_column(String(255), nullable=True)
    symbol: Mapped[str | None] = mapped_column(String(25), nullable=True)
    order_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    side: Mapped[str] = mapped_column(String(25), nullable=True)
    price: Mapped[float | None] = mapped_column(Float(), nullable=True)
    average: Mapped[float | None] = mapped_column(Float(), nullable=True)
    amount: Mapped[float | None] = mapped_column(Float(), nullable=True)
    filled: Mapped[float | None] = mapped_column(Float(), nullable=True)
    remaining: Mapped[float | None] = mapped_column(Float(), nullable=True)
    cost: Mapped[float | None] = mapped_column(Float(), nullable=True)
    stop_price: Mapped[float | None] = mapped_column(Float(), nullable=True)
    order_date: Mapped[datetime] = mapped_column(nullable=True, default=dt_now)
    order_filled_date: Mapped[datetime | None] = mapped_column(nullable=True)
# REMOVED_UNUSED_CODE:     order_update_date: Mapped[datetime | None] = mapped_column(nullable=True)
    funding_fee: Mapped[float | None] = mapped_column(Float(), nullable=True)

    ft_fee_base: Mapped[float | None] = mapped_column(Float(), nullable=True)
    ft_order_tag: Mapped[str | None] = mapped_column(String(CUSTOM_TAG_MAX_LENGTH), nullable=True)

    @property
    def order_date_utc(self) -> datetime:
        """Order-date with UTC timezoneinfo"""
        return self.order_date.replace(tzinfo=timezone.utc)

    @property
    def order_filled_utc(self) -> datetime | None:
        """last order-date with UTC timezoneinfo"""
        return (
            self.order_filled_date.replace(tzinfo=timezone.utc) if self.order_filled_date else None
        )

    @property
    def safe_amount(self) -> float:
        return self.amount or self.ft_amount

# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def safe_placement_price(self) -> float:
# REMOVED_UNUSED_CODE:         """Price at which the order was placed"""
# REMOVED_UNUSED_CODE:         return self.price or self.stop_price or self.ft_price

    @property
    def safe_price(self) -> float:
        return self.average or self.price or self.stop_price or self.ft_price

    @property
    def safe_filled(self) -> float:
        return self.filled if self.filled is not None else 0.0

# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def safe_cost(self) -> float:
# REMOVED_UNUSED_CODE:         return self.cost or 0.0

# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def safe_remaining(self) -> float:
# REMOVED_UNUSED_CODE:         return (
# REMOVED_UNUSED_CODE:             self.remaining
# REMOVED_UNUSED_CODE:             if self.remaining is not None
# REMOVED_UNUSED_CODE:             else self.safe_amount - (self.filled or 0.0)
# REMOVED_UNUSED_CODE:         )

    @property
    def safe_fee_base(self) -> float:
        return self.ft_fee_base or 0.0

    @property
    def safe_amount_after_fee(self) -> float:
        return self.safe_filled - self.safe_fee_base

    @property
    def trade(self) -> "LocalTrade":
        return self._trade_bt or self._trade_live

    @property
    def stake_amount(self) -> float:
        """Amount in stake currency used for this order"""
        return float(
            FtPrecise(self.safe_amount)
            * FtPrecise(self.safe_price)
            / FtPrecise(self.trade.leverage)
        )

# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def stake_amount_filled(self) -> float:
# REMOVED_UNUSED_CODE:         """Filled Amount in stake currency used for this order"""
# REMOVED_UNUSED_CODE:         return float(
# REMOVED_UNUSED_CODE:             FtPrecise(self.safe_filled)
# REMOVED_UNUSED_CODE:             * FtPrecise(self.safe_price)
# REMOVED_UNUSED_CODE:             / FtPrecise(self.trade.leverage)
# REMOVED_UNUSED_CODE:         )

    def __repr__(self):
        return (
            f"Order(id={self.id}, trade={self.ft_trade_id}, order_id={self.order_id}, "
            f"side={self.side}, filled={self.safe_filled}, price={self.safe_price}, "
            f"amount={self.amount}, "
            f"status={self.status}, date={self.order_date_utc:{DATETIME_PRINT_FORMAT}})"
        )

    def update_from_ccxt_object(self, order):
        """
        Update Order from ccxt response
        Only updates if fields are available from ccxt -
        """
        if self.order_id != str(order["id"]):
            raise DependencyException("Order-id's don't match")

        self.status = safe_value_fallback(order, "status", default_value=self.status)
        self.symbol = safe_value_fallback(order, "symbol", default_value=self.symbol)
        self.order_type = safe_value_fallback(order, "type", default_value=self.order_type)
        self.side = safe_value_fallback(order, "side", default_value=self.side)
        self.price = safe_value_fallback(order, "price", default_value=self.price)
        self.amount = safe_value_fallback(order, "amount", default_value=self.amount)
        self.filled = safe_value_fallback(order, "filled", default_value=self.filled)
        self.average = safe_value_fallback(order, "average", default_value=self.average)
        self.remaining = safe_value_fallback(order, "remaining", default_value=self.remaining)
        self.cost = safe_value_fallback(order, "cost", default_value=self.cost)
        self.stop_price = safe_value_fallback(order, "stopPrice", default_value=self.stop_price)
        order_date = safe_value_fallback(order, "timestamp")
        if order_date:
            self.order_date = dt_from_ts(order_date)
        elif not self.order_date:
            self.order_date = dt_now()

        self.ft_is_open = True
        if self.status in NON_OPEN_EXCHANGE_STATES:
            self.ft_is_open = False
            if (order.get("filled", 0.0) or 0.0) > 0 and not self.order_filled_date:
                self.order_filled_date = dt_from_ts(
                    safe_value_fallback(order, "lastTradeTimestamp", default_value=dt_ts())
                )
# REMOVED_UNUSED_CODE:         self.order_update_date = datetime.now(timezone.utc)

# REMOVED_UNUSED_CODE:     def to_ccxt_object(self, stopPriceName: str = "stopPrice") -> dict[str, Any]:
# REMOVED_UNUSED_CODE:         order: dict[str, Any] = {
# REMOVED_UNUSED_CODE:             "id": self.order_id,
# REMOVED_UNUSED_CODE:             "symbol": self.ft_pair,
# REMOVED_UNUSED_CODE:             "price": self.price,
# REMOVED_UNUSED_CODE:             "average": self.average,
# REMOVED_UNUSED_CODE:             "amount": self.amount,
# REMOVED_UNUSED_CODE:             "cost": self.cost,
# REMOVED_UNUSED_CODE:             "type": self.order_type,
# REMOVED_UNUSED_CODE:             "side": self.ft_order_side,
# REMOVED_UNUSED_CODE:             "filled": self.filled,
# REMOVED_UNUSED_CODE:             "remaining": self.remaining,
# REMOVED_UNUSED_CODE:             "datetime": self.order_date_utc.strftime("%Y-%m-%dT%H:%M:%S.%f"),
# REMOVED_UNUSED_CODE:             "timestamp": int(self.order_date_utc.timestamp() * 1000),
# REMOVED_UNUSED_CODE:             "status": self.status,
# REMOVED_UNUSED_CODE:             "fee": None,
# REMOVED_UNUSED_CODE:             "info": {},
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE:         if self.ft_order_side == "stoploss":
# REMOVED_UNUSED_CODE:             order.update(
# REMOVED_UNUSED_CODE:                 {
# REMOVED_UNUSED_CODE:                     stopPriceName: self.stop_price,
# REMOVED_UNUSED_CODE:                     "ft_order_type": "stoploss",
# REMOVED_UNUSED_CODE:                 }
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return order

    def to_json(self, entry_side: str, minified: bool = False) -> dict[str, Any]:
        """
        :param minified: If True, only return a subset of the data is returned.
                         Only used for backtesting.
        """
        resp = {
            "amount": self.safe_amount,
            "safe_price": self.safe_price,
            "ft_order_side": self.ft_order_side,
            "order_filled_timestamp": dt_ts_none(self.order_filled_utc),
            "ft_is_entry": self.ft_order_side == entry_side,
            "ft_order_tag": self.ft_order_tag,
            "cost": self.cost if self.cost else 0,
        }
        if not minified:
            resp.update(
                {
                    "pair": self.ft_pair,
                    "order_id": self.order_id,
                    "status": self.status,
                    "average": round(self.average, 8) if self.average else 0,
                    "filled": self.filled,
                    "is_open": self.ft_is_open,
                    "order_date": (
                        self.order_date.strftime(DATETIME_PRINT_FORMAT) if self.order_date else None
                    ),
                    "order_timestamp": (
                        int(self.order_date.replace(tzinfo=timezone.utc).timestamp() * 1000)
                        if self.order_date
                        else None
                    ),
                    "order_filled_date": (
                        self.order_filled_date.strftime(DATETIME_PRINT_FORMAT)
                        if self.order_filled_date
                        else None
                    ),
                    "order_type": self.order_type,
                    "price": self.price,
                    "remaining": self.remaining,
                    "ft_fee_base": self.ft_fee_base,
                    "funding_fee": self.funding_fee,
                }
            )
        return resp

# REMOVED_UNUSED_CODE:     def close_bt_order(self, close_date: datetime, trade: "LocalTrade"):
# REMOVED_UNUSED_CODE:         self.order_filled_date = close_date
# REMOVED_UNUSED_CODE:         self.filled = self.amount
# REMOVED_UNUSED_CODE:         self.remaining = 0
# REMOVED_UNUSED_CODE:         self.status = "closed"
# REMOVED_UNUSED_CODE:         self.ft_is_open = False
# REMOVED_UNUSED_CODE:         # Assign funding fees to Order.
# REMOVED_UNUSED_CODE:         # Assumes backtesting will use date_last_filled_utc to calculate future funding fees.
# REMOVED_UNUSED_CODE:         self.funding_fee = trade.funding_fee_running
# REMOVED_UNUSED_CODE:         trade.funding_fee_running = 0.0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.ft_order_side == trade.entry_side and self.price:
# REMOVED_UNUSED_CODE:             trade.open_rate = self.price
# REMOVED_UNUSED_CODE:             trade.recalc_trade_from_orders()
# REMOVED_UNUSED_CODE:             if trade.nr_of_successful_entries == 1:
# REMOVED_UNUSED_CODE:                 trade.initial_stop_loss_pct = None
# REMOVED_UNUSED_CODE:                 trade.is_stop_loss_trailing = False
# REMOVED_UNUSED_CODE:             trade.adjust_stop_loss(trade.open_rate, trade.stop_loss_pct)

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def update_orders(orders: list["Order"], order: CcxtOrder):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Get all non-closed orders - useful when trying to batch-update orders
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if not isinstance(order, dict):
# REMOVED_UNUSED_CODE:             logger.warning(f"{order} is not a valid response object.")
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         filtered_orders = [o for o in orders if o.order_id == order.get("id")]
# REMOVED_UNUSED_CODE:         if filtered_orders:
# REMOVED_UNUSED_CODE:             oobj = filtered_orders[0]
# REMOVED_UNUSED_CODE:             oobj.update_from_ccxt_object(order)
# REMOVED_UNUSED_CODE:             Trade.commit()
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             logger.warning(f"Did not find order for {order}.")

# REMOVED_UNUSED_CODE:     @classmethod
# REMOVED_UNUSED_CODE:     def parse_from_ccxt_object(
# REMOVED_UNUSED_CODE:         cls,
# REMOVED_UNUSED_CODE:         order: CcxtOrder,
# REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE:         side: str,
# REMOVED_UNUSED_CODE:         amount: float | None = None,
# REMOVED_UNUSED_CODE:         price: float | None = None,
# REMOVED_UNUSED_CODE:     ) -> Self:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Parse an order from a ccxt object and return a new order Object.
# REMOVED_UNUSED_CODE:         Optional support for overriding amount and price is only used for test simplification.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         o = cls(
# REMOVED_UNUSED_CODE:             order_id=str(order["id"]),
# REMOVED_UNUSED_CODE:             ft_order_side=side,
# REMOVED_UNUSED_CODE:             ft_pair=pair,
# REMOVED_UNUSED_CODE:             ft_amount=amount or order.get("amount", None) or 0.0,
# REMOVED_UNUSED_CODE:             ft_price=price or order.get("price", None),
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         o.update_from_ccxt_object(order)
# REMOVED_UNUSED_CODE:         return o

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def get_open_orders() -> Sequence["Order"]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Retrieve open orders from the database
# REMOVED_UNUSED_CODE:         :return: List of open orders
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return Order.session.scalars(select(Order).filter(Order.ft_is_open.is_(True))).all()

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def order_by_id(order_id: str) -> Optional["Order"]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Retrieve order based on order_id
# REMOVED_UNUSED_CODE:         :return: Order or None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return Order.session.scalars(select(Order).filter(Order.order_id == order_id)).first()


class LocalTrade:
    """
    Trade database model.
    Used in backtesting - must be aligned to Trade model!
    """

    use_db: bool = False
    # Trades container for backtesting
    bt_trades: list["LocalTrade"] = []
    bt_trades_open: list["LocalTrade"] = []
    # Copy of trades_open - but indexed by pair
# REMOVED_UNUSED_CODE:     bt_trades_open_pp: dict[str, list["LocalTrade"]] = defaultdict(list)
# REMOVED_UNUSED_CODE:     bt_open_open_trade_count: int = 0
# REMOVED_UNUSED_CODE:     bt_total_profit: float = 0
    realized_profit: float = 0

    id: int = 0

    orders: list[Order] = []

    exchange: str = ""
    pair: str = ""
    base_currency: str | None = ""
    stake_currency: str | None = ""
    is_open: bool = True
    fee_open: float = 0.0
    fee_open_cost: float | None = None
    fee_open_currency: str | None = ""
    fee_close: float | None = 0.0
    fee_close_cost: float | None = None
    fee_close_currency: str | None = ""
    open_rate: float = 0.0
    open_rate_requested: float | None = None
    # open_trade_value - calculated via _calc_open_trade_value
    open_trade_value: float = 0.0
    close_rate: float | None = None
    close_rate_requested: float | None = None
    close_profit: float | None = None
    close_profit_abs: float | None = None
    stake_amount: float = 0.0
    max_stake_amount: float | None = 0.0
    amount: float = 0.0
    amount_requested: float | None = None
    open_date: datetime
    close_date: datetime | None = None
    # absolute value of the stop loss
    stop_loss: float = 0.0
    # percentage value of the stop loss
    stop_loss_pct: float | None = 0.0
    # absolute value of the initial stop loss
    initial_stop_loss: float | None = 0.0
    # percentage value of the initial stop loss
    initial_stop_loss_pct: float | None = None
# REMOVED_UNUSED_CODE:     is_stop_loss_trailing: bool = False
    # absolute value of the highest reached price
    max_rate: float | None = None
    # Lowest price reached
    min_rate: float | None = None
    exit_reason: str | None = ""
    exit_order_status: str | None = ""
    strategy: str | None = ""
    enter_tag: str | None = None
    timeframe: int | None = None

    trading_mode: TradingMode = TradingMode.SPOT
    amount_precision: float | None = None
    price_precision: float | None = None
    precision_mode: int | None = None
    precision_mode_price: int | None = None
    contract_size: float | None = None

    # Leverage trading properties
    liquidation_price: float | None = None
    is_short: bool = False
    leverage: float = 1.0

    # Margin trading properties
    interest_rate: float = 0.0

    # Futures properties
    funding_fees: float | None = None
    # Used to keep running funding fees - between the last filled order and now
    # Shall not be used for calculations!
# REMOVED_UNUSED_CODE:     funding_fee_running: float | None = None

# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def stoploss_or_liquidation(self) -> float:
# REMOVED_UNUSED_CODE:         if self.liquidation_price:
# REMOVED_UNUSED_CODE:             if self.is_short:
# REMOVED_UNUSED_CODE:                 return min(self.stop_loss, self.liquidation_price)
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 return max(self.stop_loss, self.liquidation_price)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return self.stop_loss

# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def buy_tag(self) -> str | None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Compatibility between buy_tag (old) and enter_tag (new)
# REMOVED_UNUSED_CODE:         Consider buy_tag deprecated
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return self.enter_tag

    @property
    def has_no_leverage(self) -> bool:
        """Returns true if this is a non-leverage, non-short trade"""
        return (self.leverage == 1.0 or self.leverage is None) and not self.is_short

    @property
    def borrowed(self) -> float:
        """
        The amount of currency borrowed from the exchange for leverage trades
        If a long trade, the amount is in base currency
        If a short trade, the amount is in the other currency being traded
        """
        if self.has_no_leverage:
            return 0.0
        elif not self.is_short:
            return (self.amount * self.open_rate) * ((self.leverage - 1) / self.leverage)
        else:
            return self.amount

# REMOVED_UNUSED_CODE:     @property
    def _date_last_filled_utc(self) -> datetime | None:
        """Date of the last filled order"""
        orders = self.select_filled_orders()
        if orders:
            return max(o.order_filled_utc for o in orders if o.order_filled_utc)
        return None

# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def date_last_filled_utc(self) -> datetime:
# REMOVED_UNUSED_CODE:         """Date of the last filled order - or open_date if no orders are filled"""
# REMOVED_UNUSED_CODE:         dt_last_filled = self._date_last_filled_utc
# REMOVED_UNUSED_CODE:         if not dt_last_filled:
# REMOVED_UNUSED_CODE:             return self.open_date_utc
# REMOVED_UNUSED_CODE:         return max([self.open_date_utc, dt_last_filled])

    @property
    def date_entry_fill_utc(self) -> datetime | None:
        """Date of the first filled order"""
        orders = self.select_filled_orders(self.entry_side)
        if orders and len(
            filled_date := [o.order_filled_utc for o in orders if o.order_filled_utc]
        ):
            return min(filled_date)
        return None

    @property
    def open_date_utc(self):
        return self.open_date.replace(tzinfo=timezone.utc)

    @property
    def stoploss_last_update_utc(self):
        if self.has_open_sl_orders:
            return max(o.order_date_utc for o in self.open_sl_orders)
        return None

    @property
    def close_date_utc(self):
        return self.close_date.replace(tzinfo=timezone.utc) if self.close_date else None

    @property
    def entry_side(self) -> str:
        if self.is_short:
            return "sell"
        else:
            return "buy"

    @property
    def exit_side(self) -> BuySell:
        if self.is_short:
            return "buy"
        else:
            return "sell"

# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def trade_direction(self) -> LongShort:
# REMOVED_UNUSED_CODE:         if self.is_short:
# REMOVED_UNUSED_CODE:             return "short"
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             return "long"

    @property
    def safe_base_currency(self) -> str:
        """
        Compatibility layer for asset - which can be empty for old trades.
        """
        try:
            return self.base_currency or self.pair.split("/")[0]
        except IndexError:
            return ""

    @property
    def safe_quote_currency(self) -> str:
        """
        Compatibility layer for asset - which can be empty for old trades.
        """
        try:
            return self.stake_currency or self.pair.split("/")[1].split(":")[0]
        except IndexError:
            return ""

# REMOVED_UNUSED_CODE:     @property
    def open_orders(self) -> list[Order]:
        """
        All open orders for this trade excluding stoploss orders
        """
        return [o for o in self.orders if o.ft_is_open and o.ft_order_side != "stoploss"]

    @property
    def has_open_orders(self) -> bool:
        """
        True if there are open orders for this trade excluding stoploss orders
        """
        open_orders_wo_sl = [
            o for o in self.orders if o.ft_order_side not in ["stoploss"] and o.ft_is_open
        ]
        return len(open_orders_wo_sl) > 0

# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def has_open_position(self) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         True if there is an open position for this trade
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return self.amount > 0

    @property
    def open_sl_orders(self) -> list[Order]:
        """
        All open stoploss orders for this trade
        """
        return [o for o in self.orders if o.ft_order_side in ["stoploss"] and o.ft_is_open]

    @property
    def has_open_sl_orders(self) -> bool:
        """
        True if there are open stoploss orders for this trade
        """
        open_sl_orders = [
            o for o in self.orders if o.ft_order_side in ["stoploss"] and o.ft_is_open
        ]
        return len(open_sl_orders) > 0

# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def sl_orders(self) -> list[Order]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         All stoploss orders for this trade
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return [o for o in self.orders if o.ft_order_side in ["stoploss"]]

# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def open_orders_ids(self) -> list[str]:
# REMOVED_UNUSED_CODE:         open_orders_ids_wo_sl = [
# REMOVED_UNUSED_CODE:             oo.order_id for oo in self.open_orders if oo.ft_order_side not in ["stoploss"]
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE:         return open_orders_ids_wo_sl

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
        self.recalc_open_trade_value()
        self.orders = []
        if self.trading_mode == TradingMode.MARGIN and self.interest_rate is None:
            raise OperationalException(
                f"{self.trading_mode} trading requires param interest_rate on trades"
            )

    def __repr__(self):
        open_since = (
            self.open_date_utc.strftime(DATETIME_PRINT_FORMAT) if self.is_open else "closed"
        )

        return (
            f"Trade(id={self.id}, pair={self.pair}, amount={self.amount:.8f}, "
            f"is_short={self.is_short or False}, leverage={self.leverage or 1.0}, "
            f"open_rate={self.open_rate:.8f}, open_since={open_since})"
        )

    def to_json(self, minified: bool = False) -> dict[str, Any]:
        """
        :param minified: If True, only return a subset of the data is returned.
                         Only used for backtesting.
        :return: Dictionary with trade data
        """
        filled_or_open_orders = self.select_filled_or_open_orders()
        orders_json = [order.to_json(self.entry_side, minified) for order in filled_or_open_orders]

        return {
            "trade_id": self.id,
            "pair": self.pair,
            "base_currency": self.safe_base_currency,
            "quote_currency": self.safe_quote_currency,
            "is_open": self.is_open,
            "exchange": self.exchange,
            "amount": round(self.amount, 8),
            "amount_requested": round(self.amount_requested, 8) if self.amount_requested else None,
            "stake_amount": round(self.stake_amount, 8),
            "max_stake_amount": round(self.max_stake_amount, 8) if self.max_stake_amount else None,
            "strategy": self.strategy,
            "enter_tag": self.enter_tag,
            "timeframe": self.timeframe,
            "fee_open": self.fee_open,
            "fee_open_cost": self.fee_open_cost,
            "fee_open_currency": self.fee_open_currency,
            "fee_close": self.fee_close,
            "fee_close_cost": self.fee_close_cost,
            "fee_close_currency": self.fee_close_currency,
            "open_date": self.open_date.strftime(DATETIME_PRINT_FORMAT),
            "open_timestamp": dt_ts_none(self.open_date_utc),
            "open_fill_date": (
                self.date_entry_fill_utc.strftime(DATETIME_PRINT_FORMAT)
                if self.date_entry_fill_utc
                else None
            ),
            "open_fill_timestamp": dt_ts_none(self.date_entry_fill_utc),
            "open_rate": self.open_rate,
            "open_rate_requested": self.open_rate_requested,
            "open_trade_value": round(self.open_trade_value, 8),
            "close_date": (
                self.close_date.strftime(DATETIME_PRINT_FORMAT) if self.close_date else None
            ),
            "close_timestamp": dt_ts_none(self.close_date_utc),
            "realized_profit": self.realized_profit or 0.0,
            # Close-profit corresponds to relative realized_profit ratio
            "realized_profit_ratio": self.close_profit or None,
            "close_rate": self.close_rate,
            "close_rate_requested": self.close_rate_requested,
            "close_profit": self.close_profit,  # Deprecated
            "close_profit_pct": round(self.close_profit * 100, 2) if self.close_profit else None,
            "close_profit_abs": self.close_profit_abs,  # Deprecated
            "trade_duration_s": (
                int((self.close_date_utc - self.open_date_utc).total_seconds())
                if self.close_date
                else None
            ),
            "trade_duration": (
                int((self.close_date_utc - self.open_date_utc).total_seconds() // 60)
                if self.close_date
                else None
            ),
            "profit_ratio": self.close_profit,
            "profit_pct": round(self.close_profit * 100, 2) if self.close_profit else None,
            "profit_abs": self.close_profit_abs,
            "exit_reason": self.exit_reason,
            "exit_order_status": self.exit_order_status,
            "stop_loss_abs": self.stop_loss,
            "stop_loss_ratio": self.stop_loss_pct if self.stop_loss_pct else None,
            "stop_loss_pct": (self.stop_loss_pct * 100) if self.stop_loss_pct else None,
            "stoploss_last_update": (
                self.stoploss_last_update_utc.strftime(DATETIME_PRINT_FORMAT)
                if self.stoploss_last_update_utc
                else None
            ),
            "stoploss_last_update_timestamp": dt_ts_none(self.stoploss_last_update_utc),
            "initial_stop_loss_abs": self.initial_stop_loss,
            "initial_stop_loss_ratio": (
                self.initial_stop_loss_pct if self.initial_stop_loss_pct else None
            ),
            "initial_stop_loss_pct": (
                self.initial_stop_loss_pct * 100 if self.initial_stop_loss_pct else None
            ),
            "min_rate": self.min_rate,
            "max_rate": self.max_rate,
            "leverage": self.leverage,
            "interest_rate": self.interest_rate,
            "liquidation_price": self.liquidation_price,
            "is_short": self.is_short,
            "trading_mode": self.trading_mode,
            "funding_fees": self.funding_fees,
            "amount_precision": self.amount_precision,
            "price_precision": self.price_precision,
            "precision_mode": self.precision_mode,
            "precision_mode_price": self.precision_mode_price,
            "contract_size": self.contract_size,
            "has_open_orders": self.has_open_orders,
            "orders": orders_json,
        }

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def reset_trades() -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Resets all trades. Only active for backtesting mode.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         LocalTrade.bt_trades = []
# REMOVED_UNUSED_CODE:         LocalTrade.bt_trades_open = []
# REMOVED_UNUSED_CODE:         LocalTrade.bt_trades_open_pp = defaultdict(list)
# REMOVED_UNUSED_CODE:         LocalTrade.bt_open_open_trade_count = 0
# REMOVED_UNUSED_CODE:         LocalTrade.bt_total_profit = 0

# REMOVED_UNUSED_CODE:     def adjust_min_max_rates(self, current_price: float, current_price_low: float) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Adjust the max_rate and min_rate.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self.max_rate = max(current_price, self.max_rate or self.open_rate)
# REMOVED_UNUSED_CODE:         self.min_rate = min(current_price_low, self.min_rate or self.open_rate)

# REMOVED_UNUSED_CODE:     def set_liquidation_price(self, liquidation_price: float | None):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Method you should use to set self.liquidation price.
# REMOVED_UNUSED_CODE:         Assures stop_loss is not passed the liquidation price
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if liquidation_price is None:
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE:         self.liquidation_price = price_to_precision(
# REMOVED_UNUSED_CODE:             liquidation_price, self.price_precision, self.precision_mode_price
# REMOVED_UNUSED_CODE:         )

# REMOVED_UNUSED_CODE:     def set_funding_fees(self, funding_fee: float) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Assign funding fees to Trade.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if funding_fee is None:
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE:         self.funding_fee_running = funding_fee
# REMOVED_UNUSED_CODE:         prior_funding_fees = sum([o.funding_fee for o in self.orders if o.funding_fee])
# REMOVED_UNUSED_CODE:         self.funding_fees = prior_funding_fees + funding_fee

    def __set_stop_loss(self, stop_loss: float, percent: float):
        """
        Method used internally to set self.stop_loss.
        """
        if not self.stop_loss:
            self.initial_stop_loss = stop_loss
        self.stop_loss = stop_loss

        self.stop_loss_pct = -1 * abs(percent)

    def adjust_stop_loss(
        self,
        current_price: float,
        stoploss: float | None,
        initial: bool = False,
        allow_refresh: bool = False,
    ) -> None:
        """
        This adjusts the stop loss to it's most recently observed setting
        :param current_price: Current rate the asset is traded
        :param stoploss: Stoploss as factor (sample -0.05 -> -5% below current price).
        :param initial: Called to initiate stop_loss.
            Skips everything if self.stop_loss is already set.
        :param refresh: Called to refresh stop_loss, allows adjustment in both directions
        """
        if stoploss is None or (initial and not (self.stop_loss is None or self.stop_loss == 0)):
            # Don't modify if called with initial and nothing to do
            return

        leverage = self.leverage or 1.0
        if self.is_short:
            new_loss = float(current_price * (1 + abs(stoploss / leverage)))
        else:
            new_loss = float(current_price * (1 - abs(stoploss / leverage)))

        stop_loss_norm = price_to_precision(
            new_loss,
            self.price_precision,
            self.precision_mode_price,
            rounding_mode=ROUND_DOWN if self.is_short else ROUND_UP,
        )
        # no stop loss assigned yet
        if self.initial_stop_loss_pct is None:
            self.__set_stop_loss(stop_loss_norm, stoploss)
            self.initial_stop_loss = price_to_precision(
                stop_loss_norm,
                self.price_precision,
                self.precision_mode_price,
                rounding_mode=ROUND_DOWN if self.is_short else ROUND_UP,
            )
            self.initial_stop_loss_pct = -1 * abs(stoploss)

        # evaluate if the stop loss needs to be updated
        else:
            higher_stop = stop_loss_norm > self.stop_loss
            lower_stop = stop_loss_norm < self.stop_loss

            # stop losses only walk up, never down!,
            #   ? But adding more to a leveraged trade would create a lower liquidation price,
            #   ? decreasing the minimum stoploss
            if (
                allow_refresh
                or (higher_stop and not self.is_short)
                or (lower_stop and self.is_short)
            ):
                logger.debug(f"{self.pair} - Adjusting stoploss...")
                if not allow_refresh:
# REMOVED_UNUSED_CODE:                     self.is_stop_loss_trailing = True
                self.__set_stop_loss(stop_loss_norm, stoploss)
            else:
                logger.debug(f"{self.pair} - Keeping current stoploss...")

        logger.debug(
            f"{self.pair} - Stoploss adjusted. current_price={current_price:.8f}, "
            f"open_rate={self.open_rate:.8f}, max_rate={self.max_rate or self.open_rate:.8f}, "
            f"initial_stop_loss={self.initial_stop_loss:.8f}, "
            f"stop_loss={self.stop_loss:.8f}. "
            f"Trailing stoploss saved us: "
            f"{float(self.stop_loss) - float(self.initial_stop_loss or 0.0):.8f}."
        )

# REMOVED_UNUSED_CODE:     def update_trade(self, order: Order, recalculating: bool = False) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Updates this entity with amount and actual open/close rates.
# REMOVED_UNUSED_CODE:         :param order: order retrieved by exchange.fetch_order()
# REMOVED_UNUSED_CODE:         :return: None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Ignore open and cancelled orders
# REMOVED_UNUSED_CODE:         if order.status == "open" or order.safe_price is None:
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         logger.info(f"Updating trade (id={self.id}) ...")
# REMOVED_UNUSED_CODE:         if order.ft_order_side != "stoploss":
# REMOVED_UNUSED_CODE:             order.funding_fee = self.funding_fee_running
# REMOVED_UNUSED_CODE:             # Reset running funding fees
# REMOVED_UNUSED_CODE:             self.funding_fee_running = 0.0
# REMOVED_UNUSED_CODE:         order_type = order.order_type.upper() if order.order_type else None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if order.ft_order_side == self.entry_side:
# REMOVED_UNUSED_CODE:             # Update open rate and actual amount
# REMOVED_UNUSED_CODE:             self.open_rate = order.safe_price
# REMOVED_UNUSED_CODE:             self.amount = order.safe_amount_after_fee
# REMOVED_UNUSED_CODE:             if self.is_open:
# REMOVED_UNUSED_CODE:                 payment = "SELL" if self.is_short else "BUY"
# REMOVED_UNUSED_CODE:                 logger.info(f"{order_type}_{payment} has been fulfilled for {self}.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             self.recalc_trade_from_orders()
# REMOVED_UNUSED_CODE:         elif order.ft_order_side == self.exit_side:
# REMOVED_UNUSED_CODE:             if self.is_open:
# REMOVED_UNUSED_CODE:                 payment = "BUY" if self.is_short else "SELL"
# REMOVED_UNUSED_CODE:                 # * On margin shorts, you buy a little bit more than the amount (amount + interest)
# REMOVED_UNUSED_CODE:                 logger.info(f"{order_type}_{payment} has been fulfilled for {self}.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         elif order.ft_order_side == "stoploss" and order.status not in ("open",):
# REMOVED_UNUSED_CODE:             self.close_rate_requested = self.stop_loss
# REMOVED_UNUSED_CODE:             self.exit_reason = ExitType.STOPLOSS_ON_EXCHANGE.value
# REMOVED_UNUSED_CODE:             if self.is_open and order.safe_filled > 0:
# REMOVED_UNUSED_CODE:                 logger.info(f"{order_type} is hit for {self}.")
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             raise ValueError(f"Unknown order type: {order.order_type}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if order.ft_order_side != self.entry_side:
# REMOVED_UNUSED_CODE:             amount_tr = amount_to_contract_precision(
# REMOVED_UNUSED_CODE:                 self.amount, self.amount_precision, self.precision_mode, self.contract_size
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             if isclose(order.safe_amount_after_fee, amount_tr, abs_tol=MATH_CLOSE_PREC) or (
# REMOVED_UNUSED_CODE:                 not recalculating and order.safe_amount_after_fee > amount_tr
# REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE:                 # When recalculating a trade, only coming out to 0 can force a close
# REMOVED_UNUSED_CODE:                 self.close(order.safe_price)
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 self.recalc_trade_from_orders()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         Trade.commit()

# REMOVED_UNUSED_CODE:     def close(self, rate: float, *, show_msg: bool = True) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Sets close_rate to the given rate, calculates total profit
# REMOVED_UNUSED_CODE:         and marks trade as closed
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self.close_rate = rate
# REMOVED_UNUSED_CODE:         self.close_date = self.close_date or self._date_last_filled_utc or dt_now()
# REMOVED_UNUSED_CODE:         self.is_open = False
# REMOVED_UNUSED_CODE:         self.exit_order_status = "closed"
# REMOVED_UNUSED_CODE:         self.recalc_trade_from_orders(is_closing=True)
# REMOVED_UNUSED_CODE:         if show_msg:
# REMOVED_UNUSED_CODE:             logger.info(
# REMOVED_UNUSED_CODE:                 f"Marking {self} as closed as the trade is fulfilled "
# REMOVED_UNUSED_CODE:                 "and found no open orders for it."
# REMOVED_UNUSED_CODE:             )

# REMOVED_UNUSED_CODE:     def update_fee(
# REMOVED_UNUSED_CODE:         self, fee_cost: float, fee_currency: str | None, fee_rate: float | None, side: str
# REMOVED_UNUSED_CODE:     ) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Update Fee parameters. Only acts once per side
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if self.entry_side == side and self.fee_open_currency is None:
# REMOVED_UNUSED_CODE:             self.fee_open_cost = fee_cost
# REMOVED_UNUSED_CODE:             self.fee_open_currency = fee_currency
# REMOVED_UNUSED_CODE:             if fee_rate is not None:
# REMOVED_UNUSED_CODE:                 self.fee_open = fee_rate
# REMOVED_UNUSED_CODE:                 # Assume close-fee will fall into the same fee category and take an educated guess
# REMOVED_UNUSED_CODE:                 self.fee_close = fee_rate
# REMOVED_UNUSED_CODE:         elif self.exit_side == side and self.fee_close_currency is None:
# REMOVED_UNUSED_CODE:             self.fee_close_cost = fee_cost
# REMOVED_UNUSED_CODE:             self.fee_close_currency = fee_currency
# REMOVED_UNUSED_CODE:             if fee_rate is not None:
# REMOVED_UNUSED_CODE:                 self.fee_close = fee_rate

# REMOVED_UNUSED_CODE:     def fee_updated(self, side: str) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Verify if this side (buy / sell) has already been updated
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if self.entry_side == side:
# REMOVED_UNUSED_CODE:             return self.fee_open_currency is not None
# REMOVED_UNUSED_CODE:         elif self.exit_side == side:
# REMOVED_UNUSED_CODE:             return self.fee_close_currency is not None
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             return False

# REMOVED_UNUSED_CODE:     def update_order(self, order: CcxtOrder) -> None:
# REMOVED_UNUSED_CODE:         Order.update_orders(self.orders, order)

# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def fully_canceled_entry_order_count(self) -> int:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Get amount of failed exiting orders
# REMOVED_UNUSED_CODE:         assumes full exits.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return len(
# REMOVED_UNUSED_CODE:             [
# REMOVED_UNUSED_CODE:                 o
# REMOVED_UNUSED_CODE:                 for o in self.orders
# REMOVED_UNUSED_CODE:                 if o.ft_order_side == self.entry_side
# REMOVED_UNUSED_CODE:                 and o.status in CANCELED_EXCHANGE_STATES
# REMOVED_UNUSED_CODE:                 and o.filled == 0
# REMOVED_UNUSED_CODE:             ]
# REMOVED_UNUSED_CODE:         )

# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def canceled_exit_order_count(self) -> int:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Get amount of failed exiting orders
# REMOVED_UNUSED_CODE:         assumes full exits.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return len(
# REMOVED_UNUSED_CODE:             [
# REMOVED_UNUSED_CODE:                 o
# REMOVED_UNUSED_CODE:                 for o in self.orders
# REMOVED_UNUSED_CODE:                 if o.ft_order_side == self.exit_side and o.status in CANCELED_EXCHANGE_STATES
# REMOVED_UNUSED_CODE:             ]
# REMOVED_UNUSED_CODE:         )

# REMOVED_UNUSED_CODE:     def get_canceled_exit_order_count(self) -> int:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Get amount of failed exiting orders
# REMOVED_UNUSED_CODE:         assumes full exits.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return self.canceled_exit_order_count

    def _calc_open_trade_value(self, amount: float, open_rate: float) -> float:
        """
        Calculate the open_rate including open_fee.
        :return: Price in of the open trade incl. Fees
        """
        open_trade = FtPrecise(amount) * FtPrecise(open_rate)
        fees = open_trade * FtPrecise(self.fee_open)
        if self.is_short:
            return float(open_trade - fees)
        else:
            return float(open_trade + fees)

    def recalc_open_trade_value(self) -> None:
        """
        Recalculate open_trade_value.
        Must be called whenever open_rate, fee_open is changed.
        """
        self.open_trade_value = self._calc_open_trade_value(self.amount, self.open_rate)

    def calculate_interest(self) -> FtPrecise:
        """
        Calculate interest for this trade. Only applicable for Margin trading.
        """
        zero = FtPrecise(0.0)
        # If nothing was borrowed
        if self.trading_mode != TradingMode.MARGIN or self.has_no_leverage:
            return zero

        open_date = self.open_date.replace(tzinfo=None)
        now = (self.close_date or datetime.now(timezone.utc)).replace(tzinfo=None)
        sec_per_hour = FtPrecise(3600)
        total_seconds = FtPrecise((now - open_date).total_seconds())
        hours = total_seconds / sec_per_hour or zero

        rate = FtPrecise(self.interest_rate)
        borrowed = FtPrecise(self.borrowed)

        return interest(exchange_name=self.exchange, borrowed=borrowed, rate=rate, hours=hours)

    def _calc_base_close(self, amount: FtPrecise, rate: float, fee: float | None) -> FtPrecise:
        close_trade = amount * FtPrecise(rate)
        fees = close_trade * FtPrecise(fee or 0.0)

        if self.is_short:
            return close_trade + fees
        else:
            return close_trade - fees

    def calc_close_trade_value(self, rate: float, amount: float | None = None) -> float:
        """
        Calculate the Trade's close value including fees
        :param rate: rate to compare with.
        :return: value in stake currency of the open trade
        """
        if rate is None and not self.close_rate:
            return 0.0

        amount1 = FtPrecise(amount or self.amount)
        trading_mode = self.trading_mode or TradingMode.SPOT

        if trading_mode == TradingMode.SPOT:
            return float(self._calc_base_close(amount1, rate, self.fee_close))

        elif trading_mode == TradingMode.MARGIN:
            total_interest = self.calculate_interest()

            if self.is_short:
                amount1 = amount1 + total_interest
                return float(self._calc_base_close(amount1, rate, self.fee_close))
            else:
                # Currency already owned for longs, no need to purchase
                return float(self._calc_base_close(amount1, rate, self.fee_close) - total_interest)

        elif trading_mode == TradingMode.FUTURES:
            funding_fees = self.funding_fees or 0.0
            # Positive funding_fees -> Trade has gained from fees.
            # Negative funding_fees -> Trade had to pay the fees.
            if self.is_short:
                return float(self._calc_base_close(amount1, rate, self.fee_close)) - funding_fees
            else:
                return float(self._calc_base_close(amount1, rate, self.fee_close)) + funding_fees
        else:
            raise OperationalException(
                f"{self.trading_mode} trading is not yet available using freqtrade"
            )

# REMOVED_UNUSED_CODE:     def calc_profit(
# REMOVED_UNUSED_CODE:         self, rate: float, amount: float | None = None, open_rate: float | None = None
# REMOVED_UNUSED_CODE:     ) -> float:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Calculate the absolute profit in stake currency between Close and Open trade
# REMOVED_UNUSED_CODE:         Deprecated - only available for backwards compatibility
# REMOVED_UNUSED_CODE:         :param rate: close rate to compare with.
# REMOVED_UNUSED_CODE:         :param amount: Amount to use for the calculation. Falls back to trade.amount if not set.
# REMOVED_UNUSED_CODE:         :param open_rate: open_rate to use. Defaults to self.open_rate if not provided.
# REMOVED_UNUSED_CODE:         :return: profit in stake currency as float
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         prof = self.calculate_profit(rate, amount, open_rate)
# REMOVED_UNUSED_CODE:         return prof.profit_abs

    def calculate_profit(
        self, rate: float, amount: float | None = None, open_rate: float | None = None
    ) -> ProfitStruct:
        """
        Calculate profit metrics (absolute, ratio, total, total ratio).
        All calculations include fees.
        :param rate: close rate to compare with.
        :param amount: Amount to use for the calculation. Falls back to trade.amount if not set.
        :param open_rate: open_rate to use. Defaults to self.open_rate if not provided.
        :return: Profit structure, containing absolute and relative profits.
        """

        close_trade_value = self.calc_close_trade_value(rate, amount)
        if amount is None or open_rate is None:
            open_trade_value = self.open_trade_value
        else:
            open_trade_value = self._calc_open_trade_value(amount, open_rate)

        if self.is_short:
            profit_abs = open_trade_value - close_trade_value
        else:
            profit_abs = close_trade_value - open_trade_value

        try:
            if self.is_short:
                profit_ratio = (1 - (close_trade_value / open_trade_value)) * self.leverage
            else:
                profit_ratio = ((close_trade_value / open_trade_value) - 1) * self.leverage
            profit_ratio = float(f"{profit_ratio:.8f}")
        except ZeroDivisionError:
            profit_ratio = 0.0

        total_profit_abs = profit_abs + self.realized_profit
        total_profit_ratio = (
            (total_profit_abs / self.max_stake_amount) * self.leverage
            if self.max_stake_amount
            else 0.0
        )
        total_profit_ratio = float(f"{total_profit_ratio:.8f}")
        profit_abs = float(f"{profit_abs:.8f}")

        return ProfitStruct(
            profit_abs=profit_abs,
            profit_ratio=profit_ratio,
            total_profit=profit_abs + self.realized_profit,
            total_profit_ratio=total_profit_ratio,
        )

# REMOVED_UNUSED_CODE:     def calc_profit_ratio(
# REMOVED_UNUSED_CODE:         self, rate: float, amount: float | None = None, open_rate: float | None = None
# REMOVED_UNUSED_CODE:     ) -> float:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Calculates the profit as ratio (including fee).
# REMOVED_UNUSED_CODE:         :param rate: rate to compare with.
# REMOVED_UNUSED_CODE:         :param amount: Amount to use for the calculation. Falls back to trade.amount if not set.
# REMOVED_UNUSED_CODE:         :param open_rate: open_rate to use. Defaults to self.open_rate if not provided.
# REMOVED_UNUSED_CODE:         :return: profit ratio as float
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         close_trade_value = self.calc_close_trade_value(rate, amount)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if amount is None or open_rate is None:
# REMOVED_UNUSED_CODE:             open_trade_value = self.open_trade_value
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             open_trade_value = self._calc_open_trade_value(amount, open_rate)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if open_trade_value == 0.0:
# REMOVED_UNUSED_CODE:             return 0.0
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             if self.is_short:
# REMOVED_UNUSED_CODE:                 profit_ratio = (1 - (close_trade_value / open_trade_value)) * self.leverage
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 profit_ratio = ((close_trade_value / open_trade_value) - 1) * self.leverage
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return float(f"{profit_ratio:.8f}")

# REMOVED_UNUSED_CODE:     def recalc_trade_from_orders(self, *, is_closing: bool = False):
# REMOVED_UNUSED_CODE:         ZERO = FtPrecise(0.0)
# REMOVED_UNUSED_CODE:         current_amount = FtPrecise(0.0)
# REMOVED_UNUSED_CODE:         current_stake = FtPrecise(0.0)
# REMOVED_UNUSED_CODE:         max_stake_amount = FtPrecise(0.0)
# REMOVED_UNUSED_CODE:         total_stake = 0.0  # Total stake after all buy orders (does not subtract!)
# REMOVED_UNUSED_CODE:         avg_price = FtPrecise(0.0)
# REMOVED_UNUSED_CODE:         close_profit = 0.0
# REMOVED_UNUSED_CODE:         close_profit_abs = 0.0
# REMOVED_UNUSED_CODE:         # Reset funding fees
# REMOVED_UNUSED_CODE:         self.funding_fees = 0.0
# REMOVED_UNUSED_CODE:         funding_fees = 0.0
# REMOVED_UNUSED_CODE:         ordercount = len(self.orders) - 1
# REMOVED_UNUSED_CODE:         for i, o in enumerate(self.orders):
# REMOVED_UNUSED_CODE:             if o.ft_is_open or not o.filled:
# REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE:             funding_fees += o.funding_fee or 0.0
# REMOVED_UNUSED_CODE:             tmp_amount = FtPrecise(o.safe_amount_after_fee)
# REMOVED_UNUSED_CODE:             tmp_price = FtPrecise(o.safe_price)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             is_exit = o.ft_order_side != self.entry_side
# REMOVED_UNUSED_CODE:             side = FtPrecise(-1 if is_exit else 1)
# REMOVED_UNUSED_CODE:             if tmp_amount > ZERO and tmp_price is not None:
# REMOVED_UNUSED_CODE:                 current_amount += tmp_amount * side
# REMOVED_UNUSED_CODE:                 price = avg_price if is_exit else tmp_price
# REMOVED_UNUSED_CODE:                 current_stake += price * tmp_amount * side
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 if current_amount > ZERO and not is_exit:
# REMOVED_UNUSED_CODE:                     avg_price = current_stake / current_amount
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if is_exit:
# REMOVED_UNUSED_CODE:                 # Process exits
# REMOVED_UNUSED_CODE:                 if i == ordercount and is_closing:
# REMOVED_UNUSED_CODE:                     # Apply funding fees only to the last closing order
# REMOVED_UNUSED_CODE:                     self.funding_fees = funding_fees
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 exit_rate = o.safe_price
# REMOVED_UNUSED_CODE:                 exit_amount = o.safe_amount_after_fee
# REMOVED_UNUSED_CODE:                 prof = self.calculate_profit(exit_rate, exit_amount, float(avg_price))
# REMOVED_UNUSED_CODE:                 close_profit_abs += prof.profit_abs
# REMOVED_UNUSED_CODE:                 if total_stake > 0:
# REMOVED_UNUSED_CODE:                     # This needs to be calculated based on the last occurring exit to be aligned
# REMOVED_UNUSED_CODE:                     # with realized_profit.
# REMOVED_UNUSED_CODE:                     close_profit = (close_profit_abs / total_stake) * self.leverage
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 total_stake += self._calc_open_trade_value(tmp_amount, price)
# REMOVED_UNUSED_CODE:                 max_stake_amount += tmp_amount * price
# REMOVED_UNUSED_CODE:         self.funding_fees = funding_fees
# REMOVED_UNUSED_CODE:         self.max_stake_amount = float(max_stake_amount)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if close_profit:
# REMOVED_UNUSED_CODE:             self.close_profit = close_profit
# REMOVED_UNUSED_CODE:             self.realized_profit = close_profit_abs
# REMOVED_UNUSED_CODE:             self.close_profit_abs = prof.profit_abs
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         current_amount_tr = amount_to_contract_precision(
# REMOVED_UNUSED_CODE:             float(current_amount), self.amount_precision, self.precision_mode, self.contract_size
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         if current_amount_tr > 0.0:
# REMOVED_UNUSED_CODE:             # Trade is still open
# REMOVED_UNUSED_CODE:             # Leverage not updated, as we don't allow changing leverage through DCA at the moment.
# REMOVED_UNUSED_CODE:             self.open_rate = price_to_precision(
# REMOVED_UNUSED_CODE:                 float(current_stake / current_amount),
# REMOVED_UNUSED_CODE:                 self.price_precision,
# REMOVED_UNUSED_CODE:                 self.precision_mode_price,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             self.amount = current_amount_tr
# REMOVED_UNUSED_CODE:             self.stake_amount = float(current_stake) / (self.leverage or 1.0)
# REMOVED_UNUSED_CODE:             self.fee_open_cost = self.fee_open * float(self.max_stake_amount)
# REMOVED_UNUSED_CODE:             self.recalc_open_trade_value()
# REMOVED_UNUSED_CODE:             if self.stop_loss_pct is not None and self.open_rate is not None:
# REMOVED_UNUSED_CODE:                 self.adjust_stop_loss(self.open_rate, self.stop_loss_pct)
# REMOVED_UNUSED_CODE:         elif is_closing and total_stake > 0:
# REMOVED_UNUSED_CODE:             # Close profit abs / maximum owned
# REMOVED_UNUSED_CODE:             # Fees are considered as they are part of close_profit_abs
# REMOVED_UNUSED_CODE:             self.close_profit = (close_profit_abs / total_stake) * self.leverage
# REMOVED_UNUSED_CODE:             self.close_profit_abs = close_profit_abs

# REMOVED_UNUSED_CODE:     def select_order_by_order_id(self, order_id: str) -> Order | None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Finds order object by Order id.
# REMOVED_UNUSED_CODE:         :param order_id: Exchange order id
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         for o in self.orders:
# REMOVED_UNUSED_CODE:             if o.order_id == order_id:
# REMOVED_UNUSED_CODE:                 return o
# REMOVED_UNUSED_CODE:         return None

# REMOVED_UNUSED_CODE:     def select_order(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         order_side: str | None = None,
# REMOVED_UNUSED_CODE:         is_open: bool | None = None,
# REMOVED_UNUSED_CODE:         only_filled: bool = False,
# REMOVED_UNUSED_CODE:     ) -> Order | None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Finds latest order for this orderside and status
# REMOVED_UNUSED_CODE:         :param order_side: ft_order_side of the order (either 'buy', 'sell' or 'stoploss')
# REMOVED_UNUSED_CODE:         :param is_open: Only search for open orders?
# REMOVED_UNUSED_CODE:         :param only_filled: Only search for Filled orders (only valid with is_open=False).
# REMOVED_UNUSED_CODE:         :return: latest Order object if it exists, else None
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         orders = self.orders
# REMOVED_UNUSED_CODE:         if order_side:
# REMOVED_UNUSED_CODE:             orders = [o for o in orders if o.ft_order_side == order_side]
# REMOVED_UNUSED_CODE:         if is_open is not None:
# REMOVED_UNUSED_CODE:             orders = [o for o in orders if o.ft_is_open == is_open]
# REMOVED_UNUSED_CODE:         if is_open is False and only_filled:
# REMOVED_UNUSED_CODE:             orders = [o for o in orders if o.filled and o.status in NON_OPEN_EXCHANGE_STATES]
# REMOVED_UNUSED_CODE:         if len(orders) > 0:
# REMOVED_UNUSED_CODE:             return orders[-1]
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             return None

    def select_filled_orders(self, order_side: str | None = None) -> list["Order"]:
        """
        Finds filled orders for this order side.
        Will not return open orders which already partially filled.
        :param order_side: Side of the order (either 'buy', 'sell', or None)
        :return: array of Order objects
        """
        return [
            o
            for o in self.orders
            if ((o.ft_order_side == order_side) or (order_side is None))
            and o.ft_is_open is False
            and o.filled
            and o.status in NON_OPEN_EXCHANGE_STATES
        ]

    def select_filled_or_open_orders(self) -> list["Order"]:
        """
        Finds filled or open orders
        :param order_side: Side of the order (either 'buy', 'sell', or None)
        :return: array of Order objects
        """
        return [
            o
            for o in self.orders
            if (
                o.ft_is_open is False
                and (o.filled or 0) > 0
                and o.status in NON_OPEN_EXCHANGE_STATES
            )
            or (o.ft_is_open is True and o.status is not None)
        ]

    def set_custom_data(self, key: str, value: Any) -> None:
        """
        Set custom data for this trade
        :param key: key of the custom data
        :param value: value of the custom data (must be JSON serializable)
        """
        CustomDataWrapper.set_custom_data(trade_id=self.id, key=key, value=value)

    def get_custom_data(self, key: str, default: Any = None) -> Any:
        """
        Get custom data for this trade
        :param key: key of the custom data
        """
        data = CustomDataWrapper.get_custom_data(trade_id=self.id, key=key)
        if data:
            return data[0].value
        return default

# REMOVED_UNUSED_CODE:     def get_custom_data_entry(self, key: str) -> _CustomData | None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Get custom data for this trade
# REMOVED_UNUSED_CODE:         :param key: key of the custom data
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         data = CustomDataWrapper.get_custom_data(trade_id=self.id, key=key)
# REMOVED_UNUSED_CODE:         if data:
# REMOVED_UNUSED_CODE:             return data[0]
# REMOVED_UNUSED_CODE:         return None

# REMOVED_UNUSED_CODE:     def get_all_custom_data(self) -> list[_CustomData]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Get all custom data for this trade
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return CustomDataWrapper.get_custom_data(trade_id=self.id)

# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def nr_of_successful_entries(self) -> int:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Helper function to count the number of entry orders that have been filled.
# REMOVED_UNUSED_CODE:         :return: int count of entry orders that have been filled for this trade.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return len(self.select_filled_orders(self.entry_side))

# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def nr_of_successful_exits(self) -> int:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Helper function to count the number of exit orders that have been filled.
# REMOVED_UNUSED_CODE:         :return: int count of exit orders that have been filled for this trade.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return len(self.select_filled_orders(self.exit_side))

# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def nr_of_successful_buys(self) -> int:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Helper function to count the number of buy orders that have been filled.
# REMOVED_UNUSED_CODE:         WARNING: Please use nr_of_successful_entries for short support.
# REMOVED_UNUSED_CODE:         :return: int count of buy orders that have been filled for this trade.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return len(self.select_filled_orders("buy"))

# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def nr_of_successful_sells(self) -> int:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Helper function to count the number of sell orders that have been filled.
# REMOVED_UNUSED_CODE:         WARNING: Please use nr_of_successful_exits for short support.
# REMOVED_UNUSED_CODE:         :return: int count of sell orders that have been filled for this trade.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return len(self.select_filled_orders("sell"))

# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def sell_reason(self) -> str | None:
# REMOVED_UNUSED_CODE:         """DEPRECATED! Please use exit_reason instead."""
# REMOVED_UNUSED_CODE:         return self.exit_reason

# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def safe_close_rate(self) -> float:
# REMOVED_UNUSED_CODE:         return self.close_rate or self.close_rate_requested or 0.0

    @staticmethod
    def get_trades_proxy(
        *,
        pair: str | None = None,
        is_open: bool | None = None,
        open_date: datetime | None = None,
        close_date: datetime | None = None,
    ) -> list["LocalTrade"]:
        """
        Helper function to query Trades.
        Returns a List of trades, filtered on the parameters given.
        In live mode, converts the filter to a database query and returns all rows
        In Backtest mode, uses filters on Trade.bt_trades to get the result.

        :param pair: Filter by pair
        :param is_open: Filter by open/closed status
        :param open_date: Filter by open_date (filters via trade.open_date > input)
        :param close_date: Filter by close_date (filters via trade.close_date > input)
                           Will implicitly only return closed trades.
        :return: unsorted List[Trade]
        """

        # Offline mode - without database
        if is_open is not None:
            if is_open:
                sel_trades = LocalTrade.bt_trades_open
            else:
                sel_trades = LocalTrade.bt_trades

        else:
            # Not used during backtesting, but might be used by a strategy
            sel_trades = list(LocalTrade.bt_trades + LocalTrade.bt_trades_open)

        if pair:
            sel_trades = [trade for trade in sel_trades if trade.pair == pair]
        if open_date:
            sel_trades = [trade for trade in sel_trades if trade.open_date > open_date]
        if close_date:
            sel_trades = [
                trade for trade in sel_trades if trade.close_date and trade.close_date > close_date
            ]

        return sel_trades

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def close_bt_trade(trade):
# REMOVED_UNUSED_CODE:         LocalTrade.bt_trades_open.remove(trade)
# REMOVED_UNUSED_CODE:         LocalTrade.bt_trades_open_pp[trade.pair].remove(trade)
# REMOVED_UNUSED_CODE:         LocalTrade.bt_open_open_trade_count -= 1
# REMOVED_UNUSED_CODE:         LocalTrade.bt_trades.append(trade)
# REMOVED_UNUSED_CODE:         LocalTrade.bt_total_profit += trade.close_profit_abs

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def add_bt_trade(trade):
# REMOVED_UNUSED_CODE:         if trade.is_open:
# REMOVED_UNUSED_CODE:             LocalTrade.bt_trades_open.append(trade)
# REMOVED_UNUSED_CODE:             LocalTrade.bt_trades_open_pp[trade.pair].append(trade)
# REMOVED_UNUSED_CODE:             LocalTrade.bt_open_open_trade_count += 1
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             LocalTrade.bt_trades.append(trade)

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def remove_bt_trade(trade):
# REMOVED_UNUSED_CODE:         LocalTrade.bt_trades_open.remove(trade)
# REMOVED_UNUSED_CODE:         LocalTrade.bt_trades_open_pp[trade.pair].remove(trade)
# REMOVED_UNUSED_CODE:         LocalTrade.bt_open_open_trade_count -= 1

# REMOVED_UNUSED_CODE:     @staticmethod
    def get_open_trades() -> list[Any]:
        """
        Retrieve open trades
        """
        return Trade.get_trades_proxy(is_open=True)

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def get_open_trade_count() -> int:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         get open trade count
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if Trade.use_db:
# REMOVED_UNUSED_CODE:             return Trade.session.execute(
# REMOVED_UNUSED_CODE:                 select(func.count(Trade.id)).filter(Trade.is_open.is_(True))
# REMOVED_UNUSED_CODE:             ).scalar_one()
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             return LocalTrade.bt_open_open_trade_count

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def stoploss_reinitialization(desired_stoploss: float):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Adjust initial Stoploss to desired stoploss for all open trades.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         trade: Trade
# REMOVED_UNUSED_CODE:         for trade in Trade.get_open_trades():
# REMOVED_UNUSED_CODE:             logger.info(f"Found open trade: {trade}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # skip case if trailing-stop changed the stoploss already.
# REMOVED_UNUSED_CODE:             if not trade.is_stop_loss_trailing and trade.initial_stop_loss_pct != desired_stoploss:
# REMOVED_UNUSED_CODE:                 # Stoploss value got changed
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 logger.info(f"Stoploss for {trade} needs adjustment...")
# REMOVED_UNUSED_CODE:                 # Force reset of stoploss
# REMOVED_UNUSED_CODE:                 trade.stop_loss = 0.0
# REMOVED_UNUSED_CODE:                 trade.initial_stop_loss_pct = None
# REMOVED_UNUSED_CODE:                 trade.adjust_stop_loss(trade.open_rate, desired_stoploss)
# REMOVED_UNUSED_CODE:                 logger.info(f"New stoploss: {trade.stop_loss}.")

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """
        Create a Trade instance from a json string.

        Used for debugging purposes - please keep.
        :param json_str: json string to parse
        :return: Trade instance
        """
        import rapidjson

        data = rapidjson.loads(json_str)
        trade = cls(
            __FROM_JSON=True,
            id=data["trade_id"],
            pair=data["pair"],
            base_currency=data["base_currency"],
            stake_currency=data["quote_currency"],
            is_open=data["is_open"],
            exchange=data["exchange"],
            amount=data["amount"],
            amount_requested=data["amount_requested"],
            stake_amount=data["stake_amount"],
            strategy=data["strategy"],
            enter_tag=data["enter_tag"],
            timeframe=data["timeframe"],
            fee_open=data["fee_open"],
            fee_open_cost=data["fee_open_cost"],
            fee_open_currency=data["fee_open_currency"],
            fee_close=data["fee_close"],
            fee_close_cost=data["fee_close_cost"],
            fee_close_currency=data["fee_close_currency"],
            open_date=datetime.fromtimestamp(data["open_timestamp"] // 1000, tz=timezone.utc),
            open_rate=data["open_rate"],
            open_rate_requested=data["open_rate_requested"],
            open_trade_value=data["open_trade_value"],
            close_date=(
                datetime.fromtimestamp(data["close_timestamp"] // 1000, tz=timezone.utc)
                if data["close_timestamp"]
                else None
            ),
            realized_profit=data["realized_profit"],
            close_rate=data["close_rate"],
            close_rate_requested=data["close_rate_requested"],
            close_profit=data["close_profit"],
            close_profit_abs=data["close_profit_abs"],
            exit_reason=data["exit_reason"],
            exit_order_status=data["exit_order_status"],
            stop_loss=data["stop_loss_abs"],
            stop_loss_pct=data["stop_loss_ratio"],
            initial_stop_loss=data["initial_stop_loss_abs"],
            initial_stop_loss_pct=data["initial_stop_loss_ratio"],
            min_rate=data["min_rate"],
            max_rate=data["max_rate"],
            leverage=data["leverage"],
            interest_rate=data["interest_rate"],
            liquidation_price=data["liquidation_price"],
            is_short=data["is_short"],
            trading_mode=data["trading_mode"],
            funding_fees=data["funding_fees"],
            amount_precision=data.get("amount_precision", None),
            price_precision=data.get("price_precision", None),
            precision_mode=data.get("precision_mode", None),
            precision_mode_price=data.get("precision_mode_price", data.get("precision_mode", None)),
            contract_size=data.get("contract_size", None),
        )
        for order in data["orders"]:
            order_obj = Order(
                amount=order["amount"],
                ft_amount=order["amount"],
                ft_order_side=order["ft_order_side"],
                ft_pair=order["pair"],
                ft_is_open=order["is_open"],
                order_id=order["order_id"],
                status=order["status"],
                average=order["average"],
                cost=order["cost"],
                filled=order["filled"],
                order_date=datetime.strptime(order["order_date"], DATETIME_PRINT_FORMAT),
                order_filled_date=(
                    datetime.fromtimestamp(order["order_filled_timestamp"] // 1000, tz=timezone.utc)
                    if order["order_filled_timestamp"]
                    else None
                ),
                order_type=order["order_type"],
                price=order["price"],
                ft_price=order["price"],
                remaining=order["remaining"],
                funding_fee=order.get("funding_fee", None),
                ft_order_tag=order.get("ft_order_tag", None),
            )
            trade.orders.append(order_obj)

        return trade


class Trade(ModelBase, LocalTrade):
    """
    Trade database model.
    Also handles updating and querying trades

    Note: Fields must be aligned with LocalTrade class
    """

    __tablename__ = "trades"
    session: ClassVar[SessionType]

    use_db: bool = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # type: ignore

    orders: Mapped[list[Order]] = relationship(
        "Order", order_by="Order.id", cascade="all, delete-orphan", lazy="selectin", innerjoin=True
    )  # type: ignore
# REMOVED_UNUSED_CODE:     custom_data: Mapped[list[_CustomData]] = relationship(
# REMOVED_UNUSED_CODE:         "_CustomData", cascade="all, delete-orphan", lazy="raise"
# REMOVED_UNUSED_CODE:     )

    exchange: Mapped[str] = mapped_column(String(25), nullable=False)  # type: ignore
    pair: Mapped[str] = mapped_column(String(25), nullable=False, index=True)  # type: ignore
    base_currency: Mapped[str | None] = mapped_column(String(25), nullable=True)  # type: ignore
    stake_currency: Mapped[str | None] = mapped_column(String(25), nullable=True)  # type: ignore
    is_open: Mapped[bool] = mapped_column(nullable=False, default=True, index=True)  # type: ignore
    fee_open: Mapped[float] = mapped_column(Float(), nullable=False, default=0.0)  # type: ignore
    fee_open_cost: Mapped[float | None] = mapped_column(Float(), nullable=True)  # type: ignore
    fee_open_currency: Mapped[str | None] = mapped_column(  # type: ignore
        String(25), nullable=True
    )
    fee_close: Mapped[float | None] = mapped_column(  # type: ignore
        Float(), nullable=False, default=0.0
    )
    fee_close_cost: Mapped[float | None] = mapped_column(Float(), nullable=True)  # type: ignore
    fee_close_currency: Mapped[str | None] = mapped_column(  # type: ignore
        String(25), nullable=True
    )
    open_rate: Mapped[float] = mapped_column(Float())  # type: ignore
    open_rate_requested: Mapped[float | None] = mapped_column(  # type: ignore
        Float(), nullable=True
    )
    # open_trade_value - calculated via _calc_open_trade_value
    open_trade_value: Mapped[float] = mapped_column(Float(), nullable=True)  # type: ignore
    close_rate: Mapped[float | None] = mapped_column(Float())  # type: ignore
    close_rate_requested: Mapped[float | None] = mapped_column(Float())  # type: ignore
    realized_profit: Mapped[float] = mapped_column(  # type: ignore
        Float(), default=0.0, nullable=True
    )
    close_profit: Mapped[float | None] = mapped_column(Float())  # type: ignore
    close_profit_abs: Mapped[float | None] = mapped_column(Float())  # type: ignore
    stake_amount: Mapped[float] = mapped_column(Float(), nullable=False)  # type: ignore
    max_stake_amount: Mapped[float | None] = mapped_column(Float())  # type: ignore
    amount: Mapped[float] = mapped_column(Float())  # type: ignore
    amount_requested: Mapped[float | None] = mapped_column(Float())  # type: ignore
    open_date: Mapped[datetime] = mapped_column(  # type: ignore
        nullable=False, default=datetime.now
    )
    close_date: Mapped[datetime | None] = mapped_column()  # type: ignore
    # absolute value of the stop loss
    stop_loss: Mapped[float] = mapped_column(Float(), nullable=True, default=0.0)  # type: ignore
    # percentage value of the stop loss
    stop_loss_pct: Mapped[float | None] = mapped_column(Float(), nullable=True)  # type: ignore
    # absolute value of the initial stop loss
    initial_stop_loss: Mapped[float | None] = mapped_column(  # type: ignore
        Float(), nullable=True, default=0.0
    )
    # percentage value of the initial stop loss
    initial_stop_loss_pct: Mapped[float | None] = mapped_column(  # type: ignore
        Float(), nullable=True
    )
# REMOVED_UNUSED_CODE:     is_stop_loss_trailing: Mapped[bool] = mapped_column(  # type: ignore
# REMOVED_UNUSED_CODE:         nullable=False, default=False
# REMOVED_UNUSED_CODE:     )
    # absolute value of the highest reached price
    max_rate: Mapped[float | None] = mapped_column(  # type: ignore
        Float(), nullable=True, default=0.0
    )
    # Lowest price reached
    min_rate: Mapped[float | None] = mapped_column(Float(), nullable=True)  # type: ignore
    exit_reason: Mapped[str | None] = mapped_column(  # type: ignore
        String(CUSTOM_TAG_MAX_LENGTH), nullable=True
    )
    exit_order_status: Mapped[str | None] = mapped_column(  # type: ignore
        String(100), nullable=True
    )
    strategy: Mapped[str | None] = mapped_column(String(100), nullable=True)  # type: ignore
    enter_tag: Mapped[str | None] = mapped_column(  # type: ignore
        String(CUSTOM_TAG_MAX_LENGTH), nullable=True
    )
    timeframe: Mapped[int | None] = mapped_column(Integer, nullable=True)  # type: ignore

    trading_mode: Mapped[TradingMode] = mapped_column(  # type: ignore
        Enum(TradingMode), nullable=True
    )
    amount_precision: Mapped[float | None] = mapped_column(  # type: ignore
        Float(), nullable=True
    )
    price_precision: Mapped[float | None] = mapped_column(Float(), nullable=True)  # type: ignore
    precision_mode: Mapped[int | None] = mapped_column(Integer, nullable=True)  # type: ignore
    precision_mode_price: Mapped[int | None] = mapped_column(  # type: ignore
        Integer, nullable=True
    )
    contract_size: Mapped[float | None] = mapped_column(Float(), nullable=True)  # type: ignore

    # Leverage trading properties
    leverage: Mapped[float] = mapped_column(Float(), nullable=True, default=1.0)  # type: ignore
    is_short: Mapped[bool] = mapped_column(nullable=False, default=False)  # type: ignore
    liquidation_price: Mapped[float | None] = mapped_column(  # type: ignore
        Float(), nullable=True
    )

    # Margin Trading Properties
    interest_rate: Mapped[float] = mapped_column(  # type: ignore
        Float(), nullable=False, default=0.0
    )

    # Futures properties
    funding_fees: Mapped[float | None] = mapped_column(  # type: ignore
        Float(), nullable=True, default=None
    )
# REMOVED_UNUSED_CODE:     funding_fee_running: Mapped[float | None] = mapped_column(  # type: ignore
# REMOVED_UNUSED_CODE:         Float(), nullable=True, default=None
# REMOVED_UNUSED_CODE:     )

    def __init__(self, **kwargs):
        from_json = kwargs.pop("__FROM_JSON", None)
        super().__init__(**kwargs)
        if not from_json:
            # Skip recalculation when loading from json
            self.realized_profit = 0
            self.recalc_open_trade_value()

# REMOVED_UNUSED_CODE:     @validates("enter_tag", "exit_reason")
# REMOVED_UNUSED_CODE:     def validate_string_len(self, key, value):
# REMOVED_UNUSED_CODE:         max_len = getattr(self.__class__, key).prop.columns[0].type.length
# REMOVED_UNUSED_CODE:         if value and len(value) > max_len:
# REMOVED_UNUSED_CODE:             return value[:max_len]
# REMOVED_UNUSED_CODE:         return value

    def delete(self) -> None:
        for order in self.orders:
            Order.session.delete(order)

        CustomDataWrapper.delete_custom_data(trade_id=self.id)

        Trade.session.delete(self)
        Trade.commit()

    @staticmethod
    def commit():
        Trade.session.commit()

    @staticmethod
    def rollback():
        Trade.session.rollback()

    @staticmethod
    def get_trades_proxy(
        *,
        pair: str | None = None,
        is_open: bool | None = None,
        open_date: datetime | None = None,
        close_date: datetime | None = None,
    ) -> list["LocalTrade"]:
        """
        Helper function to query Trades.j
        Returns a List of trades, filtered on the parameters given.
        In live mode, converts the filter to a database query and returns all rows
        In Backtest mode, uses filters on Trade.bt_trades to get the result.

        :return: unsorted List[Trade]
        """
        if Trade.use_db:
            trade_filter = []
            if pair:
                trade_filter.append(Trade.pair == pair)
            if open_date:
                trade_filter.append(Trade.open_date > open_date)
            if close_date:
                trade_filter.append(Trade.close_date > close_date)
            if is_open is not None:
                trade_filter.append(Trade.is_open.is_(is_open))
            return cast(list[LocalTrade], Trade.get_trades(trade_filter).all())
        else:
            return LocalTrade.get_trades_proxy(
                pair=pair, is_open=is_open, open_date=open_date, close_date=close_date
            )

    @staticmethod
    def get_trades_query(trade_filter=None, include_orders: bool = True) -> Select:
        """
        Helper function to query Trades using filters.
        NOTE: Not supported in Backtesting.
        :param trade_filter: Optional filter to apply to trades
                             Can be either a Filter object, or a List of filters
                             e.g. `(trade_filter=[Trade.id == trade_id, Trade.is_open.is_(True),])`
                             e.g. `(trade_filter=Trade.id == trade_id)`
        :return: unsorted query object
        """
        if not Trade.use_db:
            raise NotImplementedError("`Trade.get_trades()` not supported in backtesting mode.")
        if trade_filter is not None:
            if not isinstance(trade_filter, list):
                trade_filter = [trade_filter]
            this_query = select(Trade).filter(*trade_filter)
        else:
            this_query = select(Trade)
        if not include_orders:
            # Don't load order relations
            # Consider using noload or raiseload instead of lazyload
            this_query = this_query.options(lazyload(Trade.orders))
        return this_query

    @staticmethod
    def get_trades(trade_filter=None, include_orders: bool = True) -> ScalarResult["Trade"]:
        """
        Helper function to query Trades using filters.
        NOTE: Not supported in Backtesting.
        :param trade_filter: Optional filter to apply to trades
                             Can be either a Filter object, or a List of filters
                             e.g. `(trade_filter=[Trade.id == trade_id, Trade.is_open.is_(True),])`
                             e.g. `(trade_filter=Trade.id == trade_id)`
        :return: unsorted query object
        """
        query = Trade.get_trades_query(trade_filter, include_orders)
        # this should remain split. if use_db is False, session is not available and the above will
        # raise an exception.
        return Trade.session.scalars(query)

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def get_open_trades_without_assigned_fees():
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Returns all open trades which don't have open fees set correctly
# REMOVED_UNUSED_CODE:         NOTE: Not supported in Backtesting.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return Trade.get_trades(
# REMOVED_UNUSED_CODE:             [
# REMOVED_UNUSED_CODE:                 Trade.fee_open_currency.is_(None),
# REMOVED_UNUSED_CODE:                 Trade.orders.any(),
# REMOVED_UNUSED_CODE:                 Trade.is_open.is_(True),
# REMOVED_UNUSED_CODE:             ]
# REMOVED_UNUSED_CODE:         ).all()

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def get_closed_trades_without_assigned_fees():
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Returns all closed trades which don't have fees set correctly
# REMOVED_UNUSED_CODE:         NOTE: Not supported in Backtesting.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return Trade.get_trades(
# REMOVED_UNUSED_CODE:             [
# REMOVED_UNUSED_CODE:                 Trade.fee_close_currency.is_(None),
# REMOVED_UNUSED_CODE:                 Trade.orders.any(),
# REMOVED_UNUSED_CODE:                 Trade.is_open.is_(False),
# REMOVED_UNUSED_CODE:             ]
# REMOVED_UNUSED_CODE:         ).all()

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def get_total_closed_profit() -> float:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Retrieves total realized profit
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if Trade.use_db:
# REMOVED_UNUSED_CODE:             total_profit = Trade.session.execute(
# REMOVED_UNUSED_CODE:                 select(func.sum(Trade.close_profit_abs)).filter(Trade.is_open.is_(False))
# REMOVED_UNUSED_CODE:             ).scalar_one()
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             total_profit = sum(
# REMOVED_UNUSED_CODE:                 t.close_profit_abs  # type: ignore
# REMOVED_UNUSED_CODE:                 for t in LocalTrade.get_trades_proxy(is_open=False)
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         return total_profit or 0

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def total_open_trades_stakes() -> float:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Calculates total invested amount in open trades
# REMOVED_UNUSED_CODE:         in stake currency
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if Trade.use_db:
# REMOVED_UNUSED_CODE:             total_open_stake_amount = Trade.session.scalar(
# REMOVED_UNUSED_CODE:                 select(func.sum(Trade.stake_amount)).filter(Trade.is_open.is_(True))
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             total_open_stake_amount = sum(
# REMOVED_UNUSED_CODE:                 t.stake_amount for t in LocalTrade.get_trades_proxy(is_open=True)
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         return total_open_stake_amount or 0

# REMOVED_UNUSED_CODE:     @staticmethod
    def _generic_performance_query(columns: list, filters: list, fallback: str = "") -> Select:
        """
        Retrieve a generic select object to calculate performance grouped on `columns`.
        Returns the following columns:
        - columns
        - profit_ratio
        - profit_sum_abs
        - count
        NOTE: Not supported in Backtesting.
        """
        columns_coal = [func.coalesce(c, fallback).label(c.name) for c in columns]
        pair_costs = (
            select(
                *columns_coal,
                func.sum(
                    (
                        func.coalesce(Order.filled, Order.amount)
                        * func.coalesce(Order.average, Order.price, Order.ft_price)
                    )
                    / func.coalesce(Trade.leverage, 1)
                ).label("cost_per_pair"),
            )
            .join(Order, Trade.id == Order.ft_trade_id)
            .filter(
                *filters,
                Order.ft_order_side == case((Trade.is_short.is_(True), "sell"), else_="buy"),
                Order.filled > 0,
            )
            .group_by(*columns)
            .cte("pair_costs")
        )
        trades_grouped = (
            select(
                *columns_coal,
                func.sum(Trade.close_profit_abs).label("profit_sum_abs"),
                func.count(*columns_coal).label("count"),
            )
            .filter(*filters)
            .group_by(*columns_coal)
            .cte("trades_grouped")
        )
        q = (
            select(
                *[trades_grouped.c[x.name] for x in columns],
                (trades_grouped.c.profit_sum_abs / pair_costs.c.cost_per_pair).label(
                    "profit_ratio"
                ),
                trades_grouped.c.profit_sum_abs,
                trades_grouped.c.count,
            )
            .join(pair_costs, *[trades_grouped.c[x.name] == pair_costs.c[x.name] for x in columns])
            .order_by(desc("profit_sum_abs"))
        )
        return q

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def get_overall_performance(start_date: datetime | None = None) -> list[dict[str, Any]]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Returns List of dicts containing all Trades, including profit and trade count
# REMOVED_UNUSED_CODE:         NOTE: Not supported in Backtesting.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         filters: list = [Trade.is_open.is_(False)]
# REMOVED_UNUSED_CODE:         if start_date:
# REMOVED_UNUSED_CODE:             filters.append(Trade.close_date >= start_date)
# REMOVED_UNUSED_CODE:         pair_rates_query = Trade._generic_performance_query([Trade.pair], filters)
# REMOVED_UNUSED_CODE:         pair_rates = Trade.session.execute(pair_rates_query).all()
# REMOVED_UNUSED_CODE:         return [
# REMOVED_UNUSED_CODE:             {
# REMOVED_UNUSED_CODE:                 "pair": pair,
# REMOVED_UNUSED_CODE:                 "profit_ratio": profit,
# REMOVED_UNUSED_CODE:                 "profit": round(profit * 100, 2),  # Compatibility mode
# REMOVED_UNUSED_CODE:                 "profit_pct": round(profit * 100, 2),
# REMOVED_UNUSED_CODE:                 "profit_abs": profit_abs,
# REMOVED_UNUSED_CODE:                 "count": count,
# REMOVED_UNUSED_CODE:             }
# REMOVED_UNUSED_CODE:             for pair, profit, profit_abs, count in pair_rates
# REMOVED_UNUSED_CODE:         ]

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def get_enter_tag_performance(pair: str | None) -> list[dict[str, Any]]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Returns List of dicts containing all Trades, based on buy tag performance
# REMOVED_UNUSED_CODE:         Can either be average for all pairs or a specific pair provided
# REMOVED_UNUSED_CODE:         NOTE: Not supported in Backtesting.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         filters: list = [Trade.is_open.is_(False)]
# REMOVED_UNUSED_CODE:         if pair is not None:
# REMOVED_UNUSED_CODE:             filters.append(Trade.pair == pair)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         pair_rates_query = Trade._generic_performance_query([Trade.enter_tag], filters, "Other")
# REMOVED_UNUSED_CODE:         enter_tag_perf = Trade.session.execute(pair_rates_query).all()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return [
# REMOVED_UNUSED_CODE:             {
# REMOVED_UNUSED_CODE:                 "enter_tag": enter_tag if enter_tag is not None else "Other",
# REMOVED_UNUSED_CODE:                 "profit_ratio": profit,
# REMOVED_UNUSED_CODE:                 "profit_pct": round(profit * 100, 2),
# REMOVED_UNUSED_CODE:                 "profit_abs": profit_abs,
# REMOVED_UNUSED_CODE:                 "count": count,
# REMOVED_UNUSED_CODE:             }
# REMOVED_UNUSED_CODE:             for enter_tag, profit, profit_abs, count in enter_tag_perf
# REMOVED_UNUSED_CODE:         ]

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def get_exit_reason_performance(pair: str | None) -> list[dict[str, Any]]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Returns List of dicts containing all Trades, based on exit reason performance
# REMOVED_UNUSED_CODE:         Can either be average for all pairs or a specific pair provided
# REMOVED_UNUSED_CODE:         NOTE: Not supported in Backtesting.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         filters: list = [Trade.is_open.is_(False)]
# REMOVED_UNUSED_CODE:         if pair is not None:
# REMOVED_UNUSED_CODE:             filters.append(Trade.pair == pair)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         pair_rates_query = Trade._generic_performance_query([Trade.exit_reason], filters, "Other")
# REMOVED_UNUSED_CODE:         sell_tag_perf = Trade.session.execute(pair_rates_query).all()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return [
# REMOVED_UNUSED_CODE:             {
# REMOVED_UNUSED_CODE:                 "exit_reason": exit_reason if exit_reason is not None else "Other",
# REMOVED_UNUSED_CODE:                 "profit_ratio": profit,
# REMOVED_UNUSED_CODE:                 "profit_pct": round(profit * 100, 2),
# REMOVED_UNUSED_CODE:                 "profit_abs": profit_abs,
# REMOVED_UNUSED_CODE:                 "count": count,
# REMOVED_UNUSED_CODE:             }
# REMOVED_UNUSED_CODE:             for exit_reason, profit, profit_abs, count in sell_tag_perf
# REMOVED_UNUSED_CODE:         ]

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def get_mix_tag_performance(pair: str | None) -> list[dict[str, Any]]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Returns List of dicts containing all Trades, based on entry_tag + exit_reason performance
# REMOVED_UNUSED_CODE:         Can either be average for all pairs or a specific pair provided
# REMOVED_UNUSED_CODE:         NOTE: Not supported in Backtesting.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         filters: list = [Trade.is_open.is_(False)]
# REMOVED_UNUSED_CODE:         if pair is not None:
# REMOVED_UNUSED_CODE:             filters.append(Trade.pair == pair)
# REMOVED_UNUSED_CODE:         mix_tag_perf = Trade.session.execute(
# REMOVED_UNUSED_CODE:             select(
# REMOVED_UNUSED_CODE:                 Trade.id,
# REMOVED_UNUSED_CODE:                 Trade.enter_tag,
# REMOVED_UNUSED_CODE:                 Trade.exit_reason,
# REMOVED_UNUSED_CODE:                 func.sum(Trade.close_profit).label("profit_sum"),
# REMOVED_UNUSED_CODE:                 func.sum(Trade.close_profit_abs).label("profit_sum_abs"),
# REMOVED_UNUSED_CODE:                 func.count(Trade.pair).label("count"),
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             .filter(*filters)
# REMOVED_UNUSED_CODE:             .group_by(Trade.id)
# REMOVED_UNUSED_CODE:             .order_by(desc("profit_sum_abs"))
# REMOVED_UNUSED_CODE:         ).all()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         resp: list[dict] = []
# REMOVED_UNUSED_CODE:         for _, enter_tag, exit_reason, profit, profit_abs, count in mix_tag_perf:
# REMOVED_UNUSED_CODE:             enter_tag = enter_tag if enter_tag is not None else "Other"
# REMOVED_UNUSED_CODE:             exit_reason = exit_reason if exit_reason is not None else "Other"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if exit_reason is not None and enter_tag is not None:
# REMOVED_UNUSED_CODE:                 mix_tag = enter_tag + " " + exit_reason
# REMOVED_UNUSED_CODE:                 i = 0
# REMOVED_UNUSED_CODE:                 if not any(item["mix_tag"] == mix_tag for item in resp):
# REMOVED_UNUSED_CODE:                     resp.append(
# REMOVED_UNUSED_CODE:                         {
# REMOVED_UNUSED_CODE:                             "mix_tag": mix_tag,
# REMOVED_UNUSED_CODE:                             "profit_ratio": profit,
# REMOVED_UNUSED_CODE:                             "profit_pct": round(profit * 100, 2),
# REMOVED_UNUSED_CODE:                             "profit_abs": profit_abs,
# REMOVED_UNUSED_CODE:                             "count": count,
# REMOVED_UNUSED_CODE:                         }
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE:                     while i < len(resp):
# REMOVED_UNUSED_CODE:                         if resp[i]["mix_tag"] == mix_tag:
# REMOVED_UNUSED_CODE:                             resp[i] = {
# REMOVED_UNUSED_CODE:                                 "mix_tag": mix_tag,
# REMOVED_UNUSED_CODE:                                 "profit_ratio": profit + resp[i]["profit_ratio"],
# REMOVED_UNUSED_CODE:                                 "profit_pct": round(profit + resp[i]["profit_ratio"] * 100, 2),
# REMOVED_UNUSED_CODE:                                 "profit_abs": profit_abs + resp[i]["profit_abs"],
# REMOVED_UNUSED_CODE:                                 "count": 1 + resp[i]["count"],
# REMOVED_UNUSED_CODE:                             }
# REMOVED_UNUSED_CODE:                         i += 1
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return resp

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def get_best_pair(start_date: datetime | None = None):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Get best pair with closed trade.
# REMOVED_UNUSED_CODE:         NOTE: Not supported in Backtesting.
# REMOVED_UNUSED_CODE:         :returns: Tuple containing (pair, profit_sum)
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         filters: list = [Trade.is_open.is_(False)]
# REMOVED_UNUSED_CODE:         if start_date:
# REMOVED_UNUSED_CODE:             filters.append(Trade.close_date >= start_date)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         pair_rates_query = Trade._generic_performance_query([Trade.pair], filters)
# REMOVED_UNUSED_CODE:         best_pair = Trade.session.execute(pair_rates_query).first()
# REMOVED_UNUSED_CODE:         # returns pair, profit_ratio, abs_profit, count
# REMOVED_UNUSED_CODE:         return best_pair

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def get_trading_volume(start_date: datetime | None = None) -> float:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Get Trade volume based on Orders
# REMOVED_UNUSED_CODE:         NOTE: Not supported in Backtesting.
# REMOVED_UNUSED_CODE:         :returns: Tuple containing (pair, profit_sum)
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         filters = [Order.status == "closed"]
# REMOVED_UNUSED_CODE:         if start_date:
# REMOVED_UNUSED_CODE:             filters.append(Order.order_filled_date >= start_date)
# REMOVED_UNUSED_CODE:         trading_volume = Trade.session.execute(
# REMOVED_UNUSED_CODE:             select(func.sum(Order.cost).label("volume")).filter(*filters)
# REMOVED_UNUSED_CODE:         ).scalar_one()
# REMOVED_UNUSED_CODE:         return trading_volume or 0.0
