import logging
import secrets
from pathlib import Path
from typing import Any

from questionary import Separator, prompt

from freqtrade.constants import UNLIMITED_STAKE_AMOUNT
from freqtrade.exceptions import OperationalException


logger = logging.getLogger(__name__)


def validate_is_int(val):
    try:
        _ = int(val)
        return True
    except Exception:
        return False


def validate_is_float(val):
    try:
        _ = float(val)
        return True
    except Exception:
        return False


# REMOVED_UNUSED_CODE: def ask_user_overwrite(config_path: Path) -> bool:
# REMOVED_UNUSED_CODE:     questions = [
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "type": "confirm",
# REMOVED_UNUSED_CODE:             "name": "overwrite",
# REMOVED_UNUSED_CODE:             "message": f"File {config_path} already exists. Overwrite?",
# REMOVED_UNUSED_CODE:             "default": False,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:     ]
# REMOVED_UNUSED_CODE:     answers = prompt(questions)
# REMOVED_UNUSED_CODE:     return answers["overwrite"]


# REMOVED_UNUSED_CODE: def ask_user_config() -> dict[str, Any]:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Ask user a few questions to build the configuration.
# REMOVED_UNUSED_CODE:     Interactive questions built using https://github.com/tmbo/questionary
# REMOVED_UNUSED_CODE:     :returns: Dict with keys to put into template
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     from freqtrade.configuration.detect_environment import running_in_docker
# REMOVED_UNUSED_CODE:     from freqtrade.exchange import available_exchanges
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     questions: list[dict[str, Any]] = [
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "type": "confirm",
# REMOVED_UNUSED_CODE:             "name": "dry_run",
# REMOVED_UNUSED_CODE:             "message": "Do you want to enable Dry-run (simulated trades)?",
# REMOVED_UNUSED_CODE:             "default": True,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "type": "text",
# REMOVED_UNUSED_CODE:             "name": "stake_currency",
# REMOVED_UNUSED_CODE:             "message": "Please insert your stake currency:",
# REMOVED_UNUSED_CODE:             "default": "USDT",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "type": "text",
# REMOVED_UNUSED_CODE:             "name": "stake_amount",
# REMOVED_UNUSED_CODE:             "message": f"Please insert your stake amount (Number or '{UNLIMITED_STAKE_AMOUNT}'):",
# REMOVED_UNUSED_CODE:             "default": "unlimited",
# REMOVED_UNUSED_CODE:             "validate": lambda val: val == UNLIMITED_STAKE_AMOUNT or validate_is_float(val),
# REMOVED_UNUSED_CODE:             "filter": lambda val: (
# REMOVED_UNUSED_CODE:                 '"' + UNLIMITED_STAKE_AMOUNT + '"' if val == UNLIMITED_STAKE_AMOUNT else val
# REMOVED_UNUSED_CODE:             ),
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "type": "text",
# REMOVED_UNUSED_CODE:             "name": "max_open_trades",
# REMOVED_UNUSED_CODE:             "message": "Please insert max_open_trades (Integer or -1 for unlimited open trades):",
# REMOVED_UNUSED_CODE:             "default": "3",
# REMOVED_UNUSED_CODE:             "validate": lambda val: validate_is_int(val),
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "type": "select",
# REMOVED_UNUSED_CODE:             "name": "timeframe_in_config",
# REMOVED_UNUSED_CODE:             "message": "Time",
# REMOVED_UNUSED_CODE:             "choices": ["Have the strategy define timeframe.", "Override in configuration."],
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "type": "text",
# REMOVED_UNUSED_CODE:             "name": "timeframe",
# REMOVED_UNUSED_CODE:             "message": "Please insert your desired timeframe (e.g. 5m):",
# REMOVED_UNUSED_CODE:             "default": "5m",
# REMOVED_UNUSED_CODE:             "when": lambda x: x["timeframe_in_config"] == "Override in configuration.",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "type": "text",
# REMOVED_UNUSED_CODE:             "name": "fiat_display_currency",
# REMOVED_UNUSED_CODE:             "message": (
# REMOVED_UNUSED_CODE:                 "Please insert your display Currency for reporting "
# REMOVED_UNUSED_CODE:                 "(leave empty to disable FIAT conversion):"
# REMOVED_UNUSED_CODE:             ),
# REMOVED_UNUSED_CODE:             "default": "USD",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "type": "select",
# REMOVED_UNUSED_CODE:             "name": "exchange_name",
# REMOVED_UNUSED_CODE:             "message": "Select exchange",
# REMOVED_UNUSED_CODE:             "choices": [
# REMOVED_UNUSED_CODE:                 "binance",
# REMOVED_UNUSED_CODE:                 "binanceus",
# REMOVED_UNUSED_CODE:                 "bingx",
# REMOVED_UNUSED_CODE:                 "gate",
# REMOVED_UNUSED_CODE:                 "htx",
# REMOVED_UNUSED_CODE:                 "kraken",
# REMOVED_UNUSED_CODE:                 "kucoin",
# REMOVED_UNUSED_CODE:                 "okx",
# REMOVED_UNUSED_CODE:                 Separator("------------------"),
# REMOVED_UNUSED_CODE:                 "other",
# REMOVED_UNUSED_CODE:             ],
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "type": "confirm",
# REMOVED_UNUSED_CODE:             "name": "trading_mode",
# REMOVED_UNUSED_CODE:             "message": "Do you want to trade Perpetual Swaps (perpetual futures)?",
# REMOVED_UNUSED_CODE:             "default": False,
# REMOVED_UNUSED_CODE:             "filter": lambda val: "futures" if val else "spot",
# REMOVED_UNUSED_CODE:             "when": lambda x: x["exchange_name"] in ["binance", "gate", "okx", "bybit"],
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "type": "autocomplete",
# REMOVED_UNUSED_CODE:             "name": "exchange_name",
# REMOVED_UNUSED_CODE:             "message": "Type your exchange name (Must be supported by ccxt)",
# REMOVED_UNUSED_CODE:             "choices": available_exchanges(),
# REMOVED_UNUSED_CODE:             "when": lambda x: x["exchange_name"] == "other",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "type": "password",
# REMOVED_UNUSED_CODE:             "name": "exchange_key",
# REMOVED_UNUSED_CODE:             "message": "Insert Exchange Key",
# REMOVED_UNUSED_CODE:             "when": lambda x: not x["dry_run"],
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "type": "password",
# REMOVED_UNUSED_CODE:             "name": "exchange_secret",
# REMOVED_UNUSED_CODE:             "message": "Insert Exchange Secret",
# REMOVED_UNUSED_CODE:             "when": lambda x: not x["dry_run"],
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "type": "password",
# REMOVED_UNUSED_CODE:             "name": "exchange_key_password",
# REMOVED_UNUSED_CODE:             "message": "Insert Exchange API Key password",
# REMOVED_UNUSED_CODE:             "when": lambda x: not x["dry_run"] and x["exchange_name"] in ("kucoin", "okx"),
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "type": "confirm",
# REMOVED_UNUSED_CODE:             "name": "telegram",
# REMOVED_UNUSED_CODE:             "message": "Do you want to enable Telegram?",
# REMOVED_UNUSED_CODE:             "default": False,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "type": "password",
# REMOVED_UNUSED_CODE:             "name": "telegram_token",
# REMOVED_UNUSED_CODE:             "message": "Insert Telegram token",
# REMOVED_UNUSED_CODE:             "when": lambda x: x["telegram"],
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "type": "password",
# REMOVED_UNUSED_CODE:             "name": "telegram_chat_id",
# REMOVED_UNUSED_CODE:             "message": "Insert Telegram chat id",
# REMOVED_UNUSED_CODE:             "when": lambda x: x["telegram"],
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "type": "confirm",
# REMOVED_UNUSED_CODE:             "name": "api_server",
# REMOVED_UNUSED_CODE:             "message": "Do you want to enable the Rest API (includes FreqUI)?",
# REMOVED_UNUSED_CODE:             "default": False,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "type": "text",
# REMOVED_UNUSED_CODE:             "name": "api_server_listen_addr",
# REMOVED_UNUSED_CODE:             "message": (
# REMOVED_UNUSED_CODE:                 "Insert Api server Listen Address (0.0.0.0 for docker, "
# REMOVED_UNUSED_CODE:                 "otherwise best left untouched)"
# REMOVED_UNUSED_CODE:             ),
# REMOVED_UNUSED_CODE:             "default": "127.0.0.1" if not running_in_docker() else "0.0.0.0",  # noqa: S104
# REMOVED_UNUSED_CODE:             "when": lambda x: x["api_server"],
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "type": "text",
# REMOVED_UNUSED_CODE:             "name": "api_server_username",
# REMOVED_UNUSED_CODE:             "message": "Insert api-server username",
# REMOVED_UNUSED_CODE:             "default": "freqtrader",
# REMOVED_UNUSED_CODE:             "when": lambda x: x["api_server"],
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "type": "password",
# REMOVED_UNUSED_CODE:             "name": "api_server_password",
# REMOVED_UNUSED_CODE:             "message": "Insert api-server password",
# REMOVED_UNUSED_CODE:             "when": lambda x: x["api_server"],
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:     ]
# REMOVED_UNUSED_CODE:     answers = prompt(questions)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if not answers:
# REMOVED_UNUSED_CODE:         # Interrupted questionary sessions return an empty dict.
# REMOVED_UNUSED_CODE:         raise OperationalException("User interrupted interactive questions.")
# REMOVED_UNUSED_CODE:     # Ensure default is set for non-futures exchanges
# REMOVED_UNUSED_CODE:     answers["trading_mode"] = answers.get("trading_mode", "spot")
# REMOVED_UNUSED_CODE:     answers["margin_mode"] = "isolated" if answers.get("trading_mode") == "futures" else ""
# REMOVED_UNUSED_CODE:     # Force JWT token to be a random string
# REMOVED_UNUSED_CODE:     answers["api_server_jwt_key"] = secrets.token_hex()
# REMOVED_UNUSED_CODE:     answers["api_server_ws_token"] = secrets.token_urlsafe(25)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return answers


