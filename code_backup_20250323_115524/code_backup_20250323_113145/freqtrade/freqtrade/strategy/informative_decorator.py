from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from pandas import DataFrame

from freqtrade.enums import CandleType
# REMOVED_UNUSED_CODE: from freqtrade.exceptions import OperationalException
# REMOVED_UNUSED_CODE: from freqtrade.strategy.strategy_helper import merge_informative_pair


# REMOVED_UNUSED_CODE: PopulateIndicators = Callable[[Any, DataFrame, dict], DataFrame]


# REMOVED_UNUSED_CODE: @dataclass
class InformativeData:
# REMOVED_UNUSED_CODE:     asset: str | None
# REMOVED_UNUSED_CODE:     timeframe: str
# REMOVED_UNUSED_CODE:     fmt: str | Callable[[Any], str] | None
# REMOVED_UNUSED_CODE:     ffill: bool
# REMOVED_UNUSED_CODE:     candle_type: CandleType | None


# REMOVED_UNUSED_CODE: def informative(
# REMOVED_UNUSED_CODE:     timeframe: str,
# REMOVED_UNUSED_CODE:     asset: str = "",
# REMOVED_UNUSED_CODE:     fmt: str | Callable[[Any], str] | None = None,
# REMOVED_UNUSED_CODE:     *,
# REMOVED_UNUSED_CODE:     candle_type: CandleType | str | None = None,
# REMOVED_UNUSED_CODE:     ffill: bool = True,
# REMOVED_UNUSED_CODE: ) -> Callable[[PopulateIndicators], PopulateIndicators]:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     A decorator for populate_indicators_Nn(self, dataframe, metadata), allowing these functions to
# REMOVED_UNUSED_CODE:     define informative indicators.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Example usage:
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         @informative('1h')
# REMOVED_UNUSED_CODE:         def populate_indicators_1h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE:             dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
# REMOVED_UNUSED_CODE:             return dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     :param timeframe: Informative timeframe. Must always be equal or higher than strategy timeframe.
# REMOVED_UNUSED_CODE:     :param asset: Informative asset, for example BTC, BTC/USDT, ETH/BTC. Do not specify to use
# REMOVED_UNUSED_CODE:                   current pair. Also supports limited pair format strings (see below)
# REMOVED_UNUSED_CODE:     :param fmt: Column format (str) or column formatter (callable(name, asset, timeframe)). When not
# REMOVED_UNUSED_CODE:     specified, defaults to:
# REMOVED_UNUSED_CODE:     * {base}_{quote}_{column}_{timeframe} if asset is specified.
# REMOVED_UNUSED_CODE:     * {column}_{timeframe} if asset is not specified.
# REMOVED_UNUSED_CODE:     Pair format supports these format variables:
# REMOVED_UNUSED_CODE:     * {base} - base currency in lower case, for example 'eth'.
# REMOVED_UNUSED_CODE:     * {BASE} - same as {base}, except in upper case.
# REMOVED_UNUSED_CODE:     * {quote} - quote currency in lower case, for example 'usdt'.
# REMOVED_UNUSED_CODE:     * {QUOTE} - same as {quote}, except in upper case.
# REMOVED_UNUSED_CODE:     Format string additionally supports this variables.
# REMOVED_UNUSED_CODE:     * {asset} - full name of the asset, for example 'BTC/USDT'.
# REMOVED_UNUSED_CODE:     * {column} - name of dataframe column.
# REMOVED_UNUSED_CODE:     * {timeframe} - timeframe of informative dataframe.
# REMOVED_UNUSED_CODE:     :param ffill: ffill dataframe after merging informative pair.
# REMOVED_UNUSED_CODE:     :param candle_type: '', mark, index, premiumIndex, or funding_rate
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     _asset = asset
# REMOVED_UNUSED_CODE:     _timeframe = timeframe
# REMOVED_UNUSED_CODE:     _fmt = fmt
# REMOVED_UNUSED_CODE:     _ffill = ffill
# REMOVED_UNUSED_CODE:     _candle_type = CandleType.from_string(candle_type) if candle_type else None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def decorator(fn: PopulateIndicators):
# REMOVED_UNUSED_CODE:         informative_pairs = getattr(fn, "_ft_informative", [])
# REMOVED_UNUSED_CODE:         informative_pairs.append(InformativeData(_asset, _timeframe, _fmt, _ffill, _candle_type))
# REMOVED_UNUSED_CODE:         setattr(fn, "_ft_informative", informative_pairs)  # noqa: B010
# REMOVED_UNUSED_CODE:         return fn
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return decorator


def __get_pair_formats(market: dict[str, Any] | None) -> dict[str, str]:
    if not market:
        return {}
    base = market["base"]
    quote = market["quote"]
    return {
        "base": base.lower(),
        "BASE": base.upper(),
        "quote": quote.lower(),
        "QUOTE": quote.upper(),
    }


