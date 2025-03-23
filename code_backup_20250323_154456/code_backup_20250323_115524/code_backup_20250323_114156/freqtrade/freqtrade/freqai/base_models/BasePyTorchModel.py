import logging
from abc import ABC, abstractmethod

import torch

from freqtrade.freqai.freqai_interface import IFreqaiModel
from freqtrade.freqai.torch.PyTorchDataConvertor import PyTorchDataConvertor


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class BasePyTorchModel(IFreqaiModel, ABC):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Base class for PyTorch type models.
# REMOVED_UNUSED_CODE:     User *must* inherit from this class and set fit() and predict() and
# REMOVED_UNUSED_CODE:     data_convertor property.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, **kwargs):
# REMOVED_UNUSED_CODE:         super().__init__(config=kwargs["config"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.dd.model_type = "pytorch"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.device = (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "mps"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if torch.backends.mps.is_available() and torch.backends.mps.is_built()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             else ("cuda" if torch.cuda.is_available() else "cpu")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         test_size = self.freqai_info.get("data_split_parameters", {}).get("test_size")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.splits = ["train", "test"] if test_size != 0 else ["train"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.window_size = self.freqai_info.get("conv_width", 1)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     @abstractmethod
# REMOVED_UNUSED_CODE:     def data_convertor(self) -> PyTorchDataConvertor:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         a class responsible for converting `*_features` & `*_labels` pandas dataframes
# REMOVED_UNUSED_CODE:         to pytorch tensors.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         raise NotImplementedError("Abstract property")
