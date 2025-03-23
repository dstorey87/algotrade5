import asyncio
import logging
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.exceptions import HTTPException

from freqtrade.configuration.config_validation import validate_config_consistency
from freqtrade.constants import Config
from freqtrade.data.btanalysis import (
    delete_backtest_result,
    get_backtest_market_change,
    get_backtest_result,
    get_backtest_resultlist,
    load_and_merge_backtest_result,
    update_backtest_metadata,
)
from freqtrade.enums import BacktestState
from freqtrade.exceptions import ConfigurationError, DependencyException, OperationalException
from freqtrade.exchange.common import remove_exchange_credentials
from freqtrade.ft_types import get_BacktestResultType_default
from freqtrade.misc import deep_merge_dicts, is_file_in_dir
from freqtrade.rpc.api_server.api_schemas import (
    BacktestHistoryEntry,
    BacktestMarketChange,
    BacktestMetadataUpdate,
    BacktestRequest,
    BacktestResponse,
)
from freqtrade.rpc.api_server.deps import get_config
from freqtrade.rpc.api_server.webserver_bgwork import ApiBG
from freqtrade.rpc.rpc import RPCException


logger = logging.getLogger(__name__)

# Private API, protected by authentication and webserver_mode dependency
router = APIRouter()


def __run_backtest_bg(btconfig: Config):
    from freqtrade.data.metrics import combined_dataframes_with_rel_mean
    from freqtrade.optimize.optimize_reports import generate_backtest_stats, store_backtest_results
    from freqtrade.resolvers import StrategyResolver

    asyncio.set_event_loop(asyncio.new_event_loop())
    try:
        # Reload strategy
        lastconfig = ApiBG.bt["last_config"]
        strat = StrategyResolver.load_strategy(btconfig)
        validate_config_consistency(btconfig)

        if (
            not ApiBG.bt["bt"]
            or lastconfig.get("timeframe") != strat.timeframe
            or lastconfig.get("timeframe_detail") != btconfig.get("timeframe_detail")
            or lastconfig.get("timerange") != btconfig["timerange"]
        ):
            from freqtrade.optimize.backtesting import Backtesting

            ApiBG.bt["bt"] = Backtesting(btconfig)
            ApiBG.bt["bt"].load_bt_data_detail()
        else:
            ApiBG.bt["bt"].config = btconfig
            ApiBG.bt["bt"].init_backtest()
        # Only reload data if timeframe changed.
        if (
            not ApiBG.bt["data"]
            or not ApiBG.bt["timerange"]
            or lastconfig.get("timeframe") != strat.timeframe
            or lastconfig.get("timerange") != btconfig["timerange"]
        ):
            ApiBG.bt["data"], ApiBG.bt["timerange"] = ApiBG.bt["bt"].load_bt_data()

        lastconfig["timerange"] = btconfig["timerange"]
        lastconfig["timeframe"] = strat.timeframe
        lastconfig["enable_protections"] = btconfig.get("enable_protections")
        lastconfig["dry_run_wallet"] = btconfig.get("dry_run_wallet")

# REMOVED_UNUSED_CODE:         ApiBG.bt["bt"].enable_protections = btconfig.get("enable_protections", False)
# REMOVED_UNUSED_CODE:         ApiBG.bt["bt"].strategylist = [strat]
        ApiBG.bt["bt"].results = get_BacktestResultType_default()
        ApiBG.bt["bt"].load_prior_backtest()

