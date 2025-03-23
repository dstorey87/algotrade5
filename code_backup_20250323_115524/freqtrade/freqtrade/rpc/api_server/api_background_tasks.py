import logging

# REMOVED_UNUSED_CODE: from fastapi import APIRouter
# REMOVED_UNUSED_CODE: from fastapi.exceptions import HTTPException

# REMOVED_UNUSED_CODE: from freqtrade.rpc.api_server.api_schemas import BackgroundTaskStatus
# REMOVED_UNUSED_CODE: from freqtrade.rpc.api_server.webserver_bgwork import ApiBG


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)

# Private API, protected by authentication and webserver_mode dependency
# REMOVED_UNUSED_CODE: router = APIRouter()


# REMOVED_UNUSED_CODE: @router.get("/background", response_model=list[BackgroundTaskStatus], tags=["webserver"])
# REMOVED_UNUSED_CODE: def background_job_list():
# REMOVED_UNUSED_CODE:     return [
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "job_id": jobid,
# REMOVED_UNUSED_CODE:             "job_category": job["category"],
# REMOVED_UNUSED_CODE:             "status": job["status"],
# REMOVED_UNUSED_CODE:             "running": job["is_running"],
# REMOVED_UNUSED_CODE:             "progress": job.get("progress"),
# REMOVED_UNUSED_CODE:             "progress_tasks": job.get("progress_tasks"),
# REMOVED_UNUSED_CODE:             "error": job.get("error", None),
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE:         for jobid, job in ApiBG.jobs.items()
# REMOVED_UNUSED_CODE:     ]


# REMOVED_UNUSED_CODE: @router.get("/background/{jobid}", response_model=BackgroundTaskStatus, tags=["webserver"])
# REMOVED_UNUSED_CODE: def background_job(jobid: str):
# REMOVED_UNUSED_CODE:     if not (job := ApiBG.jobs.get(jobid)):
# REMOVED_UNUSED_CODE:         raise HTTPException(status_code=404, detail="Job not found.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return {
# REMOVED_UNUSED_CODE:         "job_id": jobid,
# REMOVED_UNUSED_CODE:         "job_category": job["category"],
# REMOVED_UNUSED_CODE:         "status": job["status"],
# REMOVED_UNUSED_CODE:         "running": job["is_running"],
# REMOVED_UNUSED_CODE:         "progress": job.get("progress"),
# REMOVED_UNUSED_CODE:         "progress_tasks": job.get("progress_tasks"),
# REMOVED_UNUSED_CODE:         "error": job.get("error", None),
# REMOVED_UNUSED_CODE:     }
