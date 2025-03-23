from freqtrade.constants import DECIMAL_PER_COIN_FALLBACK, DECIMALS_PER_COIN


def decimals_per_coin(coin: str):
    """
    Helper method getting decimal amount for this coin
    example usage: f".{decimals_per_coin('USD')}f"
    :param coin: Which coin are we printing the price / value for
    """
    return DECIMALS_PER_COIN.get(coin, DECIMAL_PER_COIN_FALLBACK)


def strip_trailing_zeros(value: str) -> str:
    """
    Strip trailing zeros from a string
    :param value: Value to be stripped
    :return: Stripped value
    """
    return value.rstrip("0").rstrip(".")


def round_value(value: float, decimals: int, keep_trailing_zeros=False) -> str:
    """
    Round value to given decimals
    :param value: Value to be rounded
    :param decimals: Number of decimals to round to
    :param keep_trailing_zeros: Keep trailing zeros "222.200" vs. "222.2"
    :return: Rounded value as string
    """
    val = f"{value:.{decimals}f}"
    if not keep_trailing_zeros:
        val = strip_trailing_zeros(val)
    return val


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
