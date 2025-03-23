# REMOVED_UNUSED_CODE: import copy
# REMOVED_UNUSED_CODE: import inspect
import logging
# REMOVED_UNUSED_CODE: import random
# REMOVED_UNUSED_CODE: import shutil
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from datetime import datetime, timezone
# REMOVED_UNUSED_CODE: from pathlib import Path
# REMOVED_UNUSED_CODE: from typing import Any

# REMOVED_UNUSED_CODE: import numpy as np
# REMOVED_UNUSED_CODE: import numpy.typing as npt
import pandas as pd
# REMOVED_UNUSED_CODE: import psutil
# REMOVED_UNUSED_CODE: from datasieve.pipeline import Pipeline
# REMOVED_UNUSED_CODE: from pandas import DataFrame
from sklearn.model_selection import train_test_split

# REMOVED_UNUSED_CODE: from freqtrade.configuration import TimeRange
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.constants import DOCS_LINK, Config
# REMOVED_UNUSED_CODE: from freqtrade.data.converter import reduce_dataframe_footprint
# REMOVED_UNUSED_CODE: from freqtrade.exceptions import OperationalException
# REMOVED_UNUSED_CODE: from freqtrade.exchange import timeframe_to_seconds
# REMOVED_UNUSED_CODE: from freqtrade.strategy import merge_informative_pair
# REMOVED_UNUSED_CODE: from freqtrade.strategy.interface import IStrategy


pd.set_option("future.no_silent_downcasting", True)

# REMOVED_UNUSED_CODE: SECONDS_IN_DAY = 86400
# REMOVED_UNUSED_CODE: SECONDS_IN_HOUR = 3600

# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class FreqaiDataKitchen:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Class designed to analyze data for a single pair. Employed by the IFreqaiModel class.
# REMOVED_UNUSED_CODE:     Functionalities include holding, saving, loading, and analyzing the data.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     This object is not persistent, it is reinstantiated for each coin, each time the coin
# REMOVED_UNUSED_CODE:     model needs to be inferenced or trained.
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
# REMOVED_UNUSED_CODE:     def __init__(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         config: Config,
# REMOVED_UNUSED_CODE:         live: bool = False,
# REMOVED_UNUSED_CODE:         pair: str = "",
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         self.data: dict[str, Any] = {}
# REMOVED_UNUSED_CODE:         self.data_dictionary: dict[str, DataFrame] = {}
# REMOVED_UNUSED_CODE:         self.config = config
# REMOVED_UNUSED_CODE:         self.freqai_config: dict[str, Any] = config["freqai"]
# REMOVED_UNUSED_CODE:         self.full_df: DataFrame = DataFrame()
# REMOVED_UNUSED_CODE:         self.append_df: DataFrame = DataFrame()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.data_path = Path()
# REMOVED_UNUSED_CODE:         self.label_list: list = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.training_features_list: list = []
# REMOVED_UNUSED_CODE:         self.model_filename: str = ""
# REMOVED_UNUSED_CODE:         self.backtesting_results_path = Path()
# REMOVED_UNUSED_CODE:         self.backtest_predictions_folder: str = "backtesting_predictions"
# REMOVED_UNUSED_CODE:         self.live = live
# REMOVED_UNUSED_CODE:         self.pair = pair
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.keras: bool = self.freqai_config.get("keras", False)
# REMOVED_UNUSED_CODE:         self.set_all_pairs()
# REMOVED_UNUSED_CODE:         self.backtest_live_models = config.get("freqai_backtest_live_models", False)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.feature_pipeline = Pipeline()
# REMOVED_UNUSED_CODE:         self.label_pipeline = Pipeline()
# REMOVED_UNUSED_CODE:         self.DI_values: npt.NDArray = np.array([])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not self.live:
# REMOVED_UNUSED_CODE:             self.full_path = self.get_full_models_path(self.config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if not self.backtest_live_models:
# REMOVED_UNUSED_CODE:                 self.full_timerange = self.create_fulltimerange(
# REMOVED_UNUSED_CODE:                     self.config["timerange"], self.freqai_config.get("train_period_days", 0)
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 (self.training_timeranges, self.backtesting_timeranges) = self.split_timerange(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     self.full_timerange,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     config["freqai"]["train_period_days"],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     config["freqai"]["backtest_period_days"],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.data["extra_returns_per_train"] = self.freqai_config.get("extra_returns_per_train", {})
# REMOVED_UNUSED_CODE:         if not self.freqai_config.get("data_kitchen_thread_count", 0):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.thread_count = max(int(psutil.cpu_count() * 2 - 2), 1)
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.thread_count = self.freqai_config["data_kitchen_thread_count"]
# REMOVED_UNUSED_CODE:         self.train_dates: DataFrame = pd.DataFrame()
# REMOVED_UNUSED_CODE:         self.unique_classes: dict[str, list] = {}
# REMOVED_UNUSED_CODE:         self.unique_class_list: list = []
# REMOVED_UNUSED_CODE:         self.backtest_live_models_data: dict[str, Any] = {}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def set_paths(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trained_timestamp: int | None = None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Set the paths to the data for the present coin/botloop
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param metadata: dict = strategy furnished pair metadata
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param trained_timestamp: int = timestamp of most recent training
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.full_path = self.get_full_models_path(self.config)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.data_path = Path(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.full_path / f"sub-train-{pair.split('/')[0]}_{trained_timestamp}"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def make_train_test_datasets(
# REMOVED_UNUSED_CODE:         self, filtered_dataframe: DataFrame, labels: DataFrame
# REMOVED_UNUSED_CODE:     ) -> dict[Any, Any]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Given the dataframe for the full history for training, split the data into
# REMOVED_UNUSED_CODE:         training and test data according to user specified parameters in configuration
# REMOVED_UNUSED_CODE:         file.
# REMOVED_UNUSED_CODE:         :param filtered_dataframe: cleaned dataframe ready to be split.
# REMOVED_UNUSED_CODE:         :param labels: cleaned labels ready to be split.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         feat_dict = self.freqai_config["feature_parameters"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if "shuffle" not in self.freqai_config["data_split_parameters"]:
# REMOVED_UNUSED_CODE:             self.freqai_config["data_split_parameters"].update({"shuffle": False})
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         weights: npt.ArrayLike
# REMOVED_UNUSED_CODE:         if feat_dict.get("weight_factor", 0) > 0:
# REMOVED_UNUSED_CODE:             weights = self.set_weights_higher_recent(len(filtered_dataframe))
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             weights = np.ones(len(filtered_dataframe))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.freqai_config.get("data_split_parameters", {}).get("test_size", 0.1) != 0:
# REMOVED_UNUSED_CODE:             (
# REMOVED_UNUSED_CODE:                 train_features,
# REMOVED_UNUSED_CODE:                 test_features,
# REMOVED_UNUSED_CODE:                 train_labels,
# REMOVED_UNUSED_CODE:                 test_labels,
# REMOVED_UNUSED_CODE:                 train_weights,
# REMOVED_UNUSED_CODE:                 test_weights,
# REMOVED_UNUSED_CODE:             ) = train_test_split(
# REMOVED_UNUSED_CODE:                 filtered_dataframe[: filtered_dataframe.shape[0]],
# REMOVED_UNUSED_CODE:                 labels,
# REMOVED_UNUSED_CODE:                 weights,
# REMOVED_UNUSED_CODE:                 **self.config["freqai"]["data_split_parameters"],
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             test_labels = np.zeros(2)
# REMOVED_UNUSED_CODE:             test_features = pd.DataFrame()
# REMOVED_UNUSED_CODE:             test_weights = np.zeros(2)
# REMOVED_UNUSED_CODE:             train_features = filtered_dataframe
# REMOVED_UNUSED_CODE:             train_labels = labels
# REMOVED_UNUSED_CODE:             train_weights = weights
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if feat_dict["shuffle_after_split"]:
# REMOVED_UNUSED_CODE:             rint1 = random.randint(0, 100)
# REMOVED_UNUSED_CODE:             rint2 = random.randint(0, 100)
# REMOVED_UNUSED_CODE:             train_features = train_features.sample(frac=1, random_state=rint1).reset_index(
# REMOVED_UNUSED_CODE:                 drop=True
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             train_labels = train_labels.sample(frac=1, random_state=rint1).reset_index(drop=True)
# REMOVED_UNUSED_CODE:             train_weights = (
# REMOVED_UNUSED_CODE:                 pd.DataFrame(train_weights)
# REMOVED_UNUSED_CODE:                 .sample(frac=1, random_state=rint1)
# REMOVED_UNUSED_CODE:                 .reset_index(drop=True)
# REMOVED_UNUSED_CODE:                 .to_numpy()[:, 0]
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             test_features = test_features.sample(frac=1, random_state=rint2).reset_index(drop=True)
# REMOVED_UNUSED_CODE:             test_labels = test_labels.sample(frac=1, random_state=rint2).reset_index(drop=True)
# REMOVED_UNUSED_CODE:             test_weights = (
# REMOVED_UNUSED_CODE:                 pd.DataFrame(test_weights)
# REMOVED_UNUSED_CODE:                 .sample(frac=1, random_state=rint2)
# REMOVED_UNUSED_CODE:                 .reset_index(drop=True)
# REMOVED_UNUSED_CODE:                 .to_numpy()[:, 0]
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Simplest way to reverse the order of training and test data:
# REMOVED_UNUSED_CODE:         if self.freqai_config["feature_parameters"].get("reverse_train_test_order", False):
# REMOVED_UNUSED_CODE:             return self.build_data_dictionary(
# REMOVED_UNUSED_CODE:                 test_features,
# REMOVED_UNUSED_CODE:                 train_features,
# REMOVED_UNUSED_CODE:                 test_labels,
# REMOVED_UNUSED_CODE:                 train_labels,
# REMOVED_UNUSED_CODE:                 test_weights,
# REMOVED_UNUSED_CODE:                 train_weights,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             return self.build_data_dictionary(
# REMOVED_UNUSED_CODE:                 train_features,
# REMOVED_UNUSED_CODE:                 test_features,
# REMOVED_UNUSED_CODE:                 train_labels,
# REMOVED_UNUSED_CODE:                 test_labels,
# REMOVED_UNUSED_CODE:                 train_weights,
# REMOVED_UNUSED_CODE:                 test_weights,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def filter_features(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         unfiltered_df: DataFrame,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         training_feature_list: list,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         label_list: list = list(),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         training_filter: bool = True,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> tuple[DataFrame, DataFrame]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Filter the unfiltered dataframe to extract the user requested features/labels and properly
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         remove all NaNs. Any row with a NaN is removed from training dataset or replaced with
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         0s in the prediction dataset. However, prediction dataset do_predict will reflect any
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         row that had a NaN and will shield user from that prediction.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param unfiltered_df: the full dataframe for the present training period
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param training_feature_list: list, the training feature list constructed by
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                                       self.build_feature_list() according to user specified
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                                       parameters in the configuration file.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param labels: the labels for the dataset
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param training_filter: boolean which lets the function know if it is training data or
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                                 prediction data to be filtered.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :returns:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :filtered_df: dataframe cleaned of NaNs and only containing the user
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         requested feature set.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :labels: labels cleaned of NaNs.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         filtered_df = unfiltered_df.filter(training_feature_list, axis=1)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         filtered_df = filtered_df.replace([np.inf, -np.inf], np.nan)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         drop_index = pd.isnull(filtered_df).any(axis=1)  # get the rows that have NaNs,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         drop_index = drop_index.replace(True, 1).replace(False, 0).infer_objects(copy=False)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if training_filter:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # we don't care about total row number (total no. datapoints) in training, we only care
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # about removing any row with NaNs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # if labels has multiple columns (user wants to train multiple modelEs), we detect here
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             labels = unfiltered_df.filter(label_list, axis=1)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             drop_index_labels = pd.isnull(labels).any(axis=1)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             drop_index_labels = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 drop_index_labels.replace(True, 1).replace(False, 0).infer_objects(copy=False)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dates = unfiltered_df["date"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             filtered_df = filtered_df[
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 (drop_index == 0) & (drop_index_labels == 0)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ]  # dropping values
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             labels = labels[
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 (drop_index == 0) & (drop_index_labels == 0)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ]  # assuming the labels depend entirely on the dataframe here.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.train_dates = dates[(drop_index == 0) & (drop_index_labels == 0)]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             logger.info(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"{self.pair}: dropped {len(unfiltered_df) - len(filtered_df)} training points"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f" due to NaNs in populated dataset {len(unfiltered_df)}."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if len(filtered_df) == 0 and not self.live:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 raise OperationalException(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     f"{self.pair}: all training data dropped due to NaNs. "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "You likely did not download enough training data prior "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "to your backtest timerange. Hint:\n"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     f"{DOCS_LINK}/freqai-running/"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "#downloading-data-to-cover-the-full-backtest-period"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if (1 - len(filtered_df) / len(unfiltered_df)) > 0.1 and self.live:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 worst_indicator = str(unfiltered_df.count().idxmin())
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 logger.warning(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     f" {(1 - len(filtered_df) / len(unfiltered_df)) * 100:.0f} percent "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     " of training data dropped due to NaNs, model may perform inconsistent "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     f"with expectations. Verify {worst_indicator}"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.data["filter_drop_index_training"] = drop_index
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # we are backtesting so we need to preserve row number to send back to strategy,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # so now we use do_predict to avoid any prediction based on a NaN
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             drop_index = pd.isnull(filtered_df).any(axis=1)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.data["filter_drop_index_prediction"] = drop_index
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             filtered_df.fillna(0, inplace=True)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # replacing all NaNs with zeros to avoid issues in 'prediction', but any prediction
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # that was based on a single NaN is ultimately protected from buys with do_predict
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             drop_index = ~drop_index
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.do_predict = np.array(drop_index.replace(True, 1).replace(False, 0))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if (len(self.do_predict) - self.do_predict.sum()) > 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 logger.info(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "dropped %s of %s prediction data points due to NaNs.",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     len(self.do_predict) - self.do_predict.sum(),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     len(filtered_df),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             labels = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return filtered_df, labels
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def build_data_dictionary(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         train_df: DataFrame,
# REMOVED_UNUSED_CODE:         test_df: DataFrame,
# REMOVED_UNUSED_CODE:         train_labels: DataFrame,
# REMOVED_UNUSED_CODE:         test_labels: DataFrame,
# REMOVED_UNUSED_CODE:         train_weights: Any,
# REMOVED_UNUSED_CODE:         test_weights: Any,
# REMOVED_UNUSED_CODE:     ) -> dict:
# REMOVED_UNUSED_CODE:         self.data_dictionary = {
# REMOVED_UNUSED_CODE:             "train_features": train_df,
# REMOVED_UNUSED_CODE:             "test_features": test_df,
# REMOVED_UNUSED_CODE:             "train_labels": train_labels,
# REMOVED_UNUSED_CODE:             "test_labels": test_labels,
# REMOVED_UNUSED_CODE:             "train_weights": train_weights,
# REMOVED_UNUSED_CODE:             "test_weights": test_weights,
# REMOVED_UNUSED_CODE:             "train_dates": self.train_dates,
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return self.data_dictionary
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def split_timerange(
# REMOVED_UNUSED_CODE:         self, tr: str, train_split: int = 28, bt_split: float = 7
# REMOVED_UNUSED_CODE:     ) -> tuple[list, list]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Function which takes a single time range (tr) and splits it
# REMOVED_UNUSED_CODE:         into sub timeranges to train and backtest on based on user input
# REMOVED_UNUSED_CODE:         tr: str, full timerange to train on
# REMOVED_UNUSED_CODE:         train_split: the period length for the each training (days). Specified in user
# REMOVED_UNUSED_CODE:         configuration file
# REMOVED_UNUSED_CODE:         bt_split: the backtesting length (days). Specified in user configuration file
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not isinstance(train_split, int) or train_split < 1:
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 f"train_period_days must be an integer greater than 0. Got {train_split}."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         train_period_days = train_split * SECONDS_IN_DAY
# REMOVED_UNUSED_CODE:         bt_period = bt_split * SECONDS_IN_DAY
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         full_timerange = TimeRange.parse_timerange(tr)
# REMOVED_UNUSED_CODE:         config_timerange = TimeRange.parse_timerange(self.config["timerange"])
# REMOVED_UNUSED_CODE:         if config_timerange.stopts == 0:
# REMOVED_UNUSED_CODE:             config_timerange.stopts = int(datetime.now(tz=timezone.utc).timestamp())
# REMOVED_UNUSED_CODE:         timerange_train = copy.deepcopy(full_timerange)
# REMOVED_UNUSED_CODE:         timerange_backtest = copy.deepcopy(full_timerange)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         tr_training_list = []
# REMOVED_UNUSED_CODE:         tr_backtesting_list = []
# REMOVED_UNUSED_CODE:         tr_training_list_timerange = []
# REMOVED_UNUSED_CODE:         tr_backtesting_list_timerange = []
# REMOVED_UNUSED_CODE:         first = True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         while True:
# REMOVED_UNUSED_CODE:             if not first:
# REMOVED_UNUSED_CODE:                 timerange_train.startts = timerange_train.startts + int(bt_period)
# REMOVED_UNUSED_CODE:             timerange_train.stopts = timerange_train.startts + train_period_days
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             first = False
# REMOVED_UNUSED_CODE:             tr_training_list.append(timerange_train.timerange_str)
# REMOVED_UNUSED_CODE:             tr_training_list_timerange.append(copy.deepcopy(timerange_train))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # associated backtest period
# REMOVED_UNUSED_CODE:             timerange_backtest.startts = timerange_train.stopts
# REMOVED_UNUSED_CODE:             timerange_backtest.stopts = timerange_backtest.startts + int(bt_period)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if timerange_backtest.stopts > config_timerange.stopts:
# REMOVED_UNUSED_CODE:                 timerange_backtest.stopts = config_timerange.stopts
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             tr_backtesting_list.append(timerange_backtest.timerange_str)
# REMOVED_UNUSED_CODE:             tr_backtesting_list_timerange.append(copy.deepcopy(timerange_backtest))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # ensure we are predicting on exactly same amount of data as requested by user defined
# REMOVED_UNUSED_CODE:             #  --timerange
# REMOVED_UNUSED_CODE:             if timerange_backtest.stopts == config_timerange.stopts:
# REMOVED_UNUSED_CODE:                 break
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # print(tr_training_list, tr_backtesting_list)
# REMOVED_UNUSED_CODE:         return tr_training_list_timerange, tr_backtesting_list_timerange
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def slice_dataframe(self, timerange: TimeRange, df: DataFrame) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Given a full dataframe, extract the user desired window
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param tr: timerange string that we wish to extract from df
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param df: Dataframe containing all candles to run the entire backtest. Here
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                    it is sliced down to just the present training period.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not self.live:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             df = df.loc[(df["date"] >= timerange.startdt) & (df["date"] < timerange.stopdt), :]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             df = df.loc[df["date"] >= timerange.startdt, :]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return df
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def find_features(self, dataframe: DataFrame) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Find features in the strategy provided dataframe
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param dataframe: DataFrame = strategy provided dataframe
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         features: list = the features to be used for training/prediction
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         column_names = dataframe.columns
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         features = [c for c in column_names if "%" in c]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not features:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise OperationalException("Could not find any features!")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.training_features_list = features
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def find_labels(self, dataframe: DataFrame) -> None:
# REMOVED_UNUSED_CODE:         column_names = dataframe.columns
# REMOVED_UNUSED_CODE:         labels = [c for c in column_names if "&" in c]
# REMOVED_UNUSED_CODE:         self.label_list = labels
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def set_weights_higher_recent(self, num_weights: int) -> npt.ArrayLike:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Set weights so that recent data is more heavily weighted during
# REMOVED_UNUSED_CODE:         training than older data.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         wfactor = self.config["freqai"]["feature_parameters"]["weight_factor"]
# REMOVED_UNUSED_CODE:         weights = np.exp(-np.arange(num_weights) / (wfactor * num_weights))[::-1]
# REMOVED_UNUSED_CODE:         return weights
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_predictions_to_append(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, predictions: DataFrame, do_predict: npt.ArrayLike, dataframe_backtest: DataFrame
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Get backtest prediction from current backtest period
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         append_df = DataFrame()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for label in predictions.columns:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             append_df[label] = predictions[label]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if append_df[label].dtype == object:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if "labels_mean" in self.data:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 append_df[f"{label}_mean"] = self.data["labels_mean"][label]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if "labels_std" in self.data:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 append_df[f"{label}_std"] = self.data["labels_std"][label]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for extra_col in self.data["extra_returns_per_train"]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             append_df[f"{extra_col}"] = self.data["extra_returns_per_train"][extra_col]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         append_df["do_predict"] = do_predict
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.freqai_config["feature_parameters"].get("DI_threshold", 0) > 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             append_df["DI_values"] = self.DI_values
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         user_cols = [col for col in dataframe_backtest.columns if col.startswith("%%")]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         cols = ["date"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         cols.extend(user_cols)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe_backtest.reset_index(drop=True, inplace=True)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         merged_df = pd.concat([dataframe_backtest[cols], append_df], axis=1)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return merged_df
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def append_predictions(self, append_df: DataFrame) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Append backtest prediction from current backtest period to all previous periods
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.full_df.empty:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.full_df = append_df
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.full_df = pd.concat([self.full_df, append_df], axis=0, ignore_index=True)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def fill_predictions(self, dataframe):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Back fill values to before the backtesting range so that the dataframe matches size
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         when it goes back to the strategy. These rows are not included in the backtest.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         to_keep = [
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             col for col in dataframe.columns if not col.startswith("&") and not col.startswith("%%")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.return_dataframe = pd.merge(dataframe[to_keep], self.full_df, how="left", on="date")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.return_dataframe[self.full_df.columns] = self.return_dataframe[
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.full_df.columns
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ].fillna(value=0)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.full_df = DataFrame()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def create_fulltimerange(self, backtest_tr: str, backtest_period_days: int) -> str:
# REMOVED_UNUSED_CODE:         if not isinstance(backtest_period_days, int):
# REMOVED_UNUSED_CODE:             raise OperationalException("backtest_period_days must be an integer")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if backtest_period_days < 0:
# REMOVED_UNUSED_CODE:             raise OperationalException("backtest_period_days must be positive")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         backtest_timerange = TimeRange.parse_timerange(backtest_tr)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if backtest_timerange.stopts == 0:
# REMOVED_UNUSED_CODE:             # typically open ended time ranges do work, however, there are some edge cases where
# REMOVED_UNUSED_CODE:             # it does not. accommodating these kinds of edge cases just to allow open-ended
# REMOVED_UNUSED_CODE:             # timerange is not high enough priority to warrant the effort. It is safer for now
# REMOVED_UNUSED_CODE:             # to simply ask user to add their end date
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 "FreqAI backtesting does not allow open ended timeranges. "
# REMOVED_UNUSED_CODE:                 "Please indicate the end date of your desired backtesting. "
# REMOVED_UNUSED_CODE:                 "timerange."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             # backtest_timerange.stopts = int(
# REMOVED_UNUSED_CODE:             #     datetime.now(tz=timezone.utc).timestamp()
# REMOVED_UNUSED_CODE:             # )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         backtest_timerange.startts = (
# REMOVED_UNUSED_CODE:             backtest_timerange.startts - backtest_period_days * SECONDS_IN_DAY
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         full_timerange = backtest_timerange.timerange_str
# REMOVED_UNUSED_CODE:         config_path = Path(self.config["config_files"][0])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not self.full_path.is_dir():
# REMOVED_UNUSED_CODE:             self.full_path.mkdir(parents=True, exist_ok=True)
# REMOVED_UNUSED_CODE:             shutil.copy(
# REMOVED_UNUSED_CODE:                 config_path.resolve(),
# REMOVED_UNUSED_CODE:                 Path(self.full_path / config_path.parts[-1]),
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return full_timerange
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def check_if_model_expired(self, trained_timestamp: int) -> bool:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         A model age checker to determine if the model is trustworthy based on user defined
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         `expiration_hours` in the configuration file.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param trained_timestamp: int = The time of training for the most recent model.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             bool = If the model is expired or not.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         time = datetime.now(tz=timezone.utc).timestamp()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         elapsed_time = (time - trained_timestamp) / 3600  # hours
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         max_time = self.freqai_config.get("expiration_hours", 0)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if max_time > 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return elapsed_time > max_time
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def check_if_new_training_required(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, trained_timestamp: int
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> tuple[bool, TimeRange, TimeRange]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         time = datetime.now(tz=timezone.utc).timestamp()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trained_timerange = TimeRange()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         data_load_timerange = TimeRange()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         timeframes = self.freqai_config["feature_parameters"].get("include_timeframes")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         max_tf_seconds = 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for tf in timeframes:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             secs = timeframe_to_seconds(tf)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if secs > max_tf_seconds:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 max_tf_seconds = secs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # We notice that users like to use exotic indicators where
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # they do not know the required timeperiod. Here we include a factor
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # of safety by multiplying the user considered "max" by 2.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         max_period = self.config.get("startup_candle_count", 20) * 2
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         additional_seconds = max_period * max_tf_seconds
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if trained_timestamp != 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             elapsed_time = (time - trained_timestamp) / SECONDS_IN_HOUR
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             retrain = elapsed_time > self.freqai_config.get("live_retrain_hours", 0)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if retrain:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 trained_timerange.startts = int(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     time - self.freqai_config.get("train_period_days", 0) * SECONDS_IN_DAY
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 trained_timerange.stopts = int(time)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # we want to load/populate indicators on more data than we plan to train on so
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # because most of the indicators have a rolling timeperiod, and are thus NaNs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # unless they have data further back in time before the start of the train period
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 data_load_timerange.startts = int(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     time
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     - self.freqai_config.get("train_period_days", 0) * SECONDS_IN_DAY
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     - additional_seconds
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 data_load_timerange.stopts = int(time)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:  # user passed no live_trained_timerange in config
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trained_timerange.startts = int(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 time - self.freqai_config.get("train_period_days", 0) * SECONDS_IN_DAY
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             trained_timerange.stopts = int(time)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             data_load_timerange.startts = int(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 time
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 - self.freqai_config.get("train_period_days", 0) * SECONDS_IN_DAY
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 - additional_seconds
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             data_load_timerange.stopts = int(time)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             retrain = True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return retrain, trained_timerange, data_load_timerange
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def set_new_model_names(self, pair: str, timestamp_id: int):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         coin, _ = pair.split("/")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.data_path = Path(self.full_path / f"sub-train-{pair.split('/')[0]}_{timestamp_id}")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.model_filename = f"cb_{coin.lower()}_{timestamp_id}"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def set_all_pairs(self) -> None:
# REMOVED_UNUSED_CODE:         self.all_pairs = copy.deepcopy(
# REMOVED_UNUSED_CODE:             self.freqai_config["feature_parameters"].get("include_corr_pairlist", [])
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         for pair in self.config.get("exchange", "").get("pair_whitelist"):
# REMOVED_UNUSED_CODE:             if pair not in self.all_pairs:
# REMOVED_UNUSED_CODE:                 self.all_pairs.append(pair)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def extract_corr_pair_columns_from_populated_indicators(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, dataframe: DataFrame
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> dict[str, DataFrame]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Find the columns of the dataframe corresponding to the corr_pairlist, save them
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         in a dictionary to be reused and attached to other pairs.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param dataframe: fully populated dataframe (current pair + corr_pairs)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: corr_dataframes, dictionary of dataframes to be attached
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                  to other pairs in same candle.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         corr_dataframes: dict[str, DataFrame] = {}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pairs = self.freqai_config["feature_parameters"].get("include_corr_pairlist", [])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for pair in pairs:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             pair = pair.replace(":", "")  # lightgbm does not like colons
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             pair_cols = [
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 col for col in dataframe.columns if col.startswith("%") and f"{pair}_" in col
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if pair_cols:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 pair_cols.insert(0, "date")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 corr_dataframes[pair] = dataframe.filter(pair_cols, axis=1)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return corr_dataframes
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def attach_corr_pair_columns(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, dataframe: DataFrame, corr_dataframes: dict[str, DataFrame], current_pair: str
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Attach the existing corr_pair dataframes to the current pair dataframe before training
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param dataframe: current pair strategy dataframe, indicators populated already
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param corr_dataframes: dictionary of saved dataframes from earlier in the same candle
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param current_pair: current pair to which we will attach corr pair dataframe
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :dataframe: current pair dataframe of populated indicators, concatenated with corr_pairs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     ready for training
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pairs = self.freqai_config["feature_parameters"].get("include_corr_pairlist", [])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         current_pair = current_pair.replace(":", "")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for pair in pairs:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             pair = pair.replace(":", "")  # lightgbm does not work with colons
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if current_pair != pair:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 dataframe = dataframe.merge(corr_dataframes[pair], how="left", on="date")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def get_pair_data_for_features(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE:         tf: str,
# REMOVED_UNUSED_CODE:         strategy: IStrategy,
# REMOVED_UNUSED_CODE:         corr_dataframes: dict = {},
# REMOVED_UNUSED_CODE:         base_dataframes: dict = {},
# REMOVED_UNUSED_CODE:         is_corr_pairs: bool = False,
# REMOVED_UNUSED_CODE:     ) -> DataFrame:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Get the data for the pair. If it's not in the dictionary, get it from the data provider
# REMOVED_UNUSED_CODE:         :param pair: str = pair to get data for
# REMOVED_UNUSED_CODE:         :param tf: str = timeframe to get data for
# REMOVED_UNUSED_CODE:         :param strategy: IStrategy = user defined strategy object
# REMOVED_UNUSED_CODE:         :param corr_dataframes: dict = dict containing the df pair dataframes
# REMOVED_UNUSED_CODE:                                 (for user defined timeframes)
# REMOVED_UNUSED_CODE:         :param base_dataframes: dict = dict containing the current pair dataframes
# REMOVED_UNUSED_CODE:                                 (for user defined timeframes)
# REMOVED_UNUSED_CODE:         :param is_corr_pairs: bool = whether the pair is a corr pair or not
# REMOVED_UNUSED_CODE:         :return: dataframe = dataframe containing the pair data
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if is_corr_pairs:
# REMOVED_UNUSED_CODE:             dataframe = corr_dataframes[pair][tf]
# REMOVED_UNUSED_CODE:             if not dataframe.empty:
# REMOVED_UNUSED_CODE:                 return dataframe
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 dataframe = strategy.dp.get_pair_dataframe(pair=pair, timeframe=tf)
# REMOVED_UNUSED_CODE:                 return dataframe
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             dataframe = base_dataframes[tf]
# REMOVED_UNUSED_CODE:             if not dataframe.empty:
# REMOVED_UNUSED_CODE:                 return dataframe
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 dataframe = strategy.dp.get_pair_dataframe(pair=pair, timeframe=tf)
# REMOVED_UNUSED_CODE:                 return dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def merge_features(
# REMOVED_UNUSED_CODE:         self, df_main: DataFrame, df_to_merge: DataFrame, tf: str, timeframe_inf: str, suffix: str
# REMOVED_UNUSED_CODE:     ) -> DataFrame:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Merge the features of the dataframe and remove HLCV and date added columns
# REMOVED_UNUSED_CODE:         :param df_main: DataFrame = main dataframe
# REMOVED_UNUSED_CODE:         :param df_to_merge: DataFrame = dataframe to merge
# REMOVED_UNUSED_CODE:         :param tf: str = timeframe of the main dataframe
# REMOVED_UNUSED_CODE:         :param timeframe_inf: str = timeframe of the dataframe to merge
# REMOVED_UNUSED_CODE:         :param suffix: str = suffix to add to the columns of the dataframe to merge
# REMOVED_UNUSED_CODE:         :return: dataframe = merged dataframe
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         dataframe = merge_informative_pair(
# REMOVED_UNUSED_CODE:             df_main,
# REMOVED_UNUSED_CODE:             df_to_merge,
# REMOVED_UNUSED_CODE:             tf,
# REMOVED_UNUSED_CODE:             timeframe_inf=timeframe_inf,
# REMOVED_UNUSED_CODE:             append_timeframe=False,
# REMOVED_UNUSED_CODE:             suffix=suffix,
# REMOVED_UNUSED_CODE:             ffill=True,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         skip_columns = [
# REMOVED_UNUSED_CODE:             (f"{s}_{suffix}") for s in ["date", "open", "high", "low", "close", "volume"]
# REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE:         dataframe = dataframe.drop(columns=skip_columns)
# REMOVED_UNUSED_CODE:         return dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def populate_features(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         dataframe: DataFrame,
# REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE:         strategy: IStrategy,
# REMOVED_UNUSED_CODE:         corr_dataframes: dict,
# REMOVED_UNUSED_CODE:         base_dataframes: dict,
# REMOVED_UNUSED_CODE:         is_corr_pairs: bool = False,
# REMOVED_UNUSED_CODE:     ) -> DataFrame:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Use the user defined strategy functions for populating features
# REMOVED_UNUSED_CODE:         :param dataframe: DataFrame = dataframe to populate
# REMOVED_UNUSED_CODE:         :param pair: str = pair to populate
# REMOVED_UNUSED_CODE:         :param strategy: IStrategy = user defined strategy object
# REMOVED_UNUSED_CODE:         :param corr_dataframes: dict = dict containing the df pair dataframes
# REMOVED_UNUSED_CODE:         :param base_dataframes: dict = dict containing the current pair dataframes
# REMOVED_UNUSED_CODE:         :param is_corr_pairs: bool = whether the pair is a corr pair or not
# REMOVED_UNUSED_CODE:         :return: dataframe = populated dataframe
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         tfs: list[str] = self.freqai_config["feature_parameters"].get("include_timeframes")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         for tf in tfs:
# REMOVED_UNUSED_CODE:             metadata = {"pair": pair, "tf": tf}
# REMOVED_UNUSED_CODE:             informative_df = self.get_pair_data_for_features(
# REMOVED_UNUSED_CODE:                 pair, tf, strategy, corr_dataframes, base_dataframes, is_corr_pairs
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             informative_copy = informative_df.copy()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             logger.debug(f"Populating features for {pair} {tf}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             for t in self.freqai_config["feature_parameters"]["indicator_periods_candles"]:
# REMOVED_UNUSED_CODE:                 df_features = strategy.feature_engineering_expand_all(
# REMOVED_UNUSED_CODE:                     informative_copy.copy(), t, metadata=metadata
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 suffix = f"{t}"
# REMOVED_UNUSED_CODE:                 informative_df = self.merge_features(informative_df, df_features, tf, tf, suffix)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             generic_df = strategy.feature_engineering_expand_basic(
# REMOVED_UNUSED_CODE:                 informative_copy.copy(), metadata=metadata
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             suffix = "gen"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             informative_df = self.merge_features(informative_df, generic_df, tf, tf, suffix)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             indicators = [col for col in informative_df if col.startswith("%")]
# REMOVED_UNUSED_CODE:             for n in range(self.freqai_config["feature_parameters"]["include_shifted_candles"] + 1):
# REMOVED_UNUSED_CODE:                 if n == 0:
# REMOVED_UNUSED_CODE:                     continue
# REMOVED_UNUSED_CODE:                 df_shift = informative_df[indicators].shift(n)
# REMOVED_UNUSED_CODE:                 df_shift = df_shift.add_suffix("_shift-" + str(n))
# REMOVED_UNUSED_CODE:                 informative_df = pd.concat((informative_df, df_shift), axis=1)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             dataframe = self.merge_features(
# REMOVED_UNUSED_CODE:                 dataframe.copy(), informative_df, self.config["timeframe"], tf, f"{pair}_{tf}"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def use_strategy_to_populate_indicators(  # noqa: C901
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         strategy: IStrategy,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         corr_dataframes: dict = {},
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         base_dataframes: dict = {},
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair: str = "",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         prediction_dataframe: DataFrame = pd.DataFrame(),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         do_corr_pairs: bool = True,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Use the user defined strategy for populating indicators during retrain
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param strategy: IStrategy = user defined strategy object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param corr_dataframes: dict = dict containing the df pair dataframes
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                                 (for user defined timeframes)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param base_dataframes: dict = dict containing the current pair dataframes
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                                 (for user defined timeframes)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param pair: str = pair to populate
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param prediction_dataframe: DataFrame = dataframe containing the pair data
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         used for prediction
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param do_corr_pairs: bool = whether to populate corr pairs or not
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe: DataFrame = dataframe containing populated indicators
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # check if the user is using the deprecated populate_any_indicators function
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         new_version = inspect.getsource(strategy.populate_any_indicators) == (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             inspect.getsource(IStrategy.populate_any_indicators)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not new_version:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "You are using the `populate_any_indicators()` function"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 " which was deprecated on March 1, 2023. Please refer "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "to the strategy migration guide to use the new "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "feature_engineering_* methods: \n"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"{DOCS_LINK}/strategy_migration/#freqai-strategy \n"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "And the feature_engineering_* documentation: \n"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"{DOCS_LINK}/freqai-feature-engineering/"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         tfs: list[str] = self.freqai_config["feature_parameters"].get("include_timeframes")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pairs: list[str] = self.freqai_config["feature_parameters"].get("include_corr_pairlist", [])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for tf in tfs:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if tf not in base_dataframes:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 base_dataframes[tf] = pd.DataFrame()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for p in pairs:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if p not in corr_dataframes:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     corr_dataframes[p] = {}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 if tf not in corr_dataframes[p]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     corr_dataframes[p][tf] = pd.DataFrame()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not prediction_dataframe.empty:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dataframe = prediction_dataframe.copy()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             base_dataframes[self.config["timeframe"]] = dataframe.copy()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dataframe = base_dataframes[self.config["timeframe"]].copy()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         corr_pairs: list[str] = self.freqai_config["feature_parameters"].get(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "include_corr_pairlist", []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe = self.populate_features(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dataframe.copy(), pair, strategy, corr_dataframes, base_dataframes
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         metadata = {"pair": pair}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe = strategy.feature_engineering_standard(dataframe.copy(), metadata=metadata)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # ensure corr pairs are always last
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for corr_pair in corr_pairs:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if pair == corr_pair:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 continue  # dont repeat anything from whitelist
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if corr_pairs and do_corr_pairs:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 dataframe = self.populate_features(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     dataframe.copy(), corr_pair, strategy, corr_dataframes, base_dataframes, True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.live:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dataframe = strategy.set_freqai_targets(dataframe.copy(), metadata=metadata)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dataframe = self.remove_special_chars_from_feature_names(dataframe)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.get_unique_classes_from_labels(dataframe)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.config.get("reduce_df_footprint", False):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dataframe = reduce_dataframe_footprint(dataframe)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def fit_labels(self) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Fit the labels with a gaussian distribution
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         import scipy as spy
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.data["labels_mean"], self.data["labels_std"] = {}, {}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for label in self.data_dictionary["train_labels"].columns:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if self.data_dictionary["train_labels"][label].dtype == object:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f = spy.stats.norm.fit(self.data_dictionary["train_labels"][label])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.data["labels_mean"][label], self.data["labels_std"][label] = f[0], f[1]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # in case targets are classifications
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for label in self.unique_class_list:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.data["labels_mean"][label], self.data["labels_std"][label] = 0, 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def remove_features_from_df(self, dataframe: DataFrame) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Remove the features from the dataframe before returning it to strategy. This keeps it
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         compact for Frequi purposes.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         to_keep = [
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             col for col in dataframe.columns if not col.startswith("%") or col.startswith("%%")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe[to_keep]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def get_unique_classes_from_labels(self, dataframe: DataFrame) -> None:
# REMOVED_UNUSED_CODE:         # self.find_features(dataframe)
# REMOVED_UNUSED_CODE:         self.find_labels(dataframe)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         for key in self.label_list:
# REMOVED_UNUSED_CODE:             if dataframe[key].dtype == object:
# REMOVED_UNUSED_CODE:                 self.unique_classes[key] = dataframe[key].dropna().unique()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.unique_classes:
# REMOVED_UNUSED_CODE:             for label in self.unique_classes:
# REMOVED_UNUSED_CODE:                 self.unique_class_list += list(self.unique_classes[label])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def save_backtesting_prediction(self, append_df: DataFrame) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Save prediction dataframe from backtesting to feather file format
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param append_df: dataframe for backtesting period
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         full_predictions_folder = Path(self.full_path / self.backtest_predictions_folder)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not full_predictions_folder.is_dir():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             full_predictions_folder.mkdir(parents=True, exist_ok=True)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         append_df.to_feather(self.backtesting_results_path)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def get_backtesting_prediction(self) -> DataFrame:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Get prediction dataframe from feather file format
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         append_df = pd.read_feather(self.backtesting_results_path)
# REMOVED_UNUSED_CODE:         return append_df
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def check_if_backtest_prediction_is_valid(self, len_backtest_df: int) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Check if a backtesting prediction already exists and if the predictions
# REMOVED_UNUSED_CODE:         to append have the same size as the backtesting dataframe slice
# REMOVED_UNUSED_CODE:         :param length_backtesting_dataframe: Length of backtesting dataframe slice
# REMOVED_UNUSED_CODE:         :return:
# REMOVED_UNUSED_CODE:         :boolean: whether the prediction file is valid.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         path_to_predictionfile = Path(
# REMOVED_UNUSED_CODE:             self.full_path
# REMOVED_UNUSED_CODE:             / self.backtest_predictions_folder
# REMOVED_UNUSED_CODE:             / f"{self.model_filename}_prediction.feather"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         self.backtesting_results_path = path_to_predictionfile
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         file_exists = path_to_predictionfile.is_file()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if file_exists:
# REMOVED_UNUSED_CODE:             append_df = self.get_backtesting_prediction()
# REMOVED_UNUSED_CODE:             if len(append_df) == len_backtest_df and "date" in append_df:
# REMOVED_UNUSED_CODE:                 logger.info(f"Found backtesting prediction file at {path_to_predictionfile}")
# REMOVED_UNUSED_CODE:                 return True
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 logger.info(
# REMOVED_UNUSED_CODE:                     "A new backtesting prediction file is required. "
# REMOVED_UNUSED_CODE:                     "(Number of predictions is different from dataframe length or "
# REMOVED_UNUSED_CODE:                     "old prediction file version)."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 return False
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             logger.info(f"Could not find backtesting prediction file at {path_to_predictionfile}")
# REMOVED_UNUSED_CODE:             return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def get_full_models_path(self, config: Config) -> Path:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Returns default FreqAI model path
# REMOVED_UNUSED_CODE:         :param config: Configuration dictionary
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         freqai_config: dict[str, Any] = config["freqai"]
# REMOVED_UNUSED_CODE:         return Path(config["user_data_dir"] / "models" / str(freqai_config.get("identifier")))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def remove_special_chars_from_feature_names(self, dataframe: pd.DataFrame) -> pd.DataFrame:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Remove all special characters from feature strings (:)
# REMOVED_UNUSED_CODE:         :param dataframe: the dataframe that just finished indicator population. (unfiltered)
# REMOVED_UNUSED_CODE:         :return: dataframe with cleaned feature names
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         spec_chars = [":"]
# REMOVED_UNUSED_CODE:         for c in spec_chars:
# REMOVED_UNUSED_CODE:             dataframe.columns = dataframe.columns.str.replace(c, "")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return dataframe
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def buffer_timerange(self, timerange: TimeRange):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Buffer the start and end of the timerange. This is used *after* the indicators
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         are populated.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         The main example use is when predicting maxima and minima, the argrelextrema
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         function  cannot know the maxima/minima at the edges of the timerange. To improve
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         model accuracy, it is best to compute argrelextrema on the full timerange
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         and then use this function to cut off the edges (buffer) by the kernel.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         In another case, if the targets are set to a shifted price movement, this
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         buffer is unnecessary because the shifted candles at the end of the timerange
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         will be NaN and FreqAI will automatically cut those off of the training
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataset.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         buffer = self.freqai_config["feature_parameters"]["buffer_train_data_candles"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if buffer:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             timerange.stopts -= buffer * timeframe_to_seconds(self.config["timeframe"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             timerange.startts += buffer * timeframe_to_seconds(self.config["timeframe"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return timerange
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # deprecated functions
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def normalize_data(self, data_dictionary: dict) -> dict[Any, Any]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Deprecation warning, migration assistance
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.warning(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"Your custom IFreqaiModel relies on the deprecated"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             " data pipeline. Please update your model to use the new data pipeline."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             " This can be achieved by following the migration guide at "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"{DOCS_LINK}/strategy_migration/#freqai-new-data-pipeline "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "We added a basic pipeline for you, but this will be removed "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "in a future version."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return data_dictionary
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def denormalize_labels_from_metadata(self, df: DataFrame) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Deprecation warning, migration assistance
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.warning(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"Your custom IFreqaiModel relies on the deprecated"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             " data pipeline. Please update your model to use the new data pipeline."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             " This can be achieved by following the migration guide at "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"{DOCS_LINK}/strategy_migration/#freqai-new-data-pipeline "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "We added a basic pipeline for you, but this will be removed "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "in a future version."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pred_df, _, _ = self.label_pipeline.inverse_transform(df)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return pred_df
