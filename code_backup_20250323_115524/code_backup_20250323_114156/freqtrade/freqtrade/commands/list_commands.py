# REMOVED_UNUSED_CODE: import csv
import logging
import sys
# REMOVED_UNUSED_CODE: from typing import Any

# REMOVED_UNUSED_CODE: from freqtrade.enums import RunMode
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.exceptions import ConfigurationError, OperationalException
# REMOVED_UNUSED_CODE: from freqtrade.ft_types import ValidExchangesType


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: def start_list_exchanges(args: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Print available exchanges
# REMOVED_UNUSED_CODE:     :param args: Cli args from Arguments()
# REMOVED_UNUSED_CODE:     :return: None
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     from rich.console import Console
# REMOVED_UNUSED_CODE:     from rich.table import Table
# REMOVED_UNUSED_CODE:     from rich.text import Text
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     from freqtrade.exchange import list_available_exchanges
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     available_exchanges: list[ValidExchangesType] = list_available_exchanges(
# REMOVED_UNUSED_CODE:         args["list_exchanges_all"]
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if args["print_one_column"]:
# REMOVED_UNUSED_CODE:         print("\n".join([e["classname"] for e in available_exchanges]))
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         if args["list_exchanges_all"]:
# REMOVED_UNUSED_CODE:             title = (
# REMOVED_UNUSED_CODE:                 f"All exchanges supported by the ccxt library "
# REMOVED_UNUSED_CODE:                 f"({len(available_exchanges)} exchanges):"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             available_exchanges = [e for e in available_exchanges if e["valid"] is not False]
# REMOVED_UNUSED_CODE:             title = f"Exchanges available for Freqtrade ({len(available_exchanges)} exchanges):"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         table = Table(title=title)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         table.add_column("Exchange Name")
# REMOVED_UNUSED_CODE:         table.add_column("Class Name")
# REMOVED_UNUSED_CODE:         table.add_column("Markets")
# REMOVED_UNUSED_CODE:         table.add_column("Reason")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         for exchange in available_exchanges:
# REMOVED_UNUSED_CODE:             name = Text(exchange["name"])
# REMOVED_UNUSED_CODE:             if exchange["supported"]:
# REMOVED_UNUSED_CODE:                 name.append(" (Supported)", style="italic")
# REMOVED_UNUSED_CODE:                 name.stylize("green bold")
# REMOVED_UNUSED_CODE:             classname = Text(exchange["classname"])
# REMOVED_UNUSED_CODE:             if exchange["is_alias"]:
# REMOVED_UNUSED_CODE:                 name.stylize("strike")
# REMOVED_UNUSED_CODE:                 classname.stylize("strike")
# REMOVED_UNUSED_CODE:                 classname.append(f" (use {exchange['alias_for']})", style="italic")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             trade_modes = Text(
# REMOVED_UNUSED_CODE:                 ", ".join(
# REMOVED_UNUSED_CODE:                     (f"{a.get('margin_mode', '')} {a['trading_mode']}").lstrip()
# REMOVED_UNUSED_CODE:                     for a in exchange["trade_modes"]
# REMOVED_UNUSED_CODE:                 ),
# REMOVED_UNUSED_CODE:                 style="",
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             if exchange["dex"]:
# REMOVED_UNUSED_CODE:                 trade_modes = Text("DEX: ") + trade_modes
# REMOVED_UNUSED_CODE:                 trade_modes.stylize("bold", 0, 3)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             table.add_row(
# REMOVED_UNUSED_CODE:                 name,
# REMOVED_UNUSED_CODE:                 classname,
# REMOVED_UNUSED_CODE:                 trade_modes,
# REMOVED_UNUSED_CODE:                 exchange["comment"],
# REMOVED_UNUSED_CODE:                 style=None if exchange["valid"] else "red",
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             # table.add_row(*[exchange[header] for header in headers])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         console = Console()
# REMOVED_UNUSED_CODE:         console.print(table)


# REMOVED_UNUSED_CODE: def _print_objs_tabular(objs: list, print_colorized: bool) -> None:
# REMOVED_UNUSED_CODE:     from rich.console import Console
# REMOVED_UNUSED_CODE:     from rich.table import Table
# REMOVED_UNUSED_CODE:     from rich.text import Text
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     names = [s["name"] for s in objs]
# REMOVED_UNUSED_CODE:     objs_to_print: list[dict[str, Text | str]] = [
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "name": Text(s["name"] if s["name"] else "--"),
# REMOVED_UNUSED_CODE:             "location": s["location_rel"],
# REMOVED_UNUSED_CODE:             "status": (
# REMOVED_UNUSED_CODE:                 Text("LOAD FAILED", style="bold red")
# REMOVED_UNUSED_CODE:                 if s["class"] is None
# REMOVED_UNUSED_CODE:                 else Text("OK", style="bold green")
# REMOVED_UNUSED_CODE:                 if names.count(s["name"]) == 1
# REMOVED_UNUSED_CODE:                 else Text("DUPLICATE NAME", style="bold yellow")
# REMOVED_UNUSED_CODE:             ),
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE:         for s in objs
# REMOVED_UNUSED_CODE:     ]
# REMOVED_UNUSED_CODE:     for idx, s in enumerate(objs):
# REMOVED_UNUSED_CODE:         if "hyperoptable" in s:
# REMOVED_UNUSED_CODE:             objs_to_print[idx].update(
# REMOVED_UNUSED_CODE:                 {
# REMOVED_UNUSED_CODE:                     "hyperoptable": "Yes" if s["hyperoptable"]["count"] > 0 else "No",
# REMOVED_UNUSED_CODE:                     "buy-Params": str(len(s["hyperoptable"].get("buy", []))),
# REMOVED_UNUSED_CODE:                     "sell-Params": str(len(s["hyperoptable"].get("sell", []))),
# REMOVED_UNUSED_CODE:                 }
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:     table = Table()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     for header in objs_to_print[0].keys():
# REMOVED_UNUSED_CODE:         table.add_column(header.capitalize(), justify="right")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     for row in objs_to_print:
# REMOVED_UNUSED_CODE:         table.add_row(*[row[header] for header in objs_to_print[0].keys()])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     console = Console(
# REMOVED_UNUSED_CODE:         color_system="auto" if print_colorized else None,
# REMOVED_UNUSED_CODE:         width=200 if "pytest" in sys.modules else None,
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     console.print(table)


# REMOVED_UNUSED_CODE: def start_list_strategies(args: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Print files with Strategy custom classes available in the directory
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     from freqtrade.configuration import setup_utils_configuration
# REMOVED_UNUSED_CODE:     from freqtrade.resolvers import StrategyResolver
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     config = setup_utils_configuration(args, RunMode.UTIL_NO_EXCHANGE)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     strategy_objs = StrategyResolver.search_all_objects(
# REMOVED_UNUSED_CODE:         config, not args["print_one_column"], config.get("recursive_strategy_search", False)
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     # Sort alphabetically
# REMOVED_UNUSED_CODE:     strategy_objs = sorted(strategy_objs, key=lambda x: x["name"])
# REMOVED_UNUSED_CODE:     for obj in strategy_objs:
# REMOVED_UNUSED_CODE:         if obj["class"]:
# REMOVED_UNUSED_CODE:             obj["hyperoptable"] = obj["class"].detect_all_parameters()
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             obj["hyperoptable"] = {"count": 0}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if args["print_one_column"]:
# REMOVED_UNUSED_CODE:         print("\n".join([s["name"] for s in strategy_objs]))
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         _print_objs_tabular(strategy_objs, config.get("print_colorized", False))


# REMOVED_UNUSED_CODE: def start_list_freqAI_models(args: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Print files with FreqAI models custom classes available in the directory
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     from freqtrade.configuration import setup_utils_configuration
# REMOVED_UNUSED_CODE:     from freqtrade.resolvers.freqaimodel_resolver import FreqaiModelResolver
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     config = setup_utils_configuration(args, RunMode.UTIL_NO_EXCHANGE)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     model_objs = FreqaiModelResolver.search_all_objects(config, not args["print_one_column"])
# REMOVED_UNUSED_CODE:     # Sort alphabetically
# REMOVED_UNUSED_CODE:     model_objs = sorted(model_objs, key=lambda x: x["name"])
# REMOVED_UNUSED_CODE:     if args["print_one_column"]:
# REMOVED_UNUSED_CODE:         print("\n".join([s["name"] for s in model_objs]))
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         _print_objs_tabular(model_objs, config.get("print_colorized", False))


# REMOVED_UNUSED_CODE: def start_list_hyperopt_loss_functions(args: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Print files with FreqAI models custom classes available in the directory
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     from freqtrade.configuration import setup_utils_configuration
# REMOVED_UNUSED_CODE:     from freqtrade.resolvers.hyperopt_resolver import HyperOptLossResolver
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     config = setup_utils_configuration(args, RunMode.UTIL_NO_EXCHANGE)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     model_objs = HyperOptLossResolver.search_all_objects(config, not args["print_one_column"])
# REMOVED_UNUSED_CODE:     # Sort alphabetically
# REMOVED_UNUSED_CODE:     model_objs = sorted(model_objs, key=lambda x: x["name"])
# REMOVED_UNUSED_CODE:     if args["print_one_column"]:
# REMOVED_UNUSED_CODE:         print("\n".join([s["name"] for s in model_objs]))
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         _print_objs_tabular(model_objs, config.get("print_colorized", False))


# REMOVED_UNUSED_CODE: def start_list_timeframes(args: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Print timeframes available on Exchange
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     from freqtrade.configuration import setup_utils_configuration
# REMOVED_UNUSED_CODE:     from freqtrade.resolvers import ExchangeResolver
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     config = setup_utils_configuration(args, RunMode.UTIL_EXCHANGE)
# REMOVED_UNUSED_CODE:     # Do not use timeframe set in the config
# REMOVED_UNUSED_CODE:     config["timeframe"] = None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Init exchange
# REMOVED_UNUSED_CODE:     exchange = ExchangeResolver.load_exchange(config, validate=False)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if args["print_one_column"]:
# REMOVED_UNUSED_CODE:         print("\n".join(exchange.timeframes))
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         print(
# REMOVED_UNUSED_CODE:             f"Timeframes available for the exchange `{exchange.name}`: "
# REMOVED_UNUSED_CODE:             f"{', '.join(exchange.timeframes)}"
# REMOVED_UNUSED_CODE:         )


# REMOVED_UNUSED_CODE: def start_list_markets(args: dict[str, Any], pairs_only: bool = False) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Print pairs/markets on the exchange
# REMOVED_UNUSED_CODE:     :param args: Cli args from Arguments()
# REMOVED_UNUSED_CODE:     :param pairs_only: if True print only pairs, otherwise print all instruments (markets)
# REMOVED_UNUSED_CODE:     :return: None
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     from freqtrade.configuration import setup_utils_configuration
# REMOVED_UNUSED_CODE:     from freqtrade.exchange import market_is_active
# REMOVED_UNUSED_CODE:     from freqtrade.misc import plural
# REMOVED_UNUSED_CODE:     from freqtrade.resolvers import ExchangeResolver
# REMOVED_UNUSED_CODE:     from freqtrade.util import print_rich_table
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     config = setup_utils_configuration(args, RunMode.UTIL_EXCHANGE)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Init exchange
# REMOVED_UNUSED_CODE:     exchange = ExchangeResolver.load_exchange(config, validate=False)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # By default only active pairs/markets are to be shown
# REMOVED_UNUSED_CODE:     active_only = not args.get("list_pairs_all", False)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     base_currencies = args.get("base_currencies", [])
# REMOVED_UNUSED_CODE:     quote_currencies = args.get("quote_currencies", [])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     try:
# REMOVED_UNUSED_CODE:         pairs = exchange.get_markets(
# REMOVED_UNUSED_CODE:             base_currencies=base_currencies,
# REMOVED_UNUSED_CODE:             quote_currencies=quote_currencies,
# REMOVED_UNUSED_CODE:             tradable_only=pairs_only,
# REMOVED_UNUSED_CODE:             active_only=active_only,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         # Sort the pairs/markets by symbol
# REMOVED_UNUSED_CODE:         pairs = dict(sorted(pairs.items()))
# REMOVED_UNUSED_CODE:     except Exception as e:
# REMOVED_UNUSED_CODE:         raise OperationalException(f"Cannot get markets. Reason: {e}") from e
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         summary_str = (
# REMOVED_UNUSED_CODE:             (f"Exchange {exchange.name} has {len(pairs)} ")
# REMOVED_UNUSED_CODE:             + ("active " if active_only else "")
# REMOVED_UNUSED_CODE:             + (plural(len(pairs), "pair" if pairs_only else "market"))
# REMOVED_UNUSED_CODE:             + (
# REMOVED_UNUSED_CODE:                 f" with {', '.join(base_currencies)} as base "
# REMOVED_UNUSED_CODE:                 f"{plural(len(base_currencies), 'currency', 'currencies')}"
# REMOVED_UNUSED_CODE:                 if base_currencies
# REMOVED_UNUSED_CODE:                 else ""
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             + (" and" if base_currencies and quote_currencies else "")
# REMOVED_UNUSED_CODE:             + (
# REMOVED_UNUSED_CODE:                 f" with {', '.join(quote_currencies)} as quote "
# REMOVED_UNUSED_CODE:                 f"{plural(len(quote_currencies), 'currency', 'currencies')}"
# REMOVED_UNUSED_CODE:                 if quote_currencies
# REMOVED_UNUSED_CODE:                 else ""
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         headers = [
# REMOVED_UNUSED_CODE:             "Id",
# REMOVED_UNUSED_CODE:             "Symbol",
# REMOVED_UNUSED_CODE:             "Base",
# REMOVED_UNUSED_CODE:             "Quote",
# REMOVED_UNUSED_CODE:             "Active",
# REMOVED_UNUSED_CODE:             "Spot",
# REMOVED_UNUSED_CODE:             "Margin",
# REMOVED_UNUSED_CODE:             "Future",
# REMOVED_UNUSED_CODE:             "Leverage",
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         tabular_data = [
# REMOVED_UNUSED_CODE:             {
# REMOVED_UNUSED_CODE:                 "Id": v["id"],
# REMOVED_UNUSED_CODE:                 "Symbol": v["symbol"],
# REMOVED_UNUSED_CODE:                 "Base": v["base"],
# REMOVED_UNUSED_CODE:                 "Quote": v["quote"],
# REMOVED_UNUSED_CODE:                 "Active": market_is_active(v),
# REMOVED_UNUSED_CODE:                 "Spot": "Spot" if exchange.market_is_spot(v) else "",
# REMOVED_UNUSED_CODE:                 "Margin": "Margin" if exchange.market_is_margin(v) else "",
# REMOVED_UNUSED_CODE:                 "Future": "Future" if exchange.market_is_future(v) else "",
# REMOVED_UNUSED_CODE:                 "Leverage": exchange.get_max_leverage(v["symbol"], 20),
# REMOVED_UNUSED_CODE:             }
# REMOVED_UNUSED_CODE:             for _, v in pairs.items()
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if (
# REMOVED_UNUSED_CODE:             args.get("print_one_column", False)
# REMOVED_UNUSED_CODE:             or args.get("list_pairs_print_json", False)
# REMOVED_UNUSED_CODE:             or args.get("print_csv", False)
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             # Print summary string in the log in case of machine-readable
# REMOVED_UNUSED_CODE:             # regular formats.
# REMOVED_UNUSED_CODE:             logger.info(f"{summary_str}.")
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             # Print empty string separating leading logs and output in case of
# REMOVED_UNUSED_CODE:             # human-readable formats.
# REMOVED_UNUSED_CODE:             print()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if pairs:
# REMOVED_UNUSED_CODE:             if args.get("print_list", False):
# REMOVED_UNUSED_CODE:                 # print data as a list, with human-readable summary
# REMOVED_UNUSED_CODE:                 print(f"{summary_str}: {', '.join(pairs.keys())}.")
# REMOVED_UNUSED_CODE:             elif args.get("print_one_column", False):
# REMOVED_UNUSED_CODE:                 print("\n".join(pairs.keys()))
# REMOVED_UNUSED_CODE:             elif args.get("list_pairs_print_json", False):
# REMOVED_UNUSED_CODE:                 import rapidjson
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 print(rapidjson.dumps(list(pairs.keys()), default=str))
# REMOVED_UNUSED_CODE:             elif args.get("print_csv", False):
# REMOVED_UNUSED_CODE:                 writer = csv.DictWriter(sys.stdout, fieldnames=headers)
# REMOVED_UNUSED_CODE:                 writer.writeheader()
# REMOVED_UNUSED_CODE:                 writer.writerows(tabular_data)
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 print_rich_table(tabular_data, headers, summary_str)
# REMOVED_UNUSED_CODE:         elif not (
# REMOVED_UNUSED_CODE:             args.get("print_one_column", False)
# REMOVED_UNUSED_CODE:             or args.get("list_pairs_print_json", False)
# REMOVED_UNUSED_CODE:             or args.get("print_csv", False)
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             print(f"{summary_str}.")


# REMOVED_UNUSED_CODE: def start_show_trades(args: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Show trades
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     import json
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     from freqtrade.configuration import setup_utils_configuration
# REMOVED_UNUSED_CODE:     from freqtrade.misc import parse_db_uri_for_logging
# REMOVED_UNUSED_CODE:     from freqtrade.persistence import Trade, init_db
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     config = setup_utils_configuration(args, RunMode.UTIL_NO_EXCHANGE)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if "db_url" not in config:
# REMOVED_UNUSED_CODE:         raise ConfigurationError("--db-url is required for this command.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     logger.info(f'Using DB: "{parse_db_uri_for_logging(config["db_url"])}"')
# REMOVED_UNUSED_CODE:     init_db(config["db_url"])
# REMOVED_UNUSED_CODE:     tfilter = []
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if config.get("trade_ids"):
# REMOVED_UNUSED_CODE:         tfilter.append(Trade.id.in_(config["trade_ids"]))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     trades = Trade.get_trades(tfilter).all()
# REMOVED_UNUSED_CODE:     logger.info(f"Printing {len(trades)} Trades: ")
# REMOVED_UNUSED_CODE:     if config.get("print_json", False):
# REMOVED_UNUSED_CODE:         print(json.dumps([trade.to_json() for trade in trades], indent=4))
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         for trade in trades:
# REMOVED_UNUSED_CODE:             print(trade)
