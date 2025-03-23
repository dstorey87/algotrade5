import collections
# REMOVED_UNUSED_CODE: import importlib
import logging
# REMOVED_UNUSED_CODE: import re
# REMOVED_UNUSED_CODE: import shutil
import threading
# REMOVED_UNUSED_CODE: import warnings
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from datetime import datetime, timedelta, timezone
# REMOVED_UNUSED_CODE: from pathlib import Path
# REMOVED_UNUSED_CODE: from typing import Any, TypedDict

# REMOVED_UNUSED_CODE: import numpy as np
# REMOVED_UNUSED_CODE: import pandas as pd
# REMOVED_UNUSED_CODE: import psutil
# REMOVED_UNUSED_CODE: import rapidjson
# REMOVED_UNUSED_CODE: from joblib.externals import cloudpickle
# REMOVED_UNUSED_CODE: from numpy.typing import NDArray
# REMOVED_UNUSED_CODE: from pandas import DataFrame

# REMOVED_UNUSED_CODE: from freqtrade.configuration import TimeRange
# REMOVED_UNUSED_CODE: from freqtrade.constants import Config
# REMOVED_UNUSED_CODE: from freqtrade.data.history import load_pair_history
# REMOVED_UNUSED_CODE: from freqtrade.enums import CandleType
# REMOVED_UNUSED_CODE: from freqtrade.exceptions import OperationalException
# REMOVED_UNUSED_CODE: from freqtrade.freqai.data_kitchen import FreqaiDataKitchen
# REMOVED_UNUSED_CODE: from freqtrade.strategy.interface import IStrategy


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)

# REMOVED_UNUSED_CODE: FEATURE_PIPELINE = "feature_pipeline"
# REMOVED_UNUSED_CODE: LABEL_PIPELINE = "label_pipeline"
# REMOVED_UNUSED_CODE: TRAINDF = "trained_df"
# REMOVED_UNUSED_CODE: METADATA = "metadata"


# REMOVED_UNUSED_CODE: class pair_info(TypedDict):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     model_filename: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     trained_timestamp: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     data_path: str
# REMOVED_UNUSED_CODE:     extras: dict


