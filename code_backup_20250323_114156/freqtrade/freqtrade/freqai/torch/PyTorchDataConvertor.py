# REMOVED_UNUSED_CODE: from abc import ABC, abstractmethod

# REMOVED_UNUSED_CODE: import pandas as pd
# REMOVED_UNUSED_CODE: import torch


# REMOVED_UNUSED_CODE: class PyTorchDataConvertor(ABC):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     This class is responsible for converting `*_features` & `*_labels` pandas dataframes
# REMOVED_UNUSED_CODE:     to pytorch tensors.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @abstractmethod
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def convert_x(self, df: pd.DataFrame, device: str) -> torch.Tensor:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param df: "*_features" dataframe.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param device: The device to use for training (e.g. 'cpu', 'cuda').
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @abstractmethod
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def convert_y(self, df: pd.DataFrame, device: str) -> torch.Tensor:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param df: "*_labels" dataframe.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param device: The device to use for training (e.g. 'cpu', 'cuda').
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """


# REMOVED_UNUSED_CODE: class DefaultPyTorchDataConvertor(PyTorchDataConvertor):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     A default conversion that keeps features dataframe shapes.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         target_tensor_type: torch.dtype = torch.float32,
# REMOVED_UNUSED_CODE:         squeeze_target_tensor: bool = False,
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         :param target_tensor_type: type of target tensor, for classification use
# REMOVED_UNUSED_CODE:             torch.long, for regressor use torch.float or torch.double.
# REMOVED_UNUSED_CODE:         :param squeeze_target_tensor: controls the target shape, used for loss functions
# REMOVED_UNUSED_CODE:             that requires 0D or 1D.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self._target_tensor_type = target_tensor_type
# REMOVED_UNUSED_CODE:         self._squeeze_target_tensor = squeeze_target_tensor
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def convert_x(self, df: pd.DataFrame, device: str) -> torch.Tensor:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         numpy_arrays = df.values
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         x = torch.tensor(numpy_arrays, device=device, dtype=torch.float32)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return x
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def convert_y(self, df: pd.DataFrame, device: str) -> torch.Tensor:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         numpy_arrays = df.values
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         y = torch.tensor(numpy_arrays, device=device, dtype=self._target_tensor_type)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._squeeze_target_tensor:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             y = y.squeeze()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return y
