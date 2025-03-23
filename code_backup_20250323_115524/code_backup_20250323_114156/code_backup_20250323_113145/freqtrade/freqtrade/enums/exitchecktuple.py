from freqtrade.enums.exittype import ExitType


# REMOVED_UNUSED_CODE: class ExitCheckTuple:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     NamedTuple for Exit type + reason
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     exit_type: ExitType
# REMOVED_UNUSED_CODE:     exit_reason: str = ""
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, exit_type: ExitType, exit_reason: str = ""):
# REMOVED_UNUSED_CODE:         self.exit_type = exit_type
# REMOVED_UNUSED_CODE:         self.exit_reason = exit_reason or exit_type.value
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def exit_flag(self):
# REMOVED_UNUSED_CODE:         return self.exit_type != ExitType.NONE
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __eq__(self, other):
# REMOVED_UNUSED_CODE:         return self.exit_type == other.exit_type and self.exit_reason == other.exit_reason
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __repr__(self):
# REMOVED_UNUSED_CODE:         return f"ExitCheckTuple({self.exit_type}, {self.exit_reason})"
