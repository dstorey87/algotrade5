import logging
# REMOVED_UNUSED_CODE: from copy import deepcopy

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from fastapi import APIRouter, BackgroundTasks, Depends
# REMOVED_UNUSED_CODE: from fastapi.exceptions import HTTPException

from freqtrade.constants import Config
from freqtrade.exceptions import OperationalException
from freqtrade.persistence import FtNoDBContext
# REMOVED_UNUSED_CODE: from freqtrade.rpc.api_server.api_pairlists import handleExchangePayload
# REMOVED_UNUSED_CODE: from freqtrade.rpc.api_server.api_schemas import BgJobStarted, DownloadDataPayload
# REMOVED_UNUSED_CODE: from freqtrade.rpc.api_server.deps import get_config, get_exchange
from freqtrade.rpc.api_server.webserver_bgwork import ApiBG
from freqtrade.util.progress_tracker import get_progress_tracker


logger = logging.getLogger(__name__)

# Private API, protected by authentication and webserver_mode dependency
# REMOVED_UNUSED_CODE: router = APIRouter(tags=["download-data", "webserver"])


# REMOVED_UNUSED_CODE: def __run_download(job_id: str, config_loc: Config):
# REMOVED_UNUSED_CODE:     try:
# REMOVED_UNUSED_CODE:         ApiBG.jobs[job_id]["is_running"] = True
# REMOVED_UNUSED_CODE:         from freqtrade.data.history.history_utils import download_data
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         with FtNoDBContext():
# REMOVED_UNUSED_CODE:             exchange = get_exchange(config_loc)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             def ft_callback(task) -> None:
# REMOVED_UNUSED_CODE:                 ApiBG.jobs[job_id]["progress_tasks"][str(task.id)] = {
# REMOVED_UNUSED_CODE:                     "progress": task.completed,
# REMOVED_UNUSED_CODE:                     "total": task.total,
# REMOVED_UNUSED_CODE:                     "description": task.description,
# REMOVED_UNUSED_CODE:                 }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             pt = get_progress_tracker(ft_callback=ft_callback)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             download_data(config_loc, exchange, progress_tracker=pt)
# REMOVED_UNUSED_CODE:             ApiBG.jobs[job_id]["status"] = "success"
# REMOVED_UNUSED_CODE:     except (OperationalException, Exception) as e:
# REMOVED_UNUSED_CODE:         logger.exception(e)
# REMOVED_UNUSED_CODE:         ApiBG.jobs[job_id]["error"] = str(e)
# REMOVED_UNUSED_CODE:         ApiBG.jobs[job_id]["status"] = "failed"
# REMOVED_UNUSED_CODE:     finally:
# REMOVED_UNUSED_CODE:         ApiBG.jobs[job_id]["is_running"] = False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ApiBG.download_data_running = False


# REMOVED_UNUSED_CODE: @router.post("/download_data", response_model=BgJobStarted)
# REMOVED_UNUSED_CODE: def pairlists_evaluate(
# REMOVED_UNUSED_CODE:     payload: DownloadDataPayload, background_tasks: BackgroundTasks, config=Depends(get_config)
# REMOVED_UNUSED_CODE: ):
# REMOVED_UNUSED_CODE:     if ApiBG.download_data_running:
# REMOVED_UNUSED_CODE:         raise HTTPException(status_code=400, detail="Data Download is already running.")
# REMOVED_UNUSED_CODE:     config_loc = deepcopy(config)
# REMOVED_UNUSED_CODE:     config_loc["stake_currency"] = ""
# REMOVED_UNUSED_CODE:     config_loc["pairs"] = payload.pairs
# REMOVED_UNUSED_CODE:     config_loc["timerange"] = payload.timerange
# REMOVED_UNUSED_CODE:     config_loc["days"] = payload.days
# REMOVED_UNUSED_CODE:     config_loc["timeframes"] = payload.timeframes
# REMOVED_UNUSED_CODE:     config_loc["erase"] = payload.erase
# REMOVED_UNUSED_CODE:     config_loc["download_trades"] = payload.download_trades
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     handleExchangePayload(payload, config_loc)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     job_id = ApiBG.get_job_id()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     ApiBG.jobs[job_id] = {
# REMOVED_UNUSED_CODE:         "category": "download_data",
# REMOVED_UNUSED_CODE:         "status": "pending",
# REMOVED_UNUSED_CODE:         "progress": None,
# REMOVED_UNUSED_CODE:         "progress_tasks": {},
# REMOVED_UNUSED_CODE:         "is_running": False,
# REMOVED_UNUSED_CODE:         "result": {},
# REMOVED_UNUSED_CODE:         "error": None,
# REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE:     background_tasks.add_task(__run_download, job_id, config_loc)
# REMOVED_UNUSED_CODE:     ApiBG.download_data_running = True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return {
# REMOVED_UNUSED_CODE:         "status": "Data Download started in background.",
# REMOVED_UNUSED_CODE:         "job_id": job_id,
# REMOVED_UNUSED_CODE:     }
