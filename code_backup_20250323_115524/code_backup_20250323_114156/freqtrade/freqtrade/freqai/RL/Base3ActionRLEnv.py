import logging
from enum import Enum

# REMOVED_UNUSED_CODE: from gymnasium import spaces

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.freqai.RL.BaseEnvironment import BaseEnvironment, Positions


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class Actions(Enum):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     Neutral = 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     Buy = 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     Sell = 2


# REMOVED_UNUSED_CODE: class Base3ActionRLEnv(BaseEnvironment):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Base class for a 3 action environment
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, **kwargs):
# REMOVED_UNUSED_CODE:         super().__init__(**kwargs)
# REMOVED_UNUSED_CODE:         self.actions = Actions
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def set_action_space(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.action_space = spaces.Discrete(len(Actions))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def step(self, action: int):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Logic for a single step (incrementing one candle in time)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         by the agent
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param: action: int = the action type that the agent plans
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             to take for the current step.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :returns:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             observation = current state of environment
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             step_reward = the reward from `calculate_reward()`
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             _done = if the agent "died" or if the candles finished
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             info = dict passed back to openai gym lib
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._done = False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._current_tick += 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._current_tick == self._end_tick:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._done = True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._update_unrealized_total_profit()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         step_reward = self.calculate_reward(action)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.total_reward += step_reward
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.tensorboard_log(self.actions._member_names_[action], category="actions")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trade_type = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.is_tradesignal(action):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if action == Actions.Buy.value:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if self._position == Positions.Short:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     self._update_total_profit()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self._position = Positions.Long
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 trade_type = "long"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self._last_trade_tick = self._current_tick
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             elif action == Actions.Sell.value and self.can_short:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if self._position == Positions.Long:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     self._update_total_profit()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self._position = Positions.Short
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 trade_type = "short"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self._last_trade_tick = self._current_tick
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             elif action == Actions.Sell.value and not self.can_short:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self._update_total_profit()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self._position = Positions.Neutral
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 trade_type = "exit"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self._last_trade_tick = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 print("case not defined")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if trade_type is not None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.trade_history.append(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         "price": self.current_price(),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         "index": self._current_tick,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         "type": trade_type,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         "profit": self.get_unrealized_profit(),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     }
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._total_profit < self.max_drawdown
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             or self._total_unrealized_profit < self.max_drawdown
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._done = True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._position_history.append(self._position)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         info = dict(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             tick=self._current_tick,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             action=action,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             total_reward=self.total_reward,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             total_profit=self._total_profit,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             position=self._position.value,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trade_duration=self.get_trade_duration(),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             current_profit_pct=self.get_unrealized_profit(),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         observation = self._get_observation()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # user can play with time if they want
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         truncated = False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._update_history(info)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return observation, step_reward, self._done, truncated, info
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def is_tradesignal(self, action: int) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Determine if the signal is a trade signal
# REMOVED_UNUSED_CODE:         e.g.: agent wants a Actions.Buy while it is in a Positions.short
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return (
# REMOVED_UNUSED_CODE:             (action == Actions.Buy.value and self._position == Positions.Neutral)
# REMOVED_UNUSED_CODE:             or (action == Actions.Sell.value and self._position == Positions.Long)
# REMOVED_UNUSED_CODE:             or (
# REMOVED_UNUSED_CODE:                 action == Actions.Sell.value
# REMOVED_UNUSED_CODE:                 and self._position == Positions.Neutral
# REMOVED_UNUSED_CODE:                 and self.can_short
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             or (
# REMOVED_UNUSED_CODE:                 action == Actions.Buy.value and self._position == Positions.Short and self.can_short
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _is_valid(self, action: int) -> bool:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Determine if the signal is valid.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         e.g.: agent wants a Actions.Sell while it is in a Positions.Long
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.can_short:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return action in [Actions.Buy.value, Actions.Sell.value, Actions.Neutral.value]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if action == Actions.Sell.value and self._position != Positions.Long:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return True
