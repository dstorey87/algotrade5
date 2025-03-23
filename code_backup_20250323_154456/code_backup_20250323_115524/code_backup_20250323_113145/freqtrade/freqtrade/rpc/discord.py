import logging

from freqtrade.constants import Config
from freqtrade.enums import RPCMessageType
# REMOVED_UNUSED_CODE: from freqtrade.rpc import RPC
from freqtrade.rpc.webhook import Webhook


logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class Discord(Webhook):
# REMOVED_UNUSED_CODE:     def __init__(self, rpc: "RPC", config: Config):
# REMOVED_UNUSED_CODE:         self._config = config
# REMOVED_UNUSED_CODE:         self.rpc = rpc
# REMOVED_UNUSED_CODE:         self.strategy = config.get("strategy", "")
# REMOVED_UNUSED_CODE:         self.timeframe = config.get("timeframe", "")
# REMOVED_UNUSED_CODE:         self.bot_name = config.get("bot_name", "")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._url = config["discord"]["webhook_url"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._format = "json"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._retries = 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._retry_delay = 0.1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._timeout = self._config["discord"].get("timeout", 10)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def cleanup(self) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Cleanup pending module resources.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         This will do nothing for webhooks, they will simply not be called anymore
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pass
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def send_msg(self, msg) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if fields := self._config["discord"].get(msg["type"].value):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             logger.info(f"Sending discord message: {msg}")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             msg["strategy"] = self.strategy
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             msg["timeframe"] = self.timeframe
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             msg["bot_name"] = self.bot_name
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             color = 0x0000FF
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if msg["type"] in (RPCMessageType.EXIT, RPCMessageType.EXIT_FILL):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 profit_ratio = msg.get("profit_ratio")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 color = 0x00FF00 if profit_ratio > 0 else 0xFF0000
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             title = msg["type"].value
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if "pair" in msg:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 title = f"Trade: {msg['pair']} {msg['type'].value}"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             embeds = [
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "title": title,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "color": color,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "fields": [],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 }
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for f in fields:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 for k, v in f.items():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     v = v.format(**msg)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     embeds[0]["fields"].append({"name": k, "value": v, "inline": True})
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Send the message to discord channel
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             payload = {"embeds": embeds}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._send_msg(payload)
