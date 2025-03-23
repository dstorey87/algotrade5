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


# REMOVED_UNUSED_CODE: def get_progress_tracker(**kwargs) -> CustomProgress:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Get progress Bar with custom columns.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     return CustomProgress(
# REMOVED_UNUSED_CODE:         TextColumn("[progress.description]{task.description}"),
# REMOVED_UNUSED_CODE:         BarColumn(bar_width=None),
# REMOVED_UNUSED_CODE:         MofNCompleteColumn(),
# REMOVED_UNUSED_CODE:         TaskProgressColumn(),
# REMOVED_UNUSED_CODE:         "•",
# REMOVED_UNUSED_CODE:         TimeElapsedColumn(),
# REMOVED_UNUSED_CODE:         "•",
# REMOVED_UNUSED_CODE:         TimeRemainingColumn(),
# REMOVED_UNUSED_CODE:         expand=True,
# REMOVED_UNUSED_CODE:         console=error_console,
# REMOVED_UNUSED_CODE:         **kwargs,
# REMOVED_UNUSED_CODE:     )
