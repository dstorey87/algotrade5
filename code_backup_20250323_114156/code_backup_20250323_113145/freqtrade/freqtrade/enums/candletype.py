from enum import Enum


class CandleType(str, Enum):
    """Enum to distinguish candle types"""

    SPOT = "spot"
    FUTURES = "futures"
# REMOVED_UNUSED_CODE:     MARK = "mark"
# REMOVED_UNUSED_CODE:     INDEX = "index"
# REMOVED_UNUSED_CODE:     PREMIUMINDEX = "premiumIndex"

    # TODO: Could take up less memory if these weren't a CandleType
# REMOVED_UNUSED_CODE:     FUNDING_RATE = "funding_rate"
    # BORROW_RATE = "borrow_rate"  # * unimplemented

    def __str__(self):
        return f"{self.name.lower()}"

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def from_string(value: str) -> "CandleType":
# REMOVED_UNUSED_CODE:         if not value:
# REMOVED_UNUSED_CODE:             # Default to spot
# REMOVED_UNUSED_CODE:             return CandleType.SPOT
# REMOVED_UNUSED_CODE:         return CandleType(value)

# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def get_default(trading_mode: str) -> "CandleType":
# REMOVED_UNUSED_CODE:         if trading_mode == "futures":
# REMOVED_UNUSED_CODE:             return CandleType.FUTURES
# REMOVED_UNUSED_CODE:         return CandleType.SPOT
