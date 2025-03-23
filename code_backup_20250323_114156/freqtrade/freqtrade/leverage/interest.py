# REMOVED_UNUSED_CODE: from math import ceil

# REMOVED_UNUSED_CODE: from freqtrade.exceptions import OperationalException
# REMOVED_UNUSED_CODE: from freqtrade.util import FtPrecise


# REMOVED_UNUSED_CODE: one = FtPrecise(1.0)
# REMOVED_UNUSED_CODE: four = FtPrecise(4.0)
# REMOVED_UNUSED_CODE: twenty_four = FtPrecise(24.0)


# REMOVED_UNUSED_CODE: def interest(
# REMOVED_UNUSED_CODE:     exchange_name: str, borrowed: FtPrecise, rate: FtPrecise, hours: FtPrecise
# REMOVED_UNUSED_CODE: ) -> FtPrecise:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Equation to calculate interest on margin trades
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     :param exchange_name: The exchanged being trading on
# REMOVED_UNUSED_CODE:     :param borrowed: The amount of currency being borrowed
# REMOVED_UNUSED_CODE:     :param rate: The rate of interest (i.e daily interest rate)
# REMOVED_UNUSED_CODE:     :param hours: The time in hours that the currency has been borrowed for
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Raises:
# REMOVED_UNUSED_CODE:         OperationalException: Raised if freqtrade does
# REMOVED_UNUSED_CODE:         not support margin trading for this exchange
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Returns: The amount of interest owed (currency matches borrowed)
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     exchange_name = exchange_name.lower()
# REMOVED_UNUSED_CODE:     if exchange_name == "binance":
# REMOVED_UNUSED_CODE:         return borrowed * rate * FtPrecise(ceil(hours)) / twenty_four
# REMOVED_UNUSED_CODE:     elif exchange_name == "kraken":
# REMOVED_UNUSED_CODE:         # Rounded based on https://kraken-fees-calculator.github.io/
# REMOVED_UNUSED_CODE:         return borrowed * rate * (one + FtPrecise(ceil(hours / four)))
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         raise OperationalException(f"Leverage not available on {exchange_name} with freqtrade")
