from typing import Any, Literal
from uuid import uuid4

from typing_extensions import NotRequired, TypedDict

from freqtrade.exchange.exchange import Exchange


class ProgressTask(TypedDict):
# REMOVED_UNUSED_CODE:     progress: float
# REMOVED_UNUSED_CODE:     total: float
# REMOVED_UNUSED_CODE:     description: str


class JobsContainer(TypedDict):
# REMOVED_UNUSED_CODE:     category: Literal["pairlist", "download_data"]
# REMOVED_UNUSED_CODE:     is_running: bool
# REMOVED_UNUSED_CODE:     status: str
# REMOVED_UNUSED_CODE:     progress: float | None
# REMOVED_UNUSED_CODE:     progress_tasks: NotRequired[dict[str, ProgressTask]]
# REMOVED_UNUSED_CODE:     result: Any
# REMOVED_UNUSED_CODE:     error: str | None


# REMOVED_UNUSED_CODE: class ApiBG:
# REMOVED_UNUSED_CODE:     # Backtesting type: Backtesting
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     bt: dict[str, Any] = {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         "bt": None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         "data": None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         "timerange": None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         "last_config": {},
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         "bt_error": None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     bgtask_running: bool = False
# REMOVED_UNUSED_CODE:     # Exchange - only available in webserver mode.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     exchanges: dict[str, Exchange] = {}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Generic background jobs
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # TODO: Change this to TTLCache
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     jobs: dict[str, JobsContainer] = {}
# REMOVED_UNUSED_CODE:     # Pairlist evaluate things
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     pairlist_running: bool = False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     download_data_running: bool = False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def get_job_id() -> str:
# REMOVED_UNUSED_CODE:         return str(uuid4())
