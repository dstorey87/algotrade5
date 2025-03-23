import logging
from time import time
from typing import Any

import numpy as np
import numpy.typing as npt
import pandas as pd
import torch
from pandas import DataFrame
from torch.nn import functional as F

from freqtrade.exceptions import OperationalException
from freqtrade.freqai.base_models.BasePyTorchModel import BasePyTorchModel
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen


logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class BasePyTorchClassifier(BasePyTorchModel):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     A PyTorch implementation of a classifier.
# REMOVED_UNUSED_CODE:     User must implement fit method
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Important!
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     - User must declare the target class names in the strategy,
# REMOVED_UNUSED_CODE:     under IStrategy.set_freqai_targets method.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     for example, in your strategy:
# REMOVED_UNUSED_CODE:     ```
# REMOVED_UNUSED_CODE:         def set_freqai_targets(self, dataframe: DataFrame, metadata: Dict, **kwargs):
# REMOVED_UNUSED_CODE:             self.freqai.class_names = ["down", "up"]
# REMOVED_UNUSED_CODE:             dataframe['&s-up_or_down'] = np.where(dataframe["close"].shift(-100) >
# REMOVED_UNUSED_CODE:                                                   dataframe["close"], 'up', 'down')
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             return dataframe
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, **kwargs):
# REMOVED_UNUSED_CODE:         super().__init__(**kwargs)
# REMOVED_UNUSED_CODE:         self.class_name_to_index = {}
# REMOVED_UNUSED_CODE:         self.index_to_class_name = {}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def predict(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, unfiltered_df: DataFrame, dk: FreqaiDataKitchen, **kwargs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> tuple[DataFrame, npt.NDArray[np.int_]]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Filter the prediction features data and predict with it.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param dk: dk: The datakitchen object
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param unfiltered_df: Full dataframe for the current backtest period.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :pred_df: dataframe containing the predictions
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :do_predict: np.array of 1s and 0s to indicate places where freqai needed to remove
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         data (NaNs) or felt uncertain about data (PCA and DI index)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :raises ValueError: if 'class_names' doesn't exist in model meta_data.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         class_names = self.model.model_meta_data.get("class_names", None)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not class_names:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise ValueError(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "Missing class names. self.model.model_meta_data['class_names'] is None."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not self.class_name_to_index:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.init_class_names_to_index_mapping(class_names)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk.find_features(unfiltered_df)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         filtered_df, _ = dk.filter_features(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             unfiltered_df, dk.training_features_list, training_filter=False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk.data_dictionary["prediction_features"] = filtered_df
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk.data_dictionary["prediction_features"], outliers, _ = dk.feature_pipeline.transform(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.data_dictionary["prediction_features"], outlier_check=True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         x = self.data_convertor.convert_x(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.data_dictionary["prediction_features"], device=self.device
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.model.model.eval()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logits = self.model.model(x)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         probs = F.softmax(logits, dim=-1)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         predicted_classes = torch.argmax(probs, dim=-1)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         predicted_classes_str = self.decode_class_names(predicted_classes)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # used .tolist to convert probs into an iterable, in this way Tensors
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # are automatically moved to the CPU first if necessary.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pred_df_prob = DataFrame(probs.detach().tolist(), columns=class_names)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pred_df = DataFrame(predicted_classes_str, columns=[dk.label_list[0]])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pred_df = pd.concat([pred_df, pred_df_prob], axis=1)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if dk.feature_pipeline["di"]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.DI_values = dk.feature_pipeline["di"].di_values
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.DI_values = np.zeros(outliers.shape[0])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk.do_predict = outliers
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return (pred_df, dk.do_predict)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def encode_class_names(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         data_dictionary: dict[str, pd.DataFrame],
# REMOVED_UNUSED_CODE:         dk: FreqaiDataKitchen,
# REMOVED_UNUSED_CODE:         class_names: list[str],
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         encode class name, str -> int
# REMOVED_UNUSED_CODE:         assuming first column of *_labels data frame to be the target column
# REMOVED_UNUSED_CODE:         containing the class names
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         target_column_name = dk.label_list[0]
# REMOVED_UNUSED_CODE:         for split in self.splits:
# REMOVED_UNUSED_CODE:             label_df = data_dictionary[f"{split}_labels"]
# REMOVED_UNUSED_CODE:             self.assert_valid_class_names(label_df[target_column_name], class_names)
# REMOVED_UNUSED_CODE:             label_df[target_column_name] = list(
# REMOVED_UNUSED_CODE:                 map(lambda x: self.class_name_to_index[x], label_df[target_column_name])
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @staticmethod
# REMOVED_UNUSED_CODE:     def assert_valid_class_names(target_column: pd.Series, class_names: list[str]):
# REMOVED_UNUSED_CODE:         non_defined_labels = set(target_column) - set(class_names)
# REMOVED_UNUSED_CODE:         if len(non_defined_labels) != 0:
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 f"Found non defined labels: {non_defined_labels}, ",
# REMOVED_UNUSED_CODE:                 f"expecting labels: {class_names}",
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def decode_class_names(self, class_ints: torch.Tensor) -> list[str]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         decode class name, int -> str
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return list(map(lambda x: self.index_to_class_name[x.item()], class_ints))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def init_class_names_to_index_mapping(self, class_names):
# REMOVED_UNUSED_CODE:         self.class_name_to_index = {s: i for i, s in enumerate(class_names)}
# REMOVED_UNUSED_CODE:         self.index_to_class_name = {i: s for i, s in enumerate(class_names)}
# REMOVED_UNUSED_CODE:         logger.info(f"encoded class name to index: {self.class_name_to_index}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def convert_label_column_to_int(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         data_dictionary: dict[str, pd.DataFrame],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk: FreqaiDataKitchen,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         class_names: list[str],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.init_class_names_to_index_mapping(class_names)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.encode_class_names(data_dictionary, dk, class_names)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_class_names(self) -> list[str]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not self.class_names:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise ValueError(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "self.class_names is empty, "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "set self.freqai.class_names = ['class a', 'class b', 'class c'] "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "inside IStrategy.set_freqai_targets method."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self.class_names
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def train(self, unfiltered_df: DataFrame, pair: str, dk: FreqaiDataKitchen, **kwargs) -> Any:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Filter the training data and train a model to it. Train makes heavy use of the datakitchen
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for storing, saving, loading, and analyzing the data.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param unfiltered_df: Full dataframe for the current training period
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :model: Trained model which can be used to inference (self.predict)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.info(f"-------------------- Starting training {pair} --------------------")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         start_time = time()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         features_filtered, labels_filtered = dk.filter_features(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             unfiltered_df,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.training_features_list,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.label_list,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             training_filter=True,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # split data into train/test data.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dd = dk.make_train_test_datasets(features_filtered, labels_filtered)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not self.freqai_info.get("fit_live_predictions_candles", 0) or not self.live:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.fit_labels()
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
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"Training model on {len(dk.data_dictionary['train_features'].columns)} features"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.info(f"Training model on {len(dd['train_features'])} data points")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         model = self.fit(dd, dk)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         end_time = time()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.info(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"-------------------- Done training {pair} "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"({end_time - start_time:.2f} secs) --------------------"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return model
