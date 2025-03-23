from datetime import datetime
from typing import Any, TypedDict

from pandas import DataFrame
from pydantic import BaseModel, ConfigDict

from freqtrade.constants import PairWithTimeframe
from freqtrade.enums import RPCMessageType, RPCRequestType


class BaseArbitraryModel(BaseModel):
# REMOVED_UNUSED_CODE:     model_config = ConfigDict(arbitrary_types_allowed=True)


class WSRequestSchema(BaseArbitraryModel):
# REMOVED_UNUSED_CODE:     type: RPCRequestType
# REMOVED_UNUSED_CODE:     data: Any | None = None


# REMOVED_UNUSED_CODE: class WSMessageSchemaType(TypedDict):
# REMOVED_UNUSED_CODE:     # Type for typing to avoid doing pydantic typechecks.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     type: RPCMessageType
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     data: dict[str, Any] | None


class WSMessageSchema(BaseArbitraryModel):
# REMOVED_UNUSED_CODE:     type: RPCMessageType
# REMOVED_UNUSED_CODE:     data: Any | None = None
# REMOVED_UNUSED_CODE:     model_config = ConfigDict(extra="allow")


# ------------------------------ REQUEST SCHEMAS ----------------------------


# REMOVED_UNUSED_CODE: class WSSubscribeRequest(WSRequestSchema):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     type: RPCRequestType = RPCRequestType.SUBSCRIBE
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     data: list[RPCMessageType]


# REMOVED_UNUSED_CODE: class WSWhitelistRequest(WSRequestSchema):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     type: RPCRequestType = RPCRequestType.WHITELIST
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     data: None = None


# REMOVED_UNUSED_CODE: class WSAnalyzedDFRequest(WSRequestSchema):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     type: RPCRequestType = RPCRequestType.ANALYZED_DF
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     data: dict[str, Any] = {"limit": 1500, "pair": None}


# ------------------------------ MESSAGE SCHEMAS ----------------------------


# REMOVED_UNUSED_CODE: class WSWhitelistMessage(WSMessageSchema):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     type: RPCMessageType = RPCMessageType.WHITELIST
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     data: list[str]


# REMOVED_UNUSED_CODE: class WSAnalyzedDFMessage(WSMessageSchema):
# REMOVED_UNUSED_CODE:     class AnalyzedDFData(BaseArbitraryModel):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         key: PairWithTimeframe
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         df: DataFrame
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         la: datetime
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     type: RPCMessageType = RPCMessageType.ANALYZED_DF
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     data: AnalyzedDFData


# REMOVED_UNUSED_CODE: class WSErrorMessage(WSMessageSchema):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     type: RPCMessageType = RPCMessageType.EXCEPTION
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     data: str


# --------------------------------------------------------------------------
