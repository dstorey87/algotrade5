import logging
from copy import deepcopy

from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.exceptions import HTTPException

from freqtrade.constants import Config
from freqtrade.enums import CandleType
from freqtrade.exceptions import OperationalException
from freqtrade.persistence import FtNoDBContext
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.rpc.api_server.api_schemas import (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     BgJobStarted,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ExchangeModePayloadMixin,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     PairListsPayload,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     PairListsResponse,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     WhitelistEvaluateResponse,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: )
from freqtrade.rpc.api_server.deps import get_config, get_exchange
from freqtrade.rpc.api_server.webserver_bgwork import ApiBG


logger = logging.getLogger(__name__)

# Private API, protected by authentication and webserver_mode dependency
# REMOVED_UNUSED_CODE: router = APIRouter()


# REMOVED_UNUSED_CODE: @router.get(
# REMOVED_UNUSED_CODE:     "/pairlists/available", response_model=PairListsResponse, tags=["pairlists", "webserver"]
# REMOVED_UNUSED_CODE: )
# REMOVED_UNUSED_CODE: def list_pairlists(config=Depends(get_config)):
# REMOVED_UNUSED_CODE:     from freqtrade.resolvers import PairListResolver
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     pairlists = PairListResolver.search_all_objects(config, False)
# REMOVED_UNUSED_CODE:     pairlists = sorted(pairlists, key=lambda x: x["name"])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return {
# REMOVED_UNUSED_CODE:         "pairlists": [
# REMOVED_UNUSED_CODE:             {
# REMOVED_UNUSED_CODE:                 "name": x["name"],
# REMOVED_UNUSED_CODE:                 "is_pairlist_generator": x["class"].is_pairlist_generator,
# REMOVED_UNUSED_CODE:                 "params": x["class"].available_parameters(),
# REMOVED_UNUSED_CODE:                 "description": x["class"].description(),
# REMOVED_UNUSED_CODE:             }
# REMOVED_UNUSED_CODE:             for x in pairlists
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE:     }


def __run_pairlist(job_id: str, config_loc: Config):
    try:
        ApiBG.jobs[job_id]["is_running"] = True
        from freqtrade.plugins.pairlistmanager import PairListManager

        with FtNoDBContext():
            exchange = get_exchange(config_loc)
            pairlists = PairListManager(exchange, config_loc)
            pairlists.refresh_pairlist()
            ApiBG.jobs[job_id]["result"] = {
                "method": pairlists.name_list,
                "length": len(pairlists.whitelist),
                "whitelist": pairlists.whitelist,
            }
            ApiBG.jobs[job_id]["status"] = "success"
    except (OperationalException, Exception) as e:
        logger.exception(e)
        ApiBG.jobs[job_id]["error"] = str(e)
        ApiBG.jobs[job_id]["status"] = "failed"
    finally:
        ApiBG.jobs[job_id]["is_running"] = False
        ApiBG.pairlist_running = False


# REMOVED_UNUSED_CODE: @router.post("/pairlists/evaluate", response_model=BgJobStarted, tags=["pairlists", "webserver"])
# REMOVED_UNUSED_CODE: def pairlists_evaluate(
# REMOVED_UNUSED_CODE:     payload: PairListsPayload, background_tasks: BackgroundTasks, config=Depends(get_config)
# REMOVED_UNUSED_CODE: ):
# REMOVED_UNUSED_CODE:     if ApiBG.pairlist_running:
# REMOVED_UNUSED_CODE:         raise HTTPException(status_code=400, detail="Pairlist evaluation is already running.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     config_loc = deepcopy(config)
# REMOVED_UNUSED_CODE:     config_loc["stake_currency"] = payload.stake_currency
# REMOVED_UNUSED_CODE:     config_loc["pairlists"] = payload.pairlists
# REMOVED_UNUSED_CODE:     handleExchangePayload(payload, config_loc)
# REMOVED_UNUSED_CODE:     # TODO: overwrite blacklist? make it optional and fall back to the one in config?
# REMOVED_UNUSED_CODE:     # Outcome depends on the UI approach.
# REMOVED_UNUSED_CODE:     config_loc["exchange"]["pair_blacklist"] = payload.blacklist
# REMOVED_UNUSED_CODE:     # Random job id
# REMOVED_UNUSED_CODE:     job_id = ApiBG.get_job_id()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     ApiBG.jobs[job_id] = {
# REMOVED_UNUSED_CODE:         "category": "pairlist",
# REMOVED_UNUSED_CODE:         "status": "pending",
# REMOVED_UNUSED_CODE:         "progress": None,
# REMOVED_UNUSED_CODE:         "is_running": False,
# REMOVED_UNUSED_CODE:         "result": {},
# REMOVED_UNUSED_CODE:         "error": None,
# REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE:     background_tasks.add_task(__run_pairlist, job_id, config_loc)
# REMOVED_UNUSED_CODE:     ApiBG.pairlist_running = True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return {
# REMOVED_UNUSED_CODE:         "status": "Pairlist evaluation started in background.",
# REMOVED_UNUSED_CODE:         "job_id": job_id,
# REMOVED_UNUSED_CODE:     }


def handleExchangePayload(payload: ExchangeModePayloadMixin, config_loc: Config):
    """
    Handle exchange and trading mode payload.
    Updates the configuration with the payload values.
    """
    if payload.exchange:
        config_loc["exchange"]["name"] = payload.exchange
    if payload.trading_mode:
        config_loc["trading_mode"] = payload.trading_mode
        config_loc["candle_type_def"] = CandleType.get_default(
            config_loc.get("trading_mode", "spot") or "spot"
        )
    if payload.margin_mode:
        config_loc["margin_mode"] = payload.margin_mode


# REMOVED_UNUSED_CODE: @router.get(
# REMOVED_UNUSED_CODE:     "/pairlists/evaluate/{jobid}",
# REMOVED_UNUSED_CODE:     response_model=WhitelistEvaluateResponse,
# REMOVED_UNUSED_CODE:     tags=["pairlists", "webserver"],
# REMOVED_UNUSED_CODE: )
# REMOVED_UNUSED_CODE: def pairlists_evaluate_get(jobid: str):
# REMOVED_UNUSED_CODE:     if not (job := ApiBG.jobs.get(jobid)):
# REMOVED_UNUSED_CODE:         raise HTTPException(status_code=404, detail="Job not found.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if job["is_running"]:
# REMOVED_UNUSED_CODE:         raise HTTPException(status_code=400, detail="Job not finished yet.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if error := job["error"]:
# REMOVED_UNUSED_CODE:         return {
# REMOVED_UNUSED_CODE:             "status": "failed",
# REMOVED_UNUSED_CODE:             "error": error,
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return {
# REMOVED_UNUSED_CODE:         "status": "success",
# REMOVED_UNUSED_CODE:         "result": job["result"],
# REMOVED_UNUSED_CODE:     }
