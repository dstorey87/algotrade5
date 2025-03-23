from enum import Enum


class RunMode(str, Enum):
    """
    Bot running mode (backtest, hyperopt, ...)
    can be "live", "dry-run", "backtest", "edge", "hyperopt".
    """

    LIVE = "live"
    DRY_RUN = "dry_run"
    BACKTEST = "backtest"
    EDGE = "edge"
    HYPEROPT = "hyperopt"
# REMOVED_UNUSED_CODE:     UTIL_EXCHANGE = "util_exchange"
# REMOVED_UNUSED_CODE:     UTIL_NO_EXCHANGE = "util_no_exchange"
# REMOVED_UNUSED_CODE:     PLOT = "plot"
# REMOVED_UNUSED_CODE:     WEBSERVER = "webserver"
# REMOVED_UNUSED_CODE:     OTHER = "other"


# REMOVED_UNUSED_CODE: TRADE_MODES = [RunMode.LIVE, RunMode.DRY_RUN]
# REMOVED_UNUSED_CODE: OPTIMIZE_MODES = [RunMode.BACKTEST, RunMode.EDGE, RunMode.HYPEROPT]
# REMOVED_UNUSED_CODE: NON_UTIL_MODES = TRADE_MODES + OPTIMIZE_MODES
