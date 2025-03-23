import logging
import time
from typing import Any

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from fastapi import APIRouter, Depends
# REMOVED_UNUSED_CODE: from fastapi.websockets import WebSocket
from pydantic import ValidationError

from freqtrade.enums import RPCMessageType, RPCRequestType
from freqtrade.exceptions import FreqtradeException
# REMOVED_UNUSED_CODE: from freqtrade.rpc.api_server.api_auth import validate_ws_token
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.rpc.api_server.deps import get_message_stream, get_rpc
# REMOVED_UNUSED_CODE: from freqtrade.rpc.api_server.ws.channel import WebSocketChannel, create_channel
from freqtrade.rpc.api_server.ws.message_stream import MessageStream
from freqtrade.rpc.api_server.ws_schemas import (
    WSAnalyzedDFMessage,
    WSErrorMessage,
    WSMessageSchema,
    WSRequestSchema,
    WSWhitelistMessage,
)
from freqtrade.rpc.rpc import RPC


logger = logging.getLogger(__name__)

# Private router, protected by API Key authentication
# REMOVED_UNUSED_CODE: router = APIRouter()


# REMOVED_UNUSED_CODE: async def channel_reader(channel: WebSocketChannel, rpc: RPC):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Iterate over the messages from the channel and process the request
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     async for message in channel:
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             await _process_consumer_request(message, channel, rpc)
# REMOVED_UNUSED_CODE:         except FreqtradeException:
# REMOVED_UNUSED_CODE:             logger.exception(f"Error processing request from {channel}")
# REMOVED_UNUSED_CODE:             response = WSErrorMessage(data="Error processing request")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             await channel.send(response.dict(exclude_none=True))


# REMOVED_UNUSED_CODE: async def channel_broadcaster(channel: WebSocketChannel, message_stream: MessageStream):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Iterate over messages in the message stream and send them
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     async for message, ts in message_stream:
# REMOVED_UNUSED_CODE:         if channel.subscribed_to(message.get("type")):
# REMOVED_UNUSED_CODE:             # Log a warning if this channel is behind
# REMOVED_UNUSED_CODE:             # on the message stream by a lot
# REMOVED_UNUSED_CODE:             if (time.time() - ts) > 60:
# REMOVED_UNUSED_CODE:                 logger.warning(
# REMOVED_UNUSED_CODE:                     f"Channel {channel} is behind MessageStream by 1 minute,"
# REMOVED_UNUSED_CODE:                     " this can cause a memory leak if you see this message"
# REMOVED_UNUSED_CODE:                     " often, consider reducing pair list size or amount of"
# REMOVED_UNUSED_CODE:                     " consumers."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             await channel.send(message, use_timeout=True)


async def _process_consumer_request(request: dict[str, Any], channel: WebSocketChannel, rpc: RPC):
    """
    Validate and handle a request from a websocket consumer
    """
    # Validate the request, makes sure it matches the schema
    try:
        websocket_request = WSRequestSchema.model_validate(request)
    except ValidationError as e:
        logger.error(f"Invalid request from {channel}: {e}")
        return

    type_, data = websocket_request.type, websocket_request.data
    response: WSMessageSchema

    logger.debug(f"Request of type {type_} from {channel}")

    # If we have a request of type SUBSCRIBE, set the topics in this channel
    if type_ == RPCRequestType.SUBSCRIBE:
        # If the request is empty, do nothing
        if not data:
            return

        # If all topics passed are a valid RPCMessageType, set subscriptions on channel
        if all([any(x.value == topic for x in RPCMessageType) for topic in data]):
            channel.set_subscriptions(data)

        # We don't send a response for subscriptions
        return

    elif type_ == RPCRequestType.WHITELIST:
        # Get whitelist
        whitelist = rpc._ws_request_whitelist()

        # Format response
        response = WSWhitelistMessage(data=whitelist)
        await channel.send(response.model_dump(exclude_none=True))

    elif type_ == RPCRequestType.ANALYZED_DF:
        # Limit the amount of candles per dataframe to 'limit' or 1500
        limit = int(min(data.get("limit", 1500), 1500)) if data else None
        pair = data.get("pair", None) if data else None

        # For every pair in the generator, send a separate message
        for message in rpc._ws_request_analyzed_df(limit, pair):
            # Format response
            response = WSAnalyzedDFMessage(data=message)
            await channel.send(response.model_dump(exclude_none=True))


# REMOVED_UNUSED_CODE: @router.websocket("/message/ws")
# REMOVED_UNUSED_CODE: async def message_endpoint(
# REMOVED_UNUSED_CODE:     websocket: WebSocket,
# REMOVED_UNUSED_CODE:     token: str = Depends(validate_ws_token),
# REMOVED_UNUSED_CODE:     rpc: RPC = Depends(get_rpc),
# REMOVED_UNUSED_CODE:     message_stream: MessageStream = Depends(get_message_stream),
# REMOVED_UNUSED_CODE: ):
# REMOVED_UNUSED_CODE:     if token:
# REMOVED_UNUSED_CODE:         async with create_channel(websocket) as channel:
# REMOVED_UNUSED_CODE:             await channel.run_channel_tasks(
# REMOVED_UNUSED_CODE:                 channel_reader(channel, rpc), channel_broadcaster(channel, message_stream)
# REMOVED_UNUSED_CODE:             )
