import logging
# REMOVED_UNUSED_CODE: from copy import deepcopy

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from fastapi import APIRouter, Depends, HTTPException

# REMOVED_UNUSED_CODE: from freqtrade.configuration import validate_config_consistency
# REMOVED_UNUSED_CODE: from freqtrade.rpc.api_server.api_pairlists import handleExchangePayload
# REMOVED_UNUSED_CODE: from freqtrade.rpc.api_server.api_schemas import PairHistory, PairHistoryRequest
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.rpc.api_server.deps import get_config, get_exchange
# REMOVED_UNUSED_CODE: from freqtrade.rpc.rpc import RPC


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)

# REMOVED_UNUSED_CODE: router = APIRouter()


# REMOVED_UNUSED_CODE: @router.get("/pair_history", response_model=PairHistory, tags=["candle data"])
# REMOVED_UNUSED_CODE: def pair_history(
# REMOVED_UNUSED_CODE:     pair: str,
# REMOVED_UNUSED_CODE:     timeframe: str,
# REMOVED_UNUSED_CODE:     timerange: str,
# REMOVED_UNUSED_CODE:     strategy: str,
# REMOVED_UNUSED_CODE:     freqaimodel: str | None = None,
# REMOVED_UNUSED_CODE:     config=Depends(get_config),
# REMOVED_UNUSED_CODE:     exchange=Depends(get_exchange),
# REMOVED_UNUSED_CODE: ):
# REMOVED_UNUSED_CODE:     # The initial call to this endpoint can be slow, as it may need to initialize
# REMOVED_UNUSED_CODE:     # the exchange class.
# REMOVED_UNUSED_CODE:     config_loc = deepcopy(config)
# REMOVED_UNUSED_CODE:     config_loc.update(
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "timeframe": timeframe,
# REMOVED_UNUSED_CODE:             "strategy": strategy,
# REMOVED_UNUSED_CODE:             "timerange": timerange,
# REMOVED_UNUSED_CODE:             "freqaimodel": freqaimodel if freqaimodel else config_loc.get("freqaimodel"),
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     validate_config_consistency(config_loc)
# REMOVED_UNUSED_CODE:     try:
# REMOVED_UNUSED_CODE:         return RPC._rpc_analysed_history_full(config_loc, pair, timeframe, exchange, None, False)
# REMOVED_UNUSED_CODE:     except Exception as e:
# REMOVED_UNUSED_CODE:         raise HTTPException(status_code=502, detail=str(e))


# REMOVED_UNUSED_CODE: @router.post("/pair_history", response_model=PairHistory, tags=["candle data"])
# REMOVED_UNUSED_CODE: def pair_history_filtered(payload: PairHistoryRequest, config=Depends(get_config)):
# REMOVED_UNUSED_CODE:     # The initial call to this endpoint can be slow, as it may need to initialize
# REMOVED_UNUSED_CODE:     # the exchange class.
# REMOVED_UNUSED_CODE:     config_loc = deepcopy(config)
# REMOVED_UNUSED_CODE:     config_loc.update(
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "timeframe": payload.timeframe,
# REMOVED_UNUSED_CODE:             "strategy": payload.strategy,
# REMOVED_UNUSED_CODE:             "timerange": payload.timerange,
# REMOVED_UNUSED_CODE:             "freqaimodel": (
# REMOVED_UNUSED_CODE:                 payload.freqaimodel if payload.freqaimodel else config_loc.get("freqaimodel")
# REMOVED_UNUSED_CODE:             ),
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     handleExchangePayload(payload, config_loc)
# REMOVED_UNUSED_CODE:     exchange = get_exchange(config_loc)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     validate_config_consistency(config_loc)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     try:
# REMOVED_UNUSED_CODE:         return RPC._rpc_analysed_history_full(
# REMOVED_UNUSED_CODE:             config_loc,
# REMOVED_UNUSED_CODE:             payload.pair,
# REMOVED_UNUSED_CODE:             payload.timeframe,
# REMOVED_UNUSED_CODE:             exchange,
# REMOVED_UNUSED_CODE:             payload.columns,
# REMOVED_UNUSED_CODE:             payload.live_mode,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:     except Exception as e:
# REMOVED_UNUSED_CODE:         logger.exception("Error in pair_history_filtered")
# REMOVED_UNUSED_CODE:         raise HTTPException(status_code=502, detail=str(e))
