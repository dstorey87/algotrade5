import logging
# REMOVED_UNUSED_CODE: import random
# REMOVED_UNUSED_CODE: from abc import abstractmethod
from enum import Enum

# REMOVED_UNUSED_CODE: import gymnasium as gym
# REMOVED_UNUSED_CODE: import numpy as np
# REMOVED_UNUSED_CODE: import pandas as pd
# REMOVED_UNUSED_CODE: from gymnasium import spaces
# REMOVED_UNUSED_CODE: from gymnasium.utils import seeding
# REMOVED_UNUSED_CODE: from pandas import DataFrame

# REMOVED_UNUSED_CODE: from freqtrade.exceptions import OperationalException


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class BaseActions(Enum):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Default action space, mostly used for type handling.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     Neutral = 0
# REMOVED_UNUSED_CODE:     Long_enter = 1
# REMOVED_UNUSED_CODE:     Long_exit = 2
# REMOVED_UNUSED_CODE:     Short_enter = 3
# REMOVED_UNUSED_CODE:     Short_exit = 4


# REMOVED_UNUSED_CODE: class Positions(Enum):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     Short = 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     Long = 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     Neutral = 0.5

# REMOVED_UNUSED_CODE:     def opposite(self):
# REMOVED_UNUSED_CODE:         return Positions.Short if self == Positions.Long else Positions.Long


