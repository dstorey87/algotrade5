import logging
# REMOVED_UNUSED_CODE: from pathlib import Path
# REMOVED_UNUSED_CODE: from typing import Any

# REMOVED_UNUSED_CODE: import pandas as pd
# REMOVED_UNUSED_CODE: import torch
# REMOVED_UNUSED_CODE: from torch import nn
# REMOVED_UNUSED_CODE: from torch.optim import Optimizer
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from torch.utils.data import DataLoader, TensorDataset

# REMOVED_UNUSED_CODE: from freqtrade.freqai.torch.PyTorchDataConvertor import PyTorchDataConvertor
# REMOVED_UNUSED_CODE: from freqtrade.freqai.torch.PyTorchTrainerInterface import PyTorchTrainerInterface

# REMOVED_UNUSED_CODE: from .datasets import WindowDataset


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class PyTorchModelTrainer(PyTorchTrainerInterface):
# REMOVED_UNUSED_CODE:     def __init__(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         model: nn.Module,
# REMOVED_UNUSED_CODE:         optimizer: Optimizer,
# REMOVED_UNUSED_CODE:         criterion: nn.Module,
# REMOVED_UNUSED_CODE:         device: str,
# REMOVED_UNUSED_CODE:         data_convertor: PyTorchDataConvertor,
# REMOVED_UNUSED_CODE:         model_meta_data: dict[str, Any] = {},
# REMOVED_UNUSED_CODE:         window_size: int = 1,
# REMOVED_UNUSED_CODE:         tb_logger: Any = None,
# REMOVED_UNUSED_CODE:         **kwargs,
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         :param model: The PyTorch model to be trained.
# REMOVED_UNUSED_CODE:         :param optimizer: The optimizer to use for training.
# REMOVED_UNUSED_CODE:         :param criterion: The loss function to use for training.
# REMOVED_UNUSED_CODE:         :param device: The device to use for training (e.g. 'cpu', 'cuda').
# REMOVED_UNUSED_CODE:         :param init_model: A dictionary containing the initial model/optimizer
# REMOVED_UNUSED_CODE:             state_dict and model_meta_data saved by self.save() method.
# REMOVED_UNUSED_CODE:         :param model_meta_data: Additional metadata about the model (optional).
# REMOVED_UNUSED_CODE:         :param data_convertor: converter from pd.DataFrame to torch.tensor.
# REMOVED_UNUSED_CODE:         :param n_steps: used to calculate n_epochs. The number of training iterations to run.
# REMOVED_UNUSED_CODE:             iteration here refers to the number of times optimizer.step() is called.
# REMOVED_UNUSED_CODE:             ignored if n_epochs is set.
# REMOVED_UNUSED_CODE:         :param n_epochs: The maximum number batches to use for evaluation.
# REMOVED_UNUSED_CODE:         :param batch_size: The size of the batches to use during training.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self.model = model
# REMOVED_UNUSED_CODE:         self.optimizer = optimizer
# REMOVED_UNUSED_CODE:         self.criterion = criterion
# REMOVED_UNUSED_CODE:         self.model_meta_data = model_meta_data
# REMOVED_UNUSED_CODE:         self.device = device
# REMOVED_UNUSED_CODE:         self.n_epochs: int | None = kwargs.get("n_epochs", 10)
# REMOVED_UNUSED_CODE:         self.n_steps: int | None = kwargs.get("n_steps", None)
# REMOVED_UNUSED_CODE:         if self.n_steps is None and not self.n_epochs:
# REMOVED_UNUSED_CODE:             raise Exception("Either `n_steps` or `n_epochs` should be set.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.batch_size: int = kwargs.get("batch_size", 64)
# REMOVED_UNUSED_CODE:         self.data_convertor = data_convertor
# REMOVED_UNUSED_CODE:         self.window_size: int = window_size
# REMOVED_UNUSED_CODE:         self.tb_logger = tb_logger
# REMOVED_UNUSED_CODE:         self.test_batch_counter = 0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def fit(self, data_dictionary: dict[str, pd.DataFrame], splits: list[str]):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param data_dictionary: the dictionary constructed by DataHandler to hold
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         all the training and test data/labels.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param splits: splits to use in training, splits must contain "train",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         optional "test" could be added by setting freqai.data_split_parameters.test_size > 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         in the config file.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:          - Calculates the predicted output for the batch using the PyTorch model.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:          - Calculates the loss between the predicted and actual output using a loss function.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:          - Computes the gradients of the loss with respect to the model's parameters using
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:            backpropagation.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:          - Updates the model's parameters using an optimizer.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.model.train()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         data_loaders_dictionary = self.create_data_loaders_dictionary(data_dictionary, splits)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         n_obs = len(data_dictionary["train_features"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         n_epochs = self.n_epochs or self.calc_n_epochs(n_obs=n_obs)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         batch_counter = 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for _ in range(n_epochs):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             for _, batch_data in enumerate(data_loaders_dictionary["train"]):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 xb, yb = batch_data
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 xb = xb.to(self.device)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 yb = yb.to(self.device)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 yb_pred = self.model(xb)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 loss = self.criterion(yb_pred, yb)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.optimizer.zero_grad(set_to_none=True)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 loss.backward()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.optimizer.step()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.tb_logger.log_scalar("train_loss", loss.item(), batch_counter)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 batch_counter += 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # evaluation
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if "test" in splits:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.estimate_loss(data_loaders_dictionary, "test")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @torch.no_grad()
# REMOVED_UNUSED_CODE:     def estimate_loss(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         data_loader_dictionary: dict[str, DataLoader],
# REMOVED_UNUSED_CODE:         split: str,
# REMOVED_UNUSED_CODE:     ) -> None:
# REMOVED_UNUSED_CODE:         self.model.eval()
# REMOVED_UNUSED_CODE:         for _, batch_data in enumerate(data_loader_dictionary[split]):
# REMOVED_UNUSED_CODE:             xb, yb = batch_data
# REMOVED_UNUSED_CODE:             xb = xb.to(self.device)
# REMOVED_UNUSED_CODE:             yb = yb.to(self.device)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             yb_pred = self.model(xb)
# REMOVED_UNUSED_CODE:             loss = self.criterion(yb_pred, yb)
# REMOVED_UNUSED_CODE:             self.tb_logger.log_scalar(f"{split}_loss", loss.item(), self.test_batch_counter)
# REMOVED_UNUSED_CODE:             self.test_batch_counter += 1
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.model.train()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def create_data_loaders_dictionary(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, data_dictionary: dict[str, pd.DataFrame], splits: list[str]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> dict[str, DataLoader]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Converts the input data to PyTorch tensors using a data loader.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         data_loader_dictionary = {}
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for split in splits:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             x = self.data_convertor.convert_x(data_dictionary[f"{split}_features"], self.device)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             y = self.data_convertor.convert_y(data_dictionary[f"{split}_labels"], self.device)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             dataset = TensorDataset(x, y)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             data_loader = DataLoader(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 dataset,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 batch_size=self.batch_size,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 shuffle=True,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 drop_last=True,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 num_workers=0,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             data_loader_dictionary[split] = data_loader
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return data_loader_dictionary
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def calc_n_epochs(self, n_obs: int) -> int:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Calculates the number of epochs required to reach the maximum number
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         of iterations specified in the model training parameters.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         the motivation here is that `n_steps` is easier to optimize and keep stable,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         across different n_obs - the number of data points.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not isinstance(self.n_steps, int):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             raise ValueError("Either `n_steps` or `n_epochs` should be set.")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         n_batches = n_obs // self.batch_size
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         n_epochs = max(self.n_steps // n_batches, 1)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if n_epochs <= 10:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             logger.warning(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"Setting low n_epochs: {n_epochs}. "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"Please consider increasing `n_steps` hyper-parameter."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return n_epochs
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def save(self, path: Path):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         - Saving any nn.Module state_dict
# REMOVED_UNUSED_CODE:         - Saving model_meta_data, this dict should contain any additional data that the
# REMOVED_UNUSED_CODE:           user needs to store. e.g. class_names for classification models.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         torch.save(
# REMOVED_UNUSED_CODE:             {
# REMOVED_UNUSED_CODE:                 "model_state_dict": self.model.state_dict(),
# REMOVED_UNUSED_CODE:                 "optimizer_state_dict": self.optimizer.state_dict(),
# REMOVED_UNUSED_CODE:                 "model_meta_data": self.model_meta_data,
# REMOVED_UNUSED_CODE:                 "pytrainer": self,
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             path,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def load(self, path: Path):
# REMOVED_UNUSED_CODE:         checkpoint = torch.load(path)
# REMOVED_UNUSED_CODE:         return self.load_from_checkpoint(checkpoint)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def load_from_checkpoint(self, checkpoint: dict):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         when using continual_learning, DataDrawer will load the dictionary
# REMOVED_UNUSED_CODE:         (containing state dicts and model_meta_data) by calling torch.load(path).
# REMOVED_UNUSED_CODE:         you can access this dict from any class that inherits IFreqaiModel by calling
# REMOVED_UNUSED_CODE:         get_init_model method.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self.model.load_state_dict(checkpoint["model_state_dict"])
# REMOVED_UNUSED_CODE:         self.optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
# REMOVED_UNUSED_CODE:         self.model_meta_data = checkpoint["model_meta_data"]
# REMOVED_UNUSED_CODE:         return self


# REMOVED_UNUSED_CODE: class PyTorchTransformerTrainer(PyTorchModelTrainer):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Creating a trainer for the Transformer model.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def create_data_loaders_dictionary(
# REMOVED_UNUSED_CODE:         self, data_dictionary: dict[str, pd.DataFrame], splits: list[str]
# REMOVED_UNUSED_CODE:     ) -> dict[str, DataLoader]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Converts the input data to PyTorch tensors using a data loader.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         data_loader_dictionary = {}
# REMOVED_UNUSED_CODE:         for split in splits:
# REMOVED_UNUSED_CODE:             x = self.data_convertor.convert_x(data_dictionary[f"{split}_features"], self.device)
# REMOVED_UNUSED_CODE:             y = self.data_convertor.convert_y(data_dictionary[f"{split}_labels"], self.device)
# REMOVED_UNUSED_CODE:             dataset = WindowDataset(x, y, self.window_size)
# REMOVED_UNUSED_CODE:             data_loader = DataLoader(
# REMOVED_UNUSED_CODE:                 dataset,
# REMOVED_UNUSED_CODE:                 batch_size=self.batch_size,
# REMOVED_UNUSED_CODE:                 shuffle=False,
# REMOVED_UNUSED_CODE:                 drop_last=True,
# REMOVED_UNUSED_CODE:                 num_workers=0,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             data_loader_dictionary[split] = data_loader
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return data_loader_dictionary
