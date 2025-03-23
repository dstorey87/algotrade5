"""
A Rest Client for Freqtrade bot

Should not import anything from freqtrade,
so it can be used as a standalone script, and can be installed independently.
"""

# REMOVED_UNUSED_CODE: import json
import logging
# REMOVED_UNUSED_CODE: from typing import Any
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from urllib.parse import urlencode, urlparse, urlunparse

# REMOVED_UNUSED_CODE: import requests
# REMOVED_UNUSED_CODE: from requests.adapters import HTTPAdapter
# REMOVED_UNUSED_CODE: from requests.exceptions import ConnectionError as RequestConnectionError


# REMOVED_UNUSED_CODE: logger = logging.getLogger("ft_rest_client")

# REMOVED_UNUSED_CODE: ParamsT = dict[str, Any] | None
# REMOVED_UNUSED_CODE: PostDataT = dict[str, Any] | list[dict[str, Any]] | None


# REMOVED_UNUSED_CODE: class FtRestClient:
# REMOVED_UNUSED_CODE:     def __init__(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         serverurl,
# REMOVED_UNUSED_CODE:         username=None,
# REMOVED_UNUSED_CODE:         password=None,
# REMOVED_UNUSED_CODE:         *,
# REMOVED_UNUSED_CODE:         pool_connections=10,
# REMOVED_UNUSED_CODE:         pool_maxsize=10,
# REMOVED_UNUSED_CODE:         timeout=10,
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         self._serverurl = serverurl
# REMOVED_UNUSED_CODE:         self._session = requests.Session()
# REMOVED_UNUSED_CODE:         self._timeout = timeout
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # allow configuration of pool
# REMOVED_UNUSED_CODE:         adapter = HTTPAdapter(pool_connections=pool_connections, pool_maxsize=pool_maxsize)
# REMOVED_UNUSED_CODE:         self._session.mount("http://", adapter)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if username and password:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._session.auth = (username, password)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _call(self, method, apipath, params: dict | None = None, data=None, files=None):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if str(method).upper() not in ("GET", "POST", "PUT", "DELETE"):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise ValueError(f"invalid method <{method}>")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         basepath = f"{self._serverurl}/api/v1/{apipath}"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         hd = {"Accept": "application/json", "Content-Type": "application/json"}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Split url
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         schema, netloc, path, par, query, fragment = urlparse(basepath)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # URLEncode query string
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         query = urlencode(params) if params else ""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # recombine url
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         url = urlunparse((schema, netloc, path, par, query, fragment))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             resp = self._session.request(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 method, url, headers=hd, timeout=self._timeout, data=json.dumps(data)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # return resp.text
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return resp.json()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         except RequestConnectionError:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             logger.warning(f"Connection error - could not connect to {netloc}.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _get(self, apipath, params: ParamsT = None):
# REMOVED_UNUSED_CODE:         return self._call("GET", apipath, params=params)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _delete(self, apipath, params: ParamsT = None):
# REMOVED_UNUSED_CODE:         return self._call("DELETE", apipath, params=params)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _post(self, apipath, params: ParamsT = None, data: PostDataT = None):
# REMOVED_UNUSED_CODE:         return self._call("POST", apipath, params=params, data=data)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def start(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Start the bot if it's in the stopped state.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._post("start")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def stop(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Stop the bot. Use `start` to restart.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._post("stop")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def stopbuy(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Stop buying (but handle sells gracefully). Use `reload_config` to reset.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._post("stopbuy")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def reload_config(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Reload configuration.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._post("reload_config")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def balance(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Get the account balance.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get("balance")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def count(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Return the amount of open trades.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get("count")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def entries(self, pair=None):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Returns List of dicts containing all Trades, based on buy tag performance
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Can either be average for all pairs or a specific pair provided
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get("entries", params={"pair": pair} if pair else None)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def exits(self, pair=None):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Returns List of dicts containing all Trades, based on exit reason performance
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Can either be average for all pairs or a specific pair provided
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get("exits", params={"pair": pair} if pair else None)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def mix_tags(self, pair=None):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Returns List of dicts containing all Trades, based on entry_tag + exit_reason performance
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Can either be average for all pairs or a specific pair provided
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get("mix_tags", params={"pair": pair} if pair else None)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def locks(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Return current locks
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get("locks")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def delete_lock(self, lock_id):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Delete (disable) lock from the database.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param lock_id: ID for the lock to delete
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._delete(f"locks/{lock_id}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def lock_add(self, pair: str, until: str, side: str = "*", reason: str = ""):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Lock pair
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pair: Pair to lock
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param until: Lock until this date (format "2024-03-30 16:00:00Z")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param side: Side to lock (long, short, *)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param reason: Reason for the lock
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         data = [{"pair": pair, "until": until, "side": side, "reason": reason}]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._post("locks", data=data)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def daily(self, days=None):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Return the profits for each day, and amount of trades.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get("daily", params={"timescale": days} if days else None)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def weekly(self, weeks=None):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Return the profits for each week, and amount of trades.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get("weekly", params={"timescale": weeks} if weeks else None)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def monthly(self, months=None):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Return the profits for each month, and amount of trades.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get("monthly", params={"timescale": months} if months else None)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def edge(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Return information about edge.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get("edge")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def profit(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Return the profit summary.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get("profit")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def stats(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Return the stats report (durations, sell-reasons).
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get("stats")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def performance(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Return the performance of the different coins.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get("performance")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def status(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Get the status of open trades.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get("status")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def version(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Return the version of the bot.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object containing the version
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get("version")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def show_config(self):
# REMOVED_UNUSED_CODE:         """Returns part of the configuration, relevant for trading operations.
# REMOVED_UNUSED_CODE:         :return: json object containing the version
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return self._get("show_config")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def ping(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """simple ping"""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         configstatus = self.show_config()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not configstatus:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return {"status": "not_running"}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         elif configstatus["state"] == "running":
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return {"status": "pong"}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return {"status": "not_running"}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def logs(self, limit=None):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Show latest logs.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param limit: Limits log messages to the last <limit> logs. No limit to get the entire log.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get("logs", params={"limit": limit} if limit else {})
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def trades(self, limit=None, offset=None):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Return trades history, sorted by id
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param limit: Limits trades to the X last trades. Max 500 trades.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param offset: Offset by this amount of trades.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         params = {}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if limit:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             params["limit"] = limit
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if offset:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             params["offset"] = offset
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get("trades", params)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def trade(self, trade_id):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Return specific trade
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param trade_id: Specify which trade to get.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get(f"trade/{trade_id}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def delete_trade(self, trade_id):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Delete trade from the database.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Tries to close open orders. Requires manual handling of this asset on the exchange.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param trade_id: Deletes the trade with this ID from the database.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._delete(f"trades/{trade_id}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def cancel_open_order(self, trade_id):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Cancel open order for trade.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param trade_id: Cancels open orders for this trade.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._delete(f"trades/{trade_id}/open-order")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def whitelist(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Show the current whitelist.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get("whitelist")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def blacklist(self, *args):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Show the current blacklist.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param add: List of coins to add (example: "BNB/BTC")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not args:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return self._get("blacklist")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return self._post("blacklist", data={"blacklist": args})
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def forcebuy(self, pair, price=None):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Buy an asset.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pair: Pair to buy (ETH/BTC)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param price: Optional - price to buy
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object of the trade
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         data = {"pair": pair, "price": price}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._post("forcebuy", data=data)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def forceenter(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         side,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         price=None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         *,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         order_type=None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         stake_amount=None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         leverage=None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         enter_tag=None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Force entering a trade
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pair: Pair to buy (ETH/BTC)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param side: 'long' or 'short'
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param price: Optional - price to buy
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param order_type: Optional keyword argument - 'limit' or 'market'
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param stake_amount: Optional keyword argument - stake amount (as float)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param leverage: Optional keyword argument - leverage (as float)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param enter_tag: Optional keyword argument - entry tag (as string, default: 'force_enter')
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object of the trade
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         data = {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "pair": pair,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "side": side,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if price:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             data["price"] = price
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if order_type:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             data["ordertype"] = order_type
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if stake_amount:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             data["stakeamount"] = stake_amount
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if leverage:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             data["leverage"] = leverage
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if enter_tag:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             data["entry_tag"] = enter_tag
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._post("forceenter", data=data)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def forceexit(self, tradeid, ordertype=None, amount=None):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Force-exit a trade.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param tradeid: Id of the trade (can be received via status command)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param ordertype: Order type to use (must be market or limit)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param amount: Amount to sell. Full sell if not given
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._post(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "forceexit",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             data={
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "tradeid": tradeid,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "ordertype": ordertype,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "amount": amount,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def strategies(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Lists available strategies
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get("strategies")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def strategy(self, strategy):
# REMOVED_UNUSED_CODE:         """Get strategy details
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         :param strategy: Strategy class name
# REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return self._get(f"strategy/{strategy}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def pairlists_available(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Lists available pairlist providers
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get("pairlists/available")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def plot_config(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Return plot configuration if the strategy defines one.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get("plot_config")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def available_pairs(self, timeframe=None, stake_currency=None):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Return available pair (backtest data) based on timeframe / stake_currency selection
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param timeframe: Only pairs with this timeframe available.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param stake_currency: Only pairs that include this timeframe
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "available_pairs",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             params={
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "stake_currency": stake_currency if timeframe else "",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "timeframe": timeframe if timeframe else "",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def pair_candles(self, pair, timeframe, limit=None, columns=None):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Return live dataframe for <pair><timeframe>.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pair: Pair to get data for
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param timeframe: Only pairs with this timeframe available.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param limit: Limit result to the last n candles.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param columns: List of dataframe columns to return. Empty list will return OHLCV.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         params = {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "pair": pair,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "timeframe": timeframe,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if limit:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             params["limit"] = limit
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if columns is not None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             params["columns"] = columns
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return self._post("pair_candles", data=params)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get("pair_candles", params=params)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def pair_history(self, pair, timeframe, strategy, timerange=None, freqaimodel=None):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Return historic, analyzed dataframe
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pair: Pair to get data for
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param timeframe: Only pairs with this timeframe available.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param strategy: Strategy to analyze and get values for
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param freqaimodel: FreqAI model to use for analysis
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param timerange: Timerange to get data for (same format than --timerange endpoints)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "pair_history",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             params={
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "pair": pair,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "timeframe": timeframe,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "strategy": strategy,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "freqaimodel": freqaimodel,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "timerange": timerange if timerange else "",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def sysinfo(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Provides system information (CPU, RAM usage)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get("sysinfo")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def health(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """Provides a quick health check of the running bot.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: json object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get("health")