# REMOVED_UNUSED_CODE:         ApiBG.bt["bt"].abort = False
        strategy_name = strat.get_strategy_name()
        if ApiBG.bt["bt"].results and strategy_name in ApiBG.bt["bt"].results["strategy"]:
            # When previous result hash matches - reuse that result and skip backtesting.
            logger.info(f"Reusing result of previous backtest for {strategy_name}")
        else:
            min_date, max_date = ApiBG.bt["bt"].backtest_one_strategy(
                strat, ApiBG.bt["data"], ApiBG.bt["timerange"]
            )

            ApiBG.bt["bt"].results = generate_backtest_stats(
                ApiBG.bt["data"], ApiBG.bt["bt"].all_results, min_date=min_date, max_date=max_date
            )

            if btconfig.get("export", "none") == "trades":
                combined_res = combined_dataframes_with_rel_mean(
                    ApiBG.bt["data"], min_date, max_date
                )
                fn = store_backtest_results(
                    btconfig,
                    ApiBG.bt["bt"].results,
                    datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
                    market_change_data=combined_res,
                )
                ApiBG.bt["bt"].results["metadata"][strategy_name]["filename"] = str(fn.stem)
                ApiBG.bt["bt"].results["metadata"][strategy_name]["strategy"] = strategy_name

        logger.info("Backtest finished.")

    except ConfigurationError as e:
        logger.error(f"Backtesting encountered a configuration Error: {e}")

    except (Exception, OperationalException, DependencyException) as e:
        logger.exception(f"Backtesting caused an error: {e}")
        ApiBG.bt["bt_error"] = str(e)
    finally:
        ApiBG.bgtask_running = False


# REMOVED_UNUSED_CODE: @router.post("/backtest", response_model=BacktestResponse, tags=["webserver", "backtest"])
# REMOVED_UNUSED_CODE: async def api_start_backtest(
# REMOVED_UNUSED_CODE:     bt_settings: BacktestRequest, background_tasks: BackgroundTasks, config=Depends(get_config)
# REMOVED_UNUSED_CODE: ):
# REMOVED_UNUSED_CODE:     ApiBG.bt["bt_error"] = None
# REMOVED_UNUSED_CODE:     """Start backtesting if not done so already"""
# REMOVED_UNUSED_CODE:     if ApiBG.bgtask_running:
# REMOVED_UNUSED_CODE:         raise RPCException("Bot Background task already running")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if ":" in bt_settings.strategy:
# REMOVED_UNUSED_CODE:         raise HTTPException(status_code=500, detail="base64 encoded strategies are not allowed.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     btconfig = deepcopy(config)
# REMOVED_UNUSED_CODE:     remove_exchange_credentials(btconfig["exchange"], True)
# REMOVED_UNUSED_CODE:     settings = dict(bt_settings)
# REMOVED_UNUSED_CODE:     if settings.get("freqai", None) is not None:
# REMOVED_UNUSED_CODE:         settings["freqai"] = dict(settings["freqai"])
# REMOVED_UNUSED_CODE:     # Pydantic models will contain all keys, but non-provided ones are None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     btconfig = deep_merge_dicts(settings, btconfig, allow_null_overrides=False)
# REMOVED_UNUSED_CODE:     try:
# REMOVED_UNUSED_CODE:         btconfig["stake_amount"] = float(btconfig["stake_amount"])
# REMOVED_UNUSED_CODE:     except ValueError:
# REMOVED_UNUSED_CODE:         pass
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Force dry-run for backtesting
# REMOVED_UNUSED_CODE:     btconfig["dry_run"] = True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Start backtesting
# REMOVED_UNUSED_CODE:     # Initialize backtesting object
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     background_tasks.add_task(__run_backtest_bg, btconfig=btconfig)
# REMOVED_UNUSED_CODE:     ApiBG.bgtask_running = True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return {
# REMOVED_UNUSED_CODE:         "status": "running",
# REMOVED_UNUSED_CODE:         "running": True,
# REMOVED_UNUSED_CODE:         "progress": 0,
# REMOVED_UNUSED_CODE:         "step": str(BacktestState.STARTUP),
# REMOVED_UNUSED_CODE:         "status_msg": "Backtest started",
# REMOVED_UNUSED_CODE:     }


