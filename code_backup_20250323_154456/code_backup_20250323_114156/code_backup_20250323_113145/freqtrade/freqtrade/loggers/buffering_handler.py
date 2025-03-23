from logging.handlers import BufferingHandler


# REMOVED_UNUSED_CODE: class FTBufferingHandler(BufferingHandler):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def flush(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Override Flush behaviour - we keep half of the configured capacity
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         otherwise, we have moments with "empty" logs.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.acquire()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Keep half of the records in buffer.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             records_to_keep = -int(self.capacity / 2)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.buffer = self.buffer[records_to_keep:]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         finally:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.release()
