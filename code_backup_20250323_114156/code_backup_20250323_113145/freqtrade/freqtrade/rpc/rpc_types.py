from datetime import datetime
from typing import Any, Literal, TypedDict

from freqtrade.constants import PairWithTimeframe
from freqtrade.enums import RPCMessageType


ProfitLossStr = Literal["profit", "loss"]


class RPCSendMsgBase(TypedDict):
    pass
    # ty1pe: Literal[RPCMessageType]


class RPCStatusMsg(RPCSendMsgBase):
    """Used for Status, Startup and Warning messages"""

# REMOVED_UNUSED_CODE:     type: Literal[RPCMessageType.STATUS, RPCMessageType.STARTUP, RPCMessageType.WARNING]
# REMOVED_UNUSED_CODE:     status: str


class RPCStrategyMsg(RPCSendMsgBase):
    """Used for Status, Startup and Warning messages"""

# REMOVED_UNUSED_CODE:     type: Literal[RPCMessageType.STRATEGY_MSG]
# REMOVED_UNUSED_CODE:     msg: str


class RPCProtectionMsg(RPCSendMsgBase):
# REMOVED_UNUSED_CODE:     type: Literal[RPCMessageType.PROTECTION_TRIGGER, RPCMessageType.PROTECTION_TRIGGER_GLOBAL]
# REMOVED_UNUSED_CODE:     id: int
# REMOVED_UNUSED_CODE:     pair: str
# REMOVED_UNUSED_CODE:     base_currency: str | None
# REMOVED_UNUSED_CODE:     lock_time: str
# REMOVED_UNUSED_CODE:     lock_timestamp: int
# REMOVED_UNUSED_CODE:     lock_end_time: str
# REMOVED_UNUSED_CODE:     lock_end_timestamp: int
# REMOVED_UNUSED_CODE:     reason: str
# REMOVED_UNUSED_CODE:     side: str
# REMOVED_UNUSED_CODE:     active: bool


class RPCWhitelistMsg(RPCSendMsgBase):
# REMOVED_UNUSED_CODE:     type: Literal[RPCMessageType.WHITELIST]
# REMOVED_UNUSED_CODE:     data: list[str]


class __RPCEntryExitMsgBase(RPCSendMsgBase):
# REMOVED_UNUSED_CODE:     trade_id: int
# REMOVED_UNUSED_CODE:     buy_tag: str | None
# REMOVED_UNUSED_CODE:     enter_tag: str | None
# REMOVED_UNUSED_CODE:     exchange: str
# REMOVED_UNUSED_CODE:     pair: str
# REMOVED_UNUSED_CODE:     base_currency: str
# REMOVED_UNUSED_CODE:     quote_currency: str
# REMOVED_UNUSED_CODE:     leverage: float | None
# REMOVED_UNUSED_CODE:     direction: str
# REMOVED_UNUSED_CODE:     limit: float
# REMOVED_UNUSED_CODE:     open_rate: float
# REMOVED_UNUSED_CODE:     order_type: str
# REMOVED_UNUSED_CODE:     stake_amount: float
# REMOVED_UNUSED_CODE:     stake_currency: str
# REMOVED_UNUSED_CODE:     fiat_currency: str | None
# REMOVED_UNUSED_CODE:     amount: float
# REMOVED_UNUSED_CODE:     open_date: datetime
# REMOVED_UNUSED_CODE:     current_rate: float | None
# REMOVED_UNUSED_CODE:     sub_trade: bool


class RPCEntryMsg(__RPCEntryExitMsgBase):
# REMOVED_UNUSED_CODE:     type: Literal[RPCMessageType.ENTRY, RPCMessageType.ENTRY_FILL]


class RPCCancelMsg(__RPCEntryExitMsgBase):
# REMOVED_UNUSED_CODE:     type: Literal[RPCMessageType.ENTRY_CANCEL]
# REMOVED_UNUSED_CODE:     reason: str


class RPCExitMsg(__RPCEntryExitMsgBase):
# REMOVED_UNUSED_CODE:     type: Literal[RPCMessageType.EXIT, RPCMessageType.EXIT_FILL]
# REMOVED_UNUSED_CODE:     cumulative_profit: float
# REMOVED_UNUSED_CODE:     gain: ProfitLossStr
# REMOVED_UNUSED_CODE:     close_rate: float
# REMOVED_UNUSED_CODE:     profit_amount: float
# REMOVED_UNUSED_CODE:     profit_ratio: float
# REMOVED_UNUSED_CODE:     exit_reason: str | None
# REMOVED_UNUSED_CODE:     close_date: datetime
    # current_rate: float | None
# REMOVED_UNUSED_CODE:     order_rate: float | None
# REMOVED_UNUSED_CODE:     final_profit_ratio: float | None
# REMOVED_UNUSED_CODE:     is_final_exit: bool


class RPCExitCancelMsg(__RPCEntryExitMsgBase):
# REMOVED_UNUSED_CODE:     type: Literal[RPCMessageType.EXIT_CANCEL]
# REMOVED_UNUSED_CODE:     reason: str
# REMOVED_UNUSED_CODE:     gain: ProfitLossStr
# REMOVED_UNUSED_CODE:     profit_amount: float
# REMOVED_UNUSED_CODE:     profit_ratio: float
# REMOVED_UNUSED_CODE:     exit_reason: str | None
# REMOVED_UNUSED_CODE:     close_date: datetime


class _AnalyzedDFData(TypedDict):
# REMOVED_UNUSED_CODE:     key: PairWithTimeframe
# REMOVED_UNUSED_CODE:     df: Any
# REMOVED_UNUSED_CODE:     la: datetime


class RPCAnalyzedDFMsg(RPCSendMsgBase):
    """New Analyzed dataframe message"""

# REMOVED_UNUSED_CODE:     type: Literal[RPCMessageType.ANALYZED_DF]
# REMOVED_UNUSED_CODE:     data: _AnalyzedDFData


class RPCNewCandleMsg(RPCSendMsgBase):
    """New candle ping message, issued once per new candle/pair"""

# REMOVED_UNUSED_CODE:     type: Literal[RPCMessageType.NEW_CANDLE]
# REMOVED_UNUSED_CODE:     data: PairWithTimeframe


# REMOVED_UNUSED_CODE: RPCOrderMsg = RPCEntryMsg | RPCExitMsg | RPCExitCancelMsg | RPCCancelMsg


# REMOVED_UNUSED_CODE: RPCSendMsg = (
# REMOVED_UNUSED_CODE:     RPCStatusMsg
# REMOVED_UNUSED_CODE:     | RPCStrategyMsg
# REMOVED_UNUSED_CODE:     | RPCProtectionMsg
# REMOVED_UNUSED_CODE:     | RPCWhitelistMsg
# REMOVED_UNUSED_CODE:     | RPCEntryMsg
# REMOVED_UNUSED_CODE:     | RPCCancelMsg
# REMOVED_UNUSED_CODE:     | RPCExitMsg
# REMOVED_UNUSED_CODE:     | RPCExitCancelMsg
# REMOVED_UNUSED_CODE:     | RPCAnalyzedDFMsg
# REMOVED_UNUSED_CODE:     | RPCNewCandleMsg
# REMOVED_UNUSED_CODE: )
