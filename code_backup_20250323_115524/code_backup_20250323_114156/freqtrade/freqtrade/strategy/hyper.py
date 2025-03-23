"""
IHyperStrategy interface, hyperoptable Parameter class.
This module defines a base class for auto-hyperoptable strategies.
"""

import logging
from collections.abc import Iterator
from pathlib import Path
from typing import Any

# REMOVED_UNUSED_CODE: from freqtrade.constants import Config
from freqtrade.exceptions import OperationalException
# REMOVED_UNUSED_CODE: from freqtrade.misc import deep_merge_dicts
from freqtrade.optimize.hyperopt_tools import HyperoptTools
from freqtrade.strategy.parameters import BaseParameter


logger = logging.getLogger(__name__)


class HyperStrategyMixin:
    """
    A helper base class which allows HyperOptAuto class to reuse implementations of buy/sell
     strategy logic.
    """

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def __init__(self, config: Config, *args, **kwargs):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Initialize hyperoptable strategy mixin.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.config = config
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.ft_buy_params: list[BaseParameter] = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.ft_sell_params: list[BaseParameter] = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.ft_protection_params: list[BaseParameter] = []
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         params = self.load_params_from_file()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         params = params.get("params", {})
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self._ft_params_from_file = params
        # Init/loading of parameters is done as part of ft_bot_start().

# REMOVED_UNUSED_CODE:     def enumerate_parameters(
# REMOVED_UNUSED_CODE:         self, category: str | None = None
# REMOVED_UNUSED_CODE:     ) -> Iterator[tuple[str, BaseParameter]]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Find all optimizable parameters and return (name, attr) iterator.
# REMOVED_UNUSED_CODE:         :param category:
# REMOVED_UNUSED_CODE:         :return:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if category not in ("buy", "sell", "protection", None):
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 'Category must be one of: "buy", "sell", "protection", None.'
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if category is None:
# REMOVED_UNUSED_CODE:             params = self.ft_buy_params + self.ft_sell_params + self.ft_protection_params
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             params = getattr(self, f"ft_{category}_params")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         for par in params:
# REMOVED_UNUSED_CODE:             yield par.name, par

# REMOVED_UNUSED_CODE:     @classmethod
# REMOVED_UNUSED_CODE:     def detect_all_parameters(cls) -> dict:
# REMOVED_UNUSED_CODE:         """Detect all parameters and return them as a list"""
# REMOVED_UNUSED_CODE:         params: dict[str, Any] = {
# REMOVED_UNUSED_CODE:             "buy": list(detect_parameters(cls, "buy")),
# REMOVED_UNUSED_CODE:             "sell": list(detect_parameters(cls, "sell")),
# REMOVED_UNUSED_CODE:             "protection": list(detect_parameters(cls, "protection")),
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE:         params.update({"count": len(params["buy"] + params["sell"] + params["protection"])})
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return params

