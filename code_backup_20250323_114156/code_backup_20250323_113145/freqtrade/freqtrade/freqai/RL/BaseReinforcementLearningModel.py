# REMOVED_UNUSED_CODE: import copy
# REMOVED_UNUSED_CODE: import importlib
import logging
# REMOVED_UNUSED_CODE: from abc import abstractmethod
# REMOVED_UNUSED_CODE: from collections.abc import Callable
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from datetime import datetime, timezone
# REMOVED_UNUSED_CODE: from pathlib import Path
# REMOVED_UNUSED_CODE: from typing import Any

# REMOVED_UNUSED_CODE: import gymnasium as gym
# REMOVED_UNUSED_CODE: import numpy as np
# REMOVED_UNUSED_CODE: import numpy.typing as npt
# REMOVED_UNUSED_CODE: import pandas as pd
# REMOVED_UNUSED_CODE: import torch as th
import torch.multiprocessing
# REMOVED_UNUSED_CODE: from pandas import DataFrame
# REMOVED_UNUSED_CODE: from sb3_contrib.common.maskable.callbacks import MaskableEvalCallback
# REMOVED_UNUSED_CODE: from sb3_contrib.common.maskable.utils import is_masking_supported
# REMOVED_UNUSED_CODE: from stable_baselines3.common.monitor import Monitor
# REMOVED_UNUSED_CODE: from stable_baselines3.common.utils import set_random_seed
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from stable_baselines3.common.vec_env import SubprocVecEnv, VecMonitor

# REMOVED_UNUSED_CODE: from freqtrade.exceptions import OperationalException
# REMOVED_UNUSED_CODE: from freqtrade.freqai.data_kitchen import FreqaiDataKitchen
# REMOVED_UNUSED_CODE: from freqtrade.freqai.freqai_interface import IFreqaiModel
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.freqai.RL.Base5ActionRLEnv import Actions, Base5ActionRLEnv
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.freqai.RL.BaseEnvironment import BaseActions, BaseEnvironment, Positions
# REMOVED_UNUSED_CODE: from freqtrade.freqai.tensorboard.TensorboardCallback import TensorboardCallback
# REMOVED_UNUSED_CODE: from freqtrade.persistence import Trade


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)

torch.multiprocessing.set_sharing_strategy("file_system")

# REMOVED_UNUSED_CODE: SB3_MODELS = ["PPO", "A2C", "DQN"]
# REMOVED_UNUSED_CODE: SB3_CONTRIB_MODELS = ["TRPO", "ARS", "RecurrentPPO", "MaskablePPO", "QRDQN"]


