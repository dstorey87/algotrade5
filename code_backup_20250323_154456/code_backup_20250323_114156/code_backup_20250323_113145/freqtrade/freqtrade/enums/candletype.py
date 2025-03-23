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
    def from_string(value: str) -> "CandleType":
        if not value:
            # Default to spot
            return CandleType.SPOT
        return CandleType(value)

# REMOVED_UNUSED_CODE:     @staticmethod
    def get_default(trading_mode: str) -> "CandleType":
        if trading_mode == "futures":
            return CandleType.FUTURES
        return CandleType.SPOT