# REMOVED_UNUSED_CODE: def _format_pair_name(config, pair: str, market: dict[str, Any] | None = None) -> str:
# REMOVED_UNUSED_CODE:     return pair.format(
# REMOVED_UNUSED_CODE:         stake_currency=config["stake_currency"],
# REMOVED_UNUSED_CODE:         stake=config["stake_currency"],
# REMOVED_UNUSED_CODE:         **__get_pair_formats(market),
# REMOVED_UNUSED_CODE:     ).upper()


# REMOVED_UNUSED_CODE: def _create_and_merge_informative_pair(
# REMOVED_UNUSED_CODE:     strategy,
# REMOVED_UNUSED_CODE:     dataframe: DataFrame,
# REMOVED_UNUSED_CODE:     metadata: dict,
# REMOVED_UNUSED_CODE:     inf_data: InformativeData,
# REMOVED_UNUSED_CODE:     populate_indicators: PopulateIndicators,
# REMOVED_UNUSED_CODE: ):
# REMOVED_UNUSED_CODE:     asset = inf_data.asset or ""
# REMOVED_UNUSED_CODE:     timeframe = inf_data.timeframe
# REMOVED_UNUSED_CODE:     fmt = inf_data.fmt
# REMOVED_UNUSED_CODE:     candle_type = inf_data.candle_type
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     config = strategy.config
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if asset:
# REMOVED_UNUSED_CODE:         # Insert stake currency if needed.
# REMOVED_UNUSED_CODE:         market1 = strategy.dp.market(metadata["pair"])
# REMOVED_UNUSED_CODE:         asset = _format_pair_name(config, asset, market1)
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         # Not specifying an asset will define informative dataframe for current pair.
# REMOVED_UNUSED_CODE:         asset = metadata["pair"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     market = strategy.dp.market(asset)
# REMOVED_UNUSED_CODE:     if market is None:
# REMOVED_UNUSED_CODE:         raise OperationalException(f"Market {asset} is not available.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Default format. This optimizes for the common case: informative pairs using same stake
# REMOVED_UNUSED_CODE:     # currency. When quote currency matches stake currency, column name will omit base currency.
# REMOVED_UNUSED_CODE:     # This allows easily reconfiguring strategy to use different base currency. In a rare case
# REMOVED_UNUSED_CODE:     # where it is desired to keep quote currency in column name at all times user should specify
# REMOVED_UNUSED_CODE:     # fmt='{base}_{quote}_{column}_{timeframe}' format or similar.
# REMOVED_UNUSED_CODE:     if not fmt:
# REMOVED_UNUSED_CODE:         fmt = "{column}_{timeframe}"  # Informatives of current pair
# REMOVED_UNUSED_CODE:         if inf_data.asset:
# REMOVED_UNUSED_CODE:             fmt = "{base}_{quote}_" + fmt  # Informatives of other pairs
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     inf_metadata = {"pair": asset, "timeframe": timeframe}
# REMOVED_UNUSED_CODE:     inf_dataframe = strategy.dp.get_pair_dataframe(asset, timeframe, candle_type)
# REMOVED_UNUSED_CODE:     inf_dataframe = populate_indicators(strategy, inf_dataframe, inf_metadata)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     formatter: Any = None
# REMOVED_UNUSED_CODE:     if callable(fmt):
# REMOVED_UNUSED_CODE:         formatter = fmt  # A custom user-specified formatter function.
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         formatter = fmt.format  # A default string formatter.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     fmt_args = {
# REMOVED_UNUSED_CODE:         **__get_pair_formats(market),
# REMOVED_UNUSED_CODE:         "asset": asset,
# REMOVED_UNUSED_CODE:         "timeframe": timeframe,
# REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE:     inf_dataframe.rename(columns=lambda column: formatter(column=column, **fmt_args), inplace=True)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     date_column = formatter(column="date", **fmt_args)
# REMOVED_UNUSED_CODE:     if date_column in dataframe.columns:
# REMOVED_UNUSED_CODE:         raise OperationalException(
# REMOVED_UNUSED_CODE:             f"Duplicate column name {date_column} exists in "
# REMOVED_UNUSED_CODE:             f"dataframe! Ensure column names are unique!"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:     dataframe = merge_informative_pair(
# REMOVED_UNUSED_CODE:         dataframe,
# REMOVED_UNUSED_CODE:         inf_dataframe,
# REMOVED_UNUSED_CODE:         strategy.timeframe,
# REMOVED_UNUSED_CODE:         timeframe,
# REMOVED_UNUSED_CODE:         ffill=inf_data.ffill,
# REMOVED_UNUSED_CODE:         append_timeframe=False,
# REMOVED_UNUSED_CODE:         date_column=date_column,
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     return dataframe
