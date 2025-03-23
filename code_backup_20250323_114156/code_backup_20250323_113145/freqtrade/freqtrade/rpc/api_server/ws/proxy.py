# REMOVED_UNUSED_CODE: from typing import Any

# REMOVED_UNUSED_CODE: from fastapi import WebSocket as FastAPIWebSocket
from websockets.asyncio.client import ClientConnection as WebSocket

# REMOVED_UNUSED_CODE: from freqtrade.rpc.api_server.ws.ws_types import WebSocketType


# REMOVED_UNUSED_CODE: class WebSocketProxy:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     WebSocketProxy object to bring the FastAPIWebSocket and websockets.WebSocketClientProtocol
# REMOVED_UNUSED_CODE:     under the same API
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, websocket: WebSocketType):
# REMOVED_UNUSED_CODE:         self._websocket: FastAPIWebSocket | WebSocket = websocket
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def raw_websocket(self):
# REMOVED_UNUSED_CODE:         return self._websocket
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def remote_addr(self) -> tuple[Any, ...]:
# REMOVED_UNUSED_CODE:         if isinstance(self._websocket, WebSocket):
# REMOVED_UNUSED_CODE:             return self._websocket.remote_address
# REMOVED_UNUSED_CODE:         elif isinstance(self._websocket, FastAPIWebSocket):
# REMOVED_UNUSED_CODE:             if self._websocket.client:
# REMOVED_UNUSED_CODE:                 client, port = self._websocket.client.host, self._websocket.client.port
# REMOVED_UNUSED_CODE:                 return (client, port)
# REMOVED_UNUSED_CODE:         return ("unknown", 0)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def send(self, data):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Send data on the wrapped websocket
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if hasattr(self._websocket, "send_text"):
# REMOVED_UNUSED_CODE:             await self._websocket.send_text(data)
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             await self._websocket.send(data)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def recv(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Receive data on the wrapped websocket
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if hasattr(self._websocket, "receive_text"):
# REMOVED_UNUSED_CODE:             return await self._websocket.receive_text()
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             return await self._websocket.recv()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def ping(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Ping the websocket, not supported by FastAPI WebSockets
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if hasattr(self._websocket, "ping"):
# REMOVED_UNUSED_CODE:             return await self._websocket.ping()
# REMOVED_UNUSED_CODE:         return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def close(self, code: int = 1000):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Close the websocket connection, only supported by FastAPI WebSockets
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if hasattr(self._websocket, "close"):
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 return await self._websocket.close(code)
# REMOVED_UNUSED_CODE:             except RuntimeError:
# REMOVED_UNUSED_CODE:                 pass
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def accept(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Accept the WebSocket connection, only support by FastAPI WebSockets
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if hasattr(self._websocket, "accept"):
# REMOVED_UNUSED_CODE:             return await self._websocket.accept()
