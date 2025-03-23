# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.constants import DECIMAL_PER_COIN_FALLBACK, DECIMALS_PER_COIN


# REMOVED_UNUSED_CODE: def decimals_per_coin(coin: str):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Helper method getting decimal amount for this coin
# REMOVED_UNUSED_CODE:     example usage: f".{decimals_per_coin('USD')}f"
# REMOVED_UNUSED_CODE:     :param coin: Which coin are we printing the price / value for
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     return DECIMALS_PER_COIN.get(coin, DECIMAL_PER_COIN_FALLBACK)


# REMOVED_UNUSED_CODE: def strip_trailing_zeros(value: str) -> str:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Strip trailing zeros from a string
# REMOVED_UNUSED_CODE:     :param value: Value to be stripped
# REMOVED_UNUSED_CODE:     :return: Stripped value
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     return value.rstrip("0").rstrip(".")


# REMOVED_UNUSED_CODE: def round_value(value: float, decimals: int, keep_trailing_zeros=False) -> str:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Round value to given decimals
# REMOVED_UNUSED_CODE:     :param value: Value to be rounded
# REMOVED_UNUSED_CODE:     :param decimals: Number of decimals to round to
# REMOVED_UNUSED_CODE:     :param keep_trailing_zeros: Keep trailing zeros "222.200" vs. "222.2"
# REMOVED_UNUSED_CODE:     :return: Rounded value as string
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     val = f"{value:.{decimals}f}"
# REMOVED_UNUSED_CODE:     if not keep_trailing_zeros:
# REMOVED_UNUSED_CODE:         val = strip_trailing_zeros(val)
# REMOVED_UNUSED_CODE:     return val


# REMOVED_UNUSED_CODE: def fmt_coin(value: float, coin: str, show_coin_name=True, keep_trailing_zeros=False) -> str:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Format price value for this coin
# REMOVED_UNUSED_CODE:     :param value: Value to be printed
# REMOVED_UNUSED_CODE:     :param coin: Which coin are we printing the price / value for
# REMOVED_UNUSED_CODE:     :param show_coin_name: Return string in format: "222.22 USDT" or "222.22"
# REMOVED_UNUSED_CODE:     :param keep_trailing_zeros: Keep trailing zeros "222.200" vs. "222.2"
# REMOVED_UNUSED_CODE:     :return: Formatted / rounded value (with or without coin name)
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     val = round_value(value, decimals_per_coin(coin), keep_trailing_zeros)
# REMOVED_UNUSED_CODE:     if show_coin_name:
# REMOVED_UNUSED_CODE:         val = f"{val} {coin}"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return val


# REMOVED_UNUSED_CODE: def fmt_coin2(
# REMOVED_UNUSED_CODE:     value: float, coin: str, decimals: int = 8, *, show_coin_name=True, keep_trailing_zeros=False
# REMOVED_UNUSED_CODE: ) -> str:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Format price value for this coin. Should be preferred for rate formatting
# REMOVED_UNUSED_CODE:     :param value: Value to be printed
# REMOVED_UNUSED_CODE:     :param coin: Which coin are we printing the price / value for
# REMOVED_UNUSED_CODE:     :param decimals: Number of decimals to round to
# REMOVED_UNUSED_CODE:     :param show_coin_name: Return string in format: "222.22 USDT" or "222.22"
# REMOVED_UNUSED_CODE:     :param keep_trailing_zeros: Keep trailing zeros "222.200" vs. "222.2"
# REMOVED_UNUSED_CODE:     :return: Formatted / rounded value (with or without coin name)
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     val = round_value(value, decimals, keep_trailing_zeros)
# REMOVED_UNUSED_CODE:     if show_coin_name:
# REMOVED_UNUSED_CODE:         val = f"{val} {coin}"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return val
