import argparse
import inspect
import json
import logging
import re
import sys
from pathlib import Path
from typing import Any

import rapidjson

from freqtrade_client import __version__
from freqtrade_client.ft_rest_client import FtRestClient


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("ft_rest_client")


# REMOVED_UNUSED_CODE: def add_arguments(args: Any = None):
# REMOVED_UNUSED_CODE:     parser = argparse.ArgumentParser(
# REMOVED_UNUSED_CODE:         prog="freqtrade-client",
# REMOVED_UNUSED_CODE:         description="Client for the freqtrade REST API",
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     parser.add_argument(
# REMOVED_UNUSED_CODE:         "command", help="Positional argument defining the command to execute.", nargs="?"
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")
# REMOVED_UNUSED_CODE:     parser.add_argument(
# REMOVED_UNUSED_CODE:         "--show",
# REMOVED_UNUSED_CODE:         help="Show possible methods with this client",
# REMOVED_UNUSED_CODE:         dest="show",
# REMOVED_UNUSED_CODE:         action="store_true",
# REMOVED_UNUSED_CODE:         default=False,
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     parser.add_argument(
# REMOVED_UNUSED_CODE:         "-c",
# REMOVED_UNUSED_CODE:         "--config",
# REMOVED_UNUSED_CODE:         help="Specify configuration file (default: %(default)s). ",
# REMOVED_UNUSED_CODE:         dest="config",
# REMOVED_UNUSED_CODE:         type=str,
# REMOVED_UNUSED_CODE:         metavar="PATH",
# REMOVED_UNUSED_CODE:         default="config.json",
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     parser.add_argument(
# REMOVED_UNUSED_CODE:         "command_arguments",
# REMOVED_UNUSED_CODE:         help="Positional arguments for the parameters for [command]",
# REMOVED_UNUSED_CODE:         nargs="*",
# REMOVED_UNUSED_CODE:         default=[],
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     pargs = parser.parse_args(args)
# REMOVED_UNUSED_CODE:     return vars(pargs)


def load_config(configfile):
    file = Path(configfile)
    if file.is_file():
        with file.open("r") as f:
            config = rapidjson.load(
                f, parse_mode=rapidjson.PM_COMMENTS | rapidjson.PM_TRAILING_COMMAS
            )
        return config
    else:
        logger.warning(f"Could not load config file {file}.")
        sys.exit(1)


def print_commands():
    # Print dynamic help for the different commands using the commands doc-strings
    client = FtRestClient(None)
    print("Possible commands:\n")
    for x, _ in inspect.getmembers(client):
        if not x.startswith("_"):
            doc = re.sub(":return:.*", "", getattr(client, x).__doc__, flags=re.MULTILINE).rstrip()
            print(f"{x}\n\t{doc}\n")


# REMOVED_UNUSED_CODE: def main_exec(parsed: dict[str, Any]):
# REMOVED_UNUSED_CODE:     if parsed.get("show"):
# REMOVED_UNUSED_CODE:         print_commands()
# REMOVED_UNUSED_CODE:         sys.exit()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     config = load_config(parsed["config"])
# REMOVED_UNUSED_CODE:     url = config.get("api_server", {}).get("listen_ip_address", "127.0.0.1")
# REMOVED_UNUSED_CODE:     port = config.get("api_server", {}).get("listen_port", "8080")
# REMOVED_UNUSED_CODE:     username = config.get("api_server", {}).get("username")
# REMOVED_UNUSED_CODE:     password = config.get("api_server", {}).get("password")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     server_url = f"http://{url}:{port}"
# REMOVED_UNUSED_CODE:     client = FtRestClient(server_url, username, password)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     m = [x for x, y in inspect.getmembers(client) if not x.startswith("_")]
# REMOVED_UNUSED_CODE:     command = parsed["command"]
# REMOVED_UNUSED_CODE:     if command not in m:
# REMOVED_UNUSED_CODE:         logger.error(f"Command {command} not defined")
# REMOVED_UNUSED_CODE:         print_commands()
# REMOVED_UNUSED_CODE:         return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Split arguments with = into key/value pairs
# REMOVED_UNUSED_CODE:     kwargs = {x.split("=")[0]: x.split("=")[1] for x in parsed["command_arguments"] if "=" in x}
# REMOVED_UNUSED_CODE:     args = [x for x in parsed["command_arguments"] if "=" not in x]
# REMOVED_UNUSED_CODE:     try:
# REMOVED_UNUSED_CODE:         res = getattr(client, command)(*args, **kwargs)
# REMOVED_UNUSED_CODE:         print(json.dumps(res))
# REMOVED_UNUSED_CODE:     except TypeError as e:
# REMOVED_UNUSED_CODE:         logger.error(f"Error executing command {command}: {e}")
# REMOVED_UNUSED_CODE:         sys.exit(1)
# REMOVED_UNUSED_CODE:     except Exception as e:
# REMOVED_UNUSED_CODE:         logger.error(f"Fatal Error executing command {command}: {e}")
# REMOVED_UNUSED_CODE:         sys.exit(1)


# REMOVED_UNUSED_CODE: def main():
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Main entry point for the client
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     args = add_arguments()
# REMOVED_UNUSED_CODE:     main_exec(args)
