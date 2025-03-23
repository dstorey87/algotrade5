from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd
import torch
from torch import nn


# REMOVED_UNUSED_CODE: class PyTorchTrainerInterface(ABC):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @abstractmethod
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def fit(self, data_dictionary: dict[str, pd.DataFrame], splits: list[str]) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param data_dictionary: the dictionary constructed by DataHandler to hold
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         all the training and test data/labels.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param splits: splits to use in training, splits must contain "train",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         optional "test" could be added by setting freqai.data_split_parameters.test_size > 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         in the config file.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:          - Calculates the predicted output for the batch using the PyTorch model.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:          - Calculates the loss between the predicted and actual output using a loss function.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:          - Computes the gradients of the loss with respect to the model's parameters using
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:            backpropagation.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:          - Updates the model's parameters using an optimizer.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @abstractmethod
# REMOVED_UNUSED_CODE:     def save(self, path: Path) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         - Saving any nn.Module state_dict
# REMOVED_UNUSED_CODE:         - Saving model_meta_data, this dict should contain any additional data that the
# REMOVED_UNUSED_CODE:           user needs to store. e.g class_names for classification models.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def load(self, path: Path) -> nn.Module:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         :param path: path to zip file.
# REMOVED_UNUSED_CODE:         :returns: pytorch model.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         checkpoint = torch.load(path)
# REMOVED_UNUSED_CODE:         return self.load_from_checkpoint(checkpoint)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @abstractmethod
# REMOVED_UNUSED_CODE:     def load_from_checkpoint(self, checkpoint: dict) -> nn.Module:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         when using continual_learning, DataDrawer will load the dictionary
# REMOVED_UNUSED_CODE:         (containing state dicts and model_meta_data) by calling torch.load(path).
# REMOVED_UNUSED_CODE:         you can access this dict from any class that inherits IFreqaiModel by calling
# REMOVED_UNUSED_CODE:         get_init_model method.
# REMOVED_UNUSED_CODE:         :checkpoint checkpoint: dict containing the model & optimizer state dicts,
# REMOVED_UNUSED_CODE:         model_meta_data, etc..
# REMOVED_UNUSED_CODE:         """
