import logging
# REMOVED_UNUSED_CODE: from pathlib import Path

# REMOVED_UNUSED_CODE: import requests


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)

# Timeout for requests
# REMOVED_UNUSED_CODE: req_timeout = 30


# REMOVED_UNUSED_CODE: def clean_ui_subdir(directory: Path):
# REMOVED_UNUSED_CODE:     if directory.is_dir():
# REMOVED_UNUSED_CODE:         logger.info("Removing UI directory content.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         for p in reversed(list(directory.glob("**/*"))):  # iterate contents from leaves to root
# REMOVED_UNUSED_CODE:             if p.name in (".gitkeep", "fallback_file.html"):
# REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE:             if p.is_file():
# REMOVED_UNUSED_CODE:                 p.unlink()
# REMOVED_UNUSED_CODE:             elif p.is_dir():
# REMOVED_UNUSED_CODE:                 p.rmdir()


# REMOVED_UNUSED_CODE: def read_ui_version(dest_folder: Path) -> str | None:
# REMOVED_UNUSED_CODE:     file = dest_folder / ".uiversion"
# REMOVED_UNUSED_CODE:     if not file.is_file():
# REMOVED_UNUSED_CODE:         return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     with file.open("r") as f:
# REMOVED_UNUSED_CODE:         return f.read()


# REMOVED_UNUSED_CODE: def download_and_install_ui(dest_folder: Path, dl_url: str, version: str):
# REMOVED_UNUSED_CODE:     from io import BytesIO
# REMOVED_UNUSED_CODE:     from zipfile import ZipFile
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     logger.info(f"Downloading {dl_url}")
# REMOVED_UNUSED_CODE:     resp = requests.get(dl_url, timeout=req_timeout).content
# REMOVED_UNUSED_CODE:     dest_folder.mkdir(parents=True, exist_ok=True)
# REMOVED_UNUSED_CODE:     with ZipFile(BytesIO(resp)) as zf:
# REMOVED_UNUSED_CODE:         for fn in zf.filelist:
# REMOVED_UNUSED_CODE:             with zf.open(fn) as x:
# REMOVED_UNUSED_CODE:                 destfile = dest_folder / fn.filename
# REMOVED_UNUSED_CODE:                 if fn.is_dir():
# REMOVED_UNUSED_CODE:                     destfile.mkdir(exist_ok=True)
# REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE:                     destfile.write_bytes(x.read())
# REMOVED_UNUSED_CODE:     with (dest_folder / ".uiversion").open("w") as f:
# REMOVED_UNUSED_CODE:         f.write(version)


# REMOVED_UNUSED_CODE: def get_ui_download_url(version: str | None = None) -> tuple[str, str]:
# REMOVED_UNUSED_CODE:     base_url = "https://api.github.com/repos/freqtrade/frequi/"
# REMOVED_UNUSED_CODE:     # Get base UI Repo path
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     resp = requests.get(f"{base_url}releases", timeout=req_timeout)
# REMOVED_UNUSED_CODE:     resp.raise_for_status()
# REMOVED_UNUSED_CODE:     r = resp.json()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if version:
# REMOVED_UNUSED_CODE:         tmp = [x for x in r if x["name"] == version]
# REMOVED_UNUSED_CODE:         if tmp:
# REMOVED_UNUSED_CODE:             latest_version = tmp[0]["name"]
# REMOVED_UNUSED_CODE:             assets = tmp[0].get("assets", [])
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             raise ValueError("UI-Version not found.")
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         latest_version = r[0]["name"]
# REMOVED_UNUSED_CODE:         assets = r[0].get("assets", [])
# REMOVED_UNUSED_CODE:     dl_url = ""
# REMOVED_UNUSED_CODE:     if assets and len(assets) > 0:
# REMOVED_UNUSED_CODE:         dl_url = assets[0]["browser_download_url"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # URL not found - try assets url
# REMOVED_UNUSED_CODE:     if not dl_url:
# REMOVED_UNUSED_CODE:         assets = r[0]["assets_url"]
# REMOVED_UNUSED_CODE:         resp = requests.get(assets, timeout=req_timeout)
# REMOVED_UNUSED_CODE:         r = resp.json()
# REMOVED_UNUSED_CODE:         dl_url = r[0]["browser_download_url"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return dl_url, latest_version
