# REMOVED_UNUSED_CODE: from pathlib import Path

# REMOVED_UNUSED_CODE: from fastapi import APIRouter
# REMOVED_UNUSED_CODE: from fastapi.exceptions import HTTPException
# REMOVED_UNUSED_CODE: from starlette.responses import FileResponse


# REMOVED_UNUSED_CODE: router_ui = APIRouter()


# REMOVED_UNUSED_CODE: @router_ui.get("/favicon.ico", include_in_schema=False)
# REMOVED_UNUSED_CODE: async def favicon():
# REMOVED_UNUSED_CODE:     return FileResponse(str(Path(__file__).parent / "ui/favicon.ico"))


# REMOVED_UNUSED_CODE: @router_ui.get("/fallback_file.html", include_in_schema=False)
# REMOVED_UNUSED_CODE: async def fallback():
# REMOVED_UNUSED_CODE:     return FileResponse(str(Path(__file__).parent / "ui/fallback_file.html"))


# REMOVED_UNUSED_CODE: @router_ui.get("/ui_version", include_in_schema=False)
# REMOVED_UNUSED_CODE: async def ui_version():
# REMOVED_UNUSED_CODE:     from freqtrade.commands.deploy_ui import read_ui_version
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     uibase = Path(__file__).parent / "ui/installed/"
# REMOVED_UNUSED_CODE:     version = read_ui_version(uibase)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return {
# REMOVED_UNUSED_CODE:         "version": version if version else "not_installed",
# REMOVED_UNUSED_CODE:     }


# REMOVED_UNUSED_CODE: @router_ui.get("/{rest_of_path:path}", include_in_schema=False)
# REMOVED_UNUSED_CODE: async def index_html(rest_of_path: str):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Emulate path fallback to index.html.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     if rest_of_path.startswith("api") or rest_of_path.startswith("."):
# REMOVED_UNUSED_CODE:         raise HTTPException(status_code=404, detail="Not Found")
# REMOVED_UNUSED_CODE:     uibase = Path(__file__).parent / "ui/installed/"
# REMOVED_UNUSED_CODE:     filename = uibase / rest_of_path
# REMOVED_UNUSED_CODE:     # It's security relevant to check "relative_to".
# REMOVED_UNUSED_CODE:     # Without this, Directory-traversal is possible.
# REMOVED_UNUSED_CODE:     media_type: str | None = None
# REMOVED_UNUSED_CODE:     if filename.suffix == ".js":
# REMOVED_UNUSED_CODE:         # Force text/javascript for .js files - Circumvent faulty system configuration
# REMOVED_UNUSED_CODE:         media_type = "application/javascript"
# REMOVED_UNUSED_CODE:     if filename.is_file() and filename.is_relative_to(uibase):
# REMOVED_UNUSED_CODE:         return FileResponse(str(filename), media_type=media_type)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     index_file = uibase / "index.html"
# REMOVED_UNUSED_CODE:     if not index_file.is_file():
# REMOVED_UNUSED_CODE:         return FileResponse(str(uibase.parent / "fallback_file.html"))
# REMOVED_UNUSED_CODE:     # Fall back to index.html, as indicated by vue router docs
# REMOVED_UNUSED_CODE:     return FileResponse(str(index_file))
