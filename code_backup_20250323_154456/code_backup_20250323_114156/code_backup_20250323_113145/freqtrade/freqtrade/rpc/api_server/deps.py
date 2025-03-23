from collections.abc import AsyncIterator
from typing import Any
from uuid import uuid4

from fastapi import Depends, HTTPException

from freqtrade.constants import Config
from freqtrade.enums import RunMode
from freqtrade.persistence import Trade
from freqtrade.persistence.models import _request_id_ctx_var
from freqtrade.rpc.api_server.webserver_bgwork import ApiBG
from freqtrade.rpc.rpc import RPC, RPCException

from .webserver import ApiServer


def get_rpc_optional() -> RPC | None:
    if ApiServer._has_rpc:
        return ApiServer._rpc
    return None


# REMOVED_UNUSED_CODE: async def get_rpc() -> AsyncIterator[RPC] | None:
# REMOVED_UNUSED_CODE:     _rpc = get_rpc_optional()
# REMOVED_UNUSED_CODE:     if _rpc:
# REMOVED_UNUSED_CODE:         request_id = str(uuid4())
# REMOVED_UNUSED_CODE:         ctx_token = _request_id_ctx_var.set(request_id)
# REMOVED_UNUSED_CODE:         Trade.rollback()
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             yield _rpc
# REMOVED_UNUSED_CODE:         finally:
# REMOVED_UNUSED_CODE:             Trade.session.remove()
# REMOVED_UNUSED_CODE:             _request_id_ctx_var.reset(ctx_token)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         raise RPCException("Bot is not in the correct state")


def get_config() -> dict[str, Any]:
    return ApiServer._config


# REMOVED_UNUSED_CODE: def get_api_config() -> dict[str, Any]:
# REMOVED_UNUSED_CODE:     return ApiServer._config["api_server"]


def _generate_exchange_key(config: Config) -> str:
    """
    Exchange key - used for caching the exchange object.
    """
    return f"{config['exchange']['name']}_{config.get('trading_mode', 'spot')}"


# REMOVED_UNUSED_CODE: def get_exchange(config=Depends(get_config)):
# REMOVED_UNUSED_CODE:     exchange_key = _generate_exchange_key(config)
# REMOVED_UNUSED_CODE:     if not (exchange := ApiBG.exchanges.get(exchange_key)):
# REMOVED_UNUSED_CODE:         from freqtrade.resolvers import ExchangeResolver
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         exchange = ExchangeResolver.load_exchange(config, validate=False, load_leverage_tiers=False)
# REMOVED_UNUSED_CODE:         ApiBG.exchanges[exchange_key] = exchange
# REMOVED_UNUSED_CODE:     return exchange


# REMOVED_UNUSED_CODE: def get_message_stream():
# REMOVED_UNUSED_CODE:     return ApiServer._message_stream


# REMOVED_UNUSED_CODE: def is_webserver_mode(config=Depends(get_config)):
# REMOVED_UNUSED_CODE:     if config["runmode"] != RunMode.WEBSERVER:
# REMOVED_UNUSED_CODE:         raise HTTPException(status_code=503, detail="Bot is not in the correct state.")
# REMOVED_UNUSED_CODE:     return None
