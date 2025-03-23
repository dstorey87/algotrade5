import logging
from typing import Any

from lightgbm import LGBMClassifier

from freqtrade.freqai.base_models.BaseClassifierModel import BaseClassifierModel
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class LightGBMClassifier(BaseClassifierModel):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     User created prediction model. The class inherits IFreqaiModel, which
# REMOVED_UNUSED_CODE:     means it has full access to all Frequency AI functionality. Typically,
# REMOVED_UNUSED_CODE:     users would use this to override the common `fit()`, `train()`, or
# REMOVED_UNUSED_CODE:     `predict()` methods to add their custom data handling tools or change
# REMOVED_UNUSED_CODE:     various aspects of the training that cannot be configured via the
# REMOVED_UNUSED_CODE:     top level config.json file.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def fit(self, data_dictionary: dict, dk: FreqaiDataKitchen, **kwargs) -> Any:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         User sets up the training and test data to fit their desired model here
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param data_dictionary: the dictionary holding all data for train, test,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             labels, weights
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param dk: The datakitchen object for the current coin/model
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.freqai_info.get("data_split_parameters", {}).get("test_size", 0.1) == 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             eval_set = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             test_weights = None
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             eval_set = [
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     data_dictionary["test_features"].to_numpy(),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     data_dictionary["test_labels"].to_numpy()[:, 0],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             test_weights = data_dictionary["test_weights"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         X = data_dictionary["train_features"].to_numpy()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         y = data_dictionary["train_labels"].to_numpy()[:, 0]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         train_weights = data_dictionary["train_weights"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         init_model = self.get_init_model(dk.pair)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         model = LGBMClassifier(**self.model_training_parameters)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         model.fit(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             X=X,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             y=y,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             eval_set=eval_set,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             sample_weight=train_weights,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             eval_sample_weight=[test_weights],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             init_model=init_model,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return model
