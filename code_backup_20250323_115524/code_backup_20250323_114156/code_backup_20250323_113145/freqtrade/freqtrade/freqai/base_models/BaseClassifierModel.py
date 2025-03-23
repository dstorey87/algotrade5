import logging
from time import time
from typing import Any

import numpy as np
import numpy.typing as npt
import pandas as pd
from pandas import DataFrame

from freqtrade.freqai.data_kitchen import FreqaiDataKitchen
from freqtrade.freqai.freqai_interface import IFreqaiModel


logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class BaseClassifierModel(IFreqaiModel):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Base class for regression type models (e.g. Catboost, LightGBM, XGboost etc.).
# REMOVED_UNUSED_CODE:     User *must* inherit from this class and set fit(). See example scripts
# REMOVED_UNUSED_CODE:     such as prediction_models/CatboostClassifier.py for guidance.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def train(self, unfiltered_df: DataFrame, pair: str, dk: FreqaiDataKitchen, **kwargs) -> Any:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Filter the training data and train a model to it. Train makes heavy use of the datakitchen
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for storing, saving, loading, and analyzing the data.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param unfiltered_df: Full dataframe for the current training period
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param metadata: pair metadata from strategy.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :model: Trained model which can be used to inference (self.predict)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.info(f"-------------------- Starting training {pair} --------------------")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         start_time = time()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # filter the features requested by user in the configuration file and elegantly handle NaNs
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         features_filtered, labels_filtered = dk.filter_features(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             unfiltered_df,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.training_features_list,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.label_list,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             training_filter=True,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         start_date = unfiltered_df["date"].iloc[0].strftime("%Y-%m-%d")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         end_date = unfiltered_df["date"].iloc[-1].strftime("%Y-%m-%d")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.info(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"-------------------- Training on data from {start_date} to "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"{end_date} --------------------"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # split data into train/test data.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dd = dk.make_train_test_datasets(features_filtered, labels_filtered)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not self.freqai_info.get("fit_live_predictions_candles", 0) or not self.live:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.fit_labels()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk.feature_pipeline = self.define_data_pipeline(threads=dk.thread_count)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         (dd["train_features"], dd["train_labels"], dd["train_weights"]) = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.feature_pipeline.fit_transform(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 dd["train_features"], dd["train_labels"], dd["train_weights"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.freqai_info.get("data_split_parameters", {}).get("test_size", 0.1) != 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             (dd["test_features"], dd["test_labels"], dd["test_weights"]) = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 dk.feature_pipeline.transform(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     dd["test_features"], dd["test_labels"], dd["test_weights"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.info(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"Training model on {len(dk.data_dictionary['train_features'].columns)} features"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.info(f"Training model on {len(dd['train_features'])} data points")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         model = self.fit(dd, dk)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         end_time = time()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         logger.info(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"-------------------- Done training {pair} "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             f"({end_time - start_time:.2f} secs) --------------------"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return model
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def predict(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, unfiltered_df: DataFrame, dk: FreqaiDataKitchen, **kwargs
# REMOVED_UNUSED_CODE:     ) -> tuple[DataFrame, npt.NDArray[np.int_]]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Filter the prediction features data and predict with it.
# REMOVED_UNUSED_CODE:         :param unfiltered_df: Full dataframe for the current backtest period.
# REMOVED_UNUSED_CODE:         :return:
# REMOVED_UNUSED_CODE:         :pred_df: dataframe containing the predictions
# REMOVED_UNUSED_CODE:         :do_predict: np.array of 1s and 0s to indicate places where freqai needed to remove
# REMOVED_UNUSED_CODE:         data (NaNs) or felt uncertain about data (PCA and DI index)
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         dk.find_features(unfiltered_df)
# REMOVED_UNUSED_CODE:         filtered_df, _ = dk.filter_features(
# REMOVED_UNUSED_CODE:             unfiltered_df, dk.training_features_list, training_filter=False
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         dk.data_dictionary["prediction_features"] = filtered_df
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         dk.data_dictionary["prediction_features"], outliers, _ = dk.feature_pipeline.transform(
# REMOVED_UNUSED_CODE:             dk.data_dictionary["prediction_features"], outlier_check=True
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         predictions = self.model.predict(dk.data_dictionary["prediction_features"])
# REMOVED_UNUSED_CODE:         if self.CONV_WIDTH == 1:
# REMOVED_UNUSED_CODE:             predictions = np.reshape(predictions, (-1, len(dk.label_list)))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         pred_df = DataFrame(predictions, columns=dk.label_list)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         predictions_prob = self.model.predict_proba(dk.data_dictionary["prediction_features"])
# REMOVED_UNUSED_CODE:         if self.CONV_WIDTH == 1:
# REMOVED_UNUSED_CODE:             predictions_prob = np.reshape(predictions_prob, (-1, len(self.model.classes_)))
# REMOVED_UNUSED_CODE:         pred_df_prob = DataFrame(predictions_prob, columns=self.model.classes_)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         pred_df = pd.concat([pred_df, pred_df_prob], axis=1)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if dk.feature_pipeline["di"]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.DI_values = dk.feature_pipeline["di"].di_values
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dk.DI_values = np.zeros(outliers.shape[0])
# REMOVED_UNUSED_CODE:         dk.do_predict = outliers
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return (pred_df, dk.do_predict)
