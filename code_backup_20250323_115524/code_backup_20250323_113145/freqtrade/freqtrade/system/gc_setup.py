# REMOVED_UNUSED_CODE: import gc
import logging
# REMOVED_UNUSED_CODE: import platform


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: def gc_set_threshold():
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Reduce number of GC runs to improve performance (explanation video)
# REMOVED_UNUSED_CODE:     https://www.youtube.com/watch?v=p4Sn6UcFTOU
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     if platform.python_implementation() == "CPython":
# REMOVED_UNUSED_CODE:         # allocs, g1, g2 = gc.get_threshold()
# REMOVED_UNUSED_CODE:         gc.set_threshold(50_000, 500, 1000)
# REMOVED_UNUSED_CODE:         logger.debug("Adjusting python allocations to reduce GC runs")
