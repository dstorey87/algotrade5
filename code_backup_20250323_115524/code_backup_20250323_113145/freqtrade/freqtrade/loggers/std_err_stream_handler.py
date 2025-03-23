import sys
# REMOVED_UNUSED_CODE: from logging import Handler


# REMOVED_UNUSED_CODE: class FTStdErrStreamHandler(Handler):
# REMOVED_UNUSED_CODE:     def flush(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Override Flush behaviour - we keep half of the configured capacity
# REMOVED_UNUSED_CODE:         otherwise, we have moments with "empty" logs.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self.acquire()
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             sys.stderr.flush()
# REMOVED_UNUSED_CODE:         finally:
# REMOVED_UNUSED_CODE:             self.release()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def emit(self, record):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             msg = self.format(record)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Don't keep a reference to stderr - this can be problematic with progressbars.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             sys.stderr.write(msg + "\n")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.flush()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         except RecursionError:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         except Exception:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.handleError(record)
