import asyncio
import logging
import time
from collections import deque
# REMOVED_UNUSED_CODE: from collections.abc import AsyncIterator
# REMOVED_UNUSED_CODE: from contextlib import asynccontextmanager
from typing import Any
from uuid import uuid4

# REMOVED_UNUSED_CODE: from fastapi import WebSocketDisconnect
# REMOVED_UNUSED_CODE: from websockets.exceptions import ConnectionClosed

from freqtrade.rpc.api_server.ws.proxy import WebSocketProxy
from freqtrade.rpc.api_server.ws.serializer import (
    HybridJSONWebSocketSerializer,
    WebSocketSerializer,
)
from freqtrade.rpc.api_server.ws.ws_types import WebSocketType
from freqtrade.rpc.api_server.ws_schemas import WSMessageSchemaType


logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class WebSocketChannel:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Object to help facilitate managing a websocket connection
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         websocket: WebSocketType,
# REMOVED_UNUSED_CODE:         channel_id: str | None = None,
# REMOVED_UNUSED_CODE:         serializer_cls: type[WebSocketSerializer] = HybridJSONWebSocketSerializer,
# REMOVED_UNUSED_CODE:         send_throttle: float = 0.01,
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         self.channel_id = channel_id if channel_id else uuid4().hex[:8]
# REMOVED_UNUSED_CODE:         self._websocket = WebSocketProxy(websocket)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Internal event to signify a closed websocket
# REMOVED_UNUSED_CODE:         self._closed = asyncio.Event()
# REMOVED_UNUSED_CODE:         # The async tasks created for the channel
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._channel_tasks: list[asyncio.Task] = []
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Deque for average send times
# REMOVED_UNUSED_CODE:         self._send_times: deque[float] = deque([], maxlen=10)
# REMOVED_UNUSED_CODE:         # High limit defaults to 3 to start
# REMOVED_UNUSED_CODE:         self._send_high_limit = 3
# REMOVED_UNUSED_CODE:         self._send_throttle = send_throttle
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # The subscribed message types
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._subscriptions: list[str] = []
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Wrap the WebSocket in the Serializing class
# REMOVED_UNUSED_CODE:         self._wrapped_ws = serializer_cls(self._websocket)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __repr__(self):
# REMOVED_UNUSED_CODE:         return f"WebSocketChannel({self.channel_id}, {self.remote_addr})"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def raw_websocket(self):
# REMOVED_UNUSED_CODE:         return self._websocket.raw_websocket
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def remote_addr(self):
# REMOVED_UNUSED_CODE:         return self._websocket.remote_addr
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def avg_send_time(self):
# REMOVED_UNUSED_CODE:         return sum(self._send_times) / len(self._send_times)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _calc_send_limit(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Calculate the send high limit for this channel
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Only update if we have enough data
# REMOVED_UNUSED_CODE:         if len(self._send_times) == self._send_times.maxlen:
# REMOVED_UNUSED_CODE:             # At least 1s or twice the average of send times, with a
# REMOVED_UNUSED_CODE:             # maximum of 3 seconds per message
# REMOVED_UNUSED_CODE:             self._send_high_limit = min(max(self.avg_send_time * 2, 1), 3)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def send(self, message: WSMessageSchemaType | dict[str, Any], use_timeout: bool = False):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Send a message on the wrapped websocket. If the sending
# REMOVED_UNUSED_CODE:         takes too long, it will raise a TimeoutError and
# REMOVED_UNUSED_CODE:         disconnect the connection.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         :param message: The message to send
# REMOVED_UNUSED_CODE:         :param use_timeout: Enforce send high limit, defaults to False
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             _ = time.time()
# REMOVED_UNUSED_CODE:             # If the send times out, it will raise
# REMOVED_UNUSED_CODE:             # a TimeoutError and bubble up to the
# REMOVED_UNUSED_CODE:             # message_endpoint to close the connection
# REMOVED_UNUSED_CODE:             await asyncio.wait_for(
# REMOVED_UNUSED_CODE:                 self._wrapped_ws.send(message),
# REMOVED_UNUSED_CODE:                 timeout=self._send_high_limit if use_timeout else None,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             total_time = time.time() - _
# REMOVED_UNUSED_CODE:             self._send_times.append(total_time)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             self._calc_send_limit()
# REMOVED_UNUSED_CODE:         except asyncio.TimeoutError:
# REMOVED_UNUSED_CODE:             logger.info(f"Connection for {self} timed out, disconnecting")
# REMOVED_UNUSED_CODE:             raise
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Explicitly give control back to event loop as
# REMOVED_UNUSED_CODE:         # websockets.send does not
# REMOVED_UNUSED_CODE:         # Also throttles how fast we send
# REMOVED_UNUSED_CODE:         await asyncio.sleep(self._send_throttle)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def recv(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Receive a message on the wrapped websocket
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return await self._wrapped_ws.recv()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def ping(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Ping the websocket
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return await self._websocket.ping()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def accept(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Accept the underlying websocket connection,
# REMOVED_UNUSED_CODE:         if the connection has been closed before we can
# REMOVED_UNUSED_CODE:         accept, just close the channel.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             return await self._websocket.accept()
# REMOVED_UNUSED_CODE:         except RuntimeError:
# REMOVED_UNUSED_CODE:             await self.close()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def close(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Close the WebSocketChannel
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._closed.set()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             await self._websocket.close()
# REMOVED_UNUSED_CODE:         except RuntimeError:
# REMOVED_UNUSED_CODE:             pass
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def is_closed(self) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Closed flag
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return self._closed.is_set()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def set_subscriptions(self, subscriptions: list[str]) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Set which subscriptions this channel is subscribed to
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param subscriptions: List of subscriptions, List[str]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._subscriptions = subscriptions
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def subscribed_to(self, message_type: str) -> bool:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Check if this channel is subscribed to the message_type
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param message_type: The message type to check
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return message_type in self._subscriptions
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     async def run_channel_tasks(self, *tasks, **kwargs):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Create and await on the channel tasks unless an exception
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         was raised, then cancel them all.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :params *tasks: All coros or tasks to be run concurrently
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param **kwargs: Any extra kwargs to pass to gather
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not self.is_closed():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Wrap the coros into tasks if they aren't already
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._channel_tasks = [
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 task if isinstance(task, asyncio.Task) else asyncio.create_task(task)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 for task in tasks
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return await asyncio.gather(*self._channel_tasks, **kwargs)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             except Exception:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # If an exception occurred, cancel the rest of the tasks
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 await self.cancel_channel_tasks()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     async def cancel_channel_tasks(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Cancel and wait on all channel tasks
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for task in self._channel_tasks:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             task.cancel()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Wait for tasks to finish cancelling
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 await task
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             except (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 asyncio.CancelledError,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 asyncio.TimeoutError,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 WebSocketDisconnect,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 ConnectionClosed,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 RuntimeError,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 pass
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             except Exception as e:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 logger.info(f"Encountered unknown exception: {e}", exc_info=e)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._channel_tasks = []
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def __aiter__(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Generator for received messages
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         # We can not catch any errors here as websocket.recv is
# REMOVED_UNUSED_CODE:         # the first to catch any disconnects and bubble it up
# REMOVED_UNUSED_CODE:         # so the connection is garbage collected right away
# REMOVED_UNUSED_CODE:         while not self.is_closed():
# REMOVED_UNUSED_CODE:             yield await self.recv()


# REMOVED_UNUSED_CODE: @asynccontextmanager
# REMOVED_UNUSED_CODE: async def create_channel(websocket: WebSocketType, **kwargs) -> AsyncIterator[WebSocketChannel]:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Context manager for safely opening and closing a WebSocketChannel
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     channel = WebSocketChannel(websocket, **kwargs)
# REMOVED_UNUSED_CODE:     try:
# REMOVED_UNUSED_CODE:         await channel.accept()
# REMOVED_UNUSED_CODE:         logger.info(f"Connected to channel - {channel}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         yield channel
# REMOVED_UNUSED_CODE:     finally:
# REMOVED_UNUSED_CODE:         await channel.close()
# REMOVED_UNUSED_CODE:         logger.info(f"Disconnected from channel - {channel}")
