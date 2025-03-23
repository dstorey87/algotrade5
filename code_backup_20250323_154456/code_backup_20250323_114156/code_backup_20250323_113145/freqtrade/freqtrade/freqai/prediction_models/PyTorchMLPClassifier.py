from typing import Any

import torch

from freqtrade.freqai.base_models.BasePyTorchClassifier import BasePyTorchClassifier
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen
from freqtrade.freqai.torch.PyTorchDataConvertor import (
    DefaultPyTorchDataConvertor,
    PyTorchDataConvertor,
)
from freqtrade.freqai.torch.PyTorchMLPModel import PyTorchMLPModel
from freqtrade.freqai.torch.PyTorchModelTrainer import PyTorchModelTrainer


# REMOVED_UNUSED_CODE: class PyTorchMLPClassifier(BasePyTorchClassifier):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     This class implements the fit method of IFreqaiModel.
# REMOVED_UNUSED_CODE:     in the fit method we initialize the model and trainer objects.
# REMOVED_UNUSED_CODE:     the only requirement from the model is to be aligned to PyTorchClassifier
# REMOVED_UNUSED_CODE:     predict method that expects the model to predict a tensor of type long.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     parameters are passed via `model_training_parameters` under the freqai
# REMOVED_UNUSED_CODE:     section in the config file. e.g:
# REMOVED_UNUSED_CODE:     {
# REMOVED_UNUSED_CODE:         ...
# REMOVED_UNUSED_CODE:         "freqai": {
# REMOVED_UNUSED_CODE:             ...
# REMOVED_UNUSED_CODE:             "model_training_parameters" : {
# REMOVED_UNUSED_CODE:                 "learning_rate": 3e-4,
# REMOVED_UNUSED_CODE:                 "trainer_kwargs": {
# REMOVED_UNUSED_CODE:                     "n_steps": 5000,
# REMOVED_UNUSED_CODE:                     "batch_size": 64,
# REMOVED_UNUSED_CODE:                     "n_epochs": null,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "model_kwargs": {
# REMOVED_UNUSED_CODE:                     "hidden_dim": 512,
# REMOVED_UNUSED_CODE:                     "dropout_percent": 0.2,
# REMOVED_UNUSED_CODE:                     "n_layer": 1,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:             }
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def data_convertor(self) -> PyTorchDataConvertor:
# REMOVED_UNUSED_CODE:         return DefaultPyTorchDataConvertor(
# REMOVED_UNUSED_CODE:             target_tensor_type=torch.long, squeeze_target_tensor=True
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, **kwargs) -> None:
# REMOVED_UNUSED_CODE:         super().__init__(**kwargs)
# REMOVED_UNUSED_CODE:         config = self.freqai_info.get("model_training_parameters", {})
# REMOVED_UNUSED_CODE:         self.learning_rate: float = config.get("learning_rate", 3e-4)
# REMOVED_UNUSED_CODE:         self.model_kwargs: dict[str, Any] = config.get("model_kwargs", {})
# REMOVED_UNUSED_CODE:         self.trainer_kwargs: dict[str, Any] = config.get("trainer_kwargs", {})
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def fit(self, data_dictionary: dict, dk: FreqaiDataKitchen, **kwargs) -> Any:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         User sets up the training and test data to fit their desired model here
# REMOVED_UNUSED_CODE:         :param data_dictionary: the dictionary holding all data for train, test,
# REMOVED_UNUSED_CODE:             labels, weights
# REMOVED_UNUSED_CODE:         :param dk: The datakitchen object for the current coin/model
# REMOVED_UNUSED_CODE:         :raises ValueError: If self.class_names is not defined in the parent class.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         class_names = self.get_class_names()
# REMOVED_UNUSED_CODE:         self.convert_label_column_to_int(data_dictionary, dk, class_names)
# REMOVED_UNUSED_CODE:         n_features = data_dictionary["train_features"].shape[-1]
# REMOVED_UNUSED_CODE:         model = PyTorchMLPModel(
# REMOVED_UNUSED_CODE:             input_dim=n_features, output_dim=len(class_names), **self.model_kwargs
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         model.to(self.device)
# REMOVED_UNUSED_CODE:         optimizer = torch.optim.AdamW(model.parameters(), lr=self.learning_rate)
# REMOVED_UNUSED_CODE:         criterion = torch.nn.CrossEntropyLoss()
# REMOVED_UNUSED_CODE:         # check if continual_learning is activated, and retrieve the model to continue training
# REMOVED_UNUSED_CODE:         trainer = self.get_init_model(dk.pair)
# REMOVED_UNUSED_CODE:         if trainer is None:
# REMOVED_UNUSED_CODE:             trainer = PyTorchModelTrainer(
# REMOVED_UNUSED_CODE:                 model=model,
# REMOVED_UNUSED_CODE:                 optimizer=optimizer,
# REMOVED_UNUSED_CODE:                 criterion=criterion,
# REMOVED_UNUSED_CODE:                 model_meta_data={"class_names": class_names},
# REMOVED_UNUSED_CODE:                 device=self.device,
# REMOVED_UNUSED_CODE:                 data_convertor=self.data_convertor,
# REMOVED_UNUSED_CODE:                 tb_logger=self.tb_logger,
# REMOVED_UNUSED_CODE:                 **self.trainer_kwargs,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         trainer.fit(data_dictionary, self.splits)
# REMOVED_UNUSED_CODE:         return trainer
