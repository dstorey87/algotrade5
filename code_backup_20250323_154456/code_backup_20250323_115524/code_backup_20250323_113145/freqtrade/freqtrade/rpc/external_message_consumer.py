"""
ExternalMessageConsumer module

Main purpose is to connect to external bot's message websocket to consume data
from it
"""

import asyncio
import logging
import socket
from collections.abc import Callable
from threading import Thread
from typing import Any, TypedDict

import websockets
from pydantic import ValidationError

from freqtrade.constants import FULL_DATAFRAME_THRESHOLD
from freqtrade.data.dataprovider import DataProvider
from freqtrade.enums import RPCMessageType
from freqtrade.misc import remove_entry_exit_signals
from freqtrade.rpc.api_server.ws.channel import WebSocketChannel, create_channel
from freqtrade.rpc.api_server.ws.message_stream import MessageStream
from freqtrade.rpc.api_server.ws_schemas import (
    WSAnalyzedDFMessage,
    WSAnalyzedDFRequest,
    WSMessageSchema,
    WSRequestSchema,
    WSSubscribeRequest,
    WSWhitelistMessage,
    WSWhitelistRequest,
)


class Producer(TypedDict):
    name: str
    host: str
    port: int
# REMOVED_UNUSED_CODE:     secure: bool
# REMOVED_UNUSED_CODE:     ws_token: str


logger = logging.getLogger(__name__)


def schema_to_dict(schema: WSMessageSchema | WSRequestSchema):
    return schema.model_dump(exclude_none=True)


