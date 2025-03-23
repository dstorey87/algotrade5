from enum import Enum


# REMOVED_UNUSED_CODE: class CandleType(str, Enum):
# REMOVED_UNUSED_CODE:     """Enum to distinguish candle types"""
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     SPOT = "spot"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     FUTURES = "futures"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     MARK = "mark"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     INDEX = "index"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     PREMIUMINDEX = "premiumIndex"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # TODO: Could take up less memory if these weren't a CandleType
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     FUNDING_RATE = "funding_rate"
# REMOVED_UNUSED_CODE:     # BORROW_RATE = "borrow_rate"  # * unimplemented
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __str__(self):
# REMOVED_UNUSED_CODE:         return f"{self.name.lower()}"

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