# REMOVED_UNUSED_CODE:     def ft_load_params_from_file(self) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Load Parameters from parameter file
# REMOVED_UNUSED_CODE:         Should/must run before config values are loaded in strategy_resolver.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if self._ft_params_from_file:
# REMOVED_UNUSED_CODE:             # Set parameters from Hyperopt results file
# REMOVED_UNUSED_CODE:             params = self._ft_params_from_file
# REMOVED_UNUSED_CODE:             self.minimal_roi = params.get("roi", getattr(self, "minimal_roi", {}))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             self.stoploss = params.get("stoploss", {}).get(
# REMOVED_UNUSED_CODE:                 "stoploss", getattr(self, "stoploss", -0.1)
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             self.max_open_trades = params.get("max_open_trades", {}).get(
# REMOVED_UNUSED_CODE:                 "max_open_trades", getattr(self, "max_open_trades", -1)
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             trailing = params.get("trailing", {})
# REMOVED_UNUSED_CODE:             self.trailing_stop = trailing.get(
# REMOVED_UNUSED_CODE:                 "trailing_stop", getattr(self, "trailing_stop", False)
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             self.trailing_stop_positive = trailing.get(
# REMOVED_UNUSED_CODE:                 "trailing_stop_positive", getattr(self, "trailing_stop_positive", None)
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             self.trailing_stop_positive_offset = trailing.get(
# REMOVED_UNUSED_CODE:                 "trailing_stop_positive_offset", getattr(self, "trailing_stop_positive_offset", 0)
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             self.trailing_only_offset_is_reached = trailing.get(
# REMOVED_UNUSED_CODE:                 "trailing_only_offset_is_reached",
# REMOVED_UNUSED_CODE:                 getattr(self, "trailing_only_offset_is_reached", 0.0),
# REMOVED_UNUSED_CODE:             )

# REMOVED_UNUSED_CODE:     def ft_load_hyper_params(self, hyperopt: bool = False) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Load Hyperoptable parameters
# REMOVED_UNUSED_CODE:         Prevalence:
# REMOVED_UNUSED_CODE:         * Parameters from parameter file
# REMOVED_UNUSED_CODE:         * Parameters defined in parameters objects (buy_params, sell_params, ...)
# REMOVED_UNUSED_CODE:         * Parameter defaults
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         buy_params = deep_merge_dicts(
# REMOVED_UNUSED_CODE:             self._ft_params_from_file.get("buy", {}), getattr(self, "buy_params", {})
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         sell_params = deep_merge_dicts(
# REMOVED_UNUSED_CODE:             self._ft_params_from_file.get("sell", {}), getattr(self, "sell_params", {})
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         protection_params = deep_merge_dicts(
# REMOVED_UNUSED_CODE:             self._ft_params_from_file.get("protection", {}), getattr(self, "protection_params", {})
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._ft_load_params(buy_params, "buy", hyperopt)
# REMOVED_UNUSED_CODE:         self._ft_load_params(sell_params, "sell", hyperopt)
# REMOVED_UNUSED_CODE:         self._ft_load_params(protection_params, "protection", hyperopt)

# REMOVED_UNUSED_CODE:     def load_params_from_file(self) -> dict:
# REMOVED_UNUSED_CODE:         filename_str = getattr(self, "__file__", "")
# REMOVED_UNUSED_CODE:         if not filename_str:
# REMOVED_UNUSED_CODE:             return {}
# REMOVED_UNUSED_CODE:         filename = Path(filename_str).with_suffix(".json")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if filename.is_file():
# REMOVED_UNUSED_CODE:             logger.info(f"Loading parameters from file {filename}")
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 params = HyperoptTools.load_params(filename)
# REMOVED_UNUSED_CODE:                 if params.get("strategy_name") != self.__class__.__name__:
# REMOVED_UNUSED_CODE:                     raise OperationalException("Invalid parameter file provided.")
# REMOVED_UNUSED_CODE:                 return params
# REMOVED_UNUSED_CODE:             except ValueError:
# REMOVED_UNUSED_CODE:                 logger.warning("Invalid parameter file format.")
# REMOVED_UNUSED_CODE:                 return {}
# REMOVED_UNUSED_CODE:         logger.info("Found no parameter file.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return {}

# REMOVED_UNUSED_CODE:     def _ft_load_params(self, params: dict, space: str, hyperopt: bool = False) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Set optimizable parameter values.
# REMOVED_UNUSED_CODE:         :param params: Dictionary with new parameter values.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if not params:
# REMOVED_UNUSED_CODE:             logger.info(f"No params for {space} found, using default values.")
# REMOVED_UNUSED_CODE:         param_container: list[BaseParameter] = getattr(self, f"ft_{space}_params")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         for attr_name, attr in detect_parameters(self, space):
# REMOVED_UNUSED_CODE:             attr.name = attr_name
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             attr.in_space = hyperopt and HyperoptTools.has_space(self.config, space)
# REMOVED_UNUSED_CODE:             if not attr.category:
# REMOVED_UNUSED_CODE:                 attr.category = space
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             param_container.append(attr)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             if params and attr_name in params:
# REMOVED_UNUSED_CODE:                 if attr.load:
# REMOVED_UNUSED_CODE:                     attr.value = params[attr_name]
# REMOVED_UNUSED_CODE:                     logger.info(f"Strategy Parameter: {attr_name} = {attr.value}")
# REMOVED_UNUSED_CODE:                 else:
# REMOVED_UNUSED_CODE:                     logger.warning(
# REMOVED_UNUSED_CODE:                         f'Parameter "{attr_name}" exists, but is disabled. '
# REMOVED_UNUSED_CODE:                         f'Default value "{attr.value}" used.'
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 logger.info(f"Strategy Parameter(default): {attr_name} = {attr.value}")

# REMOVED_UNUSED_CODE:     def get_no_optimize_params(self) -> dict[str, dict]:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Returns list of Parameters that are not part of the current optimize job
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         params: dict[str, dict] = {
# REMOVED_UNUSED_CODE:             "buy": {},
# REMOVED_UNUSED_CODE:             "sell": {},
# REMOVED_UNUSED_CODE:             "protection": {},
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE:         for name, p in self.enumerate_parameters():
# REMOVED_UNUSED_CODE:             if p.category and (not p.optimize or not p.in_space):
# REMOVED_UNUSED_CODE:                 params[p.category][name] = p.value
# REMOVED_UNUSED_CODE:         return params


def detect_parameters(
    obj: HyperStrategyMixin | type[HyperStrategyMixin], category: str
) -> Iterator[tuple[str, BaseParameter]]:
    """
    Detect all parameters for 'category' for "obj"
    :param obj: Strategy object or class
    :param category: category - usually `'buy', 'sell', 'protection',...
    """
    for attr_name in dir(obj):
        if not attr_name.startswith("__"):  # Ignore internals, not strictly necessary.
            attr = getattr(obj, attr_name)
            if issubclass(attr.__class__, BaseParameter):
                if (
                    attr_name.startswith(category + "_")
                    and attr.category is not None
                    and attr.category != category
                ):
                    raise OperationalException(
                        f"Inconclusive parameter name {attr_name}, category: {attr.category}."
                    )

                if category == attr.category or (
                    attr_name.startswith(category + "_") and attr.category is None
                ):
                    yield attr_name, attr
