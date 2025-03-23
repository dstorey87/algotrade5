import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler, SysLogHandler
from pathlib import Path

from rich.console import Console

from freqtrade.constants import Config
from freqtrade.exceptions import OperationalException
from freqtrade.loggers.buffering_handler import FTBufferingHandler
from freqtrade.loggers.ft_rich_handler import FtRichHandler
from freqtrade.loggers.set_log_levels import set_loggers


# from freqtrade.loggers.std_err_stream_handler import FTStdErrStreamHandler


logger = logging.getLogger(__name__)
LOGFORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Initialize bufferhandler - will be used for /log endpoints
bufferHandler = FTBufferingHandler(1000)
bufferHandler.setFormatter(Formatter(LOGFORMAT))

error_console = Console(stderr=True, color_system=None)


def get_existing_handlers(handlertype):
    """
    Returns Existing handler or None (if the handler has not yet been added to the root handlers).
    """
    return next((h for h in logging.root.handlers if isinstance(h, handlertype)), None)


# REMOVED_UNUSED_CODE: def setup_logging_pre() -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Early setup for logging.
# REMOVED_UNUSED_CODE:     Uses INFO loglevel and only the Streamhandler.
# REMOVED_UNUSED_CODE:     Early messages (before proper logging setup) will therefore only be sent to additional
# REMOVED_UNUSED_CODE:     logging handlers after the real initialization, because we don't know which
# REMOVED_UNUSED_CODE:     ones the user desires beforehand.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     rh = FtRichHandler(console=error_console)
# REMOVED_UNUSED_CODE:     rh.setFormatter(Formatter("%(message)s"))
# REMOVED_UNUSED_CODE:     logging.basicConfig(
# REMOVED_UNUSED_CODE:         level=logging.INFO,
# REMOVED_UNUSED_CODE:         format=LOGFORMAT,
# REMOVED_UNUSED_CODE:         handlers=[
# REMOVED_UNUSED_CODE:             # FTStdErrStreamHandler(),
# REMOVED_UNUSED_CODE:             rh,
# REMOVED_UNUSED_CODE:             bufferHandler,
# REMOVED_UNUSED_CODE:         ],
# REMOVED_UNUSED_CODE:     )


# REMOVED_UNUSED_CODE: def setup_logging(config: Config) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Process -v/--verbose, --logfile options
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     # Log level
# REMOVED_UNUSED_CODE:     verbosity = config["verbosity"]
# REMOVED_UNUSED_CODE:     logging.root.addHandler(bufferHandler)
# REMOVED_UNUSED_CODE:     if config.get("print_colorized", True):
# REMOVED_UNUSED_CODE:         logger.info("Enabling colorized output.")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         error_console._color_system = error_console._detect_color_system()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     logfile = config.get("logfile")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if logfile:
# REMOVED_UNUSED_CODE:         s = logfile.split(":")
# REMOVED_UNUSED_CODE:         if s[0] == "syslog":
# REMOVED_UNUSED_CODE:             # Address can be either a string (socket filename) for Unix domain socket or
# REMOVED_UNUSED_CODE:             # a tuple (hostname, port) for UDP socket.
# REMOVED_UNUSED_CODE:             # Address can be omitted (i.e. simple 'syslog' used as the value of
# REMOVED_UNUSED_CODE:             # config['logfilename']), which defaults to '/dev/log', applicable for most
# REMOVED_UNUSED_CODE:             # of the systems.
# REMOVED_UNUSED_CODE:             address = (s[1], int(s[2])) if len(s) > 2 else s[1] if len(s) > 1 else "/dev/log"
# REMOVED_UNUSED_CODE:             handler_sl = get_existing_handlers(SysLogHandler)
# REMOVED_UNUSED_CODE:             if handler_sl:
# REMOVED_UNUSED_CODE:                 logging.root.removeHandler(handler_sl)
# REMOVED_UNUSED_CODE:             handler_sl = SysLogHandler(address=address)
# REMOVED_UNUSED_CODE:             # No datetime field for logging into syslog, to allow syslog
# REMOVED_UNUSED_CODE:             # to perform reduction of repeating messages if this is set in the
# REMOVED_UNUSED_CODE:             # syslog config. The messages should be equal for this.
# REMOVED_UNUSED_CODE:             handler_sl.setFormatter(Formatter("%(name)s - %(levelname)s - %(message)s"))
# REMOVED_UNUSED_CODE:             logging.root.addHandler(handler_sl)
# REMOVED_UNUSED_CODE:         elif s[0] == "journald":  # pragma: no cover
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 from cysystemd.journal import JournaldLogHandler
# REMOVED_UNUSED_CODE:             except ImportError:
# REMOVED_UNUSED_CODE:                 raise OperationalException(
# REMOVED_UNUSED_CODE:                     "You need the cysystemd python package be installed in "
# REMOVED_UNUSED_CODE:                     "order to use logging to journald."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             handler_jd = get_existing_handlers(JournaldLogHandler)
# REMOVED_UNUSED_CODE:             if handler_jd:
# REMOVED_UNUSED_CODE:                 logging.root.removeHandler(handler_jd)
# REMOVED_UNUSED_CODE:             handler_jd = JournaldLogHandler()
# REMOVED_UNUSED_CODE:             # No datetime field for logging into journald, to allow syslog
# REMOVED_UNUSED_CODE:             # to perform reduction of repeating messages if this is set in the
# REMOVED_UNUSED_CODE:             # syslog config. The messages should be equal for this.
# REMOVED_UNUSED_CODE:             handler_jd.setFormatter(Formatter("%(name)s - %(levelname)s - %(message)s"))
# REMOVED_UNUSED_CODE:             logging.root.addHandler(handler_jd)
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             handler_rf = get_existing_handlers(RotatingFileHandler)
# REMOVED_UNUSED_CODE:             if handler_rf:
# REMOVED_UNUSED_CODE:                 logging.root.removeHandler(handler_rf)
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 logfile_path = Path(logfile)
# REMOVED_UNUSED_CODE:                 logfile_path.parent.mkdir(parents=True, exist_ok=True)
# REMOVED_UNUSED_CODE:                 handler_rf = RotatingFileHandler(
# REMOVED_UNUSED_CODE:                     logfile_path,
# REMOVED_UNUSED_CODE:                     maxBytes=1024 * 1024 * 10,  # 10Mb
# REMOVED_UNUSED_CODE:                     backupCount=10,
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             except PermissionError:
# REMOVED_UNUSED_CODE:                 raise OperationalException(
# REMOVED_UNUSED_CODE:                     f'Failed to create or access log file "{logfile_path.absolute()}". '
# REMOVED_UNUSED_CODE:                     "Please make sure you have the write permission to the log file or its parent "
# REMOVED_UNUSED_CODE:                     "directories. If you're running freqtrade using docker, you see this error "
# REMOVED_UNUSED_CODE:                     "message probably because you've logged in as the root user, please switch to "
# REMOVED_UNUSED_CODE:                     "non-root user, delete and recreate the directories you need, and then try "
# REMOVED_UNUSED_CODE:                     "again."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             handler_rf.setFormatter(Formatter(LOGFORMAT))
# REMOVED_UNUSED_CODE:             logging.root.addHandler(handler_rf)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     logging.root.setLevel(logging.INFO if verbosity < 1 else logging.DEBUG)
# REMOVED_UNUSED_CODE:     set_loggers(verbosity, config.get("api_server", {}).get("verbosity", "info"))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     logger.info("Verbosity set to %s", verbosity)