# REMOVED_UNUSED_CODE: def deploy_new_config(config_path: Path, selections: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Applies selections to the template and writes the result to config_path
# REMOVED_UNUSED_CODE:     :param config_path: Path object for new config file. Should not exist yet
# REMOVED_UNUSED_CODE:     :param selections: Dict containing selections taken by the user.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     from jinja2.exceptions import TemplateNotFound
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     from freqtrade.exchange import MAP_EXCHANGE_CHILDCLASS
# REMOVED_UNUSED_CODE:     from freqtrade.util import render_template
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     try:
# REMOVED_UNUSED_CODE:         exchange_template = MAP_EXCHANGE_CHILDCLASS.get(
# REMOVED_UNUSED_CODE:             selections["exchange_name"], selections["exchange_name"]
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         selections["exchange"] = render_template(
# REMOVED_UNUSED_CODE:             templatefile=f"subtemplates/exchange_{exchange_template}.j2", arguments=selections
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:     except TemplateNotFound:
# REMOVED_UNUSED_CODE:         selections["exchange"] = render_template(
# REMOVED_UNUSED_CODE:             templatefile="subtemplates/exchange_generic.j2", arguments=selections
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     config_text = render_template(templatefile="base_config.json.j2", arguments=selections)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     logger.info(f"Writing config to `{config_path}`.")
# REMOVED_UNUSED_CODE:     logger.info(
# REMOVED_UNUSED_CODE:         "Please make sure to check the configuration contents and adjust settings to your needs."
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     config_path.write_text(config_text)
