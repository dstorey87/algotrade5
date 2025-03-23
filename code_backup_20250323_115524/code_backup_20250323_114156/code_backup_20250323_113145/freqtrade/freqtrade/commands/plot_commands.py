from typing import Any

from freqtrade.enums import RunMode
from freqtrade.exceptions import ConfigurationError


def validate_plot_args(args: dict[str, Any]) -> None:
    if not args.get("datadir") and not args.get("config"):
        raise ConfigurationError(
            "You need to specify either `--datadir` or `--config` "
            "for plot-profit and plot-dataframe."
        )


# REMOVED_UNUSED_CODE: def start_plot_dataframe(args: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Entrypoint for dataframe plotting
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     # Import here to avoid errors if plot-dependencies are not installed.
# REMOVED_UNUSED_CODE:     from freqtrade.configuration import setup_utils_configuration
# REMOVED_UNUSED_CODE:     from freqtrade.plot.plotting import load_and_plot_trades
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     validate_plot_args(args)
# REMOVED_UNUSED_CODE:     config = setup_utils_configuration(args, RunMode.PLOT)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     load_and_plot_trades(config)


# REMOVED_UNUSED_CODE: def start_plot_profit(args: dict[str, Any]) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Entrypoint for plot_profit
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     # Import here to avoid errors if plot-dependencies are not installed.
# REMOVED_UNUSED_CODE:     from freqtrade.configuration import setup_utils_configuration
# REMOVED_UNUSED_CODE:     from freqtrade.plot.plotting import plot_profit
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     validate_plot_args(args)
# REMOVED_UNUSED_CODE:     config = setup_utils_configuration(args, RunMode.PLOT)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     plot_profit(config)
