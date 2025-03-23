import logging
# REMOVED_UNUSED_CODE: from pathlib import Path
# REMOVED_UNUSED_CODE: from typing import Any

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from catboost import CatBoostClassifier, Pool

# REMOVED_UNUSED_CODE: from freqtrade.freqai.base_models.BaseClassifierModel import BaseClassifierModel
# REMOVED_UNUSED_CODE: from freqtrade.freqai.base_models.FreqaiMultiOutputClassifier import FreqaiMultiOutputClassifier
# REMOVED_UNUSED_CODE: from freqtrade.freqai.data_kitchen import FreqaiDataKitchen


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class CatboostClassifierMultiTarget(BaseClassifierModel):
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
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         cbc = CatBoostClassifier(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             allow_writing_files=True,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             loss_function="MultiClass",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             train_dir=Path(dk.data_path),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             **self.model_training_parameters,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         X = data_dictionary["train_features"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         y = data_dictionary["train_labels"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         sample_weight = data_dictionary["train_weights"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         eval_sets = [None] * y.shape[1]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.freqai_info.get("data_split_parameters", {}).get("test_size", 0.1) != 0:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             eval_sets = [None] * data_dictionary["test_labels"].shape[1]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for i in range(data_dictionary["test_labels"].shape[1]):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 eval_sets[i] = Pool(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     data=data_dictionary["test_features"],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     label=data_dictionary["test_labels"].iloc[:, i],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     weight=data_dictionary["test_weights"],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         init_model = self.get_init_model(dk.pair)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if init_model:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             init_models = init_model.estimators_
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             init_models = [None] * y.shape[1]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         fit_params = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for i in range(len(eval_sets)):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             fit_params.append(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "eval_set": eval_sets[i],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     "init_model": init_models[i],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 }
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         model = FreqaiMultiOutputClassifier(estimator=cbc)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         thread_training = self.freqai_info.get("multitarget_parallel_training", False)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if thread_training:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             model.n_jobs = y.shape[1]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         model.fit(X=X, y=y, sample_weight=sample_weight, fit_params=fit_params)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return model
