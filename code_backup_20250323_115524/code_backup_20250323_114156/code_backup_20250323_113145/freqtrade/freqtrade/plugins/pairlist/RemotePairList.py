"""
Remote PairList provider

Provides pair list fetched from a remote source
"""

import logging
from pathlib import Path
from typing import Any

import rapidjson
import requests
from cachetools import TTLCache

from freqtrade import __version__
from freqtrade.configuration.load_config import CONFIG_PARSE_MODE
from freqtrade.exceptions import OperationalException
from freqtrade.exchange.exchange_types import Tickers
from freqtrade.plugins.pairlist.IPairList import IPairList, PairlistParameter, SupportsBacktesting
from freqtrade.plugins.pairlist.pairlist_helpers import expand_pairlist


logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class RemotePairList(IPairList):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     is_pairlist_generator = True
# REMOVED_UNUSED_CODE:     # Potential winner bias
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     supports_backtesting = SupportsBacktesting.BIASED
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, *args, **kwargs) -> None:
# REMOVED_UNUSED_CODE:         super().__init__(*args, **kwargs)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if "number_assets" not in self._pairlistconfig:
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 "`number_assets` not specified. Please check your configuration "
# REMOVED_UNUSED_CODE:                 'for "pairlist.config.number_assets"'
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if "pairlist_url" not in self._pairlistconfig:
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 "`pairlist_url` not specified. Please check your configuration "
# REMOVED_UNUSED_CODE:                 'for "pairlist.config.pairlist_url"'
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._mode = self._pairlistconfig.get("mode", "whitelist")
# REMOVED_UNUSED_CODE:         self._processing_mode = self._pairlistconfig.get("processing_mode", "filter")
# REMOVED_UNUSED_CODE:         self._number_pairs = self._pairlistconfig["number_assets"]
# REMOVED_UNUSED_CODE:         self._refresh_period: int = self._pairlistconfig.get("refresh_period", 1800)
# REMOVED_UNUSED_CODE:         self._keep_pairlist_on_failure = self._pairlistconfig.get("keep_pairlist_on_failure", True)
# REMOVED_UNUSED_CODE:         self._pair_cache: TTLCache = TTLCache(maxsize=1, ttl=self._refresh_period)
# REMOVED_UNUSED_CODE:         self._pairlist_url = self._pairlistconfig.get("pairlist_url", "")
# REMOVED_UNUSED_CODE:         self._read_timeout = self._pairlistconfig.get("read_timeout", 60)
# REMOVED_UNUSED_CODE:         self._bearer_token = self._pairlistconfig.get("bearer_token", "")
# REMOVED_UNUSED_CODE:         self._init_done = False
# REMOVED_UNUSED_CODE:         self._save_to_file = self._pairlistconfig.get("save_to_file", None)
# REMOVED_UNUSED_CODE:         self._last_pairlist: list[Any] = list()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self._mode not in ["whitelist", "blacklist"]:
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 '`mode` not configured correctly. Supported Modes are "whitelist","blacklist"'
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self._processing_mode not in ["filter", "append"]:
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 '`processing_mode` not configured correctly. Supported Modes are "filter","append"'
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self._pairlist_pos == 0 and self._mode == "blacklist":
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 "A `blacklist` mode RemotePairList can not be on the first "
# REMOVED_UNUSED_CODE:                 "position of your pairlist."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def needstickers(self) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Boolean property defining if tickers are necessary.
# REMOVED_UNUSED_CODE:         If no Pairlist requires tickers, an empty Dict is passed
# REMOVED_UNUSED_CODE:         as tickers argument to filter_pairlist
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def short_desc(self) -> str:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Short whitelist method description - used for startup-messages
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return f"{self.name} - {self._pairlistconfig['number_assets']} pairs from RemotePairlist."
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def description() -> str:
# REMOVED_UNUSED_CODE:         return "Retrieve pairs from a remote API or local file."
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def available_parameters() -> dict[str, PairlistParameter]:
# REMOVED_UNUSED_CODE:         return {
# REMOVED_UNUSED_CODE:             "pairlist_url": {
# REMOVED_UNUSED_CODE:                 "type": "string",
# REMOVED_UNUSED_CODE:                 "default": "",
# REMOVED_UNUSED_CODE:                 "description": "URL to fetch pairlist from",
# REMOVED_UNUSED_CODE:                 "help": "URL to fetch pairlist from",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "number_assets": {
# REMOVED_UNUSED_CODE:                 "type": "number",
# REMOVED_UNUSED_CODE:                 "default": 30,
# REMOVED_UNUSED_CODE:                 "description": "Number of assets",
# REMOVED_UNUSED_CODE:                 "help": "Number of assets to use from the pairlist.",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "mode": {
# REMOVED_UNUSED_CODE:                 "type": "option",
# REMOVED_UNUSED_CODE:                 "default": "whitelist",
# REMOVED_UNUSED_CODE:                 "options": ["whitelist", "blacklist"],
# REMOVED_UNUSED_CODE:                 "description": "Pairlist mode",
# REMOVED_UNUSED_CODE:                 "help": "Should this pairlist operate as a whitelist or blacklist?",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "processing_mode": {
# REMOVED_UNUSED_CODE:                 "type": "option",
# REMOVED_UNUSED_CODE:                 "default": "filter",
# REMOVED_UNUSED_CODE:                 "options": ["filter", "append"],
# REMOVED_UNUSED_CODE:                 "description": "Processing mode",
# REMOVED_UNUSED_CODE:                 "help": "Append pairs to incoming pairlist or filter them?",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             **IPairList.refresh_period_parameter(),
# REMOVED_UNUSED_CODE:             "keep_pairlist_on_failure": {
# REMOVED_UNUSED_CODE:                 "type": "boolean",
# REMOVED_UNUSED_CODE:                 "default": True,
# REMOVED_UNUSED_CODE:                 "description": "Keep last pairlist on failure",
# REMOVED_UNUSED_CODE:                 "help": "Keep last pairlist on failure",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "read_timeout": {
# REMOVED_UNUSED_CODE:                 "type": "number",
# REMOVED_UNUSED_CODE:                 "default": 60,
# REMOVED_UNUSED_CODE:                 "description": "Read timeout",
# REMOVED_UNUSED_CODE:                 "help": "Request timeout for remote pairlist",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "bearer_token": {
# REMOVED_UNUSED_CODE:                 "type": "string",
# REMOVED_UNUSED_CODE:                 "default": "",
# REMOVED_UNUSED_CODE:                 "description": "Bearer token",
# REMOVED_UNUSED_CODE:                 "help": "Bearer token - used for auth against the upstream service.",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "save_to_file": {
# REMOVED_UNUSED_CODE:                 "type": "string",
# REMOVED_UNUSED_CODE:                 "default": "",
# REMOVED_UNUSED_CODE:                 "description": "Filename to save processed pairlist to.",
# REMOVED_UNUSED_CODE:                 "help": "Specify a filename to save the processed pairlist in JSON format.",
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def process_json(self, jsonparse) -> list[str]:
# REMOVED_UNUSED_CODE:         pairlist = jsonparse.get("pairs", [])
# REMOVED_UNUSED_CODE:         remote_refresh_period = int(jsonparse.get("refresh_period", self._refresh_period))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self._refresh_period < remote_refresh_period:
# REMOVED_UNUSED_CODE:             self.log_once(
# REMOVED_UNUSED_CODE:                 f"Refresh Period has been increased from {self._refresh_period}"
# REMOVED_UNUSED_CODE:                 f" to minimum allowed: {remote_refresh_period} from Remote.",
# REMOVED_UNUSED_CODE:                 logger.info,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             self._refresh_period = remote_refresh_period
# REMOVED_UNUSED_CODE:             self._pair_cache = TTLCache(maxsize=1, ttl=remote_refresh_period)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._init_done = True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return pairlist
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def return_last_pairlist(self) -> list[str]:
# REMOVED_UNUSED_CODE:         if self._keep_pairlist_on_failure:
# REMOVED_UNUSED_CODE:             pairlist = self._last_pairlist
# REMOVED_UNUSED_CODE:             self.log_once("Keeping last fetched pairlist", logger.info)
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             pairlist = []
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return pairlist
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def fetch_pairlist(self) -> tuple[list[str], float]:
# REMOVED_UNUSED_CODE:         headers = {"User-Agent": "Freqtrade/" + __version__ + " Remotepairlist"}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self._bearer_token:
# REMOVED_UNUSED_CODE:             headers["Authorization"] = f"Bearer {self._bearer_token}"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             response = requests.get(self._pairlist_url, headers=headers, timeout=self._read_timeout)
# REMOVED_UNUSED_CODE:             content_type = response.headers.get("content-type")
# REMOVED_UNUSED_CODE:             time_elapsed = response.elapsed.total_seconds()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if "application/json" in str(content_type):
# REMOVED_UNUSED_CODE:                 jsonparse = response.json()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 try:
# REMOVED_UNUSED_CODE:                     pairlist = self.process_json(jsonparse)
# REMOVED_UNUSED_CODE:                 except Exception as e:
# REMOVED_UNUSED_CODE:                     pairlist = self._handle_error(f"Failed processing JSON data: {type(e)}")
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 pairlist = self._handle_error(
# REMOVED_UNUSED_CODE:                     f"RemotePairList is not of type JSON. {self._pairlist_url}"
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         except requests.exceptions.RequestException:
# REMOVED_UNUSED_CODE:             pairlist = self._handle_error(
# REMOVED_UNUSED_CODE:                 f"Was not able to fetch pairlist from: {self._pairlist_url}"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             time_elapsed = 0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return pairlist, time_elapsed
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _handle_error(self, error: str) -> list[str]:
# REMOVED_UNUSED_CODE:         if self._init_done:
# REMOVED_UNUSED_CODE:             self.log_once("Error: " + error, logger.info)
# REMOVED_UNUSED_CODE:             return self.return_last_pairlist()
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             raise OperationalException(error)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def gen_pairlist(self, tickers: Tickers) -> list[str]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Generate the pairlist
# REMOVED_UNUSED_CODE:         :param tickers: Tickers (from exchange.get_tickers). May be cached.
# REMOVED_UNUSED_CODE:         :return: List of pairs
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self._init_done:
# REMOVED_UNUSED_CODE:             pairlist = self._pair_cache.get("pairlist")
# REMOVED_UNUSED_CODE:             if pairlist == [None]:
# REMOVED_UNUSED_CODE:                 # Valid but empty pairlist.
# REMOVED_UNUSED_CODE:                 return []
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             pairlist = []
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         time_elapsed = 0.0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if pairlist:
# REMOVED_UNUSED_CODE:             # Item found - no refresh necessary
# REMOVED_UNUSED_CODE:             return pairlist.copy()
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             if self._pairlist_url.startswith("file:///"):
# REMOVED_UNUSED_CODE:                 filename = self._pairlist_url.split("file:///", 1)[1]
# REMOVED_UNUSED_CODE:                 file_path = Path(filename)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 if file_path.exists():
# REMOVED_UNUSED_CODE:                     with file_path.open() as json_file:
# REMOVED_UNUSED_CODE:                         try:
# REMOVED_UNUSED_CODE:                             # Load the JSON data into a dictionary
# REMOVED_UNUSED_CODE:                             jsonparse = rapidjson.load(json_file, parse_mode=CONFIG_PARSE_MODE)
# REMOVED_UNUSED_CODE:                             pairlist = self.process_json(jsonparse)
# REMOVED_UNUSED_CODE:                         except Exception as e:
# REMOVED_UNUSED_CODE:                             pairlist = self._handle_error(f"processing JSON data: {type(e)}")
# REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE:                     pairlist = self._handle_error(f"{self._pairlist_url} does not exist.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 # Fetch Pairlist from Remote URL
# REMOVED_UNUSED_CODE:                 pairlist, time_elapsed = self.fetch_pairlist()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.log_once(f"Fetched pairs: {pairlist}", logger.debug)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         pairlist = expand_pairlist(pairlist, list(self._exchange.get_markets().keys()))
# REMOVED_UNUSED_CODE:         pairlist = self._whitelist_for_active_markets(pairlist)
# REMOVED_UNUSED_CODE:         pairlist = pairlist[: self._number_pairs]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if pairlist:
# REMOVED_UNUSED_CODE:             self._pair_cache["pairlist"] = pairlist.copy()
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             # If pairlist is empty, set a dummy value to avoid fetching again
# REMOVED_UNUSED_CODE:             self._pair_cache["pairlist"] = [None]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if time_elapsed != 0.0:
# REMOVED_UNUSED_CODE:             self.log_once(f"Pairlist Fetched in {time_elapsed} seconds.", logger.info)
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             self.log_once("Fetched Pairlist.", logger.info)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._last_pairlist = list(pairlist)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self._save_to_file:
# REMOVED_UNUSED_CODE:             self.save_pairlist(pairlist, self._save_to_file)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return pairlist
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def save_pairlist(self, pairlist: list[str], filename: str) -> None:
# REMOVED_UNUSED_CODE:         pairlist_data = {"pairs": pairlist}
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             file_path = Path(filename)
# REMOVED_UNUSED_CODE:             with file_path.open("w") as json_file:
# REMOVED_UNUSED_CODE:                 rapidjson.dump(pairlist_data, json_file)
# REMOVED_UNUSED_CODE:                 logger.info(f"Processed pairlist saved to {filename}")
# REMOVED_UNUSED_CODE:         except Exception as e:
# REMOVED_UNUSED_CODE:             logger.error(f"Error saving processed pairlist to {filename}: {e}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def filter_pairlist(self, pairlist: list[str], tickers: dict) -> list[str]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Filters and sorts pairlist and returns the whitelist again.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Called on each bot iteration - please use internal caching if necessary
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pairlist: pairlist to filter or sort
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param tickers: Tickers (from exchange.get_tickers). May be cached.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: new whitelist
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         rpl_pairlist = self.gen_pairlist(tickers)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         merged_list = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         filtered = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._mode == "whitelist":
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if self._processing_mode == "filter":
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 merged_list = [pair for pair in pairlist if pair in rpl_pairlist]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             elif self._processing_mode == "append":
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 merged_list = pairlist + rpl_pairlist
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             merged_list = sorted(set(merged_list), key=merged_list.index)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for pair in pairlist:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if pair not in rpl_pairlist:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     merged_list.append(pair)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     filtered.append(pair)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if filtered:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.log_once(f"Blacklist - Filtered out pairs: {filtered}", logger.info)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         merged_list = merged_list[: self._number_pairs]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return merged_list
