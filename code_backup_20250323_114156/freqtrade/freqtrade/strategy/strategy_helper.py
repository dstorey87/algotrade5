# REMOVED_UNUSED_CODE: import pandas as pd

# REMOVED_UNUSED_CODE: from freqtrade.exchange import timeframe_to_minutes


# REMOVED_UNUSED_CODE: def merge_informative_pair(
# REMOVED_UNUSED_CODE:     dataframe: pd.DataFrame,
# REMOVED_UNUSED_CODE:     informative: pd.DataFrame,
# REMOVED_UNUSED_CODE:     timeframe: str,
# REMOVED_UNUSED_CODE:     timeframe_inf: str,
# REMOVED_UNUSED_CODE:     ffill: bool = True,
# REMOVED_UNUSED_CODE:     append_timeframe: bool = True,
# REMOVED_UNUSED_CODE:     date_column: str = "date",
# REMOVED_UNUSED_CODE:     suffix: str | None = None,
# REMOVED_UNUSED_CODE: ) -> pd.DataFrame:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Correctly merge informative samples to the original dataframe, avoiding lookahead bias.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Since dates are candle open dates, merging a 15m candle that starts at 15:00, and a
# REMOVED_UNUSED_CODE:     1h candle that starts at 15:00 will result in all candles to know the close at 16:00
# REMOVED_UNUSED_CODE:     which they should not know.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Moves the date of the informative pair by 1 time interval forward.
# REMOVED_UNUSED_CODE:     This way, the 14:00 1h candle is merged to 15:00 15m candle, since the 14:00 1h candle is the
# REMOVED_UNUSED_CODE:     last candle that's closed at 15:00, 15:15, 15:30 or 15:45.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Assuming inf_tf = '1d' - then the resulting columns will be:
# REMOVED_UNUSED_CODE:     date_1d, open_1d, high_1d, low_1d, close_1d, rsi_1d
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     :param dataframe: Original dataframe
# REMOVED_UNUSED_CODE:     :param informative: Informative pair, most likely loaded via dp.get_pair_dataframe
# REMOVED_UNUSED_CODE:     :param timeframe: Timeframe of the original pair sample.
# REMOVED_UNUSED_CODE:     :param timeframe_inf: Timeframe of the informative pair sample.
# REMOVED_UNUSED_CODE:     :param ffill: Forwardfill missing values - optional but usually required
# REMOVED_UNUSED_CODE:     :param append_timeframe: Rename columns by appending timeframe.
# REMOVED_UNUSED_CODE:     :param date_column: A custom date column name.
# REMOVED_UNUSED_CODE:     :param suffix: A string suffix to add at the end of the informative columns. If specified,
# REMOVED_UNUSED_CODE:                    append_timeframe must be false.
# REMOVED_UNUSED_CODE:     :return: Merged dataframe
# REMOVED_UNUSED_CODE:     :raise: ValueError if the secondary timeframe is shorter than the dataframe timeframe
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     informative = informative.copy()
# REMOVED_UNUSED_CODE:     minutes_inf = timeframe_to_minutes(timeframe_inf)
# REMOVED_UNUSED_CODE:     minutes = timeframe_to_minutes(timeframe)
# REMOVED_UNUSED_CODE:     if minutes == minutes_inf:
# REMOVED_UNUSED_CODE:         # No need to forwardshift if the timeframes are identical
# REMOVED_UNUSED_CODE:         informative["date_merge"] = informative[date_column]
# REMOVED_UNUSED_CODE:     elif minutes < minutes_inf:
# REMOVED_UNUSED_CODE:         # Subtract "small" timeframe so merging is not delayed by 1 small candle
# REMOVED_UNUSED_CODE:         # Detailed explanation in https://github.com/freqtrade/freqtrade/issues/4073
# REMOVED_UNUSED_CODE:         if not informative.empty:
# REMOVED_UNUSED_CODE:             if timeframe_inf == "1M":
# REMOVED_UNUSED_CODE:                 informative["date_merge"] = (
# REMOVED_UNUSED_CODE:                     informative[date_column] + pd.offsets.MonthBegin(1)
# REMOVED_UNUSED_CODE:                 ) - pd.to_timedelta(minutes, "m")
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 informative["date_merge"] = (
# REMOVED_UNUSED_CODE:                     informative[date_column]
# REMOVED_UNUSED_CODE:                     + pd.to_timedelta(minutes_inf, "m")
# REMOVED_UNUSED_CODE:                     - pd.to_timedelta(minutes, "m")
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             informative["date_merge"] = informative[date_column]
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         raise ValueError(
# REMOVED_UNUSED_CODE:             "Tried to merge a faster timeframe to a slower timeframe."
# REMOVED_UNUSED_CODE:             "This would create new rows, and can throw off your regular indicators."
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Rename columns to be unique
# REMOVED_UNUSED_CODE:     date_merge = "date_merge"
# REMOVED_UNUSED_CODE:     if suffix and append_timeframe:
# REMOVED_UNUSED_CODE:         raise ValueError("You can not specify `append_timeframe` as True and a `suffix`.")
# REMOVED_UNUSED_CODE:     elif append_timeframe:
# REMOVED_UNUSED_CODE:         date_merge = f"date_merge_{timeframe_inf}"
# REMOVED_UNUSED_CODE:         informative.columns = [f"{col}_{timeframe_inf}" for col in informative.columns]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     elif suffix:
# REMOVED_UNUSED_CODE:         date_merge = f"date_merge_{suffix}"
# REMOVED_UNUSED_CODE:         informative.columns = [f"{col}_{suffix}" for col in informative.columns]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Combine the 2 dataframes
# REMOVED_UNUSED_CODE:     # all indicators on the informative sample MUST be calculated before this point
# REMOVED_UNUSED_CODE:     if ffill:
# REMOVED_UNUSED_CODE:         # https://pandas.pydata.org/docs/user_guide/merging.html#timeseries-friendly-merging
# REMOVED_UNUSED_CODE:         # merge_ordered - ffill method is 2.5x faster than separate ffill()
# REMOVED_UNUSED_CODE:         dataframe = pd.merge_ordered(
# REMOVED_UNUSED_CODE:             dataframe,
# REMOVED_UNUSED_CODE:             informative,
# REMOVED_UNUSED_CODE:             fill_method="ffill",
# REMOVED_UNUSED_CODE:             left_on="date",
# REMOVED_UNUSED_CODE:             right_on=date_merge,
# REMOVED_UNUSED_CODE:             how="left",
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         dataframe = pd.merge(
# REMOVED_UNUSED_CODE:             dataframe, informative, left_on="date", right_on=date_merge, how="left"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:     dataframe = dataframe.drop(date_merge, axis=1)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return dataframe


# REMOVED_UNUSED_CODE: def stoploss_from_open(
# REMOVED_UNUSED_CODE:     open_relative_stop: float, current_profit: float, is_short: bool = False, leverage: float = 1.0
# REMOVED_UNUSED_CODE: ) -> float:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Given the current profit, and a desired stop loss value relative to the trade entry price,
# REMOVED_UNUSED_CODE:     return a stop loss value that is relative to the current price, and which can be
# REMOVED_UNUSED_CODE:     returned from `custom_stoploss`.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     The requested stop can be positive for a stop above the open price, or negative for
# REMOVED_UNUSED_CODE:     a stop below the open price. The return value is always >= 0.
# REMOVED_UNUSED_CODE:     `open_relative_stop` will be considered as adjusted for leverage if leverage is provided..
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Returns 0 if the resulting stop price would be above/below (longs/shorts) the current price
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     :param open_relative_stop: Desired stop loss percentage, relative to the open price,
# REMOVED_UNUSED_CODE:                                adjusted for leverage
# REMOVED_UNUSED_CODE:     :param current_profit: The current profit percentage
# REMOVED_UNUSED_CODE:     :param is_short: When true, perform the calculation for short instead of long
# REMOVED_UNUSED_CODE:     :param leverage: Leverage to use for the calculation
# REMOVED_UNUSED_CODE:     :return: Stop loss value relative to current price
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # formula is undefined for current_profit -1 (longs) or 1 (shorts), return maximum value
# REMOVED_UNUSED_CODE:     _current_profit = current_profit / leverage
# REMOVED_UNUSED_CODE:     if (_current_profit == -1 and not is_short) or (is_short and _current_profit == 1):
# REMOVED_UNUSED_CODE:         return 1
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if is_short is True:
# REMOVED_UNUSED_CODE:         stoploss = -1 + ((1 - open_relative_stop / leverage) / (1 - _current_profit))
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         stoploss = 1 - ((1 + open_relative_stop / leverage) / (1 + _current_profit))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # negative stoploss values indicate the requested stop price is higher/lower
# REMOVED_UNUSED_CODE:     # (long/short) than the current price
# REMOVED_UNUSED_CODE:     return max(stoploss * leverage, 0.0)


# REMOVED_UNUSED_CODE: def stoploss_from_absolute(
# REMOVED_UNUSED_CODE:     stop_rate: float, current_rate: float, is_short: bool = False, leverage: float = 1.0
# REMOVED_UNUSED_CODE: ) -> float:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Given current price and desired stop price, return a stop loss value that is relative to current
# REMOVED_UNUSED_CODE:     price.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     The requested stop can be positive for a stop above the open price, or negative for
# REMOVED_UNUSED_CODE:     a stop below the open price. The return value is always >= 0.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Returns 0 if the resulting stop price would be above the current price.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     :param stop_rate: Stop loss price.
# REMOVED_UNUSED_CODE:     :param current_rate: Current asset price.
# REMOVED_UNUSED_CODE:     :param is_short: When true, perform the calculation for short instead of long
# REMOVED_UNUSED_CODE:     :param leverage: Leverage to use for the calculation
# REMOVED_UNUSED_CODE:     :return: Positive stop loss value relative to current price
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # formula is undefined for current_rate 0, return maximum value
# REMOVED_UNUSED_CODE:     if current_rate == 0:
# REMOVED_UNUSED_CODE:         return 1
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     stoploss = 1 - (stop_rate / current_rate)
# REMOVED_UNUSED_CODE:     if is_short:
# REMOVED_UNUSED_CODE:         stoploss = -stoploss
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # negative stoploss values indicate the requested stop price is higher/lower
# REMOVED_UNUSED_CODE:     # (long/short) than the current price
# REMOVED_UNUSED_CODE:     # shorts can yield stoploss values higher than 1, so limit that as well
# REMOVED_UNUSED_CODE:     return max(min(stoploss, 1.0), 0.0) * leverage
