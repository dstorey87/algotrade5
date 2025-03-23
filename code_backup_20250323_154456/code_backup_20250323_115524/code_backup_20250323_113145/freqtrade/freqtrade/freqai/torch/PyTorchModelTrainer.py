import logging
from pathlib import Path
from typing import Any

import pandas as pd
import torch
from torch import nn
from torch.optim import Optimizer
from torch.utils.data import DataLoader, TensorDataset

from freqtrade.freqai.torch.PyTorchDataConvertor import PyTorchDataConvertor
from freqtrade.freqai.torch.PyTorchTrainerInterface import PyTorchTrainerInterface

from .datasets import WindowDataset


logger = logging.getLogger(__name__)


class PyTorchModelTrainer(PyTorchTrainerInterface):
    def __init__(
        self,
        model: nn.Module,
        optimizer: Optimizer,
        criterion: nn.Module,
        device: str,
        data_convertor: PyTorchDataConvertor,
        model_meta_data: dict[str, Any] = {},
        window_size: int = 1,
        tb_logger: Any = None,
        **kwargs,
    ):
        """
        :param model: The PyTorch model to be trained.
        :param optimizer: The optimizer to use for training.
        :param criterion: The loss function to use for training.
        :param device: The device to use for training (e.g. 'cpu', 'cuda').
        :param init_model: A dictionary containing the initial model/optimizer
            state_dict and model_meta_data saved by self.save() method.
        :param model_meta_data: Additional metadata about the model (optional).
        :param data_convertor: converter from pd.DataFrame to torch.tensor.
        :param n_steps: used to calculate n_epochs. The number of training iterations to run.
            iteration here refers to the number of times optimizer.step() is called.
            ignored if n_epochs is set.
        :param n_epochs: The maximum number batches to use for evaluation.
        :param batch_size: The size of the batches to use during training.
        """
        self.model = model
        self.optimizer = optimizer
        self.criterion = criterion
        self.model_meta_data = model_meta_data
        self.device = device
        self.n_epochs: int | None = kwargs.get("n_epochs", 10)
        self.n_steps: int | None = kwargs.get("n_steps", None)
        if self.n_steps is None and not self.n_epochs:
            raise Exception("Either `n_steps` or `n_epochs` should be set.")

        self.batch_size: int = kwargs.get("batch_size", 64)
        self.data_convertor = data_convertor
        self.window_size: int = window_size
        self.tb_logger = tb_logger
        self.test_batch_counter = 0