# REMOVED_UNUSED_CODE: class BaseEnvironment(gym.Env):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Base class for environments. This class is agnostic to action count.
# REMOVED_UNUSED_CODE:     Inherited classes customize this to include varying action counts/types,
# REMOVED_UNUSED_CODE:     See RL/Base5ActionRLEnv.py and RL/Base4ActionRLEnv.py
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         df: DataFrame = DataFrame(),
# REMOVED_UNUSED_CODE:         prices: DataFrame = DataFrame(),
# REMOVED_UNUSED_CODE:         reward_kwargs: dict = {},
# REMOVED_UNUSED_CODE:         window_size=10,
# REMOVED_UNUSED_CODE:         starting_point=True,
# REMOVED_UNUSED_CODE:         id: str = "baseenv-1",  # noqa: A002
# REMOVED_UNUSED_CODE:         seed: int = 1,
# REMOVED_UNUSED_CODE:         config: dict = {},
# REMOVED_UNUSED_CODE:         live: bool = False,
# REMOVED_UNUSED_CODE:         fee: float = 0.0015,
# REMOVED_UNUSED_CODE:         can_short: bool = False,
# REMOVED_UNUSED_CODE:         pair: str = "",
# REMOVED_UNUSED_CODE:         df_raw: DataFrame = DataFrame(),
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Initializes the training/eval environment.
# REMOVED_UNUSED_CODE:         :param df: dataframe of features
# REMOVED_UNUSED_CODE:         :param prices: dataframe of prices to be used in the training environment
# REMOVED_UNUSED_CODE:         :param window_size: size of window (temporal) to pass to the agent
# REMOVED_UNUSED_CODE:         :param reward_kwargs: extra config settings assigned by user in `rl_config`
# REMOVED_UNUSED_CODE:         :param starting_point: start at edge of window or not
# REMOVED_UNUSED_CODE:         :param id: string id of the environment (used in backend for multiprocessed env)
# REMOVED_UNUSED_CODE:         :param seed: Sets the seed of the environment higher in the gym.Env object
# REMOVED_UNUSED_CODE:         :param config: Typical user configuration file
# REMOVED_UNUSED_CODE:         :param live: Whether or not this environment is active in dry/live/backtesting
# REMOVED_UNUSED_CODE:         :param fee: The fee to use for environmental interactions.
# REMOVED_UNUSED_CODE:         :param can_short: Whether or not the environment can short
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self.config: dict = config
# REMOVED_UNUSED_CODE:         self.rl_config: dict = config["freqai"]["rl_config"]
# REMOVED_UNUSED_CODE:         self.add_state_info: bool = self.rl_config.get("add_state_info", False)
# REMOVED_UNUSED_CODE:         self.id: str = id
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.max_drawdown: float = 1 - self.rl_config.get("max_training_drawdown_pct", 0.8)
# REMOVED_UNUSED_CODE:         self.compound_trades: bool = config["stake_amount"] == "unlimited"
# REMOVED_UNUSED_CODE:         self.pair: str = pair
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.raw_features: DataFrame = df_raw
# REMOVED_UNUSED_CODE:         if self.config.get("fee", None) is not None:
# REMOVED_UNUSED_CODE:             self.fee = self.config["fee"]
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             self.fee = fee
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # set here to default 5Ac, but all children envs can override this
# REMOVED_UNUSED_CODE:         self.actions: type[Enum] = BaseActions
# REMOVED_UNUSED_CODE:         self.tensorboard_metrics: dict = {}
# REMOVED_UNUSED_CODE:         self.can_short: bool = can_short
# REMOVED_UNUSED_CODE:         self.live: bool = live
# REMOVED_UNUSED_CODE:         if not self.live and self.add_state_info:
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 "`add_state_info` is not available in backtesting. Change "
# REMOVED_UNUSED_CODE:                 "parameter to false in your rl_config. See `add_state_info` "
# REMOVED_UNUSED_CODE:                 "docs for more info."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         self.seed(seed)
# REMOVED_UNUSED_CODE:         self.reset_env(df, prices, window_size, reward_kwargs, starting_point)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def reset_env(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         df: DataFrame,
# REMOVED_UNUSED_CODE:         prices: DataFrame,
# REMOVED_UNUSED_CODE:         window_size: int,
# REMOVED_UNUSED_CODE:         reward_kwargs: dict,
# REMOVED_UNUSED_CODE:         starting_point=True,
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Resets the environment when the agent fails (in our case, if the drawdown
# REMOVED_UNUSED_CODE:         exceeds the user set max_training_drawdown_pct)
# REMOVED_UNUSED_CODE:         :param df: dataframe of features
# REMOVED_UNUSED_CODE:         :param prices: dataframe of prices to be used in the training environment
# REMOVED_UNUSED_CODE:         :param window_size: size of window (temporal) to pass to the agent
# REMOVED_UNUSED_CODE:         :param reward_kwargs: extra config settings assigned by user in `rl_config`
# REMOVED_UNUSED_CODE:         :param starting_point: start at edge of window or not
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self.signal_features: DataFrame = df
# REMOVED_UNUSED_CODE:         self.prices: DataFrame = prices
# REMOVED_UNUSED_CODE:         self.window_size: int = window_size
# REMOVED_UNUSED_CODE:         self.starting_point: bool = starting_point
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.rr: float = reward_kwargs["rr"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.profit_aim: float = reward_kwargs["profit_aim"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # # spaces
# REMOVED_UNUSED_CODE:         if self.add_state_info:
# REMOVED_UNUSED_CODE:             self.total_features = self.signal_features.shape[1] + 3
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             self.total_features = self.signal_features.shape[1]
# REMOVED_UNUSED_CODE:         self.shape = (window_size, self.total_features)
# REMOVED_UNUSED_CODE:         self.set_action_space()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.observation_space = spaces.Box(low=-1, high=1, shape=self.shape, dtype=np.float32)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # episode
# REMOVED_UNUSED_CODE:         self._start_tick: int = self.window_size
# REMOVED_UNUSED_CODE:         self._end_tick: int = len(self.prices) - 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._done: bool = False
# REMOVED_UNUSED_CODE:         self._current_tick: int = self._start_tick
# REMOVED_UNUSED_CODE:         self._last_trade_tick: int | None = None
# REMOVED_UNUSED_CODE:         self._position = Positions.Neutral
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._position_history: list = [None]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.total_reward: float = 0
# REMOVED_UNUSED_CODE:         self._total_profit: float = 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._total_unrealized_profit: float = 1
# REMOVED_UNUSED_CODE:         self.history: dict = {}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.trade_history: list = []
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_attr(self, attr: str):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Returns the attribute of the environment
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param attr: attribute to return
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: attribute
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return getattr(self, attr)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @abstractmethod
# REMOVED_UNUSED_CODE:     def set_action_space(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Unique to the environment action count. Must be inherited.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def action_masks(self) -> list[bool]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return [self._is_valid(action.value) for action in self.actions]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def seed(self, seed: int = 1):
# REMOVED_UNUSED_CODE:         self.np_random, seed = seeding.np_random(seed)
# REMOVED_UNUSED_CODE:         return [seed]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def tensorboard_log(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         metric: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         value: int | float | None = None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         inc: bool | None = None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         category: str = "custom",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Function builds the tensorboard_metrics dictionary
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         to be parsed by the TensorboardCallback. This
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         function is designed for tracking incremented objects,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         events, actions inside the training environment.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         For example, a user can call this to track the
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         frequency of occurrence of an `is_valid` call in
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         their `calculate_reward()`:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         def calculate_reward(self, action: int) -> float:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if not self._is_valid(action):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.tensorboard_log("invalid")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return -2
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param metric: metric to be tracked and incremented
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param value: `metric` value
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param inc: (deprecated) sets whether the `value` is incremented or not
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param category: `metric` category
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         increment = True if value is None else False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         value = 1 if increment else value
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if category not in self.tensorboard_metrics:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.tensorboard_metrics[category] = {}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not increment or metric not in self.tensorboard_metrics[category]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.tensorboard_metrics[category][metric] = value
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.tensorboard_metrics[category][metric] += value
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def reset_tensorboard_log(self):
# REMOVED_UNUSED_CODE:         self.tensorboard_metrics = {}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def reset(self, seed=None):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Reset is called at the beginning of every episode
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.reset_tensorboard_log()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._done = False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.starting_point is True:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if self.rl_config.get("randomize_starting_position", False):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 length_of_data = int(self._end_tick / 4)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 start_tick = random.randint(self.window_size + 1, length_of_data)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self._start_tick = start_tick
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._position_history = (self._start_tick * [None]) + [self._position]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._position_history = (self.window_size * [None]) + [self._position]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._current_tick = self._start_tick
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._last_trade_tick = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._position = Positions.Neutral
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.total_reward = 0.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._total_profit = 1.0  # unit
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.history = {}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.trade_history = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.portfolio_log_returns = np.zeros(len(self.prices))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._profits = [(self._start_tick, 1)]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.close_trade_profit = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._total_unrealized_profit = 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._get_observation(), self.history
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @abstractmethod
# REMOVED_UNUSED_CODE:     def step(self, action: int):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Step depends on action types, this must be inherited.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _get_observation(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         This may or may not be independent of action types, user can inherit
# REMOVED_UNUSED_CODE:         this in their custom "MyRLEnv"
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         features_window = self.signal_features[
# REMOVED_UNUSED_CODE:             (self._current_tick - self.window_size) : self._current_tick
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE:         if self.add_state_info:
# REMOVED_UNUSED_CODE:             features_and_state = DataFrame(
# REMOVED_UNUSED_CODE:                 np.zeros((len(features_window), 3)),
# REMOVED_UNUSED_CODE:                 columns=["current_profit_pct", "position", "trade_duration"],
# REMOVED_UNUSED_CODE:                 index=features_window.index,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             features_and_state["current_profit_pct"] = self.get_unrealized_profit()
# REMOVED_UNUSED_CODE:             features_and_state["position"] = self._position.value
# REMOVED_UNUSED_CODE:             features_and_state["trade_duration"] = self.get_trade_duration()
# REMOVED_UNUSED_CODE:             features_and_state = pd.concat([features_window, features_and_state], axis=1)
# REMOVED_UNUSED_CODE:             return features_and_state
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             return features_window
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def get_trade_duration(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Get the trade duration if the agent is in a trade
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if self._last_trade_tick is None:
# REMOVED_UNUSED_CODE:             return 0
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             return self._current_tick - self._last_trade_tick
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def get_unrealized_profit(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Get the unrealized profit if the agent is in a trade
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if self._last_trade_tick is None:
# REMOVED_UNUSED_CODE:             return 0.0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self._position == Positions.Neutral:
# REMOVED_UNUSED_CODE:             return 0.0
# REMOVED_UNUSED_CODE:         elif self._position == Positions.Short:
# REMOVED_UNUSED_CODE:             current_price = self.add_entry_fee(self.prices.iloc[self._current_tick].open)
# REMOVED_UNUSED_CODE:             last_trade_price = self.add_exit_fee(self.prices.iloc[self._last_trade_tick].open)
# REMOVED_UNUSED_CODE:             return (last_trade_price - current_price) / last_trade_price
# REMOVED_UNUSED_CODE:         elif self._position == Positions.Long:
# REMOVED_UNUSED_CODE:             current_price = self.add_exit_fee(self.prices.iloc[self._current_tick].open)
# REMOVED_UNUSED_CODE:             last_trade_price = self.add_entry_fee(self.prices.iloc[self._last_trade_tick].open)
# REMOVED_UNUSED_CODE:             return (current_price - last_trade_price) / last_trade_price
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             return 0.0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @abstractmethod
# REMOVED_UNUSED_CODE:     def is_tradesignal(self, action: int) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Determine if the signal is a trade signal. This is
# REMOVED_UNUSED_CODE:         unique to the actions in the environment, and therefore must be
# REMOVED_UNUSED_CODE:         inherited.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _is_valid(self, action: int) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Determine if the signal is valid.This is
# REMOVED_UNUSED_CODE:         unique to the actions in the environment, and therefore must be
# REMOVED_UNUSED_CODE:         inherited.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def add_entry_fee(self, price):
# REMOVED_UNUSED_CODE:         return price * (1 + self.fee)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def add_exit_fee(self, price):
# REMOVED_UNUSED_CODE:         return price / (1 + self.fee)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _update_history(self, info):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not self.history:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.history = {key: [] for key in info.keys()}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for key, value in info.items():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.history[key].append(value)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @abstractmethod
# REMOVED_UNUSED_CODE:     def calculate_reward(self, action: int) -> float:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         An example reward function. This is the one function that users will likely
# REMOVED_UNUSED_CODE:         wish to inject their own creativity into.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         Warning!
# REMOVED_UNUSED_CODE:         This is function is a showcase of functionality designed to show as many possible
# REMOVED_UNUSED_CODE:         environment control features as possible. It is also designed to run quickly
# REMOVED_UNUSED_CODE:         on small computers. This is a benchmark, it is *not* for live production.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         :param action: int = The action made by the agent for the current candle.
# REMOVED_UNUSED_CODE:         :return:
# REMOVED_UNUSED_CODE:         float = the reward to give to the agent for current step (used for optimization
# REMOVED_UNUSED_CODE:             of weights in NN)
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _update_unrealized_total_profit(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Update the unrealized total profit in case of episode end.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._position in (Positions.Long, Positions.Short):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             pnl = self.get_unrealized_profit()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if self.compound_trades:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # assumes unit stake and compounding
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 unrl_profit = self._total_profit * (1 + pnl)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # assumes unit stake and no compounding
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 unrl_profit = self._total_profit + pnl
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._total_unrealized_profit = unrl_profit
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _update_total_profit(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pnl = self.get_unrealized_profit()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.compound_trades:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # assumes unit stake and compounding
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._total_profit = self._total_profit * (1 + pnl)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # assumes unit stake and no compounding
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._total_profit += pnl
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def current_price(self) -> float:
# REMOVED_UNUSED_CODE:         return self.prices.iloc[self._current_tick].open
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_actions(self) -> type[Enum]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Used by SubprocVecEnv to get actions from
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         initialized env for tensorboard callback
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self.actions

    # Keeping around in case we want to start building more complex environment
    # templates in the future.
    # def most_recent_return(self):
    #     """
    #     Calculate the tick to tick return if in a trade.
    #     Return is generated from rising prices in Long
    #     and falling prices in Short positions.
    #     The actions Sell/Buy or Hold during a Long position trigger the sell/buy-fee.
    #     """
    #     # Long positions
    #     if self._position == Positions.Long:
    #         current_price = self.prices.iloc[self._current_tick].open
    #         previous_price = self.prices.iloc[self._current_tick - 1].open

    #         if (self._position_history[self._current_tick - 1] == Positions.Short
    #                 or self._position_history[self._current_tick - 1] == Positions.Neutral):
    #             previous_price = self.add_entry_fee(previous_price)

    #         return np.log(current_price) - np.log(previous_price)

    #     # Short positions
    #     if self._position == Positions.Short:
    #         current_price = self.prices.iloc[self._current_tick].open
    #         previous_price = self.prices.iloc[self._current_tick - 1].open
    #         if (self._position_history[self._current_tick - 1] == Positions.Long
    #                 or self._position_history[self._current_tick - 1] == Positions.Neutral):
    #             previous_price = self.add_exit_fee(previous_price)

    #         return np.log(previous_price) - np.log(current_price)

    #     return 0

    # def update_portfolio_log_returns(self, action):
    #     self.portfolio_log_returns[self._current_tick] = self.most_recent_return(action)
