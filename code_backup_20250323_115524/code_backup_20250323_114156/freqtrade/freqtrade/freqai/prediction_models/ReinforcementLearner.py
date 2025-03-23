import logging
# REMOVED_UNUSED_CODE: from pathlib import Path
# REMOVED_UNUSED_CODE: from typing import Any

# REMOVED_UNUSED_CODE: import torch as th
# REMOVED_UNUSED_CODE: from stable_baselines3.common.callbacks import ProgressBarCallback

# REMOVED_UNUSED_CODE: from freqtrade.freqai.data_kitchen import FreqaiDataKitchen
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.freqai.RL.Base5ActionRLEnv import Actions, Base5ActionRLEnv, Positions
# REMOVED_UNUSED_CODE: from freqtrade.freqai.RL.BaseEnvironment import BaseEnvironment
# REMOVED_UNUSED_CODE: from freqtrade.freqai.RL.BaseReinforcementLearningModel import BaseReinforcementLearningModel


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class ReinforcementLearner(BaseReinforcementLearningModel):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Reinforcement Learning Model prediction model.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Users can inherit from this class to make their own RL model with custom
# REMOVED_UNUSED_CODE:     environment/training controls. Define the file as follows:
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     ```
# REMOVED_UNUSED_CODE:     from freqtrade.freqai.prediction_models.ReinforcementLearner import ReinforcementLearner
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     class MyCoolRLModel(ReinforcementLearner):
# REMOVED_UNUSED_CODE:     ```
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Save the file to `user_data/freqaimodels`, then run it with:
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     freqtrade trade --freqaimodel MyCoolRLModel --config config.json --strategy SomeCoolStrat
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Here the users can override any of the functions
# REMOVED_UNUSED_CODE:     available in the `IFreqaiModel` inheritance tree. Most importantly for RL, this
# REMOVED_UNUSED_CODE:     is where the user overrides `MyRLEnv` (see below), to define custom
# REMOVED_UNUSED_CODE:     `calculate_reward()` function, or to override any other parts of the environment.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     This class also allows users to override any other part of the IFreqaiModel tree.
# REMOVED_UNUSED_CODE:     For example, the user can override `def fit()` or `def train()` or `def predict()`
# REMOVED_UNUSED_CODE:     to take fine-tuned control over these processes.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Another common override may be `def data_cleaning_predict()` where the user can
# REMOVED_UNUSED_CODE:     take fine-tuned control over the data handling pipeline.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def fit(self, data_dictionary: dict[str, Any], dk: FreqaiDataKitchen, **kwargs):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         User customizable fit method
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param data_dictionary: dict = common data dictionary containing all train/test
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             features/labels/weights.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param dk: FreqaiDatakitchen = data kitchen for current pair.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         model Any = trained model to be used for inference in dry/live/backtesting
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         train_df = data_dictionary["train_features"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         total_timesteps = self.freqai_info["rl_config"]["train_cycles"] * len(train_df)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         policy_kwargs = dict(activation_fn=th.nn.ReLU, net_arch=self.net_arch)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.activate_tensorboard:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             tb_path = Path(dk.full_path / "tensorboard" / dk.pair.split("/")[0])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             tb_path = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if dk.pair not in self.dd.model_dictionary or not self.continual_learning:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             model = self.MODELCLASS(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.policy_type,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.train_env,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 policy_kwargs=policy_kwargs,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 tensorboard_log=tb_path,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 **self.freqai_info.get("model_training_parameters", {}),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             logger.info(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "Continual training activated - starting training from previously trained agent."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             model = self.dd.model_dictionary[dk.pair]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             model.set_env(self.train_env)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         callbacks: list[Any] = [self.eval_callback, self.tensorboard_callback]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         progressbar_callback: ProgressBarCallback | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.rl_config.get("progress_bar", False):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             progressbar_callback = ProgressBarCallback()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             callbacks.insert(0, progressbar_callback)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             model.learn(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 total_timesteps=int(total_timesteps),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 callback=callbacks,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         finally:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if progressbar_callback:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 progressbar_callback.on_training_end()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if Path(dk.data_path / "best_model.zip").is_file():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             logger.info("Callback found a best model.")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             best_model = self.MODELCLASS.load(dk.data_path / "best_model")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return best_model
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.info("Couldn't find best model, using final model instead.")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return model
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     MyRLEnv: type[BaseEnvironment]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     class MyRLEnv(Base5ActionRLEnv):  # type: ignore[no-redef]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         User can override any function in BaseRLEnv and gym.Env. Here the user
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         sets a custom reward based on profit and trade duration.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         def calculate_reward(self, action: int) -> float:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             An example reward function. This is the one function that users will likely
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             wish to inject their own creativity into.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         Warning!
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             This is function is a showcase of functionality designed to show as many possible
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             environment control features as possible. It is also designed to run quickly
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             on small computers. This is a benchmark, it is *not* for live production.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             :param action: int = The action made by the agent for the current candle.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             :return:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             float = the reward to give to the agent for current step (used for optimization
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 of weights in NN)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # first, penalize if the action is not valid
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if not self._is_valid(action):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.tensorboard_log("invalid", category="actions")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return -2
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             pnl = self.get_unrealized_profit()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             factor = 100.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # reward agent for entering trades
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if action == Actions.Long_enter.value and self._position == Positions.Neutral:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return 25
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if action == Actions.Short_enter.value and self._position == Positions.Neutral:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return 25
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # discourage agent from not entering trades
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if action == Actions.Neutral.value and self._position == Positions.Neutral:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return -1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             max_trade_duration = self.rl_config.get("max_trade_duration_candles", 300)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trade_duration = self._current_tick - self._last_trade_tick  # type: ignore
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if trade_duration <= max_trade_duration:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 factor *= 1.5
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             elif trade_duration > max_trade_duration:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 factor *= 0.5
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # discourage sitting in position
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self._position in (Positions.Short, Positions.Long)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 and action == Actions.Neutral.value
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return -1 * trade_duration / max_trade_duration
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # close long
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if action == Actions.Long_exit.value and self._position == Positions.Long:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if pnl > self.profit_aim * self.rr:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     factor *= self.rl_config["model_reward_parameters"].get("win_reward_factor", 2)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return float(pnl * factor)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # close short
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if action == Actions.Short_exit.value and self._position == Positions.Short:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if pnl > self.profit_aim * self.rr:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     factor *= self.rl_config["model_reward_parameters"].get("win_reward_factor", 2)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return float(pnl * factor)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return 0.0
