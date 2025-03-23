"""
Exchange support utils
"""

# REMOVED_UNUSED_CODE: import inspect
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from datetime import datetime, timedelta, timezone
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from math import ceil, floor
from typing import Any

import ccxt
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from ccxt import (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     DECIMAL_PLACES,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ROUND,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ROUND_DOWN,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ROUND_UP,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     SIGNIFICANT_DIGITS,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     TICK_SIZE,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     TRUNCATE,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     decimal_to_precision,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: )

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.exchange.common import (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     BAD_EXCHANGES,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     EXCHANGE_HAS_OPTIONAL,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     EXCHANGE_HAS_REQUIRED,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     MAP_EXCHANGE_CHILDCLASS,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     SUPPORTED_EXCHANGES,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.exchange.exchange_utils_timeframe import timeframe_to_minutes, timeframe_to_prev_date
# REMOVED_UNUSED_CODE: from freqtrade.ft_types import ValidExchangesType
# REMOVED_UNUSED_CODE: from freqtrade.util import FtPrecise


CcxtModuleType = Any


# REMOVED_UNUSED_CODE: def is_exchange_known_ccxt(exchange_name: str, ccxt_module: CcxtModuleType | None = None) -> bool:
# REMOVED_UNUSED_CODE:     return exchange_name in ccxt_exchanges(ccxt_module)


# REMOVED_UNUSED_CODE: def ccxt_exchanges(ccxt_module: CcxtModuleType | None = None) -> list[str]:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Return the list of all exchanges known to ccxt
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     return ccxt_module.exchanges if ccxt_module is not None else ccxt.exchanges


# REMOVED_UNUSED_CODE: def available_exchanges(ccxt_module: CcxtModuleType | None = None) -> list[str]:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Return exchanges available to the bot, i.e. non-bad exchanges in the ccxt list
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     exchanges = ccxt_exchanges(ccxt_module)
# REMOVED_UNUSED_CODE:     return [x for x in exchanges if validate_exchange(x)[0]]


# REMOVED_UNUSED_CODE: def validate_exchange(exchange: str) -> tuple[bool, str, ccxt.Exchange | None]:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     returns: can_use, reason, exchange_object
# REMOVED_UNUSED_CODE:         with Reason including both missing and missing_opt
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     try:
# REMOVED_UNUSED_CODE:         ex_mod = getattr(ccxt.pro, exchange.lower())()
# REMOVED_UNUSED_CODE:     except AttributeError:
# REMOVED_UNUSED_CODE:         ex_mod = getattr(ccxt.async_support, exchange.lower())()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if not ex_mod or not ex_mod.has:
# REMOVED_UNUSED_CODE:         return False, "", None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     result = True
# REMOVED_UNUSED_CODE:     reason = ""
# REMOVED_UNUSED_CODE:     missing = [
# REMOVED_UNUSED_CODE:         k
# REMOVED_UNUSED_CODE:         for k, v in EXCHANGE_HAS_REQUIRED.items()
# REMOVED_UNUSED_CODE:         if ex_mod.has.get(k) is not True and not (all(ex_mod.has.get(x) for x in v))
# REMOVED_UNUSED_CODE:     ]
# REMOVED_UNUSED_CODE:     if missing:
# REMOVED_UNUSED_CODE:         result = False
# REMOVED_UNUSED_CODE:         reason += f"missing: {', '.join(missing)}"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     missing_opt = [k for k in EXCHANGE_HAS_OPTIONAL if not ex_mod.has.get(k)]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if exchange.lower() in BAD_EXCHANGES:
# REMOVED_UNUSED_CODE:         result = False
# REMOVED_UNUSED_CODE:         reason = BAD_EXCHANGES.get(exchange.lower(), "")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if missing_opt:
# REMOVED_UNUSED_CODE:         reason += f"{'. ' if reason else ''}missing opt: {', '.join(missing_opt)}. "
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return result, reason, ex_mod


# REMOVED_UNUSED_CODE: def _build_exchange_list_entry(
# REMOVED_UNUSED_CODE:     exchange_name: str, exchangeClasses: dict[str, Any]
# REMOVED_UNUSED_CODE: ) -> ValidExchangesType:
# REMOVED_UNUSED_CODE:     exchange_name = exchange_name.lower()
# REMOVED_UNUSED_CODE:     valid, comment, ex_mod = validate_exchange(exchange_name)
# REMOVED_UNUSED_CODE:     mapped_exchange_name = MAP_EXCHANGE_CHILDCLASS.get(exchange_name, exchange_name).lower()
# REMOVED_UNUSED_CODE:     is_alias = getattr(ex_mod, "alias", False)
# REMOVED_UNUSED_CODE:     result: ValidExchangesType = {
# REMOVED_UNUSED_CODE:         "name": getattr(ex_mod, "name", exchange_name),
# REMOVED_UNUSED_CODE:         "classname": exchange_name,
# REMOVED_UNUSED_CODE:         "valid": valid,
# REMOVED_UNUSED_CODE:         "supported": mapped_exchange_name in SUPPORTED_EXCHANGES and not is_alias,
# REMOVED_UNUSED_CODE:         "comment": comment,
# REMOVED_UNUSED_CODE:         "dex": getattr(ex_mod, "dex", False),
# REMOVED_UNUSED_CODE:         "is_alias": is_alias,
# REMOVED_UNUSED_CODE:         "alias_for": inspect.getmro(ex_mod.__class__)[1]().id
# REMOVED_UNUSED_CODE:         if getattr(ex_mod, "alias", False)
# REMOVED_UNUSED_CODE:         else None,
# REMOVED_UNUSED_CODE:         "trade_modes": [{"trading_mode": "spot", "margin_mode": ""}],
# REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE:     if resolved := exchangeClasses.get(mapped_exchange_name):
# REMOVED_UNUSED_CODE:         supported_modes = [{"trading_mode": "spot", "margin_mode": ""}] + [
# REMOVED_UNUSED_CODE:             {"trading_mode": tm.value, "margin_mode": mm.value}
# REMOVED_UNUSED_CODE:             for tm, mm in resolved["class"]._supported_trading_mode_margin_pairs
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE:         result.update(
# REMOVED_UNUSED_CODE:             {
# REMOVED_UNUSED_CODE:                 "trade_modes": supported_modes,
# REMOVED_UNUSED_CODE:             }
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return result


# REMOVED_UNUSED_CODE: def list_available_exchanges(all_exchanges: bool) -> list[ValidExchangesType]:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     :return: List of tuples with exchangename, valid, reason.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     exchanges = ccxt_exchanges() if all_exchanges else available_exchanges()
# REMOVED_UNUSED_CODE:     from freqtrade.resolvers.exchange_resolver import ExchangeResolver
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     subclassed = {e["name"].lower(): e for e in ExchangeResolver.search_all_objects({}, False)}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     exchanges_valid: list[ValidExchangesType] = [
# REMOVED_UNUSED_CODE:         _build_exchange_list_entry(e, subclassed) for e in exchanges
# REMOVED_UNUSED_CODE:     ]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return exchanges_valid


# REMOVED_UNUSED_CODE: def date_minus_candles(timeframe: str, candle_count: int, date: datetime | None = None) -> datetime:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     subtract X candles from a date.
# REMOVED_UNUSED_CODE:     :param timeframe: timeframe in string format (e.g. "5m")
# REMOVED_UNUSED_CODE:     :param candle_count: Amount of candles to subtract.
# REMOVED_UNUSED_CODE:     :param date: date to use. Defaults to now(utc)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     if not date:
# REMOVED_UNUSED_CODE:         date = datetime.now(timezone.utc)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     tf_min = timeframe_to_minutes(timeframe)
# REMOVED_UNUSED_CODE:     new_date = timeframe_to_prev_date(timeframe, date) - timedelta(minutes=tf_min * candle_count)
# REMOVED_UNUSED_CODE:     return new_date


# REMOVED_UNUSED_CODE: def market_is_active(market: dict) -> bool:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Return True if the market is active.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     # "It's active, if the active flag isn't explicitly set to false. If it's missing or
# REMOVED_UNUSED_CODE:     # true then it's true. If it's undefined, then it's most likely true, but not 100% )"
# REMOVED_UNUSED_CODE:     # See https://github.com/ccxt/ccxt/issues/4874,
# REMOVED_UNUSED_CODE:     # https://github.com/ccxt/ccxt/issues/4075#issuecomment-434760520
# REMOVED_UNUSED_CODE:     return market.get("active", True) is not False


# REMOVED_UNUSED_CODE: def amount_to_contracts(amount: float, contract_size: float | None) -> float:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Convert amount to contracts.
# REMOVED_UNUSED_CODE:     :param amount: amount to convert
# REMOVED_UNUSED_CODE:     :param contract_size: contract size - taken from exchange.get_contract_size(pair)
# REMOVED_UNUSED_CODE:     :return: num-contracts
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     if contract_size and contract_size != 1:
# REMOVED_UNUSED_CODE:         return float(FtPrecise(amount) / FtPrecise(contract_size))
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         return amount


# REMOVED_UNUSED_CODE: def contracts_to_amount(num_contracts: float, contract_size: float | None) -> float:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Takes num-contracts and converts it to contract size
# REMOVED_UNUSED_CODE:     :param num_contracts: number of contracts
# REMOVED_UNUSED_CODE:     :param contract_size: contract size - taken from exchange.get_contract_size(pair)
# REMOVED_UNUSED_CODE:     :return: Amount
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if contract_size and contract_size != 1:
# REMOVED_UNUSED_CODE:         return float(FtPrecise(num_contracts) * FtPrecise(contract_size))
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         return num_contracts


# REMOVED_UNUSED_CODE: def amount_to_precision(
# REMOVED_UNUSED_CODE:     amount: float, amount_precision: float | None, precisionMode: int | None
# REMOVED_UNUSED_CODE: ) -> float:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Returns the amount to buy or sell to a precision the Exchange accepts
# REMOVED_UNUSED_CODE:     Re-implementation of ccxt internal methods - ensuring we can test the result is correct
# REMOVED_UNUSED_CODE:     based on our definitions.
# REMOVED_UNUSED_CODE:     :param amount: amount to truncate
# REMOVED_UNUSED_CODE:     :param amount_precision: amount precision to use.
# REMOVED_UNUSED_CODE:                              should be retrieved from markets[pair]['precision']['amount']
# REMOVED_UNUSED_CODE:     :param precisionMode: precision mode to use. Should be used from precisionMode
# REMOVED_UNUSED_CODE:                           one of ccxt's DECIMAL_PLACES, SIGNIFICANT_DIGITS, or TICK_SIZE
# REMOVED_UNUSED_CODE:     :return: truncated amount
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     if amount_precision is not None and precisionMode is not None:
# REMOVED_UNUSED_CODE:         precision = int(amount_precision) if precisionMode != TICK_SIZE else amount_precision
# REMOVED_UNUSED_CODE:         # precision must be an int for non-ticksize inputs.
# REMOVED_UNUSED_CODE:         amount = float(
# REMOVED_UNUSED_CODE:             decimal_to_precision(
# REMOVED_UNUSED_CODE:                 amount,
# REMOVED_UNUSED_CODE:                 rounding_mode=TRUNCATE,
# REMOVED_UNUSED_CODE:                 precision=precision,
# REMOVED_UNUSED_CODE:                 counting_mode=precisionMode,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return amount


# REMOVED_UNUSED_CODE: def amount_to_contract_precision(
# REMOVED_UNUSED_CODE:     amount,
# REMOVED_UNUSED_CODE:     amount_precision: float | None,
# REMOVED_UNUSED_CODE:     precisionMode: int | None,
# REMOVED_UNUSED_CODE:     contract_size: float | None,
# REMOVED_UNUSED_CODE: ) -> float:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Returns the amount to buy or sell to a precision the Exchange accepts
# REMOVED_UNUSED_CODE:     including calculation to and from contracts.
# REMOVED_UNUSED_CODE:     Re-implementation of ccxt internal methods - ensuring we can test the result is correct
# REMOVED_UNUSED_CODE:     based on our definitions.
# REMOVED_UNUSED_CODE:     :param amount: amount to truncate
# REMOVED_UNUSED_CODE:     :param amount_precision: amount precision to use.
# REMOVED_UNUSED_CODE:                              should be retrieved from markets[pair]['precision']['amount']
# REMOVED_UNUSED_CODE:     :param precisionMode: precision mode to use. Should be used from precisionMode
# REMOVED_UNUSED_CODE:                           one of ccxt's DECIMAL_PLACES, SIGNIFICANT_DIGITS, or TICK_SIZE
# REMOVED_UNUSED_CODE:     :param contract_size: contract size - taken from exchange.get_contract_size(pair)
# REMOVED_UNUSED_CODE:     :return: truncated amount
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     if amount_precision is not None and precisionMode is not None:
# REMOVED_UNUSED_CODE:         contracts = amount_to_contracts(amount, contract_size)
# REMOVED_UNUSED_CODE:         amount_p = amount_to_precision(contracts, amount_precision, precisionMode)
# REMOVED_UNUSED_CODE:         return contracts_to_amount(amount_p, contract_size)
# REMOVED_UNUSED_CODE:     return amount


# REMOVED_UNUSED_CODE: def __price_to_precision_significant_digits(
# REMOVED_UNUSED_CODE:     price: float,
# REMOVED_UNUSED_CODE:     price_precision: float,
# REMOVED_UNUSED_CODE:     *,
# REMOVED_UNUSED_CODE:     rounding_mode: int = ROUND,
# REMOVED_UNUSED_CODE: ) -> float:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Implementation of ROUND_UP/Round_down for significant digits mode.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     from decimal import ROUND_DOWN as dec_ROUND_DOWN
# REMOVED_UNUSED_CODE:     from decimal import ROUND_UP as dec_ROUND_UP
# REMOVED_UNUSED_CODE:     from decimal import Decimal
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     dec = Decimal(str(price))
# REMOVED_UNUSED_CODE:     string = f"{dec:f}"
# REMOVED_UNUSED_CODE:     precision = round(price_precision)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     q = precision - dec.adjusted() - 1
# REMOVED_UNUSED_CODE:     sigfig = Decimal("10") ** -q
# REMOVED_UNUSED_CODE:     if q < 0:
# REMOVED_UNUSED_CODE:         string_to_precision = string[:precision]
# REMOVED_UNUSED_CODE:         # string_to_precision is '' when we have zero precision
# REMOVED_UNUSED_CODE:         below = sigfig * Decimal(string_to_precision if string_to_precision else "0")
# REMOVED_UNUSED_CODE:         above = below + sigfig
# REMOVED_UNUSED_CODE:         res = above if rounding_mode == ROUND_UP else below
# REMOVED_UNUSED_CODE:         precise = f"{res:f}"
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         precise = "{:f}".format(
# REMOVED_UNUSED_CODE:             dec.quantize(
# REMOVED_UNUSED_CODE:                 sigfig, rounding=dec_ROUND_DOWN if rounding_mode == ROUND_DOWN else dec_ROUND_UP
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:     return float(precise)


# REMOVED_UNUSED_CODE: def price_to_precision(
# REMOVED_UNUSED_CODE:     price: float,
# REMOVED_UNUSED_CODE:     price_precision: float | None,
# REMOVED_UNUSED_CODE:     precisionMode: int | None,
# REMOVED_UNUSED_CODE:     *,
# REMOVED_UNUSED_CODE:     rounding_mode: int = ROUND,
# REMOVED_UNUSED_CODE: ) -> float:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Returns the price rounded to the precision the Exchange accepts.
# REMOVED_UNUSED_CODE:     Partial Re-implementation of ccxt internal method decimal_to_precision(),
# REMOVED_UNUSED_CODE:     which does not support rounding up.
# REMOVED_UNUSED_CODE:     For stoploss calculations, must use ROUND_UP for longs, and ROUND_DOWN for shorts.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     TODO: If ccxt supports ROUND_UP for decimal_to_precision(), we could remove this and
# REMOVED_UNUSED_CODE:     align with amount_to_precision().
# REMOVED_UNUSED_CODE:     :param price: price to convert
# REMOVED_UNUSED_CODE:     :param price_precision: price precision to use. Used from markets[pair]['precision']['price']
# REMOVED_UNUSED_CODE:     :param precisionMode: precision mode to use. Should be used from precisionMode
# REMOVED_UNUSED_CODE:                           one of ccxt's DECIMAL_PLACES, SIGNIFICANT_DIGITS, or TICK_SIZE
# REMOVED_UNUSED_CODE:     :param rounding_mode: rounding mode to use. Defaults to ROUND
# REMOVED_UNUSED_CODE:     :return: price rounded up to the precision the Exchange accepts
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     if price_precision is not None and precisionMode is not None:
# REMOVED_UNUSED_CODE:         if rounding_mode not in (ROUND_UP, ROUND_DOWN):
# REMOVED_UNUSED_CODE:             # Use CCXT code where possible.
# REMOVED_UNUSED_CODE:             return float(
# REMOVED_UNUSED_CODE:                 decimal_to_precision(
# REMOVED_UNUSED_CODE:                     price,
# REMOVED_UNUSED_CODE:                     rounding_mode=rounding_mode,
# REMOVED_UNUSED_CODE:                     precision=int(price_precision)
# REMOVED_UNUSED_CODE:                     if precisionMode != TICK_SIZE
# REMOVED_UNUSED_CODE:                     else price_precision,
# REMOVED_UNUSED_CODE:                     counting_mode=precisionMode,
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if precisionMode == TICK_SIZE:
# REMOVED_UNUSED_CODE:             precision = FtPrecise(price_precision)
# REMOVED_UNUSED_CODE:             price_str = FtPrecise(price)
# REMOVED_UNUSED_CODE:             missing = price_str % precision
# REMOVED_UNUSED_CODE:             if not missing == FtPrecise("0"):
# REMOVED_UNUSED_CODE:                 if rounding_mode == ROUND_UP:
# REMOVED_UNUSED_CODE:                     res = price_str - missing + precision
# REMOVED_UNUSED_CODE:                 elif rounding_mode == ROUND_DOWN:
# REMOVED_UNUSED_CODE:                     res = price_str - missing
# REMOVED_UNUSED_CODE:                 return round(float(str(res)), 14)
# REMOVED_UNUSED_CODE:             return price
# REMOVED_UNUSED_CODE:         elif precisionMode == DECIMAL_PLACES:
# REMOVED_UNUSED_CODE:             ndigits = round(price_precision)
# REMOVED_UNUSED_CODE:             ticks = price * (10**ndigits)
# REMOVED_UNUSED_CODE:             if rounding_mode == ROUND_UP:
# REMOVED_UNUSED_CODE:                 return ceil(ticks) / (10**ndigits)
# REMOVED_UNUSED_CODE:             if rounding_mode == ROUND_DOWN:
# REMOVED_UNUSED_CODE:                 return floor(ticks) / (10**ndigits)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             raise ValueError(f"Unknown rounding_mode {rounding_mode}")
# REMOVED_UNUSED_CODE:         elif precisionMode == SIGNIFICANT_DIGITS:
# REMOVED_UNUSED_CODE:             if rounding_mode in (ROUND_UP, ROUND_DOWN):
# REMOVED_UNUSED_CODE:                 return __price_to_precision_significant_digits(
# REMOVED_UNUSED_CODE:                     price, price_precision, rounding_mode=rounding_mode
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         raise ValueError(f"Unknown precisionMode {precisionMode}")
# REMOVED_UNUSED_CODE:     return price
