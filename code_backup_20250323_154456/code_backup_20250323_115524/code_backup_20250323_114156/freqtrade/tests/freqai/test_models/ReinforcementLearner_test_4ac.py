import logging

import numpy as np

from freqtrade.freqai.prediction_models.ReinforcementLearner import ReinforcementLearner
from freqtrade.freqai.RL.Base4ActionRLEnv import Actions, Base4ActionRLEnv, Positions


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


class ReinforcementLearner_test_4ac(ReinforcementLearner):
    """
    User created Reinforcement Learning Model prediction model.
    """

# REMOVED_UNUSED_CODE:     class MyRLEnv(Base4ActionRLEnv):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         User can override any function in BaseRLEnv and gym.Env. Here the user
# REMOVED_UNUSED_CODE:         sets a custom reward based on profit and trade duration.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         Warning!
# REMOVED_UNUSED_CODE:         This is function is a showcase of functionality designed to show as many possible
# REMOVED_UNUSED_CODE:         environment control features as possible. It is also designed to run quickly
# REMOVED_UNUSED_CODE:         on small computers. This is a benchmark, it is *not* for live production.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         def calculate_reward(self, action: int) -> float:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # first, penalize if the action is not valid
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if not self._is_valid(action):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return -2
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             pnl = self.get_unrealized_profit()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             rew = np.sign(pnl) * (pnl + 1)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             factor = 100.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # reward agent for entering trades
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 action in (Actions.Long_enter.value, Actions.Short_enter.value)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 and self._position == Positions.Neutral
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return 25
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # discourage agent from not entering trades
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if action == Actions.Neutral.value and self._position == Positions.Neutral:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return -1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             max_trade_duration = self.rl_config.get("max_trade_duration_candles", 300)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trade_duration = self._current_tick - self._last_trade_tick  # type: ignore
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if trade_duration <= max_trade_duration:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 factor *= 1.5
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             elif trade_duration > max_trade_duration:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 factor *= 0.5
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # discourage sitting in position
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self._position in (Positions.Short, Positions.Long)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 and action == Actions.Neutral.value
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return -1 * trade_duration / max_trade_duration
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # close long
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if action == Actions.Exit.value and self._position == Positions.Long:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if pnl > self.profit_aim * self.rr:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     factor *= self.rl_config["model_reward_parameters"].get("win_reward_factor", 2)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return float(rew * factor)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # close short
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if action == Actions.Exit.value and self._position == Positions.Short:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if pnl > self.profit_aim * self.rr:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     factor *= self.rl_config["model_reward_parameters"].get("win_reward_factor", 2)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return float(rew * factor)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return 0.0
