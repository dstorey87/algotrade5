from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

from freqtrade.loggers import error_console
from freqtrade.util.rich_progress import CustomProgress


# REMOVED_UNUSED_CODE: def retrieve_progress_tracker(pt: CustomProgress | None) -> CustomProgress:
# REMOVED_UNUSED_CODE:     if pt is None:
# REMOVED_UNUSED_CODE:         return get_progress_tracker()
# REMOVED_UNUSED_CODE:     return pt


def get_progress_tracker(**kwargs) -> CustomProgress:
    """
    Get progress Bar with custom columns.
    """
    return CustomProgress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None),
        MofNCompleteColumn(),
        TaskProgressColumn(),
        "•",
        TimeElapsedColumn(),
        "•",
        TimeRemainingColumn(),
        expand=True,
        console=error_console,
        **kwargs,
    )