# REMOVED_UNUSED_CODE: class ExternalMessageConsumer:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     The main controller class for consuming external messages from
# REMOVED_UNUSED_CODE:     other freqtrade bot's
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, config: dict[str, Any], dataprovider: DataProvider):
# REMOVED_UNUSED_CODE:         self._config = config
# REMOVED_UNUSED_CODE:         self._dp = dataprovider
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._running = False
# REMOVED_UNUSED_CODE:         self._thread = None
# REMOVED_UNUSED_CODE:         self._loop = None
# REMOVED_UNUSED_CODE:         self._main_task = None
# REMOVED_UNUSED_CODE:         self._sub_tasks = None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._emc_config = self._config.get("external_message_consumer", {})
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.enabled = self._emc_config.get("enabled", False)
# REMOVED_UNUSED_CODE:         self.producers: list[Producer] = self._emc_config.get("producers", [])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.wait_timeout = self._emc_config.get("wait_timeout", 30)  # in seconds
# REMOVED_UNUSED_CODE:         self.ping_timeout = self._emc_config.get("ping_timeout", 10)  # in seconds
# REMOVED_UNUSED_CODE:         self.sleep_time = self._emc_config.get("sleep_time", 10)  # in seconds
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # The amount of candles per dataframe on the initial request
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.initial_candle_limit = self._emc_config.get("initial_candle_limit", 1500)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Message size limit, in megabytes. Default 8mb, Use bitwise operator << 20 to convert
# REMOVED_UNUSED_CODE:         # as the websockets client expects bytes.
# REMOVED_UNUSED_CODE:         self.message_size_limit = self._emc_config.get("message_size_limit", 8) << 20
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Setting these explicitly as they probably shouldn't be changed by a user
# REMOVED_UNUSED_CODE:         # Unless we somehow integrate this with the strategy to allow creating
# REMOVED_UNUSED_CODE:         # callbacks for the messages
# REMOVED_UNUSED_CODE:         self.topics = [RPCMessageType.WHITELIST, RPCMessageType.ANALYZED_DF]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Allow setting data for each initial request
# REMOVED_UNUSED_CODE:         self._initial_requests: list[WSRequestSchema] = [
# REMOVED_UNUSED_CODE:             WSSubscribeRequest(data=self.topics),
# REMOVED_UNUSED_CODE:             WSWhitelistRequest(),
# REMOVED_UNUSED_CODE:             WSAnalyzedDFRequest(),
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Specify which function to use for which RPCMessageType
# REMOVED_UNUSED_CODE:         self._message_handlers: dict[str, Callable[[str, WSMessageSchema], None]] = {
# REMOVED_UNUSED_CODE:             RPCMessageType.WHITELIST: self._consume_whitelist_message,
# REMOVED_UNUSED_CODE:             RPCMessageType.ANALYZED_DF: self._consume_analyzed_df_message,
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._channel_streams: dict[str, MessageStream] = {}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.start()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def start(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Start the main internal loop in another thread to run coroutines
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if self._thread and self._loop:
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         logger.info("Starting ExternalMessageConsumer")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._loop = asyncio.new_event_loop()
# REMOVED_UNUSED_CODE:         self._thread = Thread(target=self._loop.run_forever)
# REMOVED_UNUSED_CODE:         self._running = True
# REMOVED_UNUSED_CODE:         self._thread.start()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._main_task = asyncio.run_coroutine_threadsafe(self._main(), loop=self._loop)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def shutdown(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Shutdown the loop, thread, and tasks
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._thread and self._loop:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             logger.info("Stopping ExternalMessageConsumer")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._running = False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._channel_streams = {}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if self._sub_tasks:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # Cancel sub tasks
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 for task in self._sub_tasks:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     task.cancel()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if self._main_task:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # Cancel the main task
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self._main_task.cancel()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._thread.join()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._thread = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._loop = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._sub_tasks = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._main_task = None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def _main(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         The main task coroutine
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         lock = asyncio.Lock()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             # Create a connection to each producer
# REMOVED_UNUSED_CODE:             self._sub_tasks = [
# REMOVED_UNUSED_CODE:                 self._loop.create_task(self._handle_producer_connection(producer, lock))
# REMOVED_UNUSED_CODE:                 for producer in self.producers
# REMOVED_UNUSED_CODE:             ]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             await asyncio.gather(*self._sub_tasks)
# REMOVED_UNUSED_CODE:         except asyncio.CancelledError:
# REMOVED_UNUSED_CODE:             pass
# REMOVED_UNUSED_CODE:         finally:
# REMOVED_UNUSED_CODE:             # Stop the loop once we are done
# REMOVED_UNUSED_CODE:             self._loop.stop()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def _handle_producer_connection(self, producer: Producer, lock: asyncio.Lock):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Main connection loop for the consumer
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         :param producer: Dictionary containing producer info
# REMOVED_UNUSED_CODE:         :param lock: An asyncio Lock
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             await self._create_connection(producer, lock)
# REMOVED_UNUSED_CODE:         except asyncio.CancelledError:
# REMOVED_UNUSED_CODE:             # Exit silently
# REMOVED_UNUSED_CODE:             pass
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def _create_connection(self, producer: Producer, lock: asyncio.Lock):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Actually creates and handles the websocket connection, pinging on timeout
# REMOVED_UNUSED_CODE:         and handling connection errors.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         :param producer: Dictionary containing producer info
# REMOVED_UNUSED_CODE:         :param lock: An asyncio Lock
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         while self._running:
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 host, port = producer["host"], producer["port"]
# REMOVED_UNUSED_CODE:                 token = producer["ws_token"]
# REMOVED_UNUSED_CODE:                 name = producer["name"]
# REMOVED_UNUSED_CODE:                 scheme = "wss" if producer.get("secure", False) else "ws"
# REMOVED_UNUSED_CODE:                 ws_url = f"{scheme}://{host}:{port}/api/v1/message/ws?token={token}"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 # This will raise InvalidURI if the url is bad
# REMOVED_UNUSED_CODE:                 async with websockets.connect(
# REMOVED_UNUSED_CODE:                     ws_url, max_size=self.message_size_limit, ping_interval=None
# REMOVED_UNUSED_CODE:                 ) as ws:
# REMOVED_UNUSED_CODE:                     async with create_channel(ws, channel_id=name, send_throttle=0.5) as channel:
# REMOVED_UNUSED_CODE:                         # Create the message stream for this channel
# REMOVED_UNUSED_CODE:                         self._channel_streams[name] = MessageStream()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                         # Run the channel tasks while connected
# REMOVED_UNUSED_CODE:                         await channel.run_channel_tasks(
# REMOVED_UNUSED_CODE:                             self._receive_messages(channel, producer, lock),
# REMOVED_UNUSED_CODE:                             self._send_requests(channel, self._channel_streams[name]),
# REMOVED_UNUSED_CODE:                         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             except (websockets.exceptions.InvalidURI, ValueError) as e:
# REMOVED_UNUSED_CODE:                 logger.error(f"{ws_url} is an invalid WebSocket URL - {e}")
# REMOVED_UNUSED_CODE:                 break
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             except (
# REMOVED_UNUSED_CODE:                 socket.gaierror,
# REMOVED_UNUSED_CODE:                 ConnectionRefusedError,
# REMOVED_UNUSED_CODE:                 websockets.exceptions.InvalidHandshake,
# REMOVED_UNUSED_CODE:             ) as e:
# REMOVED_UNUSED_CODE:                 logger.error(f"Connection Refused - {e} retrying in {self.sleep_time}s")
# REMOVED_UNUSED_CODE:                 await asyncio.sleep(self.sleep_time)
# REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             except (
# REMOVED_UNUSED_CODE:                 websockets.exceptions.ConnectionClosedError,
# REMOVED_UNUSED_CODE:                 websockets.exceptions.ConnectionClosedOK,
# REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE:                 # Just keep trying to connect again indefinitely
# REMOVED_UNUSED_CODE:                 await asyncio.sleep(self.sleep_time)
# REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             except Exception as e:
# REMOVED_UNUSED_CODE:                 # An unforeseen error has occurred, log and continue
# REMOVED_UNUSED_CODE:                 logger.error("Unexpected error has occurred:")
# REMOVED_UNUSED_CODE:                 logger.exception(e)
# REMOVED_UNUSED_CODE:                 await asyncio.sleep(self.sleep_time)
# REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def _send_requests(self, channel: WebSocketChannel, channel_stream: MessageStream):
# REMOVED_UNUSED_CODE:         # Send the initial requests
# REMOVED_UNUSED_CODE:         for init_request in self._initial_requests:
# REMOVED_UNUSED_CODE:             await channel.send(schema_to_dict(init_request))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Now send any subsequent requests published to
# REMOVED_UNUSED_CODE:         # this channel's stream
# REMOVED_UNUSED_CODE:         async for request, _ in channel_stream:
# REMOVED_UNUSED_CODE:             logger.debug(f"Sending request to channel - {channel} - {request}")
# REMOVED_UNUSED_CODE:             await channel.send(request)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def _receive_messages(
# REMOVED_UNUSED_CODE:         self, channel: WebSocketChannel, producer: Producer, lock: asyncio.Lock
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Loop to handle receiving messages from a Producer
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         :param channel: The WebSocketChannel object for the WebSocket
# REMOVED_UNUSED_CODE:         :param producer: Dictionary containing producer info
# REMOVED_UNUSED_CODE:         :param lock: An asyncio Lock
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         while self._running:
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 message = await asyncio.wait_for(channel.recv(), timeout=self.wait_timeout)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 try:
# REMOVED_UNUSED_CODE:                     async with lock:
# REMOVED_UNUSED_CODE:                         # Handle the message
# REMOVED_UNUSED_CODE:                         self.handle_producer_message(producer, message)
# REMOVED_UNUSED_CODE:                 except Exception as e:
# REMOVED_UNUSED_CODE:                     logger.exception(f"Error handling producer message: {e}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed):
# REMOVED_UNUSED_CODE:                 # We haven't received data yet. Check the connection and continue.
# REMOVED_UNUSED_CODE:                 try:
# REMOVED_UNUSED_CODE:                     # ping
# REMOVED_UNUSED_CODE:                     pong = await channel.ping()
# REMOVED_UNUSED_CODE:                     latency = await asyncio.wait_for(pong, timeout=self.ping_timeout) * 1000
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                     logger.info(f"Connection to {channel} still alive, latency: {latency}ms")
# REMOVED_UNUSED_CODE:                     continue
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 except Exception as e:
# REMOVED_UNUSED_CODE:                     # Just eat the error and continue reconnecting
# REMOVED_UNUSED_CODE:                     logger.warning(f"Ping error {channel} - {e} - retrying in {self.sleep_time}s")
# REMOVED_UNUSED_CODE:                     logger.debug(e, exc_info=e)
# REMOVED_UNUSED_CODE:                     raise
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def send_producer_request(self, producer_name: str, request: WSRequestSchema | dict[str, Any]):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Publish a message to the producer's message stream to be
# REMOVED_UNUSED_CODE:         sent by the channel task.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         :param producer_name: The name of the producer to publish the message to
# REMOVED_UNUSED_CODE:         :param request: The request to send to the producer
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if isinstance(request, WSRequestSchema):
# REMOVED_UNUSED_CODE:             request = schema_to_dict(request)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if channel_stream := self._channel_streams.get(producer_name):
# REMOVED_UNUSED_CODE:             channel_stream.publish(request)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def handle_producer_message(self, producer: Producer, message: dict[str, Any]):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Handles external messages from a Producer
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         producer_name = producer.get("name", "default")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             producer_message = WSMessageSchema.model_validate(message)
# REMOVED_UNUSED_CODE:         except ValidationError as e:
# REMOVED_UNUSED_CODE:             logger.error(f"Invalid message from `{producer_name}`: {e}")
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not producer_message.data:
# REMOVED_UNUSED_CODE:             logger.error(f"Empty message received from `{producer_name}`")
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         logger.debug(f"Received message of type `{producer_message.type}` from `{producer_name}`")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         message_handler = self._message_handlers.get(producer_message.type)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not message_handler:
# REMOVED_UNUSED_CODE:             logger.info(f"Received unhandled message: `{producer_message.data}`, ignoring...")
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         message_handler(producer_name, producer_message)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _consume_whitelist_message(self, producer_name: str, message: WSMessageSchema):
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             # Validate the message
# REMOVED_UNUSED_CODE:             whitelist_message = WSWhitelistMessage.model_validate(message.model_dump())
# REMOVED_UNUSED_CODE:         except ValidationError as e:
# REMOVED_UNUSED_CODE:             logger.error(f"Invalid message from `{producer_name}`: {e}")
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Add the pairlist data to the DataProvider
# REMOVED_UNUSED_CODE:         self._dp._set_producer_pairs(whitelist_message.data, producer_name=producer_name)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         logger.debug(f"Consumed message from `{producer_name}` of type `RPCMessageType.WHITELIST`")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _consume_analyzed_df_message(self, producer_name: str, message: WSMessageSchema):
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             df_message = WSAnalyzedDFMessage.model_validate(message.model_dump())
# REMOVED_UNUSED_CODE:         except ValidationError as e:
# REMOVED_UNUSED_CODE:             logger.error(f"Invalid message from `{producer_name}`: {e}")
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         key = df_message.data.key
# REMOVED_UNUSED_CODE:         df = df_message.data.df
# REMOVED_UNUSED_CODE:         la = df_message.data.la
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         pair, timeframe, candle_type = key
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if df.empty:
# REMOVED_UNUSED_CODE:             logger.debug(f"Received Empty Dataframe for {key}")
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # If set, remove the Entry and Exit signals from the Producer
# REMOVED_UNUSED_CODE:         if self._emc_config.get("remove_entry_exit_signals", False):
# REMOVED_UNUSED_CODE:             df = remove_entry_exit_signals(df)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         logger.debug(f"Received {len(df)} candle(s) for {key}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         did_append, n_missing = self._dp._add_external_df(
# REMOVED_UNUSED_CODE:             pair,
# REMOVED_UNUSED_CODE:             df,
# REMOVED_UNUSED_CODE:             last_analyzed=la,
# REMOVED_UNUSED_CODE:             timeframe=timeframe,
# REMOVED_UNUSED_CODE:             candle_type=candle_type,
# REMOVED_UNUSED_CODE:             producer_name=producer_name,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not did_append:
# REMOVED_UNUSED_CODE:             # We want an overlap in candles in case some data has changed
# REMOVED_UNUSED_CODE:             n_missing += 1
# REMOVED_UNUSED_CODE:             # Set to None for all candles if we missed a full df's worth of candles
# REMOVED_UNUSED_CODE:             n_missing = n_missing if n_missing < FULL_DATAFRAME_THRESHOLD else 1500
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             logger.warning(
# REMOVED_UNUSED_CODE:                 f"Holes in data or no existing df, requesting {n_missing} candles "
# REMOVED_UNUSED_CODE:                 f"for {key} from `{producer_name}`"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             self.send_producer_request(
# REMOVED_UNUSED_CODE:                 producer_name, WSAnalyzedDFRequest(data={"limit": n_missing, "pair": pair})
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         logger.debug(
# REMOVED_UNUSED_CODE:             f"Consumed message from `{producer_name}` "
# REMOVED_UNUSED_CODE:             f"of type `RPCMessageType.ANALYZED_DF` for {key}"
# REMOVED_UNUSED_CODE:         )