# REMOVED_UNUSED_CODE:     def fit(self, data_dictionary: dict[str, pd.DataFrame], splits: list[str]):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         :param data_dictionary: the dictionary constructed by DataHandler to hold
# REMOVED_UNUSED_CODE:         all the training and test data/labels.
# REMOVED_UNUSED_CODE:         :param splits: splits to use in training, splits must contain "train",
# REMOVED_UNUSED_CODE:         optional "test" could be added by setting freqai.data_split_parameters.test_size > 0
# REMOVED_UNUSED_CODE:         in the config file.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:          - Calculates the predicted output for the batch using the PyTorch model.
# REMOVED_UNUSED_CODE:          - Calculates the loss between the predicted and actual output using a loss function.
# REMOVED_UNUSED_CODE:          - Computes the gradients of the loss with respect to the model's parameters using
# REMOVED_UNUSED_CODE:            backpropagation.
# REMOVED_UNUSED_CODE:          - Updates the model's parameters using an optimizer.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self.model.train()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         data_loaders_dictionary = self.create_data_loaders_dictionary(data_dictionary, splits)
# REMOVED_UNUSED_CODE:         n_obs = len(data_dictionary["train_features"])
# REMOVED_UNUSED_CODE:         n_epochs = self.n_epochs or self.calc_n_epochs(n_obs=n_obs)
# REMOVED_UNUSED_CODE:         batch_counter = 0
# REMOVED_UNUSED_CODE:         for _ in range(n_epochs):
# REMOVED_UNUSED_CODE:             for _, batch_data in enumerate(data_loaders_dictionary["train"]):
# REMOVED_UNUSED_CODE:                 xb, yb = batch_data
# REMOVED_UNUSED_CODE:                 xb = xb.to(self.device)
# REMOVED_UNUSED_CODE:                 yb = yb.to(self.device)
# REMOVED_UNUSED_CODE:                 yb_pred = self.model(xb)
# REMOVED_UNUSED_CODE:                 loss = self.criterion(yb_pred, yb)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 self.optimizer.zero_grad(set_to_none=True)
# REMOVED_UNUSED_CODE:                 loss.backward()
# REMOVED_UNUSED_CODE:                 self.optimizer.step()
# REMOVED_UNUSED_CODE:                 self.tb_logger.log_scalar("train_loss", loss.item(), batch_counter)
# REMOVED_UNUSED_CODE:                 batch_counter += 1
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             # evaluation
# REMOVED_UNUSED_CODE:             if "test" in splits:
# REMOVED_UNUSED_CODE:                 self.estimate_loss(data_loaders_dictionary, "test")

    @torch.no_grad()
    def estimate_loss(
        self,
        data_loader_dictionary: dict[str, DataLoader],
        split: str,
    ) -> None:
        self.model.eval()
        for _, batch_data in enumerate(data_loader_dictionary[split]):
            xb, yb = batch_data
            xb = xb.to(self.device)
            yb = yb.to(self.device)

            yb_pred = self.model(xb)
            loss = self.criterion(yb_pred, yb)
            self.tb_logger.log_scalar(f"{split}_loss", loss.item(), self.test_batch_counter)
            self.test_batch_counter += 1

        self.model.train()

    def create_data_loaders_dictionary(
        self, data_dictionary: dict[str, pd.DataFrame], splits: list[str]
    ) -> dict[str, DataLoader]:
        """
        Converts the input data to PyTorch tensors using a data loader.
        """
        data_loader_dictionary = {}
        for split in splits:
            x = self.data_convertor.convert_x(data_dictionary[f"{split}_features"], self.device)
            y = self.data_convertor.convert_y(data_dictionary[f"{split}_labels"], self.device)
            dataset = TensorDataset(x, y)
            data_loader = DataLoader(
                dataset,
                batch_size=self.batch_size,
                shuffle=True,
                drop_last=True,
                num_workers=0,
            )
            data_loader_dictionary[split] = data_loader

        return data_loader_dictionary

    def calc_n_epochs(self, n_obs: int) -> int:
        """
        Calculates the number of epochs required to reach the maximum number
        of iterations specified in the model training parameters.

        the motivation here is that `n_steps` is easier to optimize and keep stable,
        across different n_obs - the number of data points.
        """
        if not isinstance(self.n_steps, int):
            raise ValueError("Either `n_steps` or `n_epochs` should be set.")
        n_batches = n_obs // self.batch_size
        n_epochs = max(self.n_steps // n_batches, 1)
        if n_epochs <= 10:
            logger.warning(
                f"Setting low n_epochs: {n_epochs}. "
                f"Please consider increasing `n_steps` hyper-parameter."
            )

        return n_epochs

    def save(self, path: Path):
        """
        - Saving any nn.Module state_dict
        - Saving model_meta_data, this dict should contain any additional data that the
          user needs to store. e.g. class_names for classification models.
        """

        torch.save(
            {
                "model_state_dict": self.model.state_dict(),
                "optimizer_state_dict": self.optimizer.state_dict(),
                "model_meta_data": self.model_meta_data,
                "pytrainer": self,
            },
            path,
        )

    def load(self, path: Path):
        checkpoint = torch.load(path)
        return self.load_from_checkpoint(checkpoint)

    def load_from_checkpoint(self, checkpoint: dict):
        """
        when using continual_learning, DataDrawer will load the dictionary
        (containing state dicts and model_meta_data) by calling torch.load(path).
        you can access this dict from any class that inherits IFreqaiModel by calling
        get_init_model method.
        """
        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
        self.model_meta_data = checkpoint["model_meta_data"]
        return self


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
