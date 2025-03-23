import logging
from abc import ABC, abstractmethod
from typing import Any

# REMOVED_UNUSED_CODE: import orjson
# REMOVED_UNUSED_CODE: import rapidjson
from pandas import DataFrame

from freqtrade.misc import dataframe_to_json, json_to_dataframe
from freqtrade.rpc.api_server.ws.proxy import WebSocketProxy
from freqtrade.rpc.api_server.ws_schemas import WSMessageSchemaType


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class WebSocketSerializer(ABC):
# REMOVED_UNUSED_CODE:     def __init__(self, websocket: WebSocketProxy):
# REMOVED_UNUSED_CODE:         self._websocket: WebSocketProxy = websocket
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @abstractmethod
# REMOVED_UNUSED_CODE:     def _serialize(self, data):
# REMOVED_UNUSED_CODE:         raise NotImplementedError()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @abstractmethod
# REMOVED_UNUSED_CODE:     def _deserialize(self, data):
# REMOVED_UNUSED_CODE:         raise NotImplementedError()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def send(self, data: WSMessageSchemaType | dict[str, Any]):
# REMOVED_UNUSED_CODE:         await self._websocket.send(self._serialize(data))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def recv(self) -> bytes:
# REMOVED_UNUSED_CODE:         data = await self._websocket.recv()
# REMOVED_UNUSED_CODE:         return self._deserialize(data)


# REMOVED_UNUSED_CODE: class HybridJSONWebSocketSerializer(WebSocketSerializer):
# REMOVED_UNUSED_CODE:     def _serialize(self, data) -> str:
# REMOVED_UNUSED_CODE:         return str(orjson.dumps(data, default=_json_default), "utf-8")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _deserialize(self, data: str):
# REMOVED_UNUSED_CODE:         # RapidJSON expects strings
# REMOVED_UNUSED_CODE:         return rapidjson.loads(data, object_hook=_json_object_hook)


# Support serializing pandas DataFrames
# REMOVED_UNUSED_CODE: def _json_default(z):
# REMOVED_UNUSED_CODE:     if isinstance(z, DataFrame):
# REMOVED_UNUSED_CODE:         return {"__type__": "dataframe", "__value__": dataframe_to_json(z)}
# REMOVED_UNUSED_CODE:     raise TypeError


# Support deserializing JSON to pandas DataFrames
# REMOVED_UNUSED_CODE: def _json_object_hook(z):
# REMOVED_UNUSED_CODE:     if z.get("__type__") == "dataframe":
# REMOVED_UNUSED_CODE:         return json_to_dataframe(z.get("__value__"))
# REMOVED_UNUSED_CODE:     return z
