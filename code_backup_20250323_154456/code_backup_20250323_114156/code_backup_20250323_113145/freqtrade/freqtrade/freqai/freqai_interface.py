import logging
import threading
import time
from abc import ABC, abstractmethod
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

import datasieve.transforms as ds
import numpy as np
import pandas as pd
import psutil
from datasieve.pipeline import Pipeline
from datasieve.transforms import SKLearnWrapper
from numpy.typing import NDArray
from pandas import DataFrame
from sklearn.preprocessing import MinMaxScaler

from freqtrade.configuration import TimeRange
from freqtrade.constants import DOCS_LINK, Config
from freqtrade.data.dataprovider import DataProvider
from freqtrade.enums import RunMode
from freqtrade.exceptions import OperationalException
from freqtrade.exchange import timeframe_to_seconds
from freqtrade.freqai.data_drawer import FreqaiDataDrawer
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen
from freqtrade.freqai.utils import get_tb_logger, plot_feature_importance, record_params
from freqtrade.strategy.interface import IStrategy


# REMOVED_UNUSED_CODE: pd.options.mode.chained_assignment = None
logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class IFreqaiModel(ABC):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Class containing all tools for training and prediction in the strategy.
# REMOVED_UNUSED_CODE:     Base*PredictionModels inherit from this class.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Record of contribution:
# REMOVED_UNUSED_CODE:     FreqAI was developed by a group of individuals who all contributed specific skillsets to the
# REMOVED_UNUSED_CODE:     project.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Conception and software development:
# REMOVED_UNUSED_CODE:     Robert Caulk @robcaulk
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Theoretical brainstorming:
# REMOVED_UNUSED_CODE:     Elin Törnquist @th0rntwig
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Code review, software architecture brainstorming:
# REMOVED_UNUSED_CODE:     @xmatthias
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Beta testing and bug reporting:
# REMOVED_UNUSED_CODE:     @bloodhunter4rc, Salah Lamkadem @ikonx, @ken11o2, @longyu, @paranoidandy, @smidelis, @smarm
# REMOVED_UNUSED_CODE:     Juha Nykänen @suikula, Wagner Costa @wagnercosta, Johan Vlugt @Jooopieeert
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, config: Config) -> None:
# REMOVED_UNUSED_CODE:         self.config = config
# REMOVED_UNUSED_CODE:         self.assert_config(self.config)
# REMOVED_UNUSED_CODE:         self.freqai_info: dict[str, Any] = config["freqai"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.data_split_parameters: dict[str, Any] = config.get("freqai", {}).get(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "data_split_parameters", {}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.model_training_parameters: dict[str, Any] = config.get("freqai", {}).get(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "model_training_parameters", {}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         self.identifier: str = self.freqai_info.get("identifier", "no_id_provided")
# REMOVED_UNUSED_CODE:         self.retrain = False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.first = True
# REMOVED_UNUSED_CODE:         self.set_full_path()
# REMOVED_UNUSED_CODE:         self.save_backtest_models: bool = self.freqai_info.get("save_backtest_models", True)
# REMOVED_UNUSED_CODE:         if self.save_backtest_models:
# REMOVED_UNUSED_CODE:             logger.info("Backtesting module configured to save all models.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.dd = FreqaiDataDrawer(Path(self.full_path), self.config)
# REMOVED_UNUSED_CODE:         # set current candle to arbitrary historical date
# REMOVED_UNUSED_CODE:         self.current_candle: datetime = datetime.fromtimestamp(637887600, tz=timezone.utc)
# REMOVED_UNUSED_CODE:         self.dd.current_candle = self.current_candle
# REMOVED_UNUSED_CODE:         self.scanning = False
# REMOVED_UNUSED_CODE:         self.ft_params = self.freqai_info["feature_parameters"]
# REMOVED_UNUSED_CODE:         self.corr_pairlist: list[str] = self.ft_params.get("include_corr_pairlist", [])
# REMOVED_UNUSED_CODE:         self.keras: bool = self.freqai_info.get("keras", False)
# REMOVED_UNUSED_CODE:         if self.keras and self.ft_params.get("DI_threshold", 0):
# REMOVED_UNUSED_CODE:             self.ft_params["DI_threshold"] = 0
# REMOVED_UNUSED_CODE:             logger.warning("DI threshold is not configured for Keras models yet. Deactivating.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.CONV_WIDTH = self.freqai_info.get("conv_width", 1)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.class_names: list[str] = []  # used in classification subclasses
# REMOVED_UNUSED_CODE:         self.pair_it = 0
# REMOVED_UNUSED_CODE:         self.pair_it_train = 0
# REMOVED_UNUSED_CODE:         self.total_pairs = len(self.config.get("exchange", {}).get("pair_whitelist"))
# REMOVED_UNUSED_CODE:         self.train_queue = self._set_train_queue()
# REMOVED_UNUSED_CODE:         self.inference_time: float = 0
# REMOVED_UNUSED_CODE:         self.train_time: float = 0
# REMOVED_UNUSED_CODE:         self.begin_time: float = 0
# REMOVED_UNUSED_CODE:         self.begin_time_train: float = 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.base_tf_seconds = timeframe_to_seconds(self.config["timeframe"])
# REMOVED_UNUSED_CODE:         self.continual_learning = self.freqai_info.get("continual_learning", False)
# REMOVED_UNUSED_CODE:         self.plot_features = self.ft_params.get("plot_feature_importances", 0)
# REMOVED_UNUSED_CODE:         self.corr_dataframes: dict[str, DataFrame] = {}
# REMOVED_UNUSED_CODE:         # get_corr_dataframes is controlling the caching of corr_dataframes
# REMOVED_UNUSED_CODE:         # for improved performance. Careful with this boolean.
# REMOVED_UNUSED_CODE:         self.get_corr_dataframes: bool = True
# REMOVED_UNUSED_CODE:         self._threads: list[threading.Thread] = []
# REMOVED_UNUSED_CODE:         self._stop_event = threading.Event()
# REMOVED_UNUSED_CODE:         self.metadata: dict[str, Any] = self.dd.load_global_metadata_from_disk()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.data_provider: DataProvider | None = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.max_system_threads = max(int(psutil.cpu_count() * 2 - 2), 1)
# REMOVED_UNUSED_CODE:         self.can_short = True  # overridden in start() with strategy.can_short
# REMOVED_UNUSED_CODE:         self.model: Any = None
# REMOVED_UNUSED_CODE:         if self.ft_params.get("principal_component_analysis", False) and self.continual_learning:
# REMOVED_UNUSED_CODE:             self.ft_params.update({"principal_component_analysis": False})
# REMOVED_UNUSED_CODE:             logger.warning("User tried to use PCA with continual learning. Deactivating PCA.")
# REMOVED_UNUSED_CODE:         self.activate_tensorboard: bool = self.freqai_info.get("activate_tensorboard", True)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         record_params(config, self.full_path)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __getstate__(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Return an empty state to be pickled in hyperopt
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         return {}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def assert_config(self, config: Config) -> None:
# REMOVED_UNUSED_CODE:         if not config.get("freqai", {}):
# REMOVED_UNUSED_CODE:             raise OperationalException("No freqai parameters found in configuration file.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def start(self, dataframe: DataFrame, metadata: dict, strategy: IStrategy) -> DataFrame:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Entry point to the FreqaiModel from a specific pair, it will train a new model if
# REMOVED_UNUSED_CODE:         necessary before making the prediction.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         :param dataframe: Full dataframe coming from strategy - it contains entire
# REMOVED_UNUSED_CODE:                            backtesting timerange + additional historical data necessary to train
# REMOVED_UNUSED_CODE:         the model.
# REMOVED_UNUSED_CODE:         :param metadata: pair metadata coming from strategy.
# REMOVED_UNUSED_CODE:         :param strategy: Strategy to train on
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self.live = strategy.dp.runmode in (RunMode.DRY_RUN, RunMode.LIVE)
# REMOVED_UNUSED_CODE:         self.dd.set_pair_dict_info(metadata)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.data_provider = strategy.dp
# REMOVED_UNUSED_CODE:         self.can_short = strategy.can_short
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.live:
# REMOVED_UNUSED_CODE:             self.inference_timer("start")
# REMOVED_UNUSED_CODE:             self.dk = FreqaiDataKitchen(self.config, self.live, metadata["pair"])
# REMOVED_UNUSED_CODE:             dk = self.start_live(dataframe, metadata, strategy, self.dk)
# REMOVED_UNUSED_CODE:             dataframe = dk.remove_features_from_df(dk.return_dataframe)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # For backtesting, each pair enters and then gets trained for each window along the
# REMOVED_UNUSED_CODE:         # sliding window defined by "train_period_days" (training window) and "live_retrain_hours"
# REMOVED_UNUSED_CODE:         # (backtest window, i.e. window immediately following the training window).
# REMOVED_UNUSED_CODE:         # FreqAI slides the window and sequentially builds the backtesting results before returning
# REMOVED_UNUSED_CODE:         # the concatenated results for the full backtesting period back to the strategy.
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             self.dk = FreqaiDataKitchen(self.config, self.live, metadata["pair"])
# REMOVED_UNUSED_CODE:             if not self.config.get("freqai_backtest_live_models", False):
# REMOVED_UNUSED_CODE:                 logger.info(f"Training {len(self.dk.training_timeranges)} timeranges")
# REMOVED_UNUSED_CODE:                 dk = self.start_backtesting(dataframe, metadata, self.dk, strategy)
# REMOVED_UNUSED_CODE:                 dataframe = dk.remove_features_from_df(dk.return_dataframe)
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 logger.info("Backtesting using historic predictions (live models)")
# REMOVED_UNUSED_CODE:                 dk = self.start_backtesting_from_historic_predictions(dataframe, metadata, self.dk)
# REMOVED_UNUSED_CODE:                 dataframe = dk.return_dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.clean_up()
# REMOVED_UNUSED_CODE:         if self.live:
# REMOVED_UNUSED_CODE:             self.inference_timer("stop", metadata["pair"])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def clean_up(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Objects that should be handled by GC already between coins, but
# REMOVED_UNUSED_CODE:         are explicitly shown here to help demonstrate the non-persistence of these
# REMOVED_UNUSED_CODE:         objects.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self.model = None
# REMOVED_UNUSED_CODE:         self.dk = None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _on_stop(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Callback for Subclasses to override to include logic for shutting down resources
# REMOVED_UNUSED_CODE:         when SIGINT is sent.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self.dd.save_historic_predictions_to_disk()
# REMOVED_UNUSED_CODE:         return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def shutdown(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Cleans up threads on Shutdown, set stop event. Join threads to wait
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for current training iteration.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.info("Stopping FreqAI")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._stop_event.set()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.data_provider = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._on_stop()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.freqai_info.get("wait_for_training_iteration_on_reload", True):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             logger.info("Waiting on Training iteration")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for _thread in self._threads:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 _thread.join()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             logger.warning(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "Breaking current training iteration because "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "you set wait_for_training_iteration_on_reload to "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 " False."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def start_scanning(self, *args, **kwargs) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Start `self._start_scanning` in a separate thread
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         _thread = threading.Thread(target=self._start_scanning, args=args, kwargs=kwargs)
# REMOVED_UNUSED_CODE:         self._threads.append(_thread)
# REMOVED_UNUSED_CODE:         _thread.start()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _start_scanning(self, strategy: IStrategy) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Function designed to constantly scan pairs for retraining on a separate thread (intracandle)
# REMOVED_UNUSED_CODE:         to improve model youth. This function is agnostic to data preparation/collection/storage,
# REMOVED_UNUSED_CODE:         it simply trains on what ever data is available in the self.dd.
# REMOVED_UNUSED_CODE:         :param strategy: IStrategy = The user defined strategy class
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         while not self._stop_event.is_set():
# REMOVED_UNUSED_CODE:             time.sleep(1)
# REMOVED_UNUSED_CODE:             pair = self.train_queue[0]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # ensure pair is available in dp
# REMOVED_UNUSED_CODE:             if pair not in strategy.dp.current_whitelist():
# REMOVED_UNUSED_CODE:                 self.train_queue.popleft()
# REMOVED_UNUSED_CODE:                 logger.warning(f"{pair} not in current whitelist, removing from train queue.")
# REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             (_, trained_timestamp) = self.dd.get_pair_dict_info(pair)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             dk = FreqaiDataKitchen(self.config, self.live, pair)
# REMOVED_UNUSED_CODE:             (
# REMOVED_UNUSED_CODE:                 retrain,
# REMOVED_UNUSED_CODE:                 new_trained_timerange,
# REMOVED_UNUSED_CODE:                 data_load_timerange,
# REMOVED_UNUSED_CODE:             ) = dk.check_if_new_training_required(trained_timestamp)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if retrain:
# REMOVED_UNUSED_CODE:                 self.train_timer("start")
# REMOVED_UNUSED_CODE:                 dk.set_paths(pair, new_trained_timerange.stopts)
# REMOVED_UNUSED_CODE:                 try:
# REMOVED_UNUSED_CODE:                     self.extract_data_and_train_model(
# REMOVED_UNUSED_CODE:                         new_trained_timerange, pair, strategy, dk, data_load_timerange
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                 except Exception as msg:
# REMOVED_UNUSED_CODE:                     logger.exception(
# REMOVED_UNUSED_CODE:                         f"Training {pair} raised exception {msg.__class__.__name__}. "
# REMOVED_UNUSED_CODE:                         f"Message: {msg}, skipping."
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 self.train_timer("stop", pair)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 # only rotate the queue after the first has been trained.
# REMOVED_UNUSED_CODE:                 self.train_queue.rotate(-1)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 self.dd.save_historic_predictions_to_disk()
# REMOVED_UNUSED_CODE:                 if self.freqai_info.get("write_metrics_to_disk", False):
# REMOVED_UNUSED_CODE:                     self.dd.save_metric_tracker_to_disk()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def start_backtesting(
# REMOVED_UNUSED_CODE:         self, dataframe: DataFrame, metadata: dict, dk: FreqaiDataKitchen, strategy: IStrategy
# REMOVED_UNUSED_CODE:     ) -> FreqaiDataKitchen:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         The main broad execution for backtesting. For backtesting, each pair enters and then gets
# REMOVED_UNUSED_CODE:         trained for each window along the sliding window defined by "train_period_days"
# REMOVED_UNUSED_CODE:         (training window) and "backtest_period_days" (backtest window, i.e. window immediately
# REMOVED_UNUSED_CODE:         following the training window). FreqAI slides the window and sequentially builds
# REMOVED_UNUSED_CODE:         the backtesting results before returning the concatenated results for the full
# REMOVED_UNUSED_CODE:         backtesting period back to the strategy.
# REMOVED_UNUSED_CODE:         :param dataframe: DataFrame = strategy passed dataframe
# REMOVED_UNUSED_CODE:         :param metadata: Dict = pair metadata
# REMOVED_UNUSED_CODE:         :param dk: FreqaiDataKitchen = Data management/analysis tool associated to present pair only
# REMOVED_UNUSED_CODE:         :param strategy: Strategy to train on
# REMOVED_UNUSED_CODE:         :return:
# REMOVED_UNUSED_CODE:             FreqaiDataKitchen = Data management/analysis tool associated to present pair only
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.pair_it += 1
# REMOVED_UNUSED_CODE:         train_it = 0
# REMOVED_UNUSED_CODE:         pair = metadata["pair"]
# REMOVED_UNUSED_CODE:         populate_indicators = True
# REMOVED_UNUSED_CODE:         check_features = True
# REMOVED_UNUSED_CODE:         # Loop enforcing the sliding window training/backtesting paradigm
# REMOVED_UNUSED_CODE:         # tr_train is the training time range e.g. 1 historical month
# REMOVED_UNUSED_CODE:         # tr_backtest is the backtesting time range e.g. the week directly
# REMOVED_UNUSED_CODE:         # following tr_train. Both of these windows slide through the
# REMOVED_UNUSED_CODE:         # entire backtest
# REMOVED_UNUSED_CODE:         for tr_train, tr_backtest in zip(
# REMOVED_UNUSED_CODE:             dk.training_timeranges, dk.backtesting_timeranges, strict=False
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             (_, _) = self.dd.get_pair_dict_info(pair)
# REMOVED_UNUSED_CODE:             train_it += 1
# REMOVED_UNUSED_CODE:             total_trains = len(dk.backtesting_timeranges)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.training_timerange = tr_train
# REMOVED_UNUSED_CODE:             len_backtest_df = len(
# REMOVED_UNUSED_CODE:                 dataframe.loc[
# REMOVED_UNUSED_CODE:                     (dataframe["date"] >= tr_backtest.startdt)
# REMOVED_UNUSED_CODE:                     & (dataframe["date"] < tr_backtest.stopdt),
# REMOVED_UNUSED_CODE:                     :,
# REMOVED_UNUSED_CODE:                 ]
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if not self.ensure_data_exists(len_backtest_df, tr_backtest, pair):
# REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             self.log_backtesting_progress(tr_train, pair, train_it, total_trains)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             timestamp_model_id = int(tr_train.stopts)
# REMOVED_UNUSED_CODE:             if dk.backtest_live_models:
# REMOVED_UNUSED_CODE:                 timestamp_model_id = int(tr_backtest.startts)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             dk.set_paths(pair, timestamp_model_id)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             dk.set_new_model_names(pair, timestamp_model_id)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if dk.check_if_backtest_prediction_is_valid(len_backtest_df):
# REMOVED_UNUSED_CODE:                 if check_features:
# REMOVED_UNUSED_CODE:                     self.dd.load_metadata(dk)
# REMOVED_UNUSED_CODE:                     df_fts = self.dk.use_strategy_to_populate_indicators(
# REMOVED_UNUSED_CODE:                         strategy, prediction_dataframe=dataframe.tail(1), pair=pair
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                     df_fts = dk.remove_special_chars_from_feature_names(df_fts)
# REMOVED_UNUSED_CODE:                     dk.find_features(df_fts)
# REMOVED_UNUSED_CODE:                     self.check_if_feature_list_matches_strategy(dk)
# REMOVED_UNUSED_CODE:                     check_features = False
# REMOVED_UNUSED_CODE:                 append_df = dk.get_backtesting_prediction()
# REMOVED_UNUSED_CODE:                 dk.append_predictions(append_df)
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 if populate_indicators:
# REMOVED_UNUSED_CODE:                     dataframe = self.dk.use_strategy_to_populate_indicators(
# REMOVED_UNUSED_CODE:                         strategy, prediction_dataframe=dataframe, pair=pair
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:                     populate_indicators = False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 dataframe_base_train = dataframe.loc[dataframe["date"] < tr_train.stopdt, :]
# REMOVED_UNUSED_CODE:                 dataframe_base_train = strategy.set_freqai_targets(
# REMOVED_UNUSED_CODE:                     dataframe_base_train, metadata=metadata
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 dataframe_base_backtest = dataframe.loc[dataframe["date"] < tr_backtest.stopdt, :]
# REMOVED_UNUSED_CODE:                 dataframe_base_backtest = strategy.set_freqai_targets(
# REMOVED_UNUSED_CODE:                     dataframe_base_backtest, metadata=metadata
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 tr_train = dk.buffer_timerange(tr_train)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 dataframe_train = dk.slice_dataframe(tr_train, dataframe_base_train)
# REMOVED_UNUSED_CODE:                 dataframe_backtest = dk.slice_dataframe(tr_backtest, dataframe_base_backtest)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 dataframe_train = dk.remove_special_chars_from_feature_names(dataframe_train)
# REMOVED_UNUSED_CODE:                 dataframe_backtest = dk.remove_special_chars_from_feature_names(dataframe_backtest)
# REMOVED_UNUSED_CODE:                 dk.get_unique_classes_from_labels(dataframe_train)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 if not self.model_exists(dk):
# REMOVED_UNUSED_CODE:                     dk.find_features(dataframe_train)
# REMOVED_UNUSED_CODE:                     dk.find_labels(dataframe_train)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                     try:
# REMOVED_UNUSED_CODE:                         self.tb_logger = get_tb_logger(
# REMOVED_UNUSED_CODE:                             self.dd.model_type, dk.data_path, self.activate_tensorboard
# REMOVED_UNUSED_CODE:                         )
# REMOVED_UNUSED_CODE:                         self.model = self.train(dataframe_train, pair, dk)
# REMOVED_UNUSED_CODE:                         self.tb_logger.close()
# REMOVED_UNUSED_CODE:                     except Exception as msg:
# REMOVED_UNUSED_CODE:                         logger.warning(
# REMOVED_UNUSED_CODE:                             f"Training {pair} raised exception {msg.__class__.__name__}. "
# REMOVED_UNUSED_CODE:                             f"Message: {msg}, skipping.",
# REMOVED_UNUSED_CODE:                             exc_info=True,
# REMOVED_UNUSED_CODE:                         )
# REMOVED_UNUSED_CODE:                         self.model = None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                     self.dd.pair_dict[pair]["trained_timestamp"] = int(tr_train.stopts)
# REMOVED_UNUSED_CODE:                     if self.plot_features and self.model is not None:
# REMOVED_UNUSED_CODE:                         plot_feature_importance(self.model, pair, dk, self.plot_features)
# REMOVED_UNUSED_CODE:                     if self.save_backtest_models and self.model is not None:
# REMOVED_UNUSED_CODE:                         logger.info("Saving backtest model to disk.")
# REMOVED_UNUSED_CODE:                         self.dd.save_data(self.model, pair, dk)
# REMOVED_UNUSED_CODE:                     else:
# REMOVED_UNUSED_CODE:                         logger.info("Saving metadata to disk.")
# REMOVED_UNUSED_CODE:                         self.dd.save_metadata(dk)
# REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE:                     self.model = self.dd.load_data(pair, dk)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 pred_df, do_preds = self.predict(dataframe_backtest, dk)
# REMOVED_UNUSED_CODE:                 append_df = dk.get_predictions_to_append(pred_df, do_preds, dataframe_backtest)
# REMOVED_UNUSED_CODE:                 dk.append_predictions(append_df)
# REMOVED_UNUSED_CODE:                 dk.save_backtesting_prediction(append_df)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.backtesting_fit_live_predictions(dk)
# REMOVED_UNUSED_CODE:         dk.fill_predictions(dataframe)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return dk
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def start_live(
# REMOVED_UNUSED_CODE:         self, dataframe: DataFrame, metadata: dict, strategy: IStrategy, dk: FreqaiDataKitchen
# REMOVED_UNUSED_CODE:     ) -> FreqaiDataKitchen:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         The main broad execution for dry/live. This function will check if a retraining should be
# REMOVED_UNUSED_CODE:         performed, and if so, retrain and reset the model.
# REMOVED_UNUSED_CODE:         :param dataframe: DataFrame = strategy passed dataframe
# REMOVED_UNUSED_CODE:         :param metadata: Dict = pair metadata
# REMOVED_UNUSED_CODE:         :param strategy: IStrategy = currently employed strategy
# REMOVED_UNUSED_CODE:         dk: FreqaiDataKitchen = Data management/analysis tool associated to present pair only
# REMOVED_UNUSED_CODE:         :returns:
# REMOVED_UNUSED_CODE:         dk: FreqaiDataKitchen = Data management/analysis tool associated to present pair only
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not strategy.process_only_new_candles:
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 "You are trying to use a FreqAI strategy with "
# REMOVED_UNUSED_CODE:                 "process_only_new_candles = False. This is not supported "
# REMOVED_UNUSED_CODE:                 "by FreqAI, and it is therefore aborting."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # get the model metadata associated with the current pair
# REMOVED_UNUSED_CODE:         (_, trained_timestamp) = self.dd.get_pair_dict_info(metadata["pair"])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # append the historic data once per round
# REMOVED_UNUSED_CODE:         if self.dd.historic_data:
# REMOVED_UNUSED_CODE:             self.dd.update_historic_data(strategy, dk)
# REMOVED_UNUSED_CODE:             logger.debug(f"Updating historic data on pair {metadata['pair']}")
# REMOVED_UNUSED_CODE:             self.track_current_candle()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         (_, new_trained_timerange, data_load_timerange) = dk.check_if_new_training_required(
# REMOVED_UNUSED_CODE:             trained_timestamp
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         dk.set_paths(metadata["pair"], new_trained_timerange.stopts)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # load candle history into memory if it is not yet.
# REMOVED_UNUSED_CODE:         if not self.dd.historic_data:
# REMOVED_UNUSED_CODE:             self.dd.load_all_pair_histories(data_load_timerange, dk)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not self.scanning:
# REMOVED_UNUSED_CODE:             self.scanning = True
# REMOVED_UNUSED_CODE:             self.start_scanning(strategy)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # load the model and associated data into the data kitchen
# REMOVED_UNUSED_CODE:         self.model = self.dd.load_data(metadata["pair"], dk)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         dataframe = dk.use_strategy_to_populate_indicators(
# REMOVED_UNUSED_CODE:             strategy,
# REMOVED_UNUSED_CODE:             prediction_dataframe=dataframe,
# REMOVED_UNUSED_CODE:             pair=metadata["pair"],
# REMOVED_UNUSED_CODE:             do_corr_pairs=self.get_corr_dataframes,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not self.model:
# REMOVED_UNUSED_CODE:             logger.warning(
# REMOVED_UNUSED_CODE:                 f"No model ready for {metadata['pair']}, returning null values to strategy."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             self.dd.return_null_values_to_strategy(dataframe, dk)
# REMOVED_UNUSED_CODE:             return dk
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.corr_pairlist:
# REMOVED_UNUSED_CODE:             dataframe = self.cache_corr_pairlist_dfs(dataframe, dk)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         dk.find_labels(dataframe)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.build_strategy_return_arrays(dataframe, dk, metadata["pair"], trained_timestamp)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return dk
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def build_strategy_return_arrays(
# REMOVED_UNUSED_CODE:         self, dataframe: DataFrame, dk: FreqaiDataKitchen, pair: str, trained_timestamp: int
# REMOVED_UNUSED_CODE:     ) -> None:
# REMOVED_UNUSED_CODE:         # hold the historical predictions in memory so we are sending back
# REMOVED_UNUSED_CODE:         # correct array to strategy
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if pair not in self.dd.model_return_values:
# REMOVED_UNUSED_CODE:             # first predictions are made on entire historical candle set coming from strategy. This
# REMOVED_UNUSED_CODE:             # allows FreqUI to show full return values.
# REMOVED_UNUSED_CODE:             pred_df, do_preds = self.predict(dataframe, dk)
# REMOVED_UNUSED_CODE:             if pair not in self.dd.historic_predictions:
# REMOVED_UNUSED_CODE:                 self.set_initial_historic_predictions(pred_df, dk, pair, dataframe)
# REMOVED_UNUSED_CODE:             self.dd.set_initial_return_values(pair, pred_df, dataframe)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             dk.return_dataframe = self.dd.attach_return_values_to_return_dataframe(pair, dataframe)
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE:         elif self.dk.check_if_model_expired(trained_timestamp):
# REMOVED_UNUSED_CODE:             pred_df = DataFrame(np.zeros((2, len(dk.label_list))), columns=dk.label_list)
# REMOVED_UNUSED_CODE:             do_preds = np.ones(2, dtype=np.int_) * 2
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.DI_values = np.zeros(2)
# REMOVED_UNUSED_CODE:             logger.warning(
# REMOVED_UNUSED_CODE:                 f"Model expired for {pair}, returning null values to strategy. Strategy "
# REMOVED_UNUSED_CODE:                 "construction should take care to consider this event with "
# REMOVED_UNUSED_CODE:                 "prediction == 0 and do_predict == 2"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             # remaining predictions are made only on the most recent candles for performance and
# REMOVED_UNUSED_CODE:             # historical accuracy reasons.
# REMOVED_UNUSED_CODE:             pred_df, do_preds = self.predict(dataframe.iloc[-self.CONV_WIDTH :], dk, first=False)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.freqai_info.get("fit_live_predictions_candles", 0) and self.live:
# REMOVED_UNUSED_CODE:             self.fit_live_predictions(dk, pair)
# REMOVED_UNUSED_CODE:         self.dd.append_model_predictions(pair, pred_df, do_preds, dk, dataframe)
# REMOVED_UNUSED_CODE:         dk.return_dataframe = self.dd.attach_return_values_to_return_dataframe(pair, dataframe)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def check_if_feature_list_matches_strategy(self, dk: FreqaiDataKitchen) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Ensure user is passing the proper feature set if they are reusing an `identifier` pointing
# REMOVED_UNUSED_CODE:         to a folder holding existing models.
# REMOVED_UNUSED_CODE:         :param dataframe: DataFrame = strategy provided dataframe
# REMOVED_UNUSED_CODE:         :param dk: FreqaiDataKitchen = non-persistent data container/analyzer for
# REMOVED_UNUSED_CODE:                    current coin/bot loop
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if "training_features_list_raw" in dk.data:
# REMOVED_UNUSED_CODE:             feature_list = dk.data["training_features_list_raw"]
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             feature_list = dk.data["training_features_list"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if dk.training_features_list != feature_list:
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 "Trying to access pretrained model with `identifier` "
# REMOVED_UNUSED_CODE:                 "but found different features furnished by current strategy. "
# REMOVED_UNUSED_CODE:                 "Change `identifier` to train from scratch, or ensure the "
# REMOVED_UNUSED_CODE:                 "strategy is furnishing the same features as the pretrained "
# REMOVED_UNUSED_CODE:                 "model. In case of --strategy-list, please be aware that FreqAI "
# REMOVED_UNUSED_CODE:                 "requires all strategies to maintain identical "
# REMOVED_UNUSED_CODE:                 "feature_engineering_* functions"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def define_data_pipeline(self, threads=-1) -> Pipeline:
# REMOVED_UNUSED_CODE:         ft_params = self.freqai_info["feature_parameters"]
# REMOVED_UNUSED_CODE:         pipe_steps = [
# REMOVED_UNUSED_CODE:             ("const", ds.VarianceThreshold(threshold=0)),
# REMOVED_UNUSED_CODE:             ("scaler", SKLearnWrapper(MinMaxScaler(feature_range=(-1, 1)))),
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if ft_params.get("principal_component_analysis", False):
# REMOVED_UNUSED_CODE:             pipe_steps.append(("pca", ds.PCA(n_components=0.999)))
# REMOVED_UNUSED_CODE:             pipe_steps.append(
# REMOVED_UNUSED_CODE:                 ("post-pca-scaler", SKLearnWrapper(MinMaxScaler(feature_range=(-1, 1))))
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if ft_params.get("use_SVM_to_remove_outliers", False):
# REMOVED_UNUSED_CODE:             svm_params = ft_params.get("svm_params", {"shuffle": False, "nu": 0.01})
# REMOVED_UNUSED_CODE:             pipe_steps.append(("svm", ds.SVMOutlierExtractor(**svm_params)))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         di = ft_params.get("DI_threshold", 0)
# REMOVED_UNUSED_CODE:         if di:
# REMOVED_UNUSED_CODE:             pipe_steps.append(("di", ds.DissimilarityIndex(di_threshold=di, n_jobs=threads)))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if ft_params.get("use_DBSCAN_to_remove_outliers", False):
# REMOVED_UNUSED_CODE:             pipe_steps.append(("dbscan", ds.DBSCAN(n_jobs=threads)))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         sigma = self.freqai_info["feature_parameters"].get("noise_standard_deviation", 0)
# REMOVED_UNUSED_CODE:         if sigma:
# REMOVED_UNUSED_CODE:             pipe_steps.append(("noise", ds.Noise(sigma=sigma)))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return Pipeline(pipe_steps)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def define_label_pipeline(self, threads=-1) -> Pipeline:
# REMOVED_UNUSED_CODE:         label_pipeline = Pipeline([("scaler", SKLearnWrapper(MinMaxScaler(feature_range=(-1, 1))))])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return label_pipeline
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def model_exists(self, dk: FreqaiDataKitchen) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Given a pair and path, check if a model already exists
# REMOVED_UNUSED_CODE:         :param pair: pair e.g. BTC/USD
# REMOVED_UNUSED_CODE:         :param path: path to model
# REMOVED_UNUSED_CODE:         :return:
# REMOVED_UNUSED_CODE:         :boolean: whether the model file exists or not.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if self.dd.model_type == "joblib":
# REMOVED_UNUSED_CODE:             file_type = ".joblib"
# REMOVED_UNUSED_CODE:         elif self.dd.model_type in ["stable_baselines3", "sb3_contrib", "pytorch"]:
# REMOVED_UNUSED_CODE:             file_type = ".zip"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         path_to_modelfile = Path(dk.data_path / f"{dk.model_filename}_model{file_type}")
# REMOVED_UNUSED_CODE:         file_exists = path_to_modelfile.is_file()
# REMOVED_UNUSED_CODE:         if file_exists:
# REMOVED_UNUSED_CODE:             logger.info("Found model at %s", dk.data_path / dk.model_filename)
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             logger.info("Could not find model at %s", dk.data_path / dk.model_filename)
# REMOVED_UNUSED_CODE:         return file_exists
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def set_full_path(self) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Creates and sets the full path for the identifier
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self.full_path = Path(self.config["user_data_dir"] / "models" / f"{self.identifier}")
# REMOVED_UNUSED_CODE:         self.full_path.mkdir(parents=True, exist_ok=True)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def extract_data_and_train_model(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         new_trained_timerange: TimeRange,
# REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE:         strategy: IStrategy,
# REMOVED_UNUSED_CODE:         dk: FreqaiDataKitchen,
# REMOVED_UNUSED_CODE:         data_load_timerange: TimeRange,
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Retrieve data and train model.
# REMOVED_UNUSED_CODE:         :param new_trained_timerange: TimeRange = the timerange to train the model on
# REMOVED_UNUSED_CODE:         :param metadata: dict = strategy provided metadata
# REMOVED_UNUSED_CODE:         :param strategy: IStrategy = user defined strategy object
# REMOVED_UNUSED_CODE:         :param dk: FreqaiDataKitchen = non-persistent data container for current coin/loop
# REMOVED_UNUSED_CODE:         :param data_load_timerange: TimeRange = the amount of data to be loaded
# REMOVED_UNUSED_CODE:                                     for populating indicators
# REMOVED_UNUSED_CODE:                                     (larger than new_trained_timerange so that
# REMOVED_UNUSED_CODE:                                     new_trained_timerange does not contain any NaNs)
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         corr_dataframes, base_dataframes = self.dd.get_base_and_corr_dataframes(
# REMOVED_UNUSED_CODE:             data_load_timerange, pair, dk
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         unfiltered_dataframe = dk.use_strategy_to_populate_indicators(
# REMOVED_UNUSED_CODE:             strategy, corr_dataframes, base_dataframes, pair
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         trained_timestamp = new_trained_timerange.stopts
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         buffered_timerange = dk.buffer_timerange(new_trained_timerange)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         unfiltered_dataframe = dk.slice_dataframe(buffered_timerange, unfiltered_dataframe)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # find the features indicated by strategy and store in datakitchen
# REMOVED_UNUSED_CODE:         dk.find_features(unfiltered_dataframe)
# REMOVED_UNUSED_CODE:         dk.find_labels(unfiltered_dataframe)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.tb_logger = get_tb_logger(self.dd.model_type, dk.data_path, self.activate_tensorboard)
# REMOVED_UNUSED_CODE:         model = self.train(unfiltered_dataframe, pair, dk)
# REMOVED_UNUSED_CODE:         self.tb_logger.close()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.dd.pair_dict[pair]["trained_timestamp"] = trained_timestamp
# REMOVED_UNUSED_CODE:         dk.set_new_model_names(pair, trained_timestamp)
# REMOVED_UNUSED_CODE:         self.dd.save_data(model, pair, dk)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.plot_features:
# REMOVED_UNUSED_CODE:             plot_feature_importance(model, pair, dk, self.plot_features)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.dd.purge_old_models()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def set_initial_historic_predictions(
# REMOVED_UNUSED_CODE:         self, pred_df: DataFrame, dk: FreqaiDataKitchen, pair: str, strat_df: DataFrame
# REMOVED_UNUSED_CODE:     ) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         This function is called only if the datadrawer failed to load an
# REMOVED_UNUSED_CODE:         existing set of historic predictions. In this case, it builds
# REMOVED_UNUSED_CODE:         the structure and sets fake predictions off the first training
# REMOVED_UNUSED_CODE:         data. After that, FreqAI will append new real predictions to the
# REMOVED_UNUSED_CODE:         set of historic predictions.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         These values are used to generate live statistics which can be used
# REMOVED_UNUSED_CODE:         in the strategy for adaptive values. E.g. &*_mean/std are quantities
# REMOVED_UNUSED_CODE:         that can computed based on live predictions from the set of historical
# REMOVED_UNUSED_CODE:         predictions. Those values can be used in the user strategy to better
# REMOVED_UNUSED_CODE:         assess prediction rarity, and thus wait for probabilistically favorable
# REMOVED_UNUSED_CODE:         entries relative to the live historical predictions.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         If the user reuses an identifier on a subsequent instance,
# REMOVED_UNUSED_CODE:         this function will not be called. In that case, "real" predictions
# REMOVED_UNUSED_CODE:         will be appended to the loaded set of historic predictions.
# REMOVED_UNUSED_CODE:         :param pred_df: DataFrame = the dataframe containing the predictions coming
# REMOVED_UNUSED_CODE:             out of a model
# REMOVED_UNUSED_CODE:         :param dk: FreqaiDataKitchen = object containing methods for data analysis
# REMOVED_UNUSED_CODE:         :param pair: str = current pair
# REMOVED_UNUSED_CODE:         :param strat_df: DataFrame = dataframe coming from strategy
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.dd.historic_predictions[pair] = pred_df
# REMOVED_UNUSED_CODE:         hist_preds_df = self.dd.historic_predictions[pair]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.set_start_dry_live_date(strat_df)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         for label in hist_preds_df.columns:
# REMOVED_UNUSED_CODE:             if hist_preds_df[label].dtype == object:
# REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE:             hist_preds_df[f"{label}_mean"] = 0
# REMOVED_UNUSED_CODE:             hist_preds_df[f"{label}_std"] = 0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         hist_preds_df["do_predict"] = 0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.freqai_info["feature_parameters"].get("DI_threshold", 0) > 0:
# REMOVED_UNUSED_CODE:             hist_preds_df["DI_values"] = 0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         for return_str in dk.data["extra_returns_per_train"]:
# REMOVED_UNUSED_CODE:             hist_preds_df[return_str] = dk.data["extra_returns_per_train"][return_str]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         hist_preds_df["high_price"] = strat_df["high"]
# REMOVED_UNUSED_CODE:         hist_preds_df["low_price"] = strat_df["low"]
# REMOVED_UNUSED_CODE:         hist_preds_df["close_price"] = strat_df["close"]
# REMOVED_UNUSED_CODE:         hist_preds_df["date_pred"] = strat_df["date"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def fit_live_predictions(self, dk: FreqaiDataKitchen, pair: str) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Fit the labels with a gaussian distribution
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         import scipy as spy
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # add classes from classifier label types if used
# REMOVED_UNUSED_CODE:         full_labels = dk.label_list + dk.unique_class_list
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         num_candles = self.freqai_info.get("fit_live_predictions_candles", 100)
# REMOVED_UNUSED_CODE:         dk.data["labels_mean"], dk.data["labels_std"] = {}, {}
# REMOVED_UNUSED_CODE:         for label in full_labels:
# REMOVED_UNUSED_CODE:             if self.dd.historic_predictions[dk.pair][label].dtype == object:
# REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE:             f = spy.stats.norm.fit(self.dd.historic_predictions[dk.pair][label].tail(num_candles))
# REMOVED_UNUSED_CODE:             dk.data["labels_mean"][label], dk.data["labels_std"][label] = f[0], f[1]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def inference_timer(self, do: Literal["start", "stop"] = "start", pair: str = ""):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Timer designed to track the cumulative time spent in FreqAI for one pass through
# REMOVED_UNUSED_CODE:         the whitelist. This will check if the time spent is more than 1/4 the time
# REMOVED_UNUSED_CODE:         of a single candle, and if so, it will warn the user of degraded performance
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if do == "start":
# REMOVED_UNUSED_CODE:             self.pair_it += 1
# REMOVED_UNUSED_CODE:             self.begin_time = time.time()
# REMOVED_UNUSED_CODE:         elif do == "stop":
# REMOVED_UNUSED_CODE:             end = time.time()
# REMOVED_UNUSED_CODE:             time_spent = end - self.begin_time
# REMOVED_UNUSED_CODE:             if self.freqai_info.get("write_metrics_to_disk", False):
# REMOVED_UNUSED_CODE:                 self.dd.update_metric_tracker("inference_time", time_spent, pair)
# REMOVED_UNUSED_CODE:             self.inference_time += time_spent
# REMOVED_UNUSED_CODE:             if self.pair_it == self.total_pairs:
# REMOVED_UNUSED_CODE:                 logger.info(
# REMOVED_UNUSED_CODE:                     f"Total time spent inferencing pairlist {self.inference_time:.2f} seconds"
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 self.pair_it = 0
# REMOVED_UNUSED_CODE:                 self.inference_time = 0
# REMOVED_UNUSED_CODE:         return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def train_timer(self, do: Literal["start", "stop"] = "start", pair: str = ""):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Timer designed to track the cumulative time spent training the full pairlist in
# REMOVED_UNUSED_CODE:         FreqAI.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if do == "start":
# REMOVED_UNUSED_CODE:             self.pair_it_train += 1
# REMOVED_UNUSED_CODE:             self.begin_time_train = time.time()
# REMOVED_UNUSED_CODE:         elif do == "stop":
# REMOVED_UNUSED_CODE:             end = time.time()
# REMOVED_UNUSED_CODE:             time_spent = end - self.begin_time_train
# REMOVED_UNUSED_CODE:             if self.freqai_info.get("write_metrics_to_disk", False):
# REMOVED_UNUSED_CODE:                 self.dd.collect_metrics(time_spent, pair)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             self.train_time += time_spent
# REMOVED_UNUSED_CODE:             if self.pair_it_train == self.total_pairs:
# REMOVED_UNUSED_CODE:                 logger.info(f"Total time spent training pairlist {self.train_time:.2f} seconds")
# REMOVED_UNUSED_CODE:                 self.pair_it_train = 0
# REMOVED_UNUSED_CODE:                 self.train_time = 0
# REMOVED_UNUSED_CODE:         return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_init_model(self, pair: str) -> Any:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if pair not in self.dd.model_dictionary or not self.continual_learning:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             init_model = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             init_model = self.dd.model_dictionary[pair]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return init_model
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _set_train_queue(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Sets train queue from existing train timestamps if they exist
# REMOVED_UNUSED_CODE:         otherwise it sets the train queue based on the provided whitelist.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         current_pairlist = self.config.get("exchange", {}).get("pair_whitelist")
# REMOVED_UNUSED_CODE:         if not self.dd.pair_dict:
# REMOVED_UNUSED_CODE:             logger.info(f"Set fresh train queue from whitelist. Queue: {current_pairlist}")
# REMOVED_UNUSED_CODE:             return deque(current_pairlist)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         best_queue = deque()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         pair_dict_sorted = sorted(
# REMOVED_UNUSED_CODE:             self.dd.pair_dict.items(), key=lambda k: k[1]["trained_timestamp"]
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         for pair in pair_dict_sorted:
# REMOVED_UNUSED_CODE:             if pair[0] in current_pairlist:
# REMOVED_UNUSED_CODE:                 best_queue.append(pair[0])
# REMOVED_UNUSED_CODE:         for pair in current_pairlist:
# REMOVED_UNUSED_CODE:             if pair not in best_queue:
# REMOVED_UNUSED_CODE:                 best_queue.appendleft(pair)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         logger.info(
# REMOVED_UNUSED_CODE:             f"Set existing queue from trained timestamps. Best approximation queue: {best_queue}"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         return best_queue
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def cache_corr_pairlist_dfs(self, dataframe: DataFrame, dk: FreqaiDataKitchen) -> DataFrame:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Cache the corr_pairlist dfs to speed up performance for subsequent pairs during the
# REMOVED_UNUSED_CODE:         current candle.
# REMOVED_UNUSED_CODE:         :param dataframe: strategy fed dataframe
# REMOVED_UNUSED_CODE:         :param dk: datakitchen object for current asset
# REMOVED_UNUSED_CODE:         :return: dataframe to attach/extract cached corr_pair dfs to/from.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.get_corr_dataframes:
# REMOVED_UNUSED_CODE:             self.corr_dataframes = dk.extract_corr_pair_columns_from_populated_indicators(dataframe)
# REMOVED_UNUSED_CODE:             if not self.corr_dataframes:
# REMOVED_UNUSED_CODE:                 logger.warning(
# REMOVED_UNUSED_CODE:                     "Couldn't cache corr_pair dataframes for improved performance. "
# REMOVED_UNUSED_CODE:                     "Consider ensuring that the full coin/stake, e.g. XYZ/USD, "
# REMOVED_UNUSED_CODE:                     "is included in the column names when you are creating features "
# REMOVED_UNUSED_CODE:                     "in `feature_engineering_*` functions."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             self.get_corr_dataframes = not bool(self.corr_dataframes)
# REMOVED_UNUSED_CODE:         elif self.corr_dataframes:
# REMOVED_UNUSED_CODE:             dataframe = dk.attach_corr_pair_columns(dataframe, self.corr_dataframes, dk.pair)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def track_current_candle(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Checks if the latest candle appended by the datadrawer is
# REMOVED_UNUSED_CODE:         equivalent to the latest candle seen by FreqAI. If not, it
# REMOVED_UNUSED_CODE:         asks to refresh the cached corr_dfs, and resets the pair
# REMOVED_UNUSED_CODE:         counter.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if self.dd.current_candle > self.current_candle:
# REMOVED_UNUSED_CODE:             self.get_corr_dataframes = True
# REMOVED_UNUSED_CODE:             self.pair_it = 1
# REMOVED_UNUSED_CODE:             self.current_candle = self.dd.current_candle
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def ensure_data_exists(
# REMOVED_UNUSED_CODE:         self, len_dataframe_backtest: int, tr_backtest: TimeRange, pair: str
# REMOVED_UNUSED_CODE:     ) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Check if the dataframe is empty, if not, report useful information to user.
# REMOVED_UNUSED_CODE:         :param len_dataframe_backtest: the len of backtesting dataframe
# REMOVED_UNUSED_CODE:         :param tr_backtest: current backtesting timerange.
# REMOVED_UNUSED_CODE:         :param pair: current pair
# REMOVED_UNUSED_CODE:         :return: if the data exists or not
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if self.config.get("freqai_backtest_live_models", False) and len_dataframe_backtest == 0:
# REMOVED_UNUSED_CODE:             logger.info(
# REMOVED_UNUSED_CODE:                 f"No data found for pair {pair} from "
# REMOVED_UNUSED_CODE:                 f"from {tr_backtest.start_fmt} to {tr_backtest.stop_fmt}. "
# REMOVED_UNUSED_CODE:                 "Probably more than one training within the same candle period."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE:         return True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def log_backtesting_progress(
# REMOVED_UNUSED_CODE:         self, tr_train: TimeRange, pair: str, train_it: int, total_trains: int
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Log the backtesting progress so user knows how many pairs have been trained and
# REMOVED_UNUSED_CODE:         how many more pairs/trains remain.
# REMOVED_UNUSED_CODE:         :param tr_train: the training timerange
# REMOVED_UNUSED_CODE:         :param train_it: the train iteration for the current pair (the sliding window progress)
# REMOVED_UNUSED_CODE:         :param pair: the current pair
# REMOVED_UNUSED_CODE:         :param total_trains: total trains (total number of slides for the sliding window)
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if not self.config.get("freqai_backtest_live_models", False):
# REMOVED_UNUSED_CODE:             logger.info(
# REMOVED_UNUSED_CODE:                 f"Training {pair}, {self.pair_it}/{self.total_pairs} pairs"
# REMOVED_UNUSED_CODE:                 f" from {tr_train.start_fmt} "
# REMOVED_UNUSED_CODE:                 f"to {tr_train.stop_fmt}, {train_it}/{total_trains} "
# REMOVED_UNUSED_CODE:                 "trains"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def backtesting_fit_live_predictions(self, dk: FreqaiDataKitchen):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Apply fit_live_predictions function in backtesting with a dummy historic_predictions
# REMOVED_UNUSED_CODE:         The loop is required to simulate dry/live operation, as it is not possible to predict
# REMOVED_UNUSED_CODE:         the type of logic implemented by the user.
# REMOVED_UNUSED_CODE:         :param dk: datakitchen object
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         fit_live_predictions_candles = self.freqai_info.get("fit_live_predictions_candles", 0)
# REMOVED_UNUSED_CODE:         if fit_live_predictions_candles:
# REMOVED_UNUSED_CODE:             logger.info("Applying fit_live_predictions in backtesting")
# REMOVED_UNUSED_CODE:             label_columns = [
# REMOVED_UNUSED_CODE:                 col
# REMOVED_UNUSED_CODE:                 for col in dk.full_df.columns
# REMOVED_UNUSED_CODE:                 if (
# REMOVED_UNUSED_CODE:                     col.startswith("&")
# REMOVED_UNUSED_CODE:                     and not (col.startswith("&") and col.endswith("_mean"))
# REMOVED_UNUSED_CODE:                     and not (col.startswith("&") and col.endswith("_std"))
# REMOVED_UNUSED_CODE:                     and col not in self.dk.data["extra_returns_per_train"]
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             ]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             for index in range(len(dk.full_df)):
# REMOVED_UNUSED_CODE:                 if index >= fit_live_predictions_candles:
# REMOVED_UNUSED_CODE:                     self.dd.historic_predictions[self.dk.pair] = dk.full_df.iloc[
# REMOVED_UNUSED_CODE:                         index - fit_live_predictions_candles : index
# REMOVED_UNUSED_CODE:                     ]
# REMOVED_UNUSED_CODE:                     self.fit_live_predictions(self.dk, self.dk.pair)
# REMOVED_UNUSED_CODE:                     for label in label_columns:
# REMOVED_UNUSED_CODE:                         if dk.full_df[label].dtype == object:
# REMOVED_UNUSED_CODE:                             continue
# REMOVED_UNUSED_CODE:                         if "labels_mean" in self.dk.data:
# REMOVED_UNUSED_CODE:                             dk.full_df.at[index, f"{label}_mean"] = self.dk.data["labels_mean"][
# REMOVED_UNUSED_CODE:                                 label
# REMOVED_UNUSED_CODE:                             ]
# REMOVED_UNUSED_CODE:                         if "labels_std" in self.dk.data:
# REMOVED_UNUSED_CODE:                             dk.full_df.at[index, f"{label}_std"] = self.dk.data["labels_std"][label]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                     for extra_col in self.dk.data["extra_returns_per_train"]:
# REMOVED_UNUSED_CODE:                         dk.full_df.at[index, f"{extra_col}"] = self.dk.data[
# REMOVED_UNUSED_CODE:                             "extra_returns_per_train"
# REMOVED_UNUSED_CODE:                         ][extra_col]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def update_metadata(self, metadata: dict[str, Any]):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Update global metadata and save the updated json file
# REMOVED_UNUSED_CODE:         :param metadata: new global metadata dict
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self.dd.save_global_metadata_to_disk(metadata)
# REMOVED_UNUSED_CODE:         self.metadata = metadata
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def set_start_dry_live_date(self, live_dataframe: DataFrame):
# REMOVED_UNUSED_CODE:         key_name = "start_dry_live_date"
# REMOVED_UNUSED_CODE:         if key_name not in self.metadata:
# REMOVED_UNUSED_CODE:             metadata = self.metadata
# REMOVED_UNUSED_CODE:             metadata[key_name] = int(
# REMOVED_UNUSED_CODE:                 pd.to_datetime(live_dataframe.tail(1)["date"].values[0]).timestamp()
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             self.update_metadata(metadata)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def start_backtesting_from_historic_predictions(
# REMOVED_UNUSED_CODE:         self, dataframe: DataFrame, metadata: dict, dk: FreqaiDataKitchen
# REMOVED_UNUSED_CODE:     ) -> FreqaiDataKitchen:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         :param dataframe: DataFrame = strategy passed dataframe
# REMOVED_UNUSED_CODE:         :param metadata: Dict = pair metadata
# REMOVED_UNUSED_CODE:         :param dk: FreqaiDataKitchen = Data management/analysis tool associated to present pair only
# REMOVED_UNUSED_CODE:         :return:
# REMOVED_UNUSED_CODE:             FreqaiDataKitchen = Data management/analysis tool associated to present pair only
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         pair = metadata["pair"]
# REMOVED_UNUSED_CODE:         dk.return_dataframe = dataframe
# REMOVED_UNUSED_CODE:         saved_dataframe = self.dd.historic_predictions[pair]
# REMOVED_UNUSED_CODE:         columns_to_drop = list(
# REMOVED_UNUSED_CODE:             set(saved_dataframe.columns).intersection(dk.return_dataframe.columns)
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         dk.return_dataframe = dk.return_dataframe.drop(columns=list(columns_to_drop))
# REMOVED_UNUSED_CODE:         dk.return_dataframe = pd.merge(
# REMOVED_UNUSED_CODE:             dk.return_dataframe, saved_dataframe, how="left", left_on="date", right_on="date_pred"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         return dk
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Following methods which are overridden by user made prediction models.
# REMOVED_UNUSED_CODE:     # See freqai/prediction_models/CatboostPredictionModel.py for an example.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @abstractmethod
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def train(self, unfiltered_df: DataFrame, pair: str, dk: FreqaiDataKitchen, **kwargs) -> Any:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Filter the training data and train a model to it. Train makes heavy use of the datahandler
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for storing, saving, loading, and analyzing the data.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param unfiltered_df: Full dataframe for the current training period
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param metadata: pair metadata from strategy.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: Trained model which can be used to inference (self.predict)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @abstractmethod
# REMOVED_UNUSED_CODE:     def fit(self, data_dictionary: dict[str, Any], dk: FreqaiDataKitchen, **kwargs) -> Any:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Most regressors use the same function names and arguments e.g. user
# REMOVED_UNUSED_CODE:         can drop in LGBMRegressor in place of CatBoostRegressor and all data
# REMOVED_UNUSED_CODE:         management will be properly handled by Freqai.
# REMOVED_UNUSED_CODE:         :param data_dictionary: Dict = the dictionary constructed by DataHandler to hold
# REMOVED_UNUSED_CODE:                                 all the training and test data/labels.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @abstractmethod
# REMOVED_UNUSED_CODE:     def predict(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, unfiltered_df: DataFrame, dk: FreqaiDataKitchen, **kwargs
# REMOVED_UNUSED_CODE:     ) -> tuple[DataFrame, NDArray[np.int_]]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Filter the prediction features data and predict with it.
# REMOVED_UNUSED_CODE:         :param unfiltered_df: Full dataframe for the current backtest period.
# REMOVED_UNUSED_CODE:         :param dk: FreqaiDataKitchen = Data management/analysis tool associated to present pair only
# REMOVED_UNUSED_CODE:         :param first: boolean = whether this is the first prediction or not.
# REMOVED_UNUSED_CODE:         :return:
# REMOVED_UNUSED_CODE:         :predictions: np.array of predictions
# REMOVED_UNUSED_CODE:         :do_predict: np.array of 1s and 0s to indicate places where freqai needed to remove
# REMOVED_UNUSED_CODE:         data (NaNs) or felt uncertain about data (i.e. SVM and/or DI index)
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # deprecated functions
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def data_cleaning_train(self, dk: FreqaiDataKitchen, pair: str):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         throw deprecation warning if this function is called
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.warning(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"Your model {self.__class__.__name__} relies on the deprecated"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             " data pipeline. Please update your model to use the new data pipeline."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             " This can be achieved by following the migration guide at "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"{DOCS_LINK}/strategy_migration/#freqai-new-data-pipeline"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk.feature_pipeline = self.define_data_pipeline(threads=dk.thread_count)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dd = dk.data_dictionary
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         (dd["train_features"], dd["train_labels"], dd["train_weights"]) = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.feature_pipeline.fit_transform(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 dd["train_features"], dd["train_labels"], dd["train_weights"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         (dd["test_features"], dd["test_labels"], dd["test_weights"]) = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.feature_pipeline.transform(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 dd["test_features"], dd["test_labels"], dd["test_weights"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk.label_pipeline = self.define_label_pipeline(threads=dk.thread_count)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dd["train_labels"], _, _ = dk.label_pipeline.fit_transform(dd["train_labels"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dd["test_labels"], _, _ = dk.label_pipeline.transform(dd["test_labels"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def data_cleaning_predict(self, dk: FreqaiDataKitchen, pair: str):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         throw deprecation warning if this function is called
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.warning(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"Your model {self.__class__.__name__} relies on the deprecated"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             " data pipeline. Please update your model to use the new data pipeline."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             " This can be achieved by following the migration guide at "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"{DOCS_LINK}/strategy_migration/#freqai-new-data-pipeline"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dd = dk.data_dictionary
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dd["predict_features"], outliers, _ = dk.feature_pipeline.transform(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dd["predict_features"], outlier_check=True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.freqai_info.get("DI_threshold", 0) > 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.DI_values = dk.feature_pipeline["di"].di_values
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.DI_values = np.zeros(outliers.shape[0])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk.do_predict = outliers
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return
