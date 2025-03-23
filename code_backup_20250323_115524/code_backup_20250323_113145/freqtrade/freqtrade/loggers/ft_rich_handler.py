# REMOVED_UNUSED_CODE: from datetime import datetime
# REMOVED_UNUSED_CODE: from logging import Handler

# REMOVED_UNUSED_CODE: from rich._null_file import NullFile
# REMOVED_UNUSED_CODE: from rich.console import Console
# REMOVED_UNUSED_CODE: from rich.text import Text


# REMOVED_UNUSED_CODE: class FtRichHandler(Handler):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Basic colorized logging handler using Rich.
# REMOVED_UNUSED_CODE:     Does not support all features of the standard logging handler, and uses a hard-coded log format
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, console: Console, *args, **kwargs) -> None:
# REMOVED_UNUSED_CODE:         super().__init__(*args, **kwargs)
# REMOVED_UNUSED_CODE:         self._console = console
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def emit(self, record):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             msg = self.format(record)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Format log message
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             log_time = Text(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S,%f")[:-3],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             name = Text(record.name, style="violet")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             log_level = Text(record.levelname, style=f"logging.level.{record.levelname.lower()}")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             gray_sep = Text(" - ", style="gray46")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if isinstance(self._console.file, NullFile):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # Handles pythonw, where stdout/stderr are null, and we return NullFile
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # instance from Console.file. In this case, we still want to make a log record
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # even though we won't be writing anything to a file.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.handleError(record)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._console.print(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 Text() + log_time + gray_sep + name + gray_sep + log_level + gray_sep + msg
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         except RecursionError:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         except Exception:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.handleError(record)
