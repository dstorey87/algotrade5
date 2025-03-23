from enum import Enum


class RPCMessageType(str, Enum):
# REMOVED_UNUSED_CODE:     STATUS = "status"
# REMOVED_UNUSED_CODE:     WARNING = "warning"
# REMOVED_UNUSED_CODE:     EXCEPTION = "exception"
# REMOVED_UNUSED_CODE:     STARTUP = "startup"

# REMOVED_UNUSED_CODE:     ENTRY = "entry"
# REMOVED_UNUSED_CODE:     ENTRY_FILL = "entry_fill"
# REMOVED_UNUSED_CODE:     ENTRY_CANCEL = "entry_cancel"

# REMOVED_UNUSED_CODE:     EXIT = "exit"
# REMOVED_UNUSED_CODE:     EXIT_FILL = "exit_fill"
# REMOVED_UNUSED_CODE:     EXIT_CANCEL = "exit_cancel"

# REMOVED_UNUSED_CODE:     PROTECTION_TRIGGER = "protection_trigger"
# REMOVED_UNUSED_CODE:     PROTECTION_TRIGGER_GLOBAL = "protection_trigger_global"

# REMOVED_UNUSED_CODE:     STRATEGY_MSG = "strategy_msg"

    WHITELIST = "whitelist"
    ANALYZED_DF = "analyzed_df"
    NEW_CANDLE = "new_candle"

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value


# Enum for parsing requests from ws consumers
# REMOVED_UNUSED_CODE: class RPCRequestType(str, Enum):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     SUBSCRIBE = "subscribe"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     WHITELIST = "whitelist"
# REMOVED_UNUSED_CODE:     ANALYZED_DF = "analyzed_df"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __str__(self):
# REMOVED_UNUSED_CODE:         return self.value


# REMOVED_UNUSED_CODE: NO_ECHO_MESSAGES = (RPCMessageType.ANALYZED_DF, RPCMessageType.WHITELIST, RPCMessageType.NEW_CANDLE)