# REMOVED_UNUSED_CODE: class FreqaiDataDrawer:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Class aimed at holding all pair models/info in memory for better inferencing/retrainig/saving
# REMOVED_UNUSED_CODE:     /loading to/from disk.
# REMOVED_UNUSED_CODE:     This object remains persistent throughout live/dry.
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
# REMOVED_UNUSED_CODE:     def __init__(self, full_path: Path, config: Config):
# REMOVED_UNUSED_CODE:         self.config = config
# REMOVED_UNUSED_CODE:         self.freqai_info = config.get("freqai", {})
# REMOVED_UNUSED_CODE:         # dictionary holding all pair metadata necessary to load in from disk
# REMOVED_UNUSED_CODE:         self.pair_dict: dict[str, pair_info] = {}
# REMOVED_UNUSED_CODE:         # dictionary holding all actively inferenced models in memory given a model filename
# REMOVED_UNUSED_CODE:         self.model_dictionary: dict[str, Any] = {}
# REMOVED_UNUSED_CODE:         # all additional metadata that we want to keep in ram
# REMOVED_UNUSED_CODE:         self.meta_data_dictionary: dict[str, dict[str, Any]] = {}
# REMOVED_UNUSED_CODE:         self.model_return_values: dict[str, DataFrame] = {}
# REMOVED_UNUSED_CODE:         self.historic_data: dict[str, dict[str, DataFrame]] = {}
# REMOVED_UNUSED_CODE:         self.historic_predictions: dict[str, DataFrame] = {}
# REMOVED_UNUSED_CODE:         self.full_path = full_path
# REMOVED_UNUSED_CODE:         self.historic_predictions_path = Path(self.full_path / "historic_predictions.pkl")
# REMOVED_UNUSED_CODE:         self.historic_predictions_bkp_path = Path(
# REMOVED_UNUSED_CODE:             self.full_path / "historic_predictions.backup.pkl"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         self.pair_dictionary_path = Path(self.full_path / "pair_dictionary.json")
# REMOVED_UNUSED_CODE:         self.global_metadata_path = Path(self.full_path / "global_metadata.json")
# REMOVED_UNUSED_CODE:         self.metric_tracker_path = Path(self.full_path / "metric_tracker.json")
# REMOVED_UNUSED_CODE:         self.load_drawer_from_disk()
# REMOVED_UNUSED_CODE:         self.load_historic_predictions_from_disk()
# REMOVED_UNUSED_CODE:         self.metric_tracker: dict[str, dict[str, dict[str, list]]] = {}
# REMOVED_UNUSED_CODE:         self.load_metric_tracker_from_disk()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.training_queue: dict[str, int] = {}
# REMOVED_UNUSED_CODE:         self.history_lock = threading.Lock()
# REMOVED_UNUSED_CODE:         self.save_lock = threading.Lock()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.pair_dict_lock = threading.Lock()
# REMOVED_UNUSED_CODE:         self.metric_tracker_lock = threading.Lock()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.old_DBSCAN_eps: dict[str, float] = {}
# REMOVED_UNUSED_CODE:         self.empty_pair_dict: pair_info = {
# REMOVED_UNUSED_CODE:             "model_filename": "",
# REMOVED_UNUSED_CODE:             "trained_timestamp": 0,
# REMOVED_UNUSED_CODE:             "data_path": "",
# REMOVED_UNUSED_CODE:             "extras": {},
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE:         self.model_type = self.freqai_info.get("model_save_type", "joblib")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def update_metric_tracker(self, metric: str, value: float, pair: str) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         General utility for adding and updating custom metrics. Typically used
# REMOVED_UNUSED_CODE:         for adding training performance, train timings, inferenc timings, cpu loads etc.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         with self.metric_tracker_lock:
# REMOVED_UNUSED_CODE:             if pair not in self.metric_tracker:
# REMOVED_UNUSED_CODE:                 self.metric_tracker[pair] = {}
# REMOVED_UNUSED_CODE:             if metric not in self.metric_tracker[pair]:
# REMOVED_UNUSED_CODE:                 self.metric_tracker[pair][metric] = {"timestamp": [], "value": []}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             timestamp = int(datetime.now(timezone.utc).timestamp())
# REMOVED_UNUSED_CODE:             self.metric_tracker[pair][metric]["value"].append(value)
# REMOVED_UNUSED_CODE:             self.metric_tracker[pair][metric]["timestamp"].append(timestamp)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def collect_metrics(self, time_spent: float, pair: str):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Add metrics to the metric tracker dictionary
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         load1, load5, load15 = psutil.getloadavg()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         cpus = psutil.cpu_count()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.update_metric_tracker("train_time", time_spent, pair)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.update_metric_tracker("cpu_load1min", load1 / cpus, pair)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.update_metric_tracker("cpu_load5min", load5 / cpus, pair)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.update_metric_tracker("cpu_load15min", load15 / cpus, pair)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def load_global_metadata_from_disk(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Locate and load a previously saved global metadata in present model folder.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         exists = self.global_metadata_path.is_file()
# REMOVED_UNUSED_CODE:         if exists:
# REMOVED_UNUSED_CODE:             with self.global_metadata_path.open("r") as fp:
# REMOVED_UNUSED_CODE:                 metatada_dict = rapidjson.load(fp, number_mode=rapidjson.NM_NATIVE)
# REMOVED_UNUSED_CODE:                 return metatada_dict
# REMOVED_UNUSED_CODE:         return {}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def load_drawer_from_disk(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Locate and load a previously saved data drawer full of all pair model metadata in
# REMOVED_UNUSED_CODE:         present model folder.
# REMOVED_UNUSED_CODE:         Load any existing metric tracker that may be present.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         exists = self.pair_dictionary_path.is_file()
# REMOVED_UNUSED_CODE:         if exists:
# REMOVED_UNUSED_CODE:             with self.pair_dictionary_path.open("r") as fp:
# REMOVED_UNUSED_CODE:                 self.pair_dict = rapidjson.load(fp, number_mode=rapidjson.NM_NATIVE)
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             logger.info("Could not find existing datadrawer, starting from scratch")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def load_metric_tracker_from_disk(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Tries to load an existing metrics dictionary if the user
# REMOVED_UNUSED_CODE:         wants to collect metrics.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if self.freqai_info.get("write_metrics_to_disk", False):
# REMOVED_UNUSED_CODE:             exists = self.metric_tracker_path.is_file()
# REMOVED_UNUSED_CODE:             if exists:
# REMOVED_UNUSED_CODE:                 with self.metric_tracker_path.open("r") as fp:
# REMOVED_UNUSED_CODE:                     self.metric_tracker = rapidjson.load(fp, number_mode=rapidjson.NM_NATIVE)
# REMOVED_UNUSED_CODE:                 logger.info("Loading existing metric tracker from disk.")
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 logger.info("Could not find existing metric tracker, starting from scratch")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def load_historic_predictions_from_disk(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Locate and load a previously saved historic predictions.
# REMOVED_UNUSED_CODE:         :return: bool - whether or not the drawer was located
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         exists = self.historic_predictions_path.is_file()
# REMOVED_UNUSED_CODE:         if exists:
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 with self.historic_predictions_path.open("rb") as fp:
# REMOVED_UNUSED_CODE:                     self.historic_predictions = cloudpickle.load(fp)
# REMOVED_UNUSED_CODE:                 logger.info(
# REMOVED_UNUSED_CODE:                     f"Found existing historic predictions at {self.full_path}, but beware "
# REMOVED_UNUSED_CODE:                     "that statistics may be inaccurate if the bot has been offline for "
# REMOVED_UNUSED_CODE:                     "an extended period of time."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             except EOFError:
# REMOVED_UNUSED_CODE:                 logger.warning(
# REMOVED_UNUSED_CODE:                     "Historical prediction file was corrupted. Trying to load backup file."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 with self.historic_predictions_bkp_path.open("rb") as fp:
# REMOVED_UNUSED_CODE:                     self.historic_predictions = cloudpickle.load(fp)
# REMOVED_UNUSED_CODE:                 logger.warning("FreqAI successfully loaded the backup historical predictions file.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             logger.info("Could not find existing historic_predictions, starting from scratch")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return exists
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def save_historic_predictions_to_disk(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Save historic predictions pickle to disk
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         with self.historic_predictions_path.open("wb") as fp:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             cloudpickle.dump(self.historic_predictions, fp, protocol=cloudpickle.DEFAULT_PROTOCOL)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # create a backup
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         shutil.copy(self.historic_predictions_path, self.historic_predictions_bkp_path)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def save_metric_tracker_to_disk(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Save metric tracker of all pair metrics collected.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         with self.save_lock:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             with self.metric_tracker_path.open("w") as fp:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 rapidjson.dump(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     self.metric_tracker,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     fp,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     default=self.np_encoder,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     number_mode=rapidjson.NM_NATIVE,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def save_drawer_to_disk(self) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Save data drawer full of all pair model metadata in present model folder.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         with self.save_lock:
# REMOVED_UNUSED_CODE:             with self.pair_dictionary_path.open("w") as fp:
# REMOVED_UNUSED_CODE:                 rapidjson.dump(
# REMOVED_UNUSED_CODE:                     self.pair_dict, fp, default=self.np_encoder, number_mode=rapidjson.NM_NATIVE
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def save_global_metadata_to_disk(self, metadata: dict[str, Any]):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Save global metadata json to disk
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         with self.save_lock:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             with self.global_metadata_path.open("w") as fp:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 rapidjson.dump(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     metadata, fp, default=self.np_encoder, number_mode=rapidjson.NM_NATIVE
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def np_encoder(self, obj):
# REMOVED_UNUSED_CODE:         if isinstance(obj, np.generic):
# REMOVED_UNUSED_CODE:             return obj.item()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_pair_dict_info(self, pair: str) -> tuple[str, int]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Locate and load existing model metadata from persistent storage. If not located,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         create a new one and append the current pair to it and prepare it for its first
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         training
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pair: str: pair to lookup
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             model_filename: str = unique filename used for loading persistent objects from disk
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trained_timestamp: int = the last time the coin was trained
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair_dict = self.pair_dict.get(pair)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if pair_dict:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             model_filename = pair_dict["model_filename"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trained_timestamp = pair_dict["trained_timestamp"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.pair_dict[pair] = self.empty_pair_dict.copy()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             model_filename = ""
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trained_timestamp = 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return model_filename, trained_timestamp
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def set_pair_dict_info(self, metadata: dict) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair_in_dict = self.pair_dict.get(metadata["pair"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if pair_in_dict:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.pair_dict[metadata["pair"]] = self.empty_pair_dict.copy()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def set_initial_return_values(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, pair: str, pred_df: DataFrame, dataframe: DataFrame
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Set the initial return values to the historical predictions dataframe. This avoids needing
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         to repredict on historical candles, and also stores historical predictions despite
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         retrainings (so stored predictions are true predictions, not just inferencing on trained
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         data).
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         We also aim to keep the date from historical predictions so that the FreqUI displays
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         zeros during any downtime (between FreqAI reloads).
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         new_pred = pred_df.copy()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # set new_pred values to nans (we want to signal to user that there was nothing
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # historically made during downtime. The newest pred will get appended later in
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # append_model_predictions)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         new_pred["date_pred"] = dataframe["date"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # set everything to nan except date_pred
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         columns_to_nan = new_pred.columns.difference(["date_pred", "date"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         new_pred[columns_to_nan] = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         hist_preds = self.historic_predictions[pair].copy()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # ensure both dataframes have the same date format so they can be merged
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         new_pred["date_pred"] = pd.to_datetime(new_pred["date_pred"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         hist_preds["date_pred"] = pd.to_datetime(hist_preds["date_pred"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # find the closest common date between new_pred and historic predictions
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # and cut off the new_pred dataframe at that date
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         common_dates = pd.merge(new_pred, hist_preds, on="date_pred", how="inner")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if len(common_dates.index) > 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             new_pred = new_pred.iloc[len(common_dates) :]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             logger.warning(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "No common dates found between new predictions and historic "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "predictions. You likely left your FreqAI instance offline "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"for more than {len(dataframe.index)} candles."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Pandas warns that its keeping dtypes of non NaN columns...
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # yea we know and we already want that behavior. Ignoring.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         with warnings.catch_warnings():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             warnings.filterwarnings("ignore", category=FutureWarning)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # reindex new_pred columns to match the historic predictions dataframe
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             new_pred_reindexed = new_pred.reindex(columns=hist_preds.columns)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             df_concat = pd.concat([hist_preds, new_pred_reindexed], ignore_index=True)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # any missing values will get zeroed out so users can see the exact
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # downtime in FreqUI
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         df_concat = df_concat.fillna(0)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.historic_predictions[pair] = df_concat
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.model_return_values[pair] = df_concat.tail(len(dataframe.index)).reset_index(drop=True)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def append_model_predictions(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         predictions: DataFrame,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         do_preds: NDArray[np.int_],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk: FreqaiDataKitchen,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         strat_df: DataFrame,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Append model predictions to historic predictions dataframe, then set the
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         strategy return dataframe to the tail of the historic predictions. The length of
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         the tail is equivalent to the length of the dataframe that entered FreqAI from
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         the strategy originally. Doing this allows FreqUI to always display the correct
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         historic predictions.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         len_df = len(strat_df)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         index = self.historic_predictions[pair].index[-1:]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         columns = self.historic_predictions[pair].columns
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         zeros_df = pd.DataFrame(np.zeros((1, len(columns))), index=index, columns=columns)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.historic_predictions[pair] = pd.concat(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             [self.historic_predictions[pair], zeros_df], ignore_index=True, axis=0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         df = self.historic_predictions[pair]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # model outputs and associated statistics
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for label in predictions.columns:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             label_loc = df.columns.get_loc(label)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             pred_label_loc = predictions.columns.get_loc(label)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             df.iloc[-1, label_loc] = predictions.iloc[-1, pred_label_loc]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if df[label].dtype == object:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             label_mean_loc = df.columns.get_loc(f"{label}_mean")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             label_std_loc = df.columns.get_loc(f"{label}_std")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             df.iloc[-1, label_mean_loc] = dk.data["labels_mean"][label]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             df.iloc[-1, label_std_loc] = dk.data["labels_std"][label]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # outlier indicators
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         do_predict_loc = df.columns.get_loc("do_predict")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         df.iloc[-1, do_predict_loc] = do_preds[-1]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.freqai_info["feature_parameters"].get("DI_threshold", 0) > 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             DI_values_loc = df.columns.get_loc("DI_values")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             df.iloc[-1, DI_values_loc] = dk.DI_values[-1]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # extra values the user added within custom prediction model
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if dk.data["extra_returns_per_train"]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             rets = dk.data["extra_returns_per_train"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for return_str in rets:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return_loc = df.columns.get_loc(return_str)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 df.iloc[-1, return_loc] = rets[return_str]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         high_price_loc = df.columns.get_loc("high_price")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         high_loc = strat_df.columns.get_loc("high")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         df.iloc[-1, high_price_loc] = strat_df.iloc[-1, high_loc]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         low_price_loc = df.columns.get_loc("low_price")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         low_loc = strat_df.columns.get_loc("low")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         df.iloc[-1, low_price_loc] = strat_df.iloc[-1, low_loc]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         close_price_loc = df.columns.get_loc("close_price")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         close_loc = strat_df.columns.get_loc("close")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         df.iloc[-1, close_price_loc] = strat_df.iloc[-1, close_loc]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         date_pred_loc = df.columns.get_loc("date_pred")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         date_loc = strat_df.columns.get_loc("date")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         df.iloc[-1, date_pred_loc] = strat_df.iloc[-1, date_loc]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.model_return_values[pair] = df.tail(len_df).reset_index(drop=True)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def attach_return_values_to_return_dataframe(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, pair: str, dataframe: DataFrame
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Attach the return values to the strat dataframe
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param dataframe: DataFrame = strategy dataframe
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: DataFrame = strat dataframe with return values attached
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         df = self.model_return_values[pair]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         to_keep = [col for col in dataframe.columns if not col.startswith("&")]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe = pd.concat([dataframe[to_keep], df], axis=1)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def return_null_values_to_strategy(self, dataframe: DataFrame, dk: FreqaiDataKitchen) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Build 0 filled dataframe to return to strategy
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk.find_features(dataframe)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk.find_labels(dataframe)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         full_labels = dk.label_list + dk.unique_class_list
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for label in full_labels:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dataframe[label] = 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dataframe[f"{label}_mean"] = 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dataframe[f"{label}_std"] = 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["do_predict"] = 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.freqai_info["feature_parameters"].get("DI_threshold", 0) > 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dataframe["DI_values"] = 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if dk.data["extra_returns_per_train"]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             rets = dk.data["extra_returns_per_train"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for return_str in rets:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 dataframe[return_str] = 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk.return_dataframe = dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def purge_old_models(self) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         num_keep = self.freqai_info["purge_old_models"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not num_keep:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         elif isinstance(num_keep, bool):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             num_keep = 2
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         model_folders = [x for x in self.full_path.iterdir() if x.is_dir()]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pattern = re.compile(r"sub-train-(\w+)_(\d{10})")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         delete_dict: dict[str, Any] = {}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for directory in model_folders:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             result = pattern.match(str(directory.name))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if result is None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             coin = result.group(1)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             timestamp = result.group(2)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if coin not in delete_dict:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 delete_dict[coin] = {}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 delete_dict[coin]["num_folders"] = 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 delete_dict[coin]["timestamps"] = {int(timestamp): directory}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 delete_dict[coin]["num_folders"] += 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 delete_dict[coin]["timestamps"][int(timestamp)] = directory
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for coin in delete_dict:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if delete_dict[coin]["num_folders"] > num_keep:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 sorted_dict = collections.OrderedDict(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     sorted(delete_dict[coin]["timestamps"].items())
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 num_delete = len(sorted_dict) - num_keep
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 deleted = 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 for k, v in sorted_dict.items():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     if deleted >= num_delete:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         break
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     logger.info(f"Freqai purging old model file {v}")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     shutil.rmtree(v)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     deleted += 1
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def save_metadata(self, dk: FreqaiDataKitchen) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Saves only metadata for backtesting studies if user prefers
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         not to save model data. This saves tremendous amounts of space
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for users generating huge studies.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         This is only active when `save_backtest_models`: false (not default)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not dk.data_path.is_dir():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.data_path.mkdir(parents=True, exist_ok=True)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         save_path = Path(dk.data_path)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk.data["data_path"] = str(dk.data_path)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk.data["model_filename"] = str(dk.model_filename)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk.data["training_features_list"] = list(dk.data_dictionary["train_features"].columns)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk.data["label_list"] = dk.label_list
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         with (save_path / f"{dk.model_filename}_{METADATA}.json").open("w") as fp:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             rapidjson.dump(dk.data, fp, default=self.np_encoder, number_mode=rapidjson.NM_NATIVE)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def save_data(self, model: Any, coin: str, dk: FreqaiDataKitchen) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Saves all data associated with a model for a single sub-train time range
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param model: User trained model which can be reused for inferencing to generate
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                       predictions
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not dk.data_path.is_dir():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.data_path.mkdir(parents=True, exist_ok=True)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         save_path = Path(dk.data_path)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Save the trained model
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.model_type == "joblib":
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             with (save_path / f"{dk.model_filename}_model.joblib").open("wb") as fp:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 cloudpickle.dump(model, fp)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         elif self.model_type == "keras":
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             model.save(save_path / f"{dk.model_filename}_model.h5")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         elif self.model_type in ["stable_baselines3", "sb3_contrib", "pytorch"]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             model.save(save_path / f"{dk.model_filename}_model.zip")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk.data["data_path"] = str(dk.data_path)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk.data["model_filename"] = str(dk.model_filename)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk.data["training_features_list"] = dk.training_features_list
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk.data["label_list"] = dk.label_list
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # store the metadata
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         with (save_path / f"{dk.model_filename}_{METADATA}.json").open("w") as fp:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             rapidjson.dump(dk.data, fp, default=self.np_encoder, number_mode=rapidjson.NM_NATIVE)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # save the pipelines to pickle files
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         with (save_path / f"{dk.model_filename}_{FEATURE_PIPELINE}.pkl").open("wb") as fp:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             cloudpickle.dump(dk.feature_pipeline, fp)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         with (save_path / f"{dk.model_filename}_{LABEL_PIPELINE}.pkl").open("wb") as fp:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             cloudpickle.dump(dk.label_pipeline, fp)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # save the train data to file for post processing if desired
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk.data_dictionary["train_features"].to_pickle(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             save_path / f"{dk.model_filename}_{TRAINDF}.pkl"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk.data_dictionary["train_dates"].to_pickle(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             save_path / f"{dk.model_filename}_trained_dates_df.pkl"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.model_dictionary[coin] = model
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.pair_dict[coin]["model_filename"] = dk.model_filename
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.pair_dict[coin]["data_path"] = str(dk.data_path)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if coin not in self.meta_data_dictionary:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.meta_data_dictionary[coin] = {}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.meta_data_dictionary[coin][METADATA] = dk.data
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.meta_data_dictionary[coin][FEATURE_PIPELINE] = dk.feature_pipeline
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.meta_data_dictionary[coin][LABEL_PIPELINE] = dk.label_pipeline
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.save_drawer_to_disk()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def load_metadata(self, dk: FreqaiDataKitchen) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Load only metadata into datakitchen to increase performance during
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         presaved backtesting (prediction file loading).
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         with (dk.data_path / f"{dk.model_filename}_{METADATA}.json").open("r") as fp:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.data = rapidjson.load(fp, number_mode=rapidjson.NM_NATIVE)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.training_features_list = dk.data["training_features_list"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.label_list = dk.data["label_list"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def load_data(self, coin: str, dk: FreqaiDataKitchen) -> Any:  # noqa: C901
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         loads all data required to make a prediction on a sub-train time range
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :returns:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :model: User trained model which can be inferenced for new predictions
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not self.pair_dict[coin]["model_filename"]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if dk.live:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.model_filename = self.pair_dict[coin]["model_filename"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.data_path = Path(self.pair_dict[coin]["data_path"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if coin in self.meta_data_dictionary:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.data = self.meta_data_dictionary[coin][METADATA]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.feature_pipeline = self.meta_data_dictionary[coin][FEATURE_PIPELINE]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.label_pipeline = self.meta_data_dictionary[coin][LABEL_PIPELINE]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             with (dk.data_path / f"{dk.model_filename}_{METADATA}.json").open("r") as fp:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 dk.data = rapidjson.load(fp, number_mode=rapidjson.NM_NATIVE)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             with (dk.data_path / f"{dk.model_filename}_{FEATURE_PIPELINE}.pkl").open("rb") as fp:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 dk.feature_pipeline = cloudpickle.load(fp)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             with (dk.data_path / f"{dk.model_filename}_{LABEL_PIPELINE}.pkl").open("rb") as fp:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 dk.label_pipeline = cloudpickle.load(fp)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk.training_features_list = dk.data["training_features_list"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk.label_list = dk.data["label_list"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # try to access model in memory instead of loading object from disk to save time
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if dk.live and coin in self.model_dictionary:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             model = self.model_dictionary[coin]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         elif self.model_type == "joblib":
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             with (dk.data_path / f"{dk.model_filename}_model.joblib").open("rb") as fp:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 model = cloudpickle.load(fp)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         elif "stable_baselines" in self.model_type or "sb3_contrib" == self.model_type:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             mod = importlib.import_module(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.model_type, self.freqai_info["rl_config"]["model_type"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             MODELCLASS = getattr(mod, self.freqai_info["rl_config"]["model_type"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             model = MODELCLASS.load(dk.data_path / f"{dk.model_filename}_model")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         elif self.model_type == "pytorch":
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             import torch
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             zipfile = torch.load(dk.data_path / f"{dk.model_filename}_model.zip")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             model = zipfile["pytrainer"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             model = model.load_from_checkpoint(zipfile)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not model:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"Unable to load model, ensure model exists at {dk.data_path} "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # load it into ram if it was loaded from disk
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if coin not in self.model_dictionary:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.model_dictionary[coin] = model
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return model
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def update_historic_data(self, strategy: IStrategy, dk: FreqaiDataKitchen) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Append new candles to our stores historic data (in memory) so that
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         we do not need to load candle history from disk and we dont need to
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pinging exchange multiple times for the same candle.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param dataframe: DataFrame = strategy provided dataframe
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         feat_params = self.freqai_info["feature_parameters"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         with self.history_lock:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             history_data = self.historic_data
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for pair in dk.all_pairs:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 for tf in feat_params.get("include_timeframes"):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     hist_df = history_data[pair][tf]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     # check if newest candle is already appended
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     df_dp = strategy.dp.get_pair_dataframe(pair, tf)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     if len(df_dp.index) == 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         continue
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     if str(hist_df.iloc[-1]["date"]) == str(df_dp.iloc[-1:]["date"].iloc[-1]):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         continue
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     try:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         index = df_dp.loc[df_dp["date"] == hist_df.iloc[-1]["date"]].index[0] + 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     except IndexError:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         if hist_df.iloc[-1]["date"] < df_dp["date"].iloc[0]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                             raise OperationalException(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                                 "In memory historical data is older than "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                                 f"oldest DataProvider candle for {pair} on "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                                 f"timeframe {tf}"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                             index = -1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                             logger.warning(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                                 f"No common dates in historical data and dataprovider for {pair}. "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                                 f"Appending latest dataprovider candle to historical data "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                                 "but please be aware that there is likely a gap in the historical "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                                 "data. \n"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                                 f"Historical data ends at {hist_df.iloc[-1]['date']} "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                                 f"while dataprovider starts at {df_dp['date'].iloc[0]} and"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                                 f"ends at {df_dp['date'].iloc[0]}."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     history_data[pair][tf] = pd.concat(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         [
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                             hist_df,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                             df_dp.iloc[index:],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         ],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         ignore_index=True,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         axis=0,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.current_candle = history_data[dk.pair][self.config["timeframe"]].iloc[-1]["date"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def load_all_pair_histories(self, timerange: TimeRange, dk: FreqaiDataKitchen) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Load pair histories for all whitelist and corr_pairlist pairs.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Only called once upon startup of bot.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param timerange: TimeRange = full timerange required to populate all indicators
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                           for training according to user defined train_period_days
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         history_data = self.historic_data
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for pair in dk.all_pairs:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if pair not in history_data:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 history_data[pair] = {}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for tf in self.freqai_info["feature_parameters"].get("include_timeframes"):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 history_data[pair][tf] = load_pair_history(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     datadir=self.config["datadir"],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     timeframe=tf,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     pair=pair,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     timerange=timerange,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     data_format=self.config.get("dataformat_ohlcv", "feather"),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     candle_type=self.config.get("candle_type_def", CandleType.SPOT),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_base_and_corr_dataframes(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, timerange: TimeRange, pair: str, dk: FreqaiDataKitchen
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> tuple[dict[Any, Any], dict[Any, Any]]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Searches through our historic_data in memory and returns the dataframes relevant
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         to the present pair.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param timerange: TimeRange = full timerange required to populate all indicators
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                           for training according to user defined train_period_days
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param metadata: dict = strategy furnished pair metadata
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         with self.history_lock:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             corr_dataframes: dict[Any, Any] = {}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             base_dataframes: dict[Any, Any] = {}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             historic_data = self.historic_data
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             pairs = self.freqai_info["feature_parameters"].get("include_corr_pairlist", [])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for tf in self.freqai_info["feature_parameters"].get("include_timeframes"):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 base_dataframes[tf] = dk.slice_dataframe(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     timerange, historic_data[pair][tf]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 ).reset_index(drop=True)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if pairs:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     for p in pairs:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         if pair in p:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                             continue  # dont repeat anything from whitelist
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         if p not in corr_dataframes:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                             corr_dataframes[p] = {}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         corr_dataframes[p][tf] = dk.slice_dataframe(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                             timerange, historic_data[p][tf]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         ).reset_index(drop=True)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return corr_dataframes, base_dataframes
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_timerange_from_live_historic_predictions(self) -> TimeRange:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Returns timerange information based on historic predictions file
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: timerange calculated from saved live data
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not self.historic_predictions_path.is_file():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "Historic predictions not found. Historic predictions data is required "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "to run backtest with the freqai-backtest-live-models option "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.load_historic_predictions_from_disk()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         all_pairs_end_dates = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for pair in self.historic_predictions:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             pair_historic_data = self.historic_predictions[pair]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             all_pairs_end_dates.append(pair_historic_data.date_pred.max())
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         global_metadata = self.load_global_metadata_from_disk()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         start_date = datetime.fromtimestamp(int(global_metadata["start_dry_live_date"]))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         end_date = max(all_pairs_end_dates)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # add 1 day to string timerange to ensure BT module will load all dataframe data
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         end_date = end_date + timedelta(days=1)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         backtesting_timerange = TimeRange(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "date", "date", int(start_date.timestamp()), int(end_date.timestamp())
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return backtesting_timerange
