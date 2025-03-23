import logging
from typing import Any

import numpy as np
import numpy.typing as npt
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

from freqtrade.freqai.base_models.BaseClassifierModel import BaseClassifierModel
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen


logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class SKLearnRandomForestClassifier(BaseClassifierModel):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     User created prediction model. The class inherits IFreqaiModel, which
# REMOVED_UNUSED_CODE:     means it has full access to all Frequency AI functionality. Typically,
# REMOVED_UNUSED_CODE:     users would use this to override the common `fit()`, `train()`, or
# REMOVED_UNUSED_CODE:     `predict()` methods to add their custom data handling tools or change
# REMOVED_UNUSED_CODE:     various aspects of the training that cannot be configured via the
# REMOVED_UNUSED_CODE:     top level config.json file.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def fit(self, data_dictionary: dict, dk: FreqaiDataKitchen, **kwargs) -> Any:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         User sets up the training and test data to fit their desired model here
# REMOVED_UNUSED_CODE:         :param data_dictionary: the dictionary holding all data for train, test,
# REMOVED_UNUSED_CODE:             labels, weights
# REMOVED_UNUSED_CODE:         :param dk: The datakitchen object for the current coin/model
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         X = data_dictionary["train_features"].to_numpy()
# REMOVED_UNUSED_CODE:         y = data_dictionary["train_labels"].to_numpy()[:, 0]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.freqai_info.get("data_split_parameters", {}).get("test_size", 0.1) == 0:
# REMOVED_UNUSED_CODE:             eval_set = None
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             test_features = data_dictionary["test_features"].to_numpy()
# REMOVED_UNUSED_CODE:             test_labels = data_dictionary["test_labels"].to_numpy()[:, 0]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             eval_set = (test_features, test_labels)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self.freqai_info.get("continual_learning", False):
# REMOVED_UNUSED_CODE:             logger.warning(
# REMOVED_UNUSED_CODE:                 "Continual learning is not supported for SKLearnRandomForestClassifier, ignoring."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         train_weights = data_dictionary["train_weights"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         model = RandomForestClassifier(**self.model_training_parameters)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         model.fit(X=X, y=y, sample_weight=train_weights)
# REMOVED_UNUSED_CODE:         if eval_set:
# REMOVED_UNUSED_CODE:             logger.info("Score: %s", model.score(eval_set[0], eval_set[1]))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return model
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def predict(
# REMOVED_UNUSED_CODE:         self, unfiltered_df: DataFrame, dk: FreqaiDataKitchen, **kwargs
# REMOVED_UNUSED_CODE:     ) -> tuple[DataFrame, npt.NDArray[np.int_]]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Filter the prediction features data and predict with it.
# REMOVED_UNUSED_CODE:         :param  unfiltered_df: Full dataframe for the current backtest period.
# REMOVED_UNUSED_CODE:         :return:
# REMOVED_UNUSED_CODE:         :pred_df: dataframe containing the predictions
# REMOVED_UNUSED_CODE:         :do_predict: np.array of 1s and 0s to indicate places where freqai needed to remove
# REMOVED_UNUSED_CODE:         data (NaNs) or felt uncertain about data (PCA and DI index)
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         (pred_df, dk.do_predict) = super().predict(unfiltered_df, dk, **kwargs)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         le = LabelEncoder()
# REMOVED_UNUSED_CODE:         label = dk.label_list[0]
# REMOVED_UNUSED_CODE:         labels_before = list(dk.data["labels_std"].keys())
# REMOVED_UNUSED_CODE:         labels_after = le.fit_transform(labels_before).tolist()
# REMOVED_UNUSED_CODE:         pred_df[label] = le.inverse_transform(pred_df[label])
# REMOVED_UNUSED_CODE:         pred_df = pred_df.rename(
# REMOVED_UNUSED_CODE:             columns={labels_after[i]: labels_before[i] for i in range(len(labels_before))}
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return (pred_df, dk.do_predict)
