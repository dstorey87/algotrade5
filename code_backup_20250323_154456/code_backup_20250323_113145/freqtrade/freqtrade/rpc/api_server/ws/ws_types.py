# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from typing import Any, TypeVar

# REMOVED_UNUSED_CODE: from fastapi import WebSocket as FastAPIWebSocket
from websockets.asyncio.client import ClientConnection as WebSocket


# REMOVED_UNUSED_CODE: WebSocketType = TypeVar("WebSocketType", FastAPIWebSocket, WebSocket)
# REMOVED_UNUSED_CODE: MessageType = dict[str, Any]
