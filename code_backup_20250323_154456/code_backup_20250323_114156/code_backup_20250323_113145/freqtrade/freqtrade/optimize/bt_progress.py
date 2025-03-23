from freqtrade.enums import BacktestState


# REMOVED_UNUSED_CODE: class BTProgress:
# REMOVED_UNUSED_CODE:     _action: BacktestState = BacktestState.STARTUP
# REMOVED_UNUSED_CODE:     _progress: float = 0
# REMOVED_UNUSED_CODE:     _max_steps: float = 0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self):
# REMOVED_UNUSED_CODE:         pass
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def init_step(self, action: BacktestState, max_steps: float):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._action = action
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._max_steps = max_steps
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._progress = 0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def set_new_value(self, new_value: float):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._progress = new_value
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def increment(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._progress += 1
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def progress(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Get progress as ratio, capped to be between 0 and 1 (to avoid small calculation errors).
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return max(
# REMOVED_UNUSED_CODE:             min(round(self._progress / self._max_steps, 5) if self._max_steps > 0 else 0, 1), 0
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def action(self):
# REMOVED_UNUSED_CODE:         return str(self._action)