# REMOVED_UNUSED_CODE: @router.get("/backtest", response_model=BacktestResponse, tags=["webserver", "backtest"])
# REMOVED_UNUSED_CODE: def api_get_backtest():
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Get backtesting result.
# REMOVED_UNUSED_CODE:     Returns Result after backtesting has been ran.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     from freqtrade.persistence import LocalTrade
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if ApiBG.bgtask_running:
# REMOVED_UNUSED_CODE:         return {
# REMOVED_UNUSED_CODE:             "status": "running",
# REMOVED_UNUSED_CODE:             "running": True,
# REMOVED_UNUSED_CODE:             "step": (
# REMOVED_UNUSED_CODE:                 ApiBG.bt["bt"].progress.action if ApiBG.bt["bt"] else str(BacktestState.STARTUP)
# REMOVED_UNUSED_CODE:             ),
# REMOVED_UNUSED_CODE:             "progress": ApiBG.bt["bt"].progress.progress if ApiBG.bt["bt"] else 0,
# REMOVED_UNUSED_CODE:             "trade_count": len(LocalTrade.bt_trades),
# REMOVED_UNUSED_CODE:             "status_msg": "Backtest running",
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if not ApiBG.bt["bt"]:
# REMOVED_UNUSED_CODE:         return {
# REMOVED_UNUSED_CODE:             "status": "not_started",
# REMOVED_UNUSED_CODE:             "running": False,
# REMOVED_UNUSED_CODE:             "step": "",
# REMOVED_UNUSED_CODE:             "progress": 0,
# REMOVED_UNUSED_CODE:             "status_msg": "Backtest not yet executed",
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE:     if ApiBG.bt["bt_error"]:
# REMOVED_UNUSED_CODE:         return {
# REMOVED_UNUSED_CODE:             "status": "error",
# REMOVED_UNUSED_CODE:             "running": False,
# REMOVED_UNUSED_CODE:             "step": "",
# REMOVED_UNUSED_CODE:             "progress": 0,
# REMOVED_UNUSED_CODE:             "status_msg": f"Backtest failed with {ApiBG.bt['bt_error']}",
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return {
# REMOVED_UNUSED_CODE:         "status": "ended",
# REMOVED_UNUSED_CODE:         "running": False,
# REMOVED_UNUSED_CODE:         "status_msg": "Backtest ended",
# REMOVED_UNUSED_CODE:         "step": "finished",
# REMOVED_UNUSED_CODE:         "progress": 1,
# REMOVED_UNUSED_CODE:         "backtest_result": ApiBG.bt["bt"].results,
# REMOVED_UNUSED_CODE:     }


# REMOVED_UNUSED_CODE: @router.delete("/backtest", response_model=BacktestResponse, tags=["webserver", "backtest"])
# REMOVED_UNUSED_CODE: def api_delete_backtest():
# REMOVED_UNUSED_CODE:     """Reset backtesting"""
# REMOVED_UNUSED_CODE:     if ApiBG.bgtask_running:
# REMOVED_UNUSED_CODE:         return {
# REMOVED_UNUSED_CODE:             "status": "running",
# REMOVED_UNUSED_CODE:             "running": True,
# REMOVED_UNUSED_CODE:             "step": "",
# REMOVED_UNUSED_CODE:             "progress": 0,
# REMOVED_UNUSED_CODE:             "status_msg": "Backtest running",
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE:     if ApiBG.bt["bt"]:
# REMOVED_UNUSED_CODE:         ApiBG.bt["bt"].cleanup()
# REMOVED_UNUSED_CODE:         del ApiBG.bt["bt"]
# REMOVED_UNUSED_CODE:         ApiBG.bt["bt"] = None
# REMOVED_UNUSED_CODE:         del ApiBG.bt["data"]
# REMOVED_UNUSED_CODE:         ApiBG.bt["data"] = None
# REMOVED_UNUSED_CODE:         logger.info("Backtesting reset")
# REMOVED_UNUSED_CODE:     return {
# REMOVED_UNUSED_CODE:         "status": "reset",
# REMOVED_UNUSED_CODE:         "running": False,
# REMOVED_UNUSED_CODE:         "step": "",
# REMOVED_UNUSED_CODE:         "progress": 0,
# REMOVED_UNUSED_CODE:         "status_msg": "Backtest reset",
# REMOVED_UNUSED_CODE:     }


@router.get("/backtest/abort", response_model=BacktestResponse, tags=["webserver", "backtest"])
def api_backtest_abort():
    if not ApiBG.bgtask_running:
        return {
            "status": "not_running",
            "running": False,
            "step": "",
            "progress": 0,
            "status_msg": "Backtest ended",
        }
# REMOVED_UNUSED_CODE:     ApiBG.bt["bt"].abort = True
    return {
        "status": "stopping",
        "running": False,
        "step": "",
        "progress": 0,
        "status_msg": "Backtest ended",
    }


@router.get(
    "/backtest/history", response_model=list[BacktestHistoryEntry], tags=["webserver", "backtest"]
)
def api_backtest_history(config=Depends(get_config)):
    # Get backtest result history, read from metadata files
    return get_backtest_resultlist(config["user_data_dir"] / "backtest_results")


@router.get(
    "/backtest/history/result", response_model=BacktestResponse, tags=["webserver", "backtest"]
)
def api_backtest_history_result(filename: str, strategy: str, config=Depends(get_config)):
    # Get backtest result history, read from metadata files
    bt_results_base: Path = config["user_data_dir"] / "backtest_results"
    for ext in [".zip", ".json"]:
        fn = (bt_results_base / filename).with_suffix(ext)
        if is_file_in_dir(fn, bt_results_base):
            break
    else:
        raise HTTPException(status_code=404, detail="File not found.")

    results: dict[str, Any] = {
        "metadata": {},
        "strategy": {},
        "strategy_comparison": [],
    }
    load_and_merge_backtest_result(strategy, fn, results)
    return {
        "status": "ended",
        "running": False,
        "step": "",
        "progress": 1,
        "status_msg": "Historic result",
        "backtest_result": results,
    }


@router.delete(
    "/backtest/history/{file}",
    response_model=list[BacktestHistoryEntry],
    tags=["webserver", "backtest"],
)
def api_delete_backtest_history_entry(file: str, config=Depends(get_config)):
    # Get backtest result history, read from metadata files
    bt_results_base: Path = config["user_data_dir"] / "backtest_results"
    for ext in [".zip", ".json"]:
        file_abs = (bt_results_base / file).with_suffix(ext)
        # Ensure file is in backtest_results directory
        if is_file_in_dir(file_abs, bt_results_base):
            break
    else:
        raise HTTPException(status_code=404, detail="File not found.")

    delete_backtest_result(file_abs)
    return get_backtest_resultlist(config["user_data_dir"] / "backtest_results")


@router.patch(
    "/backtest/history/{file}",
    response_model=list[BacktestHistoryEntry],
    tags=["webserver", "backtest"],
)
def api_update_backtest_history_entry(
    file: str, body: BacktestMetadataUpdate, config=Depends(get_config)
):
    # Get backtest result history, read from metadata files
    bt_results_base: Path = config["user_data_dir"] / "backtest_results"
    for ext in [".zip", ".json"]:
        file_abs = (bt_results_base / file).with_suffix(ext)
        # Ensure file is in backtest_results directory
        if is_file_in_dir(file_abs, bt_results_base):
            break
    else:
        raise HTTPException(status_code=404, detail="File not found.")

    content = {"notes": body.notes}
    try:
        update_backtest_metadata(file_abs, body.strategy, content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return get_backtest_result(file_abs)


@router.get(
    "/backtest/history/{file}/market_change",
    response_model=BacktestMarketChange,
    tags=["webserver", "backtest"],
)
def api_get_backtest_market_change(file: str, config=Depends(get_config)):
    bt_results_base: Path = config["user_data_dir"] / "backtest_results"
    for fn in (
        Path(file).with_suffix(".zip"),
        Path(f"{file}_market_change").with_suffix(".feather"),
    ):
        file_abs = bt_results_base / fn
        # Ensure file is in backtest_results directory
        if is_file_in_dir(file_abs, bt_results_base):
            break
    else:
        raise HTTPException(status_code=404, detail="File not found.")

    df = get_backtest_market_change(file_abs)

    return {
        "columns": df.columns.tolist(),
        "data": df.values.tolist(),
        "length": len(df),
    }