# REMOVED_UNUSED_CODE: class BaseReinforcementLearningModel(IFreqaiModel):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     User created Reinforcement Learning Model prediction class
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, **kwargs) -> None:
# REMOVED_UNUSED_CODE:         super().__init__(config=kwargs["config"])
# REMOVED_UNUSED_CODE:         self.max_threads = min(
# REMOVED_UNUSED_CODE:             self.freqai_info["rl_config"].get("cpu_count", 1),
# REMOVED_UNUSED_CODE:             max(int(self.max_system_threads / 2), 1),
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         th.set_num_threads(self.max_threads)
# REMOVED_UNUSED_CODE:         self.reward_params = self.freqai_info["rl_config"]["model_reward_parameters"]
# REMOVED_UNUSED_CODE:         self.train_env: VecMonitor | SubprocVecEnv | gym.Env = gym.Env()
# REMOVED_UNUSED_CODE:         self.eval_env: VecMonitor | SubprocVecEnv | gym.Env = gym.Env()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.eval_callback: MaskableEvalCallback | None = None
# REMOVED_UNUSED_CODE:         self.model_type = self.freqai_info["rl_config"]["model_type"]
# REMOVED_UNUSED_CODE:         self.rl_config = self.freqai_info["rl_config"]
# REMOVED_UNUSED_CODE:         self.df_raw: DataFrame = DataFrame()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.continual_learning = self.freqai_info.get("continual_learning", False)
# REMOVED_UNUSED_CODE:         if self.model_type in SB3_MODELS:
# REMOVED_UNUSED_CODE:             import_str = "stable_baselines3"
# REMOVED_UNUSED_CODE:         elif self.model_type in SB3_CONTRIB_MODELS:
# REMOVED_UNUSED_CODE:             import_str = "sb3_contrib"
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 f"{self.model_type} not available in stable_baselines3 or "
# REMOVED_UNUSED_CODE:                 f"sb3_contrib. please choose one of {SB3_MODELS} or "
# REMOVED_UNUSED_CODE:                 f"{SB3_CONTRIB_MODELS}"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         mod = importlib.import_module(import_str, self.model_type)
# REMOVED_UNUSED_CODE:         self.MODELCLASS = getattr(mod, self.model_type)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.policy_type = self.freqai_info["rl_config"]["policy_type"]
# REMOVED_UNUSED_CODE:         self.unset_outlier_removal()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.net_arch = self.rl_config.get("net_arch", [128, 128])
# REMOVED_UNUSED_CODE:         self.dd.model_type = import_str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.tensorboard_callback: TensorboardCallback = TensorboardCallback(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             verbose=1, actions=BaseActions
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def unset_outlier_removal(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         If user has activated any function that may remove training points, this
# REMOVED_UNUSED_CODE:         function will set them to false and warn them
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if self.ft_params.get("use_SVM_to_remove_outliers", False):
# REMOVED_UNUSED_CODE:             self.ft_params.update({"use_SVM_to_remove_outliers": False})
# REMOVED_UNUSED_CODE:             logger.warning("User tried to use SVM with RL. Deactivating SVM.")
# REMOVED_UNUSED_CODE:         if self.ft_params.get("use_DBSCAN_to_remove_outliers", False):
# REMOVED_UNUSED_CODE:             self.ft_params.update({"use_DBSCAN_to_remove_outliers": False})
# REMOVED_UNUSED_CODE:             logger.warning("User tried to use DBSCAN with RL. Deactivating DBSCAN.")
# REMOVED_UNUSED_CODE:         if self.ft_params.get("DI_threshold", False):
# REMOVED_UNUSED_CODE:             self.ft_params.update({"DI_threshold": False})
# REMOVED_UNUSED_CODE:             logger.warning("User tried to use DI_threshold with RL. Deactivating DI_threshold.")
# REMOVED_UNUSED_CODE:         if self.freqai_info["data_split_parameters"].get("shuffle", False):
# REMOVED_UNUSED_CODE:             self.freqai_info["data_split_parameters"].update({"shuffle": False})
# REMOVED_UNUSED_CODE:             logger.warning("User tried to shuffle training data. Setting shuffle to False")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def train(self, unfiltered_df: DataFrame, pair: str, dk: FreqaiDataKitchen, **kwargs) -> Any:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Filter the training data and train a model to it. Train makes heavy use of the datakitchen
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for storing, saving, loading, and analyzing the data.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param unfiltered_df: Full dataframe for the current training period
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param metadata: pair metadata from strategy.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :returns:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :model: Trained model which can be used to inference (self.predict)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.info(f"--------------------Starting training {pair} --------------------")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         features_filtered, labels_filtered = dk.filter_features(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             unfiltered_df,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.training_features_list,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.label_list,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             training_filter=True,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dd: dict[str, Any] = dk.make_train_test_datasets(features_filtered, labels_filtered)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.df_raw = copy.deepcopy(dd["train_features"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk.fit_labels()  # FIXME useless for now, but just satiating append methods
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # normalize all data based on train_dataset only
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         prices_train, prices_test = self.build_ohlc_price_dataframes(dk.data_dictionary, pair, dk)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk.feature_pipeline = self.define_data_pipeline(threads=dk.thread_count)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         (dd["train_features"], dd["train_labels"], dd["train_weights"]) = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.feature_pipeline.fit_transform(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 dd["train_features"], dd["train_labels"], dd["train_weights"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.freqai_info.get("data_split_parameters", {}).get("test_size", 0.1) != 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             (dd["test_features"], dd["test_labels"], dd["test_weights"]) = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 dk.feature_pipeline.transform(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     dd["test_features"], dd["test_labels"], dd["test_weights"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.info(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"Training model on {len(dk.data_dictionary['train_features'].columns)}"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f" features and {len(dd['train_features'])} data points"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.set_train_and_eval_environments(dd, prices_train, prices_test, dk)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         model = self.fit(dd, dk)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.info(f"--------------------done training {pair}--------------------")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return model
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def set_train_and_eval_environments(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         data_dictionary: dict[str, DataFrame],
# REMOVED_UNUSED_CODE:         prices_train: DataFrame,
# REMOVED_UNUSED_CODE:         prices_test: DataFrame,
# REMOVED_UNUSED_CODE:         dk: FreqaiDataKitchen,
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         User can override this if they are using a custom MyRLEnv
# REMOVED_UNUSED_CODE:         :param data_dictionary: dict = common data dictionary containing train and test
# REMOVED_UNUSED_CODE:             features/labels/weights.
# REMOVED_UNUSED_CODE:         :param prices_train/test: DataFrame = dataframe comprised of the prices to be used in the
# REMOVED_UNUSED_CODE:             environment during training or testing
# REMOVED_UNUSED_CODE:         :param dk: FreqaiDataKitchen = the datakitchen for the current pair
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         train_df = data_dictionary["train_features"]
# REMOVED_UNUSED_CODE:         test_df = data_dictionary["test_features"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         env_info = self.pack_env_dict(dk.pair)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.train_env = self.MyRLEnv(df=train_df, prices=prices_train, **env_info)
# REMOVED_UNUSED_CODE:         self.eval_env = Monitor(self.MyRLEnv(df=test_df, prices=prices_test, **env_info))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.eval_callback = MaskableEvalCallback(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.eval_env,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             deterministic=True,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             render=False,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             eval_freq=len(train_df),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             best_model_save_path=str(dk.data_path),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             use_masking=(self.model_type == "MaskablePPO" and is_masking_supported(self.eval_env)),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         actions = self.train_env.get_actions()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.tensorboard_callback = TensorboardCallback(verbose=1, actions=actions)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def pack_env_dict(self, pair: str) -> dict[str, Any]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Create dictionary of environment arguments
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         env_info = {
# REMOVED_UNUSED_CODE:             "window_size": self.CONV_WIDTH,
# REMOVED_UNUSED_CODE:             "reward_kwargs": self.reward_params,
# REMOVED_UNUSED_CODE:             "config": self.config,
# REMOVED_UNUSED_CODE:             "live": self.live,
# REMOVED_UNUSED_CODE:             "can_short": self.can_short,
# REMOVED_UNUSED_CODE:             "pair": pair,
# REMOVED_UNUSED_CODE:             "df_raw": self.df_raw,
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE:         if self.data_provider:
# REMOVED_UNUSED_CODE:             env_info["fee"] = self.data_provider._exchange.get_fee(  # type: ignore
# REMOVED_UNUSED_CODE:                 symbol=self.data_provider.current_whitelist()[0]
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return env_info
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @abstractmethod
# REMOVED_UNUSED_CODE:     def fit(self, data_dictionary: dict[str, Any], dk: FreqaiDataKitchen, **kwargs):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Agent customizations and abstract Reinforcement Learning customizations
# REMOVED_UNUSED_CODE:         go in here. Abstract method, so this function must be overridden by
# REMOVED_UNUSED_CODE:         user class.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def get_state_info(self, pair: str) -> tuple[float, float, int]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         State info during dry/live (not backtesting) which is fed back
# REMOVED_UNUSED_CODE:         into the model.
# REMOVED_UNUSED_CODE:         :param pair: str = COIN/STAKE to get the environment information for
# REMOVED_UNUSED_CODE:         :return:
# REMOVED_UNUSED_CODE:         :market_side: float = representing short, long, or neutral for
# REMOVED_UNUSED_CODE:             pair
# REMOVED_UNUSED_CODE:         :current_profit: float = unrealized profit of the current trade
# REMOVED_UNUSED_CODE:         :trade_duration: int = the number of candles that the trade has
# REMOVED_UNUSED_CODE:             been open for
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         open_trades = Trade.get_trades_proxy(is_open=True)
# REMOVED_UNUSED_CODE:         market_side = 0.5
# REMOVED_UNUSED_CODE:         current_profit: float = 0
# REMOVED_UNUSED_CODE:         trade_duration = 0
# REMOVED_UNUSED_CODE:         for trade in open_trades:
# REMOVED_UNUSED_CODE:             if trade.pair == pair:
# REMOVED_UNUSED_CODE:                 if self.data_provider._exchange is None:  # type: ignore
# REMOVED_UNUSED_CODE:                     logger.error("No exchange available.")
# REMOVED_UNUSED_CODE:                     return 0, 0, 0
# REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE:                     current_rate = self.data_provider._exchange.get_rate(  # type: ignore
# REMOVED_UNUSED_CODE:                         pair, refresh=False, side="exit", is_short=trade.is_short
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 now = datetime.now(timezone.utc).timestamp()
# REMOVED_UNUSED_CODE:                 trade_duration = int((now - trade.open_date_utc.timestamp()) / self.base_tf_seconds)
# REMOVED_UNUSED_CODE:                 current_profit = trade.calc_profit_ratio(current_rate)
# REMOVED_UNUSED_CODE:                 if trade.is_short:
# REMOVED_UNUSED_CODE:                     market_side = 0
# REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE:                     market_side = 1
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return market_side, current_profit, int(trade_duration)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def predict(
# REMOVED_UNUSED_CODE:         self, unfiltered_df: DataFrame, dk: FreqaiDataKitchen, **kwargs
# REMOVED_UNUSED_CODE:     ) -> tuple[DataFrame, npt.NDArray[np.int_]]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Filter the prediction features data and predict with it.
# REMOVED_UNUSED_CODE:         :param unfiltered_dataframe: Full dataframe for the current backtest period.
# REMOVED_UNUSED_CODE:         :return:
# REMOVED_UNUSED_CODE:         :pred_df: dataframe containing the predictions
# REMOVED_UNUSED_CODE:         :do_predict: np.array of 1s and 0s to indicate places where freqai needed to remove
# REMOVED_UNUSED_CODE:         data (NaNs) or felt uncertain about data (PCA and DI index)
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         dk.find_features(unfiltered_df)
# REMOVED_UNUSED_CODE:         filtered_dataframe, _ = dk.filter_features(
# REMOVED_UNUSED_CODE:             unfiltered_df, dk.training_features_list, training_filter=False
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         dk.data_dictionary["prediction_features"] = self.drop_ohlc_from_df(filtered_dataframe, dk)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         dk.data_dictionary["prediction_features"], _, _ = dk.feature_pipeline.transform(
# REMOVED_UNUSED_CODE:             dk.data_dictionary["prediction_features"], outlier_check=True
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         pred_df = self.rl_model_predict(dk.data_dictionary["prediction_features"], dk, self.model)
# REMOVED_UNUSED_CODE:         pred_df.fillna(0, inplace=True)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return (pred_df, dk.do_predict)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def rl_model_predict(
# REMOVED_UNUSED_CODE:         self, dataframe: DataFrame, dk: FreqaiDataKitchen, model: Any
# REMOVED_UNUSED_CODE:     ) -> DataFrame:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         A helper function to make predictions in the Reinforcement learning module.
# REMOVED_UNUSED_CODE:         :param dataframe: DataFrame = the dataframe of features to make the predictions on
# REMOVED_UNUSED_CODE:         :param dk: FreqaiDatakitchen = data kitchen for the current pair
# REMOVED_UNUSED_CODE:         :param model: Any = the trained model used to inference the features.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         output = pd.DataFrame(np.zeros(len(dataframe)), columns=dk.label_list)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         def _predict(window):
# REMOVED_UNUSED_CODE:             observations = dataframe.iloc[window.index]
# REMOVED_UNUSED_CODE:             if self.live and self.rl_config.get("add_state_info", False):
# REMOVED_UNUSED_CODE:                 market_side, current_profit, trade_duration = self.get_state_info(dk.pair)
# REMOVED_UNUSED_CODE:                 observations["current_profit_pct"] = current_profit
# REMOVED_UNUSED_CODE:                 observations["position"] = market_side
# REMOVED_UNUSED_CODE:                 observations["trade_duration"] = trade_duration
# REMOVED_UNUSED_CODE:             res, _ = model.predict(observations, deterministic=True)
# REMOVED_UNUSED_CODE:             return res
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         output = output.rolling(window=self.CONV_WIDTH).apply(_predict)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return output
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def build_ohlc_price_dataframes(
# REMOVED_UNUSED_CODE:         self, data_dictionary: dict, pair: str, dk: FreqaiDataKitchen
# REMOVED_UNUSED_CODE:     ) -> tuple[DataFrame, DataFrame]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Builds the train prices and test prices for the environment.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         pair = pair.replace(":", "")
# REMOVED_UNUSED_CODE:         train_df = data_dictionary["train_features"]
# REMOVED_UNUSED_CODE:         test_df = data_dictionary["test_features"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # price data for model training and evaluation
# REMOVED_UNUSED_CODE:         tf = self.config["timeframe"]
# REMOVED_UNUSED_CODE:         rename_dict = {
# REMOVED_UNUSED_CODE:             "%-raw_open": "open",
# REMOVED_UNUSED_CODE:             "%-raw_low": "low",
# REMOVED_UNUSED_CODE:             "%-raw_high": " high",
# REMOVED_UNUSED_CODE:             "%-raw_close": "close",
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE:         rename_dict_old = {
# REMOVED_UNUSED_CODE:             f"%-{pair}raw_open_{tf}": "open",
# REMOVED_UNUSED_CODE:             f"%-{pair}raw_low_{tf}": "low",
# REMOVED_UNUSED_CODE:             f"%-{pair}raw_high_{tf}": " high",
# REMOVED_UNUSED_CODE:             f"%-{pair}raw_close_{tf}": "close",
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         prices_train = train_df.filter(rename_dict.keys(), axis=1)
# REMOVED_UNUSED_CODE:         prices_train_old = train_df.filter(rename_dict_old.keys(), axis=1)
# REMOVED_UNUSED_CODE:         if prices_train.empty or not prices_train_old.empty:
# REMOVED_UNUSED_CODE:             if not prices_train_old.empty:
# REMOVED_UNUSED_CODE:                 prices_train = prices_train_old
# REMOVED_UNUSED_CODE:                 rename_dict = rename_dict_old
# REMOVED_UNUSED_CODE:             logger.warning(
# REMOVED_UNUSED_CODE:                 "Reinforcement learning module didn't find the correct raw prices "
# REMOVED_UNUSED_CODE:                 "assigned in feature_engineering_standard(). "
# REMOVED_UNUSED_CODE:                 "Please assign them with:\n"
# REMOVED_UNUSED_CODE:                 'dataframe["%-raw_close"] = dataframe["close"]\n'
# REMOVED_UNUSED_CODE:                 'dataframe["%-raw_open"] = dataframe["open"]\n'
# REMOVED_UNUSED_CODE:                 'dataframe["%-raw_high"] = dataframe["high"]\n'
# REMOVED_UNUSED_CODE:                 'dataframe["%-raw_low"] = dataframe["low"]\n'
# REMOVED_UNUSED_CODE:                 "inside `feature_engineering_standard()"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         elif prices_train.empty:
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 "No prices found, please follow log warning instructions to correct the strategy."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         prices_train.rename(columns=rename_dict, inplace=True)
# REMOVED_UNUSED_CODE:         prices_train.reset_index(drop=True)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         prices_test = test_df.filter(rename_dict.keys(), axis=1)
# REMOVED_UNUSED_CODE:         prices_test.rename(columns=rename_dict, inplace=True)
# REMOVED_UNUSED_CODE:         prices_test.reset_index(drop=True)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         train_df = self.drop_ohlc_from_df(train_df, dk)
# REMOVED_UNUSED_CODE:         test_df = self.drop_ohlc_from_df(test_df, dk)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return prices_train, prices_test
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def drop_ohlc_from_df(self, df: DataFrame, dk: FreqaiDataKitchen):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Given a dataframe, drop the ohlc data
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         drop_list = ["%-raw_open", "%-raw_low", "%-raw_high", "%-raw_close"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.rl_config["drop_ohlc_from_features"]:
# REMOVED_UNUSED_CODE:             df.drop(drop_list, axis=1, inplace=True)
# REMOVED_UNUSED_CODE:             feature_list = dk.training_features_list
# REMOVED_UNUSED_CODE:             dk.training_features_list = [e for e in feature_list if e not in drop_list]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return df
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def load_model_from_disk(self, dk: FreqaiDataKitchen) -> Any:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Can be used by user if they are trying to limit_ram_usage *and*
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         perform continual learning.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         For now, this is unused.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         exists = Path(dk.data_path / f"{dk.model_filename}_model").is_file()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if exists:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             model = self.MODELCLASS.load(dk.data_path / f"{dk.model_filename}_model")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             logger.info("No model file on disk to continue learning from.")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return model
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def _on_stop(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Hook called on bot shutdown. Close SubprocVecEnv subprocesses for clean shutdown.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.train_env:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.train_env.close()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.eval_env:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.eval_env.close()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Nested class which can be overridden by user to customize further
# REMOVED_UNUSED_CODE:     class MyRLEnv(Base5ActionRLEnv):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         User can override any function in BaseRLEnv and gym.Env. Here the user
# REMOVED_UNUSED_CODE:         sets a custom reward based on profit and trade duration.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         def calculate_reward(self, action: int) -> float:  # noqa: C901
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             An example reward function. This is the one function that users will likely
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             wish to inject their own creativity into.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             Warning!
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             This is function is a showcase of functionality designed to show as many possible
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             environment control features as possible. It is also designed to run quickly
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             on small computers. This is a benchmark, it is *not* for live production.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             :param action: int = The action made by the agent for the current candle.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             :return:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             float = the reward to give to the agent for current step (used for optimization
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 of weights in NN)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # first, penalize if the action is not valid
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if not self._is_valid(action):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return -2
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             pnl = self.get_unrealized_profit()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             factor = 100.0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # you can use feature values from dataframe
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             rsi_now = self.raw_features[
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"%-rsi-period-10_shift-1_{self.pair}_{self.config['timeframe']}"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ].iloc[self._current_tick]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # reward agent for entering trades
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 action in (Actions.Long_enter.value, Actions.Short_enter.value)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 and self._position == Positions.Neutral
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if rsi_now < 40:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     factor = 40 / rsi_now
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     factor = 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return 25 * factor
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # discourage agent from not entering trades
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if action == Actions.Neutral.value and self._position == Positions.Neutral:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return -1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             max_trade_duration = self.rl_config.get("max_trade_duration_candles", 300)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if self._last_trade_tick:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 trade_duration = self._current_tick - self._last_trade_tick
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 trade_duration = 0
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
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if action == Actions.Long_exit.value and self._position == Positions.Long:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if pnl > self.profit_aim * self.rr:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     factor *= self.rl_config["model_reward_parameters"].get("win_reward_factor", 2)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return float(pnl * factor)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # close short
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if action == Actions.Short_exit.value and self._position == Positions.Short:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if pnl > self.profit_aim * self.rr:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     factor *= self.rl_config["model_reward_parameters"].get("win_reward_factor", 2)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return float(pnl * factor)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return 0.0


# REMOVED_UNUSED_CODE: def make_env(
# REMOVED_UNUSED_CODE:     MyRLEnv: type[BaseEnvironment],
# REMOVED_UNUSED_CODE:     env_id: str,
# REMOVED_UNUSED_CODE:     rank: int,
# REMOVED_UNUSED_CODE:     seed: int,
# REMOVED_UNUSED_CODE:     train_df: DataFrame,
# REMOVED_UNUSED_CODE:     price: DataFrame,
# REMOVED_UNUSED_CODE:     env_info: dict[str, Any] = {},
# REMOVED_UNUSED_CODE: ) -> Callable:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Utility function for multiprocessed env.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     :param env_id: (str) the environment ID
# REMOVED_UNUSED_CODE:     :param num_env: (int) the number of environment you wish to have in subprocesses
# REMOVED_UNUSED_CODE:     :param seed: (int) the initial seed for RNG
# REMOVED_UNUSED_CODE:     :param rank: (int) index of the subprocess
# REMOVED_UNUSED_CODE:     :param env_info: (dict) all required arguments to instantiate the environment.
# REMOVED_UNUSED_CODE:     :return: (Callable)
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _init() -> gym.Env:
# REMOVED_UNUSED_CODE:         env = MyRLEnv(df=train_df, prices=price, id=env_id, seed=seed + rank, **env_info)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return env
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     set_random_seed(seed)
# REMOVED_UNUSED_CODE:     return _init
